"""Checks on a register export a person downloaded by hand (DR-0118, issue #197).

DR-0118 route A: the collector cannot fetch the NSDC State Register of
Sanctions' exports (its Cloudflare challenge refuses every automated session),
so a person downloads each CSV in a browser and `Collector.import_file` takes
the file. Before anything is admitted, the file is read once, hashed while it
is read, and refused if it is empty, is not UTF-8, carries a header other than
the one recorded for its class, or holds more records than the register said
it had when the person downloaded it.

The expected headers are the ones the founder read from real exports on
2026-09-22 and recorded in ``docs/sources/verification-ua-nsdc-sanctions.md``
(§2d vessels, §2e legal entities and individuals). That record lists the
field names and says the files are UTF-8; it does not record the delimiter
or the quoting. This module assumes a comma-separated file with standard CSV
quoting. If the real file differs, the header check refuses it: the check
fails closed, it does not admit a file it cannot read.

No row content is ever put into a message: a refusal names counts and field
names only. The individuals export carries personal data (DR-0071(b)).
"""

from __future__ import annotations

import csv
import hashlib
import io
from pathlib import Path

# Field names per candidate key, in file order. Source: the verification
# record cited above. Defined once here; the import command and the tests
# read them from this dict.
EXPORT_HEADERS: dict[str, tuple[str, ...]] = {
    "ua-nsdc-sanctions-legal-entities": (
        "sid", "name", "translit_name", "aliases", "status", "country",
        "reg_id", "tax_id", "additional_info", "active_sanctions",
        "sanctions_term", "sanctions_end_date", "last_action_type",
        "last_action_decree", "decree_date", "decree_appendix",
        "position_in_appendix",
    ),
    "ua-nsdc-sanctions-vessels": (
        "sid", "name", "translit_name", "aliases", "status", "country",
        "reg_id", "additional_info", "active_sanctions", "sanctions_term",
        "sanctions_end_date", "last_action_type", "last_action_decree",
        "decree_date", "decree_appendix", "position_in_appendix",
    ),
    "ua-nsdc-sanctions-individuals": (
        "sid", "name", "translit_name", "aliases", "status", "birthdate",
        "citizenship", "identity_docs", "reg_id", "tax_id", "additional_info",
        "active_sanctions", "sanctions_term", "sanctions_end_date",
        "last_action_type", "last_action_decree", "decree_date",
        "decree_appendix", "position_in_appendix",
    ),
}

# DR-0118 Decision 4 (founder, 2026-11-11): the individuals class is not
# imported before DR-0072's successor is recorded. The header stays above so
# the check is ready; the import command refuses the key until this changes,
# which is a founder decision, not a code edit to make in passing.
HELD_UNTIL_DR0072_SUCCESSOR: frozenset[str] = frozenset({"ua-nsdc-sanctions-individuals"})

CHUNK = 1 << 20


def read_hashed(path: Path | str) -> tuple[bytes, str]:
    """Read a file once, computing its SHA-256 as the bytes are read.

    Args:
        path: the downloaded file.

    Returns:
        The file's bytes and their SHA-256 as lower-case hex.

    Raises:
        OSError: the file cannot be read.
    """
    digest = hashlib.sha256()
    buffer = bytearray()
    with open(path, "rb") as handle:
        while chunk := handle.read(CHUNK):
            digest.update(chunk)
            buffer.extend(chunk)
    return bytes(buffer), digest.hexdigest()


def check_export(data: bytes, expected_header: tuple[str, ...],
                 stated_count: int) -> tuple[int, str | None]:
    """Decide whether a downloaded export may be admitted.

    Args:
        data: the file's bytes, as read.
        expected_header: the field names recorded for its class.
        stated_count: the number of records the register's page stated when
            the person downloaded the file.

    Returns:
        ``(records, refusal)``: the number of data records read (0 when the
        file could not be read that far) and ``None`` when the file passes,
        or the reason it is refused. A refusal is a recorded outcome, not an
        exception (PRES-007).
    """
    if not data:
        return 0, "the file is empty"
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        return 0, f"the file is not UTF-8 (byte {exc.start})"
    try:
        rows = [row for row in csv.reader(io.StringIO(text, newline=""))
                if any(field.strip() for field in row)]
    except csv.Error as exc:
        return 0, f"the file is not readable as CSV: {exc}"
    if not rows:
        return 0, "the file holds no rows"
    header = tuple(field.strip() for field in rows[0])
    if header != tuple(expected_header):
        missing = [f for f in expected_header if f not in header]
        extra = [f for f in header if f not in expected_header]
        detail = (f"missing {missing}, unexpected {extra}" if missing or extra
                  else "same fields in a different order")
        return 0, (f"the header is not the one recorded for this class "
                   f"({len(header)} fields, expected {len(expected_header)}; "
                   f"{detail})")
    records = len(rows) - 1
    if records == 0:
        return 0, "the file has a header and no records"
    if records > stated_count:
        return records, (f"the file holds {records} records, more than the "
                         f"{stated_count} the register stated")
    return records, None
