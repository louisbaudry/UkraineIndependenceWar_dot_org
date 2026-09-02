#!/usr/bin/env bash
#
# One-command setup for a fresh Debian or Ubuntu server.
#
#   curl -fsSL https://raw.githubusercontent.com/louisbaudry/UkraineIndependenceWar_dot_org/main/setup/install.sh | bash
#
# or, if the repository is already cloned:
#
#   bash setup/install.sh
#
# Installs PostgreSQL and Python, creates the database and the OCFL storage
# roots, loads the schema, and runs the test suite. It stops at the first
# failure rather than continuing in a half-built state.
#
# It does NOT collect anything. Nothing here reaches the network except the
# package manager, and nothing registers a source. Collection is authorised
# by registering sources (OPS-001) and performed by a separate act, both of
# which come after this script.
#
# Safe to re-run: every step checks whether it has already been done.

set -euo pipefail

REPO_URL="${REPO_URL:-https://github.com/louisbaudry/UkraineIndependenceWar_dot_org.git}"
INSTALL_DIR="${INSTALL_DIR:-$HOME/uiw}"
DB_NAME="${DB_NAME:-uiw}"
ARCHIVE_ROOT="${ARCHIVE_ROOT:-$HOME/uiw-archive}"

step()  { printf '\n\033[1m==> %s\033[0m\n' "$1"; }
ok()    { printf '    \033[32m✓\033[0m %s\n' "$1"; }
warn()  { printf '    \033[33m!\033[0m %s\n' "$1"; }
die()   { printf '\n\033[31mSTOPPED: %s\033[0m\n' "$1" >&2; exit 1; }

# ---------------------------------------------------------------------------

step "Checking the system"

[ -f /etc/debian_version ] || die \
  "this script is for Debian or Ubuntu. On another system, install
  PostgreSQL 14+, Python 3.11+, python3-psycopg, python3-yaml and git by
  hand, then run the rest of the steps below manually."

if [ "$(id -u)" -eq 0 ]; then
  SUDO=""
  warn "running as root; consider a non-root user for day-to-day work"
else
  SUDO="sudo"
  command -v sudo >/dev/null || die "sudo not found and not running as root"
fi
ok "Debian-family system"

# ---------------------------------------------------------------------------

step "Installing PostgreSQL, Python and git"

export DEBIAN_FRONTEND=noninteractive
$SUDO apt-get update -qq
$SUDO apt-get install -y -qq \
  postgresql postgresql-client python3 python3-pip python3-venv git \
  >/dev/null
ok "packages installed"

PG_VERSION="$(psql --version | grep -oE '[0-9]+' | head -1)"
[ "$PG_VERSION" -ge 14 ] || die \
  "PostgreSQL $PG_VERSION is too old; the schema needs 14 or newer"
ok "PostgreSQL $PG_VERSION"

PY_MINOR="$(python3 -c 'import sys; print(sys.version_info.minor)')"
[ "$PY_MINOR" -ge 11 ] || die \
  "Python 3.$PY_MINOR is too old; the code needs 3.11 or newer"
ok "Python 3.$PY_MINOR"

# ---------------------------------------------------------------------------

step "Cloning the repository into $INSTALL_DIR"

if [ -d "$INSTALL_DIR/.git" ]; then
  git -C "$INSTALL_DIR" pull --quiet
  ok "already present, updated"
else
  git clone --quiet "$REPO_URL" "$INSTALL_DIR"
  ok "cloned"
fi
cd "$INSTALL_DIR"

# ---------------------------------------------------------------------------

step "Setting up Python packages"

python3 -m venv --system-site-packages .venv 2>/dev/null || python3 -m venv .venv
# shellcheck disable=SC1091
source .venv/bin/activate
pip install --quiet --upgrade pip
pip install --quiet "psycopg[binary]" PyYAML
ok "psycopg and PyYAML installed in $INSTALL_DIR/.venv"

# ---------------------------------------------------------------------------

step "Creating the database"

$SUDO systemctl enable --now postgresql >/dev/null 2>&1 || true

DB_USER="$(id -un)"
if ! $SUDO -u postgres psql -tAc \
      "SELECT 1 FROM pg_roles WHERE rolname='$DB_USER'" | grep -q 1; then
  $SUDO -u postgres createuser --createdb "$DB_USER"
  ok "database user $DB_USER created"
else
  ok "database user $DB_USER exists"
fi

if $SUDO -u postgres psql -tAc \
     "SELECT 1 FROM pg_database WHERE datname='$DB_NAME'" | grep -q 1; then
  warn "database '$DB_NAME' already exists — leaving it alone"
  warn "to start clean:  dropdb $DB_NAME  then re-run this script"
  SCHEMA_LOADED=yes
else
  createdb "$DB_NAME"
  ok "database '$DB_NAME' created"
  SCHEMA_LOADED=no
fi

# ---------------------------------------------------------------------------

step "Loading the schema"

if [ "$SCHEMA_LOADED" = no ]; then
  for sql in schema/0*.sql; do
    psql -q -d "$DB_NAME" -v ON_ERROR_STOP=1 -f "$sql" >/dev/null \
      || die "schema file $sql failed to load"
    ok "$(basename "$sql")"
  done
else
  ok "skipped (database already existed)"
fi

# ---------------------------------------------------------------------------

step "Creating the archive storage roots"

# Two roots, separated by retention tier (DR-0076): material kept forever and
# material kept for a defined period never share a storage root, so a
# retention decision cannot be undone by a filesystem mistake.
mkdir -p "$ARCHIVE_ROOT/permanent" "$ARCHIVE_ROOT/medium-term" \
         "$ARCHIVE_ROOT/quarantine"
chmod 700 "$ARCHIVE_ROOT"
ok "$ARCHIVE_ROOT/{permanent,medium-term,quarantine}"
warn "these directories are NOT backed up by anything yet (OPS-005)"

# ---------------------------------------------------------------------------

step "Compiling the semantic registry"

python3 registry/validate.py >/dev/null || die "registry validation failed"
python3 registry/compile.py >/dev/null || die "registry compilation failed"
ok "registry valid and compiled"

# ---------------------------------------------------------------------------

step "Running the test suite"

FAILED=0
for suite in \
    schema/tests/run.sh \
    sources/tests/test_register.py \
    storage/tests/test_ocfl.py \
    storage/tests/test_fixity_schedule.py \
    collector/tests/test_pipeline.py \
    editorial/tests/test_gate2.py \
    publication/tests/test_gate3.py \
    export/tests/test_dump.py \
    release/tests/test_baseline.py ; do
  name="$(basename "$(dirname "$(dirname "$suite")")")"
  if [ "${suite##*.}" = "sh" ]; then
    out="$(bash "$suite" 2>&1)" || true
  else
    out="$(python3 "$suite" 2>&1)" || true
  fi
  line="$(printf '%s' "$out" | grep -Ei 'passed|failed' | tail -1)"
  if printf '%s' "$line" | grep -q ' 0 failed'; then
    ok "$(printf '%-12s %s' "$name" "$line")"
  else
    printf '    \033[31m✗\033[0m %-12s %s\n' "$name" "${line:-no result}"
    printf '%s\n' "$out" | tail -20
    FAILED=1
  fi
done

[ "$FAILED" -eq 0 ] || die \
  "the suite does not pass on this machine. That is worth knowing: everything
  until now has only ever run in one container. Send the output above."

# ---------------------------------------------------------------------------

step "Done"

cat <<EOF

  The archive is installed and every test passes on this machine.

    repository   $INSTALL_DIR
    database     $DB_NAME
    storage      $ARCHIVE_ROOT

  Nothing has been collected. No source is registered, so nothing is
  authorised to be collected yet — that is the next step, and it is a
  deliberate decision rather than a setting (OPS-001).

  Before anything else, whenever you work here:

      cd $INSTALL_DIR && source .venv/bin/activate

  Then, to see where the project stands:

      python3 release/baseline.py --check --dbname $DB_NAME

  Two things this script did NOT do, both of which matter:

    * No backups. $ARCHIVE_ROOT is the only copy of anything you
      collect (OPS-005 is unsatisfied).
    * No firewall or hardening. This is a plain server.

EOF
