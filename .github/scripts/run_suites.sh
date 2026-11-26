#!/usr/bin/env bash
# Run every check the repository defines and fail if any fails (issue #201).
#
# Used by .github/workflows/tests.yml and runnable by hand in a session with a
# PostgreSQL server reachable through PGHOST/PGPORT/PGUSER(/PGPASSWORD). Each
# suite is run even after an earlier one fails, so one red suite does not hide
# another; the script exits non-zero if any did.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

failed=()
run() {
    local name="$1"; shift
    echo "::group::${name}"
    if "$@"; then
        echo "::endgroup::"
        echo "ok      ${name}"
    else
        echo "::endgroup::"
        echo "FAILED  ${name}"
        failed+=("$name")
    fi
}

run "registry/validate.py" python3 registry/validate.py
run "schema/gen_enums.py --check" python3 schema/gen_enums.py --check
run "decision-record numbering" python3 docs/decision-records/check_numbering.py
run "schema/tests/run.sh" ./schema/tests/run.sh
for suite in */tests/test_*.py; do
    run "$suite" python3 "$suite"
done

echo
if [ "${#failed[@]}" -gt 0 ]; then
    echo "${#failed[@]} check(s) failed:"
    printf '  %s\n' "${failed[@]}"
    exit 1
fi
echo "all checks passed"
