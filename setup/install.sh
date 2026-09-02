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

# Refuse to install anything into a directory a web server publishes. The
# archive holds material at every access tier, including `confidential`, and a
# document root is the one place on the machine where a file is public by
# default. SEC-004 forbids a tier leak in any layer; a path leak is the
# crudest possible version of one.
for path in "$INSTALL_DIR" "$ARCHIVE_ROOT"; do
  case "$path" in
    /var/www/*|/srv/www/*|/usr/share/nginx/*|/home/*/public_html/*|*/httpdocs/*)
      die "refusing to install into '$path', which looks web-served.
  The archive holds material at every access tier and a document root
  publishes files by default. Choose a path outside the web tree:

      INSTALL_DIR=/opt/uiw ARCHIVE_ROOT=/opt/uiw-archive bash setup/install.sh"
      ;;
  esac
done

# A control panel manages its own services and package pins. Postgres from apt
# does not normally collide with one, but it is worth knowing you are on such
# a machine before it does.
if [ -d /usr/local/psa ] || [ -d /usr/local/cpanel ] || [ -d /opt/plesk ]; then
  warn "this looks like a control-panel host (Plesk/cPanel)"
  warn "the archive will run alongside whatever else it serves — see the note"
  warn "at the end of this script about keeping the two separate"
  CONTROL_PANEL=yes
else
  CONTROL_PANEL=no
fi

# ---------------------------------------------------------------------------

step "Installing PostgreSQL, Python and git"

export DEBIAN_FRONTEND=noninteractive

# Another process may hold the dpkg lock — unattended-upgrades on a fresh
# server, or a control panel doing its own housekeeping. That is ordinary and
# temporary, so wait for it rather than failing. Waiting is also the only safe
# response: killing the holder or deleting the lock can leave dpkg in a
# half-configured state that is far more work to repair than the wait.
wait_for_apt() {
    local waited=0 holder
    while $SUDO fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1; do
        if [ "$waited" -eq 0 ]; then
            holder="$($SUDO fuser /var/lib/dpkg/lock-frontend 2>/dev/null \
                      | tr -d ' ')"
            warn "another process (pid ${holder:-?}) is using apt; waiting"
            [ -n "$holder" ] && ps -p "$holder" -o cmd= 2>/dev/null \
                | sed 's/^/      /'
        fi
        sleep 5
        waited=$((waited + 5))
        [ "$waited" -lt 600 ] || die \
          "apt has been locked for 10 minutes. Check how long the holder has
  actually been running:

    ps -o pid,stat,tty,etime,cmd -p \$(sudo fuser /var/lib/dpkg/lock-frontend)

  If ELAPSED is minutes, it is working — wait and re-run this script.

  If ELAPSED is hours or days, it is STUCK, not busy. An interactive
  apt/dpkg run that lost its terminal sits forever on a prompt nobody can
  answer (a modified config file, or 'which services should be restarted?').
  A machine in that state has also stopped receiving security updates.
  Check for a recoverable session first — 'screen -ls', 'tmux ls' — since
  reattaching and answering the prompt is much the cleanest fix.

  Either way: do NOT delete the lock file, and do not SIGKILL the holder.
  Interrupting a package transaction mid-write turns an annoyance into a
  broken system."
        [ $((waited % 60)) -eq 0 ] && warn "still waiting (${waited}s)"
    done
    [ "$waited" -gt 0 ] && ok "apt lock released after ${waited}s"
    return 0
}

# `fuser` lives in psmisc, which is not guaranteed to be present. Without it
# the wait cannot run, so fall through to apt's own retry behaviour rather
# than pretending to have waited.
if command -v fuser >/dev/null 2>&1; then
    wait_for_apt
else
    warn "fuser not available; cannot detect the apt lock in advance"
fi

# -o DPkg::Lock::Timeout makes apt itself wait too, which covers the race
# between the check above and the command below.
APT_OPTS=(-o DPkg::Lock::Timeout=300)
$SUDO apt-get "${APT_OPTS[@]}" update -qq
$SUDO apt-get "${APT_OPTS[@]}" install -y -qq \
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

if [ "$CONTROL_PANEL" = yes ]; then
cat <<EOF
  A note about this machine specifically.

  It runs a control panel, so it is presumably also serving a public website.
  The archive now shares it. That works, and it is a reasonable place to
  start, but two things follow:

    * Keep them apart on disk. The archive lives at $ARCHIVE_ROOT
      and the repository at $INSTALL_DIR, both outside the web tree.
      Nothing should ever be moved or symlinked into a document root: the
      archive holds material at every access tier, and a document root
      publishes files by default (SEC-004).

    * They fail together. A compromise of the public site, or of the panel,
      reaches the archive on the same box. The archive is the part that
      cannot be rebuilt. Separating them onto different machines is worth
      doing before there is much in it — and backups matter more here, not
      less, for the same reason.

EOF
fi
