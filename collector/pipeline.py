#!/usr/bin/env python3
"""The collection pipeline: discovery through Gate 1.

Implements SPEC-0003 under DR-0066 (three gates), DR-0069 (quarantine sits
outside the archive), DR-0070 (collector-run coverage), DR-0068 (retention
tiers) and DR-0071 (interim personal-data constraints).

Scope: **discovery, acquisition, quarantine and Gate 1 only.** Gate 2
(editorial acceptance) and Gate 3 (publication) require human decisions at a
risk tier (§78, DR-0063) and are not automated here — which is the point of
their being gates.

Two acquisition paths share everything below the network seam:

- `run()` — live fetches of locators through a `Fetcher`;
- `ingest_warc()` — retrospective recovery from an external web archive's
  WARC file (record §9; WP 3.4 §4, CDR-P3-35 — a **candidate** proposal).
  Each response record within the registered source's scope enters
  quarantine and Gate 1 exactly as a live fetch does; the archive is recorded
  as the acquisition source, distinct from the original publisher (§28).

Integrity note. A holding row and its OCFL object are written in two systems
and cannot share a transaction. The order is: write OCFL first (idempotent by
content), then the database rows in one transaction. If the transaction
fails, the OCFL object exists unreferenced — harmless, and detectable by
`find_orphaned_objects()`. The reverse order would leave a holding pointing
at bytes that do not exist, which is worse: the archive would claim to hold
something it does not (§26).
"""

from __future__ import annotations

import hashlib
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

import psycopg

from fetch import FetchResult, Fetcher
from warc import WarcFormatError, WarcRecord, in_scope, iter_warc_records, verify_payload_digest

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "storage"))
from ocfl import ContentFile, StorageRoot  # noqa: E402


def _uuid() -> str:
    return str(uuid.uuid4())


def _now() -> datetime:
    return datetime.now(timezone.utc)


class PolicyViolation(Exception):
    """Raised when an action would breach a Decision Record."""


@dataclass
class Source:
    """A registered source, as the registry holds it (DR-0067)."""

    id: str
    name: str
    source_type: str
    locator: str | None
    default_retention_tier: str
    default_access_tier: str
    rights_permission: str
    capture_format: str
    lifecycle_state: str
    expects_graphic_content: bool


@dataclass
class RunTotals:
    """Coverage for one collector run (DR-0070, §57)."""

    discovered: int = 0
    acquired: int = 0
    skipped: int = 0
    failed: int = 0
    bytes_preserved: int = 0
    skip_reasons: dict[str, int] = None  # type: ignore[assignment]
    failure_details: list[dict] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.skip_reasons = self.skip_reasons or {}
        self.failure_details = self.failure_details or []


@dataclass(frozen=True)
class Acquisition:
    """How, and from whom, the bytes were obtained (§28).

    The registered source is the *original publisher*. When the bytes come
    from somewhere else — an external web archive, a depositor — that is the
    *acquisition source*, and the project records it rather than implying it
    captured the material itself. `original_captured_at` is the archive's
    capture time (WARC-Date); the attempt's own timestamp is when *we*
    obtained the record.
    """

    route: str = "live-fetch"  # 'live-fetch' | 'external-archive' | 'manual-deposit'
    acquisition_source: str | None = None
    original_captured_at: datetime | None = None
    external_record_id: str | None = None
    external_payload_digest: str | None = None


def capture_series_id(source_id: str, locator: str) -> str:
    """Deterministic series identity: one series per (source, locator).

    Successive captures of one locator — live or recovered from an archive,
    years apart — are different holdings related in the same series
    (DR-0074), so the series needs an identity that does not depend on which
    capture arrived first.
    """
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"{source_id}|{locator}"))


class Collector:
    """Runs one source's collection cycle."""

    def __init__(
        self,
        connection: psycopg.Connection,
        fetcher: Fetcher,
        quarantine_dir: Path,
        storage_roots: dict[str, StorageRoot],
        collector_agent_id: str,
        scanner=None,
    ):
        self.conn = connection
        self.fetcher = fetcher
        self.quarantine_dir = Path(quarantine_dir)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)
        self.roots = storage_roots
        self.agent_id = collector_agent_id
        # Injected so the security check is testable, and so a real scanner
        # can be swapped in without touching the gate logic.
        self.scan = scanner or self._default_scan

    # -- policy ------------------------------------------------------------

    def load_source(self, source_id: str) -> Source:
        row = self.conn.execute(
            """
            SELECT id, name, source_type, locator, default_retention_tier,
                   default_access_tier, rights_permission, capture_format,
                   lifecycle_state, expects_graphic_content
              FROM source WHERE id = %s
            """,
            (source_id,),
        ).fetchone()
        if row is None:
            # DR-0071(a): registered sources only. An unregistered locator is
            # not merely unknown, it is out of policy.
            raise PolicyViolation(
                f"source {source_id} is not in the registry; DR-0071 permits "
                "collection from registered sources only until the "
                "personal-data policy's legal review is recorded"
            )
        return Source(*row)

    @staticmethod
    def _default_scan(content: bytes) -> str:
        """Stand-in security check (DR-0069).

        Returns a `security_check_outcome`. A real deployment substitutes a
        malware scanner; this exists so the gate cannot be bypassed by the
        check being absent, and so the outcome is always recorded.
        """
        if not content:
            return "unreadable"
        # A deliberately visible marker, so the test suite can prove that
        # Gate 1 refuses material a scanner rejects.
        if b"__MALICIOUS_TEST_MARKER__" in content:
            return "malicious"
        return "clean"

    # -- the run -----------------------------------------------------------

    def run(self, source_id: str, locators: list[str], configuration: dict) -> str:
        """Collect the given locators for one source. Returns the run id.

        Coverage is recorded whatever happens: a run that acquires nothing
        still records that it looked, so that absence from the archive is
        never mistaken for absence in the world (§57, DR-0070).
        """
        source = self._active_source(source_id)
        run_id = self._open_run(source, configuration)

        totals = RunTotals()
        for locator in locators:
            totals.discovered += 1
            try:
                self._collect_one(source, locator, run_id, totals)
            except PolicyViolation:
                raise
            except Exception as exc:  # noqa: BLE001
                totals.failed += 1
                totals.failure_details.append(
                    {"locator": locator, "error": f"{type(exc).__name__}: {exc}"}
                )

        self._close_run(run_id, totals)
        return run_id

    def ingest_warc(
        self,
        source_id: str,
        warc_path: Path | str,
        acquisition_source: str,
        configuration: dict,
    ) -> str:
        """Recover a registered source's captures from an external archive's WARC.

        WP 3.4 §4 / CDR-P3-35 (candidate). The file is read locally; obtaining
        it from the archive is a separate, network-bound step this method does
        not perform. Returns the run id.

        Policy, in order:
        - registered, active source only (DR-0071(a), DR-0067), and one with a
          locator — without one there is no scope to enforce;
        - only response records under the source's locator are the source's.
          Anything else in the file is skipped and **not written down**: an
          out-of-scope URL is not this source's, and recording it would put
          material outside human-configured scope into the store;
        - the archive's declared payload digest, where present, must match
          the payload held, or the acquisition is a recorded failure (DR-0075);
        - the complete WARC record is what is quarantined and preserved
          (DR-0006), with the archive as acquisition source and its capture
          time kept distinct from our own (§28).
        """
        source = self._active_source(source_id)
        if not source.locator:
            raise PolicyViolation(
                f"source {source.name!r} has no locator; DR-0071(a) requires "
                "human-configured scope, and without a locator there is none "
                "to hold a WARC file to"
            )
        if not acquisition_source:
            raise PolicyViolation("an external archive must be named (§28)")

        warc_path = Path(warc_path)
        configuration = {
            **configuration,
            "acquisition_route": "external-archive",
            "acquisition_source": acquisition_source,
            "warc_file": warc_path.name,
            "warc_file_sha256": hashlib.sha256(warc_path.read_bytes()).hexdigest(),
        }
        run_id = self._open_run(source, configuration)
        totals = RunTotals()

        try:
            for record in iter_warc_records(warc_path):
                if record.record_type == "revisit":
                    # The archive saw the page unchanged. Evidence of a kind,
                    # but no bytes to hold; counted, not admitted (WP 3.4 §9).
                    totals.discovered += 1
                    self._skip(totals, "warc:revisit")
                    continue
                if not record.is_http_response:
                    continue  # warcinfo, request, metadata: not items
                totals.discovered += 1
                if not in_scope(source.locator, record.target_uri):
                    self._skip(totals, "scope:outside-registered-source")
                    continue
                try:
                    self._ingest_record(source, record, run_id, totals, acquisition_source)
                except PolicyViolation:
                    raise
                except Exception as exc:  # noqa: BLE001
                    totals.failed += 1
                    totals.failure_details.append(
                        {"locator": record.target_uri,
                         "error": f"{type(exc).__name__}: {exc}"}
                    )
        except WarcFormatError as exc:
            # The file itself is bad from here on. What was read stands; the
            # fault is part of the coverage record (§57), not a crash.
            totals.failed += 1
            totals.failure_details.append(
                {"warc_file": warc_path.name, "error": f"WarcFormatError: {exc}",
                 "records_read_before_fault": totals.discovered}
            )

        self._close_run(run_id, totals)
        return run_id

    def _ingest_record(
        self, source: Source, record: WarcRecord, run_id: str,
        totals: RunTotals, acquisition_source: str,
    ) -> None:
        attempted_at = _now()
        locator = record.target_uri or "(no WARC-Target-URI)"
        acquisition = Acquisition(
            route="external-archive",
            acquisition_source=acquisition_source,
            original_captured_at=record.date or attempted_at,
            external_record_id=record.record_id,
            external_payload_digest=record.headers.get("warc-payload-digest"),
        )
        status, _, _ = record.http()
        digest_status, digest_detail = verify_payload_digest(record)
        captured = record.date.isoformat() if record.date else "an unknown time"

        if digest_status == "mismatch":
            result = FetchResult(locator, attempted_at, "failure",
                                 error_detail=f"{digest_detail} (captured {captured})")
        elif status in (404, 410):
            result = FetchResult(locator, attempted_at, "not-found",
                                 error_detail=f"archive holds HTTP {status} captured {captured}")
        elif status is None or not 200 <= status < 300:
            result = FetchResult(locator, attempted_at, "refused",
                                 error_detail=f"archive holds HTTP {status} captured {captured}")
        else:
            result = FetchResult(
                locator, attempted_at, "success",
                content=record.raw,  # the whole record: headers and all (DR-0006)
                media_type="application/warc",
                response_headers=dict(record.headers),
            )
        self._admit(source, locator, run_id, totals, result, acquisition,
                    content_name="original.warc",
                    digest_note=(digest_detail if digest_status == "verified" else None))

    # -- run bookkeeping -----------------------------------------------------

    def _active_source(self, source_id: str) -> Source:
        source = self.load_source(source_id)
        if source.lifecycle_state != "active":
            raise PolicyViolation(
                f"source {source.name!r} is {source.lifecycle_state}, not active"
            )
        return source

    def _open_run(self, source: Source, configuration: dict) -> str:
        run_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO collector_run
                (id, source_id, collector_agent_id, configuration, started_at)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (run_id, source.id, self.agent_id,
             psycopg.types.json.Jsonb(configuration), _now()),
        )
        return run_id

    @staticmethod
    def _skip(totals: RunTotals, reason: str) -> None:
        totals.skipped += 1
        totals.skip_reasons[reason] = totals.skip_reasons.get(reason, 0) + 1

    def _close_run(self, run_id: str, totals: RunTotals) -> None:
        self.conn.execute(
            """
            UPDATE collector_run
               SET ended_at = %s, items_discovered = %s, items_acquired = %s,
                   items_skipped = %s, items_failed = %s, bytes_preserved = %s,
                   skip_reasons = %s, failure_details = %s
             WHERE id = %s
            """,
            (
                _now(), totals.discovered, totals.acquired, totals.skipped,
                totals.failed, totals.bytes_preserved,
                psycopg.types.json.Jsonb(totals.skip_reasons),
                psycopg.types.json.Jsonb(totals.failure_details),
                run_id,
            ),
        )

    # -- one item, from acquisition result to Gate 1 -------------------------

    def _collect_one(
        self, source: Source, locator: str, run_id: str, totals: RunTotals
    ) -> None:
        result = self.fetcher.fetch(locator)
        self._admit(source, locator, run_id, totals, result, Acquisition())

    def _admit(
        self, source: Source, locator: str, run_id: str, totals: RunTotals,
        result: FetchResult, acquisition: Acquisition,
        content_name: str = "original.bin", digest_note: str | None = None,
    ) -> None:
        """Everything after the bytes are in hand, whichever way they came."""
        attempt_id = self._record_attempt(source, locator, run_id, result, acquisition)

        if result.outcome != "success":
            totals.failed += 1
            totals.failure_details.append(
                {"locator": locator, "outcome": result.outcome,
                 "error": result.error_detail}
            )
            return

        quarantine_id = self._quarantine(attempt_id, result)
        if digest_note:
            # The archive's own digest checked against what we hold (DR-0075).
            self._record_event("fixity-check", None, quarantine_id, "success", digest_note)
        outcome = self._security_check(quarantine_id, result)

        if outcome != "clean":
            self._decide_gate1(quarantine_id, "rejected",
                               f"security check: {outcome}")
            self._skip(totals, f"security:{outcome}")
            return

        if source.default_retention_tier in ("discard", "metadata-only"):
            # Recorded as seen, deliberately not stored (DR-0068).
            self._decide_gate1(quarantine_id, "admitted",
                               f"retention tier {source.default_retention_tier}")
            self._skip(totals, f"retention:{source.default_retention_tier}")
            return

        self._decide_gate1(quarantine_id, "admitted", "passed security check")
        captured_at = acquisition.original_captured_at or result.attempted_at
        self._preserve(source, quarantine_id, locator, result, captured_at, content_name)
        totals.acquired += 1
        totals.bytes_preserved += len(result.content or b"")

    # -- steps -------------------------------------------------------------

    def _record_attempt(
        self, source: Source, locator: str, run_id: str, result: FetchResult,
        acquisition: Acquisition,
    ) -> str:
        attempt_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO acquisition_attempt
                (id, source_id, collector_run_id, locator, attempted_at,
                 outcome, error_detail, acquisition_route, acquisition_source,
                 original_captured_at, external_record_id, external_payload_digest)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (attempt_id, source.id, run_id, locator, result.attempted_at,
             result.outcome, result.error_detail, acquisition.route,
             acquisition.acquisition_source, acquisition.original_captured_at,
             acquisition.external_record_id, acquisition.external_payload_digest),
        )
        return attempt_id

    def _quarantine(self, attempt_id: str, result: FetchResult) -> str:
        """Hold acquired bytes outside the archive until Gate 1 (DR-0069)."""
        quarantine_id = _uuid()
        path = self.quarantine_dir / quarantine_id
        path.write_bytes(result.content or b"")
        self.conn.execute(
            """
            INSERT INTO quarantine_item
                (id, acquisition_attempt_id, received_at, byte_size, sha256)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (quarantine_id, attempt_id, result.attempted_at,
             len(result.content or b""), result.sha256),
        )
        return quarantine_id

    def _security_check(self, quarantine_id: str, result: FetchResult) -> str:
        outcome = self.scan(result.content or b"")
        self.conn.execute(
            "UPDATE quarantine_item SET security_check_at = %s, "
            "security_check_outcome = %s WHERE id = %s",
            (_now(), outcome, quarantine_id),
        )
        self._record_event("virus-check", None, quarantine_id,
                           "success" if outcome == "clean" else "failure",
                           f"scanner outcome: {outcome}")
        return outcome

    def _decide_gate1(self, quarantine_id: str, decision: str, rationale: str) -> None:
        self.conn.execute(
            """
            UPDATE quarantine_item
               SET gate1_decision = %s, gate1_decided_at = %s,
                   gate1_decided_by = %s, gate1_rationale = %s
             WHERE id = %s
            """,
            (decision, _now(), self.agent_id, rationale, quarantine_id),
        )

    def _preserve(
        self, source: Source, quarantine_id: str, locator: str, result: FetchResult,
        captured_at: datetime, content_name: str,
    ) -> None:
        """Gate 1 admission: quarantine -> OCFL -> canonical store -> series."""
        tier = source.default_retention_tier
        root = self.roots.get(tier)
        if root is None:
            raise PolicyViolation(f"no storage root configured for tier {tier!r}")

        holding_id = _uuid()
        ocfl_object_id = f"holding-{holding_id}"
        quarantine_path = self.quarantine_dir / quarantine_id

        # OCFL first: an unreferenced object is recoverable, whereas a holding
        # pointing at absent bytes would have the archive claim to hold what
        # it does not (§26).
        root.create_object(
            ocfl_object_id,
            [ContentFile(quarantine_path, content_name)],
            message=f"Gate 1 admission: {locator}",
            user=str(self.agent_id),
        )
        inventory = root.read_inventory(ocfl_object_id)
        content_digest = next(iter(inventory["manifest"]))
        fixity_digest = next(iter(inventory["fixity"]["sha256"]))

        object_id = _uuid()
        self.conn.execute(
            """
            INSERT INTO preserved_object
                (id, object_level, original_name, format_identifier, byte_size,
                 sha512, sha256, ocfl_root, ocfl_object_id, ocfl_version,
                 ingested_at)
            VALUES (%s, 'representation', %s, %s, %s, decode(%s,'hex'),
                    decode(%s,'hex'), %s, %s, 'v1', %s)
            """,
            (object_id, locator, result.media_type, len(result.content or b""),
             content_digest, fixity_digest, tier, ocfl_object_id, _now()),
        )

        self.conn.execute(
            """
            INSERT INTO holding
                (id, completeness, retention_tier, access_tier,
                 rights_permission, ocfl_object_id)
            VALUES (%s, 'original', %s, %s, %s, %s)
            """,
            (holding_id, tier, source.default_access_tier,
             source.rights_permission, ocfl_object_id),
        )
        self.conn.execute(
            "INSERT INTO holding_representation VALUES (%s, %s, 'original')",
            (holding_id, object_id),
        )
        # DR-0074: a capture series relates successive captures of one
        # locator as separate holdings. `captured_at` is when the page was
        # captured — by us, or by the archive we recovered it from — which is
        # the time the series is ordered by.
        self.conn.execute(
            """
            INSERT INTO capture_series_member (series_id, holding_id, locator, captured_at)
            VALUES (%s, %s, %s, %s)
            """,
            (capture_series_id(source.id, locator), holding_id, locator, captured_at),
        )

        self._record_event("ingestion", object_id, None, "success",
                           f"admitted from quarantine {quarantine_id}")
        self._record_event("message-digest-calculation", object_id, None,
                           "success", "sha512 content address, sha256 fixity")

    def _record_event(
        self, event_type: str, object_id: str | None,
        quarantine_id: str | None, outcome: str, detail: str,
    ) -> None:
        self.conn.execute(
            """
            INSERT INTO preservation_event
                (id, event_type, object_id, quarantine_item_id, agent_id,
                 occurred_at, outcome, outcome_detail)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (_uuid(), event_type, object_id, quarantine_id, self.agent_id,
             _now(), outcome, detail),
        )


def find_orphaned_objects(
    connection: psycopg.Connection, roots: dict[str, StorageRoot]
) -> list[str]:
    """OCFL objects no holding references.

    The reconciliation that makes the two-system write order safe: an object
    written before a failed database transaction shows up here rather than
    being lost track of.
    """
    referenced = {
        row[0] for row in connection.execute(
            "SELECT ocfl_object_id FROM holding WHERE ocfl_object_id IS NOT NULL"
        )
    }
    orphans = []
    for root in roots.values():
        orphans.extend(oid for oid in root.object_ids() if oid not in referenced)
    return sorted(orphans)
