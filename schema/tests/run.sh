#!/usr/bin/env bash
# Build the canonical store from scratch and run the schema test suite.
#
# Always drops and recreates the database: the suite asserts on a known
# fixture state, so it must never run against a dirty one.
#
# Exits non-zero on any failure, so it can gate a release baseline (DR-0048).
#
# Environment: PGHOST, PGPORT, PGUSER as usual. PGDATABASE defaults to uiw_test.
set -euo pipefail

DB="${PGDATABASE:-uiw_test}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
unset PGDATABASE

echo "Rebuilding ${DB}"
psql -q -c "DROP DATABASE IF EXISTS ${DB}" -c "CREATE DATABASE ${DB}" postgres

for f in "$ROOT"/schema/0*.sql; do
    echo "  loading $(basename "$f")"
    psql -q -d "$DB" -v ON_ERROR_STOP=1 -f "$f" > /dev/null
done

echo
output=$(psql -d "$DB" -v ON_ERROR_STOP=1 -f "$ROOT/schema/tests/test_schema.sql" 2>&1) || {
    echo "$output" | grep -E "ERROR|FAIL" || true
    echo
    echo "SUITE FAILED"
    exit 1
}

echo "$output" | grep -o "PASS  .*" || true
passes=$(echo "$output" | grep -c "PASS" || true)
echo
echo "${passes} passed, 0 failed"
