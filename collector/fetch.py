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
from typing import Protocol


@dataclass(frozen=True)
class FetchResult:
    """The outcome of one acquisition attempt.

    A failure is as much a result as a success: a failed acquisition can
    itself be historically significant (record §28, PRES-007), so this type
    carries failures rather than raising them.
    """

    locator: str
    attempted_at: datetime
    outcome: str  # 'success' | 'failure' | 'refused' | 'not-found'
    content: bytes | None = None
    media_type: str | None = None
    error_detail: str | None = None
    response_headers: dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.outcome == "success" and self.content is None:
            raise ValueError("a successful fetch must carry content")
        if self.outcome != "success" and not self.error_detail:
            raise ValueError("a failed fetch must explain itself (§28)")

    @property
    def sha256(self) -> bytes:
        if self.content is None:
            raise ValueError("no content to digest")
        return hashlib.sha256(self.content).digest()


class Fetcher(Protocol):
    """How the collector obtains bytes. The seam that keeps the network out."""

    def fetch(self, locator: str) -> FetchResult: ...


def _now() -> datetime:
    return datetime.now(timezone.utc)


class FixtureFetcher:
    """Serves recorded bytes from disk. Used by the test suite.

    Not a mock in the pejorative sense: the pipeline below this layer runs
    exactly as it would in production, against real files, a real database
    and real OCFL storage.
    """

    def __init__(self, fixtures: dict[str, Path | Exception | FetchResult]):
        self.fixtures = fixtures
        self.calls: list[str] = []

    def fetch(self, locator: str) -> FetchResult:
        self.calls.append(locator)
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

    def __init__(self, user_agent: str, timeout: float = 30.0):
        self.user_agent = user_agent
        self.timeout = timeout

    def fetch(self, locator: str) -> FetchResult:
        import urllib.error
        import urllib.request

        request = urllib.request.Request(
            locator, headers={"User-Agent": self.user_agent}
        )
        attempted_at = _now()
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return FetchResult(
                    locator=locator,
                    attempted_at=attempted_at,
                    outcome="success",
                    content=response.read(),
                    media_type=response.headers.get_content_type(),
                    response_headers=dict(response.headers),
                )
        except urllib.error.HTTPError as exc:
            return FetchResult(
                locator=locator,
                attempted_at=attempted_at,
                outcome="not-found" if exc.code == 404 else "refused",
                error_detail=f"HTTP {exc.code}: {exc.reason}",
            )
        except Exception as exc:  # noqa: BLE001 — every failure is recordable
            return FetchResult(
                locator=locator,
                attempted_at=attempted_at,
                outcome="failure",
                error_detail=f"{type(exc).__name__}: {exc}",
            )
