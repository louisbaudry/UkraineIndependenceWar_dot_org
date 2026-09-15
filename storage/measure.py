#!/usr/bin/env python3
"""Storage and bandwidth measurement (WP 3.4 §4.1, Track A item A7).

WP 3.4 §5.3 leaves storage volume, bandwidth and backup cost "unknown until
A7 measures them" and says the plan sizes storage "after the first
retrospective pull, not before". This module is that measurement: it reads
what the pipeline already recorded (`collector_run`, DR-0070) and what is
actually on disk (the OCFL storage roots, DR-0073/0076, and the quarantine
directory, DR-0069) and reports real bytes and real throughput, never an
estimate dressed up as one.

It collects nothing itself — no fetch, no database write. Reading
`collector_run` and walking a storage root is exactly the kind of
preparatory measurement DR-0071's scale-up bar (record standing ruling,
2026-09-08) does not touch: it reports on collection already authorised and
already done, the same posture as `find_orphaned_objects` in
collector/pipeline.py.

Two things this module does **not** attempt, and why:

* **"One retrospective pull for a registered domain" (WP 3.4's other A7
  clause).** That is a new acquisition — it belongs to `collector/run.py`
  against a registered source, on the archive server, the same as any other
  collection run (DR-0093 §3: a person is the agent of record). Running it
  from here would be new collection decided unilaterally by a session, not
  measurement of what was decided. This module reports on whatever such a
  pull produces once it exists as a `collector_run` row; it does not create
  one.
* **Sizing the *other* five sanctions sources.** Nothing about the two
  registered sources' size predicts an unregistered one's — `eur-lex-sanctions`
  and `ua-nsdc-sanctions` are not yet identified to a specific instrument
  (CLAUDE.md Track A row A1), and the founder has not registered the
  remaining candidates. `--extrapolate` multiplies the measured *average per
  source* by a source count the caller supplies, clearly labelled as a
  projection, not a fifth measured number.

What is measured, given a reachable database and storage roots:

* **Preserved bytes and throughput per source and per run**, from
  `collector_run.bytes_preserved` and `ended_at - started_at` — the figure
  the pipeline itself records as "bytes this run actually admitted",
  distinct from what quarantine received (which includes items later
  rejected or discarded, DR-0068/0069).
* **Actual on-disk footprint**, per retention-tier storage root and for the
  quarantine directory, by walking the filesystem rather than trusting any
  database total — the two are expected to disagree, and the disagreement
  is the point (see below).
* **The duplication overhead collector/README documents as an open gap**:
  quarantine copies are never removed after Gate 1 admits them (see
  collector/README.md, "What is verified, and what is not"), so today's
  on-disk footprint is expected to run close to double `bytes_preserved`.
  Reporting the actual ratio turns that known gap into the real number
  WP 3.4 §5.3 needs, instead of leaving it as a caveat with no size.

Run:
    PGHOST=… PGPORT=… PGUSER=… python3 storage/measure.py \\
        --archive-root /path/to/archive [--source-id UUID] [--json]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from ocfl import StorageRoot, TIERS  # noqa: E402


@dataclass
class RunMeasurement:
    run_id: str
    source_id: str
    source_name: str
    started_at: str
    duration_seconds: float | None
    items_acquired: int
    bytes_preserved: int
    bytes_per_second: float | None  # None when duration is zero or unknown


@dataclass
class SourceMeasurement:
    source_id: str
    source_name: str
    runs: int
    items_acquired: int
    bytes_preserved: int
    total_duration_seconds: float
    average_bytes_per_second: float | None


@dataclass
class DiskFootprint:
    path: str
    file_count: int
    on_disk_bytes: int


@dataclass
class Report:
    by_run: list[RunMeasurement] = field(default_factory=list)
    by_source: list[SourceMeasurement] = field(default_factory=list)
    total_bytes_preserved: int = 0
    ocfl_footprint: list[DiskFootprint] = field(default_factory=list)
    quarantine_footprint: DiskFootprint | None = None
    duplication_ratio: float | None = None  # (ocfl + quarantine) / preserved
    extrapolated_sources: int | None = None
    extrapolated_bytes: float | None = None

    def to_dict(self) -> dict:
        d = asdict(self)
        return d


# ---------------------------------------------------------------------------
# What was recorded (collector_run)
# ---------------------------------------------------------------------------

def measure_runs(conn, source_id: str | None = None) -> list[RunMeasurement]:
    """One row per completed collector_run, with derived throughput.

    Only runs with an `ended_at` yield a throughput figure — a run still in
    progress, or one that crashed before recording an end (§57's outage
    case), has an unknown duration, not a zero one.
    """
    query = """
        SELECT cr.id, cr.source_id, s.name, cr.started_at,
               EXTRACT(EPOCH FROM (cr.ended_at - cr.started_at)),
               cr.items_acquired, cr.bytes_preserved
          FROM collector_run cr
          JOIN source s ON s.id = cr.source_id
         WHERE cr.ended_at IS NOT NULL
    """
    params: tuple = ()
    if source_id is not None:
        query += " AND cr.source_id = %s"
        params = (source_id,)
    query += " ORDER BY cr.started_at"

    measurements = []
    for row in conn.execute(query, params):
        (run_id, src_id, src_name, started_at, duration, acquired,
         bytes_preserved) = row
        duration_s = float(duration) if duration is not None else None
        throughput = (
            bytes_preserved / duration_s
            if duration_s and duration_s > 0
            else None
        )
        measurements.append(RunMeasurement(
            run_id=str(run_id), source_id=str(src_id), source_name=src_name,
            started_at=str(started_at), duration_seconds=duration_s,
            items_acquired=acquired, bytes_preserved=bytes_preserved,
            bytes_per_second=throughput,
        ))
    return measurements


def summarize_by_source(runs: list[RunMeasurement]) -> list[SourceMeasurement]:
    """Fold per-run measurements into one row per source (WP 3.4 A7's unit)."""
    by_source: dict[str, dict] = {}
    for r in runs:
        acc = by_source.setdefault(r.source_id, {
            "source_name": r.source_name, "runs": 0, "items_acquired": 0,
            "bytes_preserved": 0, "total_duration_seconds": 0.0,
        })
        acc["runs"] += 1
        acc["items_acquired"] += r.items_acquired
        acc["bytes_preserved"] += r.bytes_preserved
        acc["total_duration_seconds"] += r.duration_seconds or 0.0

    summaries = []
    for source_id, acc in by_source.items():
        avg = (
            acc["bytes_preserved"] / acc["total_duration_seconds"]
            if acc["total_duration_seconds"] > 0
            else None
        )
        summaries.append(SourceMeasurement(
            source_id=source_id, source_name=acc["source_name"],
            runs=acc["runs"], items_acquired=acc["items_acquired"],
            bytes_preserved=acc["bytes_preserved"],
            total_duration_seconds=acc["total_duration_seconds"],
            average_bytes_per_second=avg,
        ))
    return sorted(summaries, key=lambda s: s.source_name)


# ---------------------------------------------------------------------------
# What is actually on disk
# ---------------------------------------------------------------------------

def disk_footprint(path: Path) -> DiskFootprint:
    """Real bytes on disk under `path`, walked directly — never trusted from
    a database total, per the OCFL layer's own principle (PRES-009: the
    archive must be readable, and here measurable, without this project's
    code agreeing with itself).
    """
    file_count = 0
    total_bytes = 0
    if path.exists():
        for root, _dirs, files in os.walk(path):
            for name in files:
                file_count += 1
                total_bytes += (Path(root) / name).stat().st_size
    return DiskFootprint(path=str(path), file_count=file_count, on_disk_bytes=total_bytes)


def measure_ocfl_roots(archive_root: Path) -> list[DiskFootprint]:
    return [disk_footprint(archive_root / tier) for tier in TIERS]


def measure_quarantine(archive_root: Path) -> DiskFootprint:
    return disk_footprint(archive_root / "quarantine")


# ---------------------------------------------------------------------------
# Assembling the report
# ---------------------------------------------------------------------------

def build_report(
    conn, archive_root: Path, source_id: str | None = None,
    extrapolate_sources: int | None = None,
) -> Report:
    runs = measure_runs(conn, source_id)
    by_source = summarize_by_source(runs)
    total_preserved = sum(r.bytes_preserved for r in runs)

    ocfl = measure_ocfl_roots(archive_root)
    quarantine = measure_quarantine(archive_root)

    on_disk_total = sum(f.on_disk_bytes for f in ocfl) + quarantine.on_disk_bytes
    ratio = (on_disk_total / total_preserved) if total_preserved > 0 else None

    report = Report(
        by_run=runs, by_source=by_source, total_bytes_preserved=total_preserved,
        ocfl_footprint=ocfl, quarantine_footprint=quarantine,
        duplication_ratio=ratio,
    )

    if extrapolate_sources is not None and by_source:
        average_per_source = total_preserved / len(by_source)
        report.extrapolated_sources = extrapolate_sources
        report.extrapolated_bytes = average_per_source * extrapolate_sources

    return report


def render_text(report: Report) -> str:
    lines = ["Storage and bandwidth measurement (WP 3.4 A7)", ""]
    if not report.by_source:
        lines.append(
            "No completed collector_run rows found — nothing to measure yet. "
            "This is expected against a database that has not run a real "
            "collection (see collector/README.md)."
        )
    for s in report.by_source:
        throughput = (
            f"{s.average_bytes_per_second:,.0f} B/s"
            if s.average_bytes_per_second is not None else "unknown (no timed runs)"
        )
        lines.append(
            f"  {s.source_name}: {s.runs} run(s), {s.items_acquired} item(s), "
            f"{s.bytes_preserved:,} bytes preserved, {throughput}"
        )
    lines.append("")
    lines.append(f"Total bytes preserved (collector_run.bytes_preserved sum): "
                 f"{report.total_bytes_preserved:,}")
    for f in report.ocfl_footprint:
        lines.append(f"  On-disk ({f.path}): {f.on_disk_bytes:,} bytes, {f.file_count} files")
    if report.quarantine_footprint:
        q = report.quarantine_footprint
        lines.append(f"  On-disk ({q.path}): {q.on_disk_bytes:,} bytes, {q.file_count} files "
                     f"[undischarged quarantine copies — collector/README's known gap]")
    if report.duplication_ratio is not None:
        lines.append(
            f"  Duplication ratio (on-disk / preserved): {report.duplication_ratio:.2f}x"
        )
    if report.extrapolated_bytes is not None:
        lines.append("")
        lines.append(
            f"PROJECTION, not a measurement: {report.extrapolated_bytes:,.0f} bytes "
            f"if {report.extrapolated_sources} sources average what the "
            f"{len(report.by_source)} measured source(s) do. Nothing supports "
            f"assuming the unregistered candidates resemble these two in size."
        )
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archive-root", required=True, type=Path,
                        help="Directory containing the tier storage roots "
                             "(permanent/, medium-term/) and quarantine/")
    parser.add_argument("--source-id", default=None,
                        help="Limit collector_run measurement to one source")
    parser.add_argument("--extrapolate", type=int, default=None, metavar="N",
                        help="Also project the measured average per source "
                             "onto N sources (labelled as a projection)")
    parser.add_argument("--json", action="store_true",
                        help="Emit the report as JSON instead of text")
    args = parser.parse_args(argv)

    import psycopg  # local import: only needed when actually run

    with psycopg.connect(autocommit=True) as conn:
        report = build_report(conn, args.archive_root, args.source_id, args.extrapolate)

    if args.json:
        print(json.dumps(report.to_dict(), indent=2))
    else:
        print(render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
