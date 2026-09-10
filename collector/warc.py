#!/usr/bin/env python3
"""Reading WARC records for retrospective recovery from external web archives.

Implements the reader half of WP 3.4 §4 / CDR-P3-35 (**candidate** — if the
founder amends that proposal, this module changes with it). The pipeline half
is `Collector.ingest_warc` in pipeline.py.

Why a reader of our own rather than a library: the project's runtime
dependencies are PostgreSQL, Python, psycopg and PyYAML (setup/install.sh),
and WARC (ISO 28500) is a deliberately simple format — a version line,
header lines, a blank line, a Content-Length block, and a two-CRLF trailer.
Reading it takes a page of code, and that page can be read by a future
archivist without installing anything. Where a WARC library is available in
the test environment, the suite cross-checks this reader against it.

What is preserved is the **complete record** — WARC headers, HTTP status
line and headers, and body — because the server-response evidence is what
gives web preservation its evidentiary weight (DR-0006). The body alone is a
derivative, produced later by normalization (SPEC-0003 §6).

Verified against files written by this repository's tests and by warcio;
**not** verified against Common Crawl or Wayback Machine output, which the
build environment cannot reach. Expect to find something on first contact.
"""

from __future__ import annotations

import base64
import binascii
import gzip
import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import BinaryIO, Iterable, Iterator
from urllib.parse import urlsplit


class WarcFormatError(Exception):
    """The bytes do not form a WARC record we can read."""


@dataclass(frozen=True)
class WarcRecord:
    """One WARC record, kept whole.

    `raw` is the record exactly as it lay in the file, including its WARC
    headers and trailer: what goes into the archive. `block` is the record's
    content block; for response records that is an HTTP message.
    """

    version: str
    record_type: str
    record_id: str | None
    date: datetime | None
    target_uri: str | None
    headers: dict[str, str]  # WARC header names lower-cased
    block: bytes
    raw: bytes

    # -- HTTP, for response records ---------------------------------------

    @property
    def is_http_response(self) -> bool:
        ct = self.headers.get("content-type", "").lower()
        return self.record_type == "response" and (
            ct.startswith("application/http") or self.block.startswith(b"HTTP/")
        )

    def http(self) -> tuple[int | None, dict[str, str], bytes]:
        """Status, headers (lower-cased names), and body as transmitted.

        Returns (None, {}, block) when the block is not an HTTP message, so
        callers can still preserve it.
        """
        if not self.block.startswith(b"HTTP/"):
            return None, {}, self.block
        sep = self.block.find(b"\r\n\r\n")
        seplen = 4
        if sep < 0:
            sep = self.block.find(b"\n\n")
            seplen = 2
        if sep < 0:
            head, body = self.block, b""
        else:
            head, body = self.block[:sep], self.block[sep + seplen:]
        lines = head.decode("iso-8859-1").splitlines()
        status: int | None = None
        parts = lines[0].split(" ", 2) if lines else []
        if len(parts) >= 2 and parts[1].isdigit():
            status = int(parts[1])
        headers: dict[str, str] = {}
        for line in lines[1:]:
            name, colon, value = line.partition(":")
            if colon:
                headers[name.strip().lower()] = value.strip()
        return status, headers, body

    def payload(self) -> bytes:
        """The HTTP entity body with chunked transfer-encoding removed.

        Best effort: a body that claims to be chunked but is not parseable is
        returned as transmitted rather than lost.
        """
        _, headers, body = self.http()
        if "chunked" in headers.get("transfer-encoding", "").lower():
            try:
                return _dechunk(body)
            except ValueError:
                return body
        return body


def _dechunk(body: bytes) -> bytes:
    out = bytearray()
    pos = 0
    while True:
        end = body.find(b"\r\n", pos)
        if end < 0:
            raise ValueError("chunk size line never ends")
        size_field = body[pos:end].split(b";", 1)[0].strip()
        size = int(size_field, 16)
        pos = end + 2
        if size == 0:
            return bytes(out)
        chunk = body[pos:pos + size]
        if len(chunk) != size:
            raise ValueError("chunk shorter than declared")
        out += chunk
        pos += size
        if body[pos:pos + 2] != b"\r\n":
            raise ValueError("chunk not terminated")
        pos += 2


# -- reading -----------------------------------------------------------------


def iter_warc_records(path: Path | str) -> Iterator[WarcRecord]:
    """Yield every record in a .warc or .warc.gz file, in order.

    Multi-member gzip (one member per record, the usual layout) is handled by
    the standard library's gzip reader transparently. Raises WarcFormatError
    on a malformed or truncated record; records read before the fault have
    already been yielded, so a caller can record how far it got (§28).
    """
    with open(path, "rb") as fh:
        magic = fh.read(2)
        fh.seek(0)
        if magic == b"\x1f\x8b":
            with gzip.GzipFile(fileobj=fh) as gz:
                yield from read_records(gz)
        else:
            yield from read_records(fh)


def read_records(stream: BinaryIO) -> Iterator[WarcRecord]:
    while True:
        line = stream.readline()
        while line in (b"\r\n", b"\n"):  # inter-record separators
            line = stream.readline()
        if not line:
            return
        if not line.startswith(b"WARC/"):
            raise WarcFormatError(
                f"expected a WARC version line, got {line[:24]!r}"
            )
        raw = bytearray(line)
        version = line.rstrip(b"\r\n").decode("ascii", "replace")

        headers: dict[str, str] = {}
        while True:
            hline = stream.readline()
            if not hline:
                raise WarcFormatError("truncated record: header block never ended")
            raw += hline
            if hline in (b"\r\n", b"\n"):
                break
            name, colon, value = hline.decode("utf-8", "replace").partition(":")
            if not colon:
                raise WarcFormatError(f"malformed WARC header line {hline[:40]!r}")
            headers[name.strip().lower()] = value.strip()

        try:
            length = int(headers["content-length"])
        except (KeyError, ValueError):
            raise WarcFormatError("record without a valid Content-Length") from None
        block = stream.read(length)
        if len(block) != length:
            raise WarcFormatError(
                f"truncated record: Content-Length {length}, only {len(block)} bytes present"
            )
        raw += block

        # The trailer is two CRLFs. Consume line terminators one at a time so
        # a file that is short of the specification does not cost us the
        # start of the next record.
        for _ in range(4):
            nxt = stream.peek(1)[:1]
            if nxt not in (b"\r", b"\n"):
                break
            raw += stream.read(1)

        yield WarcRecord(
            version=version,
            record_type=headers.get("warc-type", "").lower(),
            record_id=headers.get("warc-record-id"),
            date=_parse_date(headers.get("warc-date")),
            target_uri=_strip_angles(headers.get("warc-target-uri")),
            headers=headers,
            block=bytes(block),
            raw=bytes(raw),
        )


def _strip_angles(value: str | None) -> str | None:
    # WARC 1.0 wrote the target URI as <uri>; 1.1 and every tool write it bare.
    if value and value.startswith("<") and value.endswith(">"):
        return value[1:-1]
    return value


def _parse_date(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


# -- writing -----------------------------------------------------------------------

HOP_BY_HOP_UNDONE = ("transfer-encoding",)


def digest_header(data: bytes, algorithm: str = "sha1") -> str:
    """`algo:BASE32` as WARC tools write it (sha1, upper-case base32, no padding)."""
    return f"{algorithm}:" + base64.b32encode(hashlib.new(algorithm, data).digest()).decode()


def build_response_record(
    target_uri: str,
    status: int,
    reason: str,
    headers: Iterable[tuple[str, str]],
    body: bytes,
    captured_at: datetime,
    http_version: str = "HTTP/1.1",
    record_id: str | None = None,
) -> bytes:
    """A single WARC 1.1 response record wrapping one HTTP response.

    Used by the live path so a source whose capture format is `warc`
    (DR-0006) actually receives one: status line, headers and body preserved
    together, with WARC-Date as the capture time and payload and block
    digests declared. It is written by the same rules the reader reads, so
    the two paths — live capture and recovery from an external archive —
    produce byte-comparable holdings.

    Honest limits: this wraps what an HTTP client library delivered, not the
    wire. Chunked transfer-encoding has already been undone by the client, so
    the Transfer-Encoding header is dropped to keep the recorded message
    self-consistent; the request, and any redirect responses on the way, are
    not recorded. A WARC-native capture tool for the high-value tier remains
    DR-0006's plan; this is the lighter form, recorded as such (§26).
    """
    if captured_at.tzinfo is None:
        raise ValueError("captured_at must be timezone-aware")
    kept = [(k, v) for k, v in headers if k.lower() not in HOP_BY_HOP_UNDONE]
    http_head = f"{http_version} {status} {reason}\r\n" + "".join(
        f"{k}: {v}\r\n" for k, v in kept
    )
    block = http_head.encode("iso-8859-1") + b"\r\n" + body
    rid = record_id or f"<urn:uuid:{uuid.uuid4()}>"
    date = captured_at.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    warc_head = (
        "WARC/1.1\r\n"
        "WARC-Type: response\r\n"
        f"WARC-Record-ID: {rid}\r\n"
        f"WARC-Date: {date}\r\n"
        f"WARC-Target-URI: {target_uri}\r\n"
        "Content-Type: application/http; msgtype=response\r\n"
        f"WARC-Payload-Digest: {digest_header(body)}\r\n"
        f"WARC-Block-Digest: {digest_header(block)}\r\n"
        f"Content-Length: {len(block)}\r\n"
        "\r\n"
    )
    return warc_head.encode("utf-8") + block + b"\r\n\r\n"


# -- the archive's own digest --------------------------------------------------


def verify_payload_digest(record: WarcRecord) -> tuple[str, str]:
    """Check the record's WARC-Payload-Digest against its payload.

    Returns (status, detail), status one of 'verified', 'mismatch',
    'undeclared', 'unsupported'. Two digests disagreeing is a signal
    (DR-0075); an archive's declared digest that does not match what we hold
    means the bytes are not what the archive says it captured, and the
    acquisition is recorded as failed rather than preserved as if intact.

    Tools differ on whether the payload digest covers the body as transmitted
    or after chunked decoding, so both are accepted.
    """
    declared = record.headers.get("warc-payload-digest")
    if not declared:
        return "undeclared", "no WARC-Payload-Digest declared by the archive"
    algorithm, _, encoded = declared.partition(":")
    algorithm = algorithm.strip().lower()
    if algorithm not in hashlib.algorithms_available:
        return "unsupported", f"digest algorithm {algorithm!r} not available"
    expected = _decode_digest(encoded.strip())
    if expected is None:
        return "unsupported", f"digest value {encoded!r} is neither base32 nor hex"

    _, _, transmitted = record.http()
    candidates = [transmitted]
    decoded = record.payload()
    if decoded != transmitted:
        candidates.append(decoded)
    for candidate in candidates:
        if hashlib.new(algorithm, candidate).digest() == expected:
            return "verified", f"WARC-Payload-Digest {declared} verified"
    return "mismatch", f"WARC-Payload-Digest {declared} does not match the payload held"


def _decode_digest(value: str) -> bytes | None:
    for decoder in (
        lambda v: base64.b32decode(v.upper() + "=" * (-len(v) % 8)),
        lambda v: bytes.fromhex(v),
    ):
        try:
            return decoder(value)
        except (binascii.Error, ValueError):
            continue
    return None


# -- scope (DR-0071(a)) ----------------------------------------------------------


def in_scope(source_locator: str | None, target_uri: str | None) -> bool:
    """Is this URI within the registered source's locator?

    A WARC from an external archive contains whatever the archive crawled.
    Only records under the registered locator are the registered source's;
    everything else is outside human-configured scope (DR-0071(a)) and is not
    even written down. The rule: same host or a subdomain of it (a leading
    "www." is disregarded on both sides), and the source's path as a prefix
    when it has one. Scheme is ignored — http and https captures of one site
    are one site.
    """
    if not source_locator or not target_uri:
        return False
    src, tgt = urlsplit(source_locator), urlsplit(target_uri)
    if tgt.scheme.lower() not in ("http", "https"):
        return False
    src_host = _host(src.hostname)
    tgt_host = _host(tgt.hostname)
    if not src_host or not tgt_host:
        return False
    if not (tgt_host == src_host or tgt_host.endswith("." + src_host)):
        return False
    prefix = (src.path or "/").rstrip("/")
    if prefix:
        tgt_path = tgt.path or "/"
        if not (tgt_path == prefix or tgt_path.startswith(prefix + "/")):
            return False
    return True


def _host(hostname: str | None) -> str:
    host = (hostname or "").lower().rstrip(".")
    return host[4:] if host.startswith("www.") else host
