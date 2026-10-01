#!/usr/bin/env python3
"""Acquisition: fetching bytes from a source.

Deliberately the *only* part of the collector that touches the network, so
that everything downstream — quarantine, the three gates, storage, coverage
accounting — is exercised by tests without one.

See collector/README.md on what that means for verification: the pipeline
below this layer is tested end to end; `HttpFetcher` itself is not, because
the build environment's network policy denies general internet hosts.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Mapping, Protocol

# Headers that describe the server's session with *us*, not the document. A
# cookie is state the origin set for a client, never a statement about the
# thing acquired, and a session identifier is the nearest thing a response
# carries to a credential. Dropped by design (issue #74), not by oversight.
UNRECORDED_HEADERS = frozenset({"set-cookie", "set-cookie2"})


def record_headers(headers: Mapping[str, object] | None) -> dict[str, str] | None:
    """The response headers as the acquisition record keeps them (issue #74).

    What the origin sent with the bytes — `Last-Modified`, `ETag`, the
    publisher's own filename and dates — existed only at fetch time and cannot
    be recovered later, so the record keeps them. Shape rules, each for a
    reason:

    - **Names are lower-cased.** HTTP names are case-insensitive (and HTTP/2
      requires lower case), but a JSON key is not: stored as received,
      `ETag` and `Etag` would be two different keys and a conditional request
      (issue #50) looking up one would silently miss the other.
    - **Repeated headers are joined with ", "** (RFC 9110 §5.3), in the order
      received, so none is lost.
    - **Cookies are not recorded** (`UNRECORDED_HEADERS`).
    - **A bad value is repaired, not raised.** A response with a malformed
      header is itself part of the coverage record (record §28, PRES-007);
      it must not turn a successful acquisition into a crash. NUL and
      unpaired surrogates, which PostgreSQL's jsonb cannot hold, are replaced
      with U+FFFD, and a non-text value is stored as its text form.

    Returns None when no headers were received (the request failed before a
    response, or a fixture supplied none), so "none recorded" is a distinct
    state from a response that really carried headers.
    """
    if not headers:
        return None
    merged: dict[str, str] = {}
    for raw_name, raw_value in headers.items():
        name = str(raw_name).strip().lower()
        if not name or name in UNRECORDED_HEADERS:
            continue
        value = raw_value if isinstance(raw_value, str) else str(raw_value)
        value = value.encode("utf-8", "replace").decode("utf-8").replace("\x00", "\ufffd")
        merged[name] = f"{merged[name]}, {value}" if name in merged else value.strip()
    return merged or None


@dataclass(frozen=True)
class FetchResult:
    """The outcome of one acquisition attempt.

    A failure is as much a result as a success: a failed acquisition can
    itself be historically significant (record §28, PRES-007), so this type
    carries failures rather than raising them.
    """

    locator: str
    attempted_at: datetime
    # 'not-modified' is the origin's answer to a conditional request (HTTP 304):
    # the bytes are unchanged since the capture the validators came from, and
    # none were sent (issue #50). It carries no content and needs no
    # explanation, because it is not a failure.
    outcome: str  # 'success' | 'failure' | 'refused' | 'not-found' | 'not-modified'
    content: bytes | None = None
    media_type: str | None = None
    error_detail: str | None = None
    response_headers: dict[str, str] = field(default_factory=dict)
    # The HTTP envelope, needed to wrap the response as a WARC record for
    # sources whose capture format is `warc` (DR-0006). A fetcher that cannot
    # report them cannot serve such a source.
    http_status: int | None = None
    http_reason: str | None = None
    http_version: str = "HTTP/1.1"
    # Where the bytes actually came from after redirects, when that differs
    # from the locator asked for. The redirect chain itself is not captured.
    final_locator: str | None = None

    def __post_init__(self) -> None:
        if self.outcome == "success" and self.content is None:
            raise ValueError("a successful fetch must carry content")
        if self.outcome not in ("success", "not-modified") and not self.error_detail:
            raise ValueError("a failed fetch must explain itself (§28)")

    @property
    def sha256(self) -> bytes:
        if self.content is None:
            raise ValueError("no content to digest")
        return hashlib.sha256(self.content).digest()


class Fetcher(Protocol):
    """How the collector obtains bytes. The seam that keeps the network out.

    A fetcher that can make a conditional request sets `supports_conditional`
    and accepts `validators` (issue #50); one that cannot is simply called
    without it and the collector still skips unchanged bytes by comparing
    digests after the fetch.
    """

    def fetch(self, locator: str) -> FetchResult: ...


def validators_from(headers: Mapping[str, str] | None) -> dict[str, str] | None:
    """The cache validators in a recorded header block, or None if it has none.

    `etag` and `last-modified` are what an origin offers so that a client can
    ask "has this changed since the copy I hold?" (issue #50). They are read
    from the *recorded* headers (`record_headers`, lower-cased names), so the
    answer is the same whichever case the origin used.
    """
    if not headers:
        return None
    found = {k: headers[k] for k in ("etag", "last-modified") if headers.get(k)}
    return found or None


def _header_dict(message) -> dict[str, str]:
    """An http.client header block as one dict, repeated headers joined.

    `dict(message)` keeps only the *first* of a repeated header, so a server
    sending `Link` or `Warning` twice would lose the second at the seam where
    this archive can no longer recover it (issue #74). RFC 9110 §5.3 says a
    repeated field is equivalent to one comma-joined field, except Set-Cookie,
    which is never combined (and is not recorded at all, `UNRECORDED_HEADERS`).
    """
    merged: dict[str, str] = {}
    for name, value in message.items():
        if name in merged and name.lower() not in UNRECORDED_HEADERS:
            merged[name] = f"{merged[name]}, {value}"
        elif name not in merged:
            merged[name] = value
    return merged


def _now() -> datetime:
    return datetime.now(timezone.utc)


class FixtureFetcher:
    """Serves recorded bytes from disk. Used by the test suite.

    Not a mock in the pejorative sense: the pipeline below this layer runs
    exactly as it would in production, against real files, a real database
    and real OCFL storage.
    """

    supports_conditional = True

    def __init__(self, fixtures: dict[str, Path | Exception | FetchResult]):
        self.fixtures = fixtures
        self.calls: list[str] = []
        # What the collector asked, so a test can see whether a conditional
        # request was made and against which validators (issue #50).
        self.validators_seen: list[tuple[str, dict[str, str] | None]] = []

    def fetch(self, locator: str, validators: dict[str, str] | None = None) -> FetchResult:
        self.calls.append(locator)
        self.validators_seen.append((locator, validators))
        entry = self.fixtures.get(locator)

        if entry is None:
            return FetchResult(
                locator=locator,
                attempted_at=_now(),
                outcome="not-found",
                error_detail="no fixture registered for this locator",
            )
        if isinstance(entry, FetchResult):
            return entry
        if isinstance(entry, Exception):
            return FetchResult(
                locator=locator,
                attempted_at=_now(),
                outcome="failure",
                error_detail=f"{type(entry).__name__}: {entry}",
            )
        return FetchResult(
            locator=locator,
            attempted_at=_now(),
            outcome="success",
            content=entry.read_bytes(),
            media_type="application/octet-stream",
            response_headers={"Content-Type": "application/octet-stream"},
            http_status=200,
            http_reason="OK",
        )


class HttpFetcher:
    """Fetches over HTTPS.

    UNVERIFIED IN THIS BUILD. The environment's network policy denies general
    internet hosts, so this class has never completed a live fetch here. It is
    written to the same standard as the rest, but it must be exercised against
    a real source before any claim is made that collection works end to end.

    Politeness and rate limits are per-source policy (DR-0067) and belong to
    the caller; this class does one request.
    """

    supports_conditional = True

    def __init__(self, user_agent: str, timeout: float = 30.0):
        self.user_agent = user_agent
        self.timeout = timeout

    def fetch(self, locator: str, validators: dict[str, str] | None = None) -> FetchResult:
        import urllib.error
        import urllib.request

        request_headers = {"User-Agent": self.user_agent}
        if validators:
            # A conditional request (issue #50): "send it only if it changed".
            if validators.get("etag"):
                request_headers["If-None-Match"] = validators["etag"]
            if validators.get("last-modified"):
                request_headers["If-Modified-Since"] = validators["last-modified"]
        request = urllib.request.Request(locator, headers=request_headers)
        attempted_at = _now()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                # http.client has already undone chunked transfer-encoding;
                # the recorded headers are what it delivered, and a WARC
                # wrapper drops the Transfer-Encoding header so the recorded
                # message stays self-consistent (see warc.build_response_record).
                version = {10: "HTTP/1.0", 11: "HTTP/1.1"}.get(response.version, "HTTP/1.1")
                final = response.geturl()
                return FetchResult(
                    locator=locator,
                    attempted_at=attempted_at,
                    outcome="success",
                    content=response.read(),
                    media_type=response.headers.get_content_type(),
                    response_headers=_header_dict(response.headers),
                    http_status=response.status,
                    http_reason=response.reason,
                    http_version=version,
                    final_locator=final if final != locator else None,
                )
        except urllib.error.HTTPError as exc:
            if exc.code == 304 and validators:
                # Not a failure and not an error: the origin says the bytes are
                # the ones we already hold. Only meaningful when we asked.
                return FetchResult(
                    locator=locator,
                    attempted_at=attempted_at,
                    outcome="not-modified",
                    response_headers=_header_dict(exc.headers) if exc.headers else {},
                    http_status=304,
                    http_reason=str(exc.reason),
                )
            # A refusal or a 404 is a response too: its headers (Retry-After,
            # Server, Date) are coverage facts about the failure (§28).
            return FetchResult(
                locator=locator,
                attempted_at=attempted_at,
                outcome="not-found" if exc.code == 404 else "refused",
                error_detail=f"HTTP {exc.code}: {exc.reason}",
                response_headers=_header_dict(exc.headers) if exc.headers else {},
                http_status=exc.code,
                http_reason=str(exc.reason),
            )
        except Exception as exc:  # noqa: BLE001 — every failure is recordable
            return FetchResult(
                locator=locator,
                attempted_at=attempted_at,
                outcome="failure",
                error_detail=f"{type(exc).__name__}: {exc}",
            )
