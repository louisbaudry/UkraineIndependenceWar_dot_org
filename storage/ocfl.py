#!/usr/bin/env python3
"""OCFL 1.1 storage for the archive's preserved bytes.

Implements DR-0073 (OCFL as the at-rest layout, objects as AIP containers),
DR-0074 (an OCFL object is a holding; derivatives are later versions),
DR-0075 (SHA-512 content addressing with SHA-256 in the fixity block) and
DR-0076 (tier-separated roots, hashed n-tuple layout).

Direct implementation rather than a library. WP 3.3 §8 Q1 left this open to
be decided at build time; the evidence at build time was:

  * ocfl-py, the reference-quality implementation, does not install — its
    `pairtree` dependency is Python 2-era and fails to build.
  * ocflcore 0.1.0 installs but has **no fixity-block support**, which
    DR-0075 requires, and its 0.x API does not match its documentation.

The counter-argument WP 3.3 recorded for using a library was that libraries
are validated. That assurance is not available, so it is replaced here by
`validate_object()`, which checks written objects against the OCFL 1.1
requirements this project depends on. Independent third-party conformance
validation remains an open item — see storage/README.md.

The archive must be readable without this code (PRES-009): what matters is
that the bytes on disk conform, not that they were written by this module.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

OCFL_VERSION = "1.1"
SPEC_URI = f"https://ocfl.io/{OCFL_VERSION}/spec/#inventory"
CONTENT_DIR = "content"

# DR-0075: SHA-512 addresses content; SHA-256 rides in the fixity block,
# satisfying DR-0005 and preserving continuity with every hash recorded so
# far. Two algorithms disagreeing on the same content is itself a signal.
CONTENT_ALGORITHM = "sha512"
FIXITY_ALGORITHM = "sha256"

# DR-0076: retention tiers get separate roots so that disposition at a
# medium-term review date can never touch the permanent archive.
TIERS = ("permanent", "medium-term")


class OcflError(Exception):
    """Raised for any violation of the layout's guarantees."""


def _digest(path: Path, algorithm: str) -> str:
    h = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _digest_bytes(data: bytes, algorithm: str) -> str:
    return hashlib.new(algorithm, data).hexdigest()


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def hashed_n_tuple(object_id: str, tuple_size: int = 3, depth: int = 3) -> str:
    """Map an object id to a storage path (DR-0076).

    The hashed n-tuple layout avoids directory-size limits and keeps
    identifiers — which may echo source URLs — out of directory names.
    """
    digest = hashlib.sha256(object_id.encode("utf-8")).hexdigest()
    segments = [digest[i * tuple_size:(i + 1) * tuple_size] for i in range(depth)]
    return "/".join(segments + [digest])


@dataclass(frozen=True)
class ContentFile:
    """A file to place in a version: its bytes' source and its logical path."""

    source: Path
    logical_path: str


class StorageRoot:
    """One OCFL storage root, holding objects for a single retention tier."""

    def __init__(self, path: Path | str, tier: str):
        if tier not in TIERS:
            raise OcflError(
                f"unknown retention tier {tier!r}; DR-0076 defines roots for "
                f"{TIERS} only (metadata-only and discard hold no bytes)"
            )
        self.path = Path(path)
        self.tier = tier

    # -- root ---------------------------------------------------------------

    @property
    def namaste(self) -> Path:
        return self.path / f"0=ocfl_{OCFL_VERSION}"

    def initialize(self) -> None:
        self.path.mkdir(parents=True, exist_ok=True)
        if any(self.path.iterdir()):
            raise OcflError(f"storage root {self.path} is not empty")
        self.namaste.write_text(f"ocfl_{OCFL_VERSION}\n")
        (self.path / "ocfl_layout.json").write_text(
            json.dumps(
                {
                    "extension": "0004-hashed-n-tuple-storage-layout",
                    "description": (
                        "Hashed n-tuple storage layout, SHA-256 of the object "
                        "id, tuple size 3, depth 3 (DR-0076)."
                    ),
                },
                indent=2,
            )
            + "\n"
        )
        # A note for a future archivist reading the bytes without this code.
        (self.path / "README.txt").write_text(
            f"OCFL {OCFL_VERSION} storage root — retention tier: {self.tier}.\n"
            "Each object is one archival holding (DR-0074). Content is addressed\n"
            f"by {CONTENT_ALGORITHM}; each inventory also carries a "
            f"{FIXITY_ALGORITHM} fixity block (DR-0075).\n"
            "The layout is specified at https://ocfl.io/ and is readable without\n"
            "the software that wrote it.\n"
        )

    def object_path(self, object_id: str) -> Path:
        return self.path / hashed_n_tuple(object_id)

    def has_object(self, object_id: str) -> bool:
        return (self.object_path(object_id) / "inventory.json").exists()

    def object_ids(self) -> list[str]:
        found = []
        for inventory in sorted(self.path.rglob("inventory.json")):
            if inventory.parent.name.startswith("v"):
                continue  # per-version copy, not the object root
            found.append(json.loads(inventory.read_text())["id"])
        return sorted(found)

    # -- writing ------------------------------------------------------------

    def create_object(
        self, object_id: str, files: list[ContentFile], message: str, user: str
    ) -> dict:
        """Create an object at v1. Its content is the acquired original."""
        if self.has_object(object_id):
            raise OcflError(f"object {object_id!r} already exists")
        return self._write_version(object_id, files, message, user, first=True)

    def add_version(
        self, object_id: str, files: list[ContentFile], message: str, user: str
    ) -> dict:
        """Add a version — typically a derivative representation (DR-0074).

        Forward-delta: content already present under an earlier version is
        referenced by digest, never copied. The original in v1 is never
        touched, which is how OCFL implements PRES-001's immutability rather
        than merely coexisting with it.
        """
        if not self.has_object(object_id):
            raise OcflError(f"object {object_id!r} does not exist")
        return self._write_version(object_id, files, message, user, first=False)

    def _write_version(
        self,
        object_id: str,
        files: list[ContentFile],
        message: str,
        user: str,
        first: bool,
    ) -> dict:
        root = self.object_path(object_id)
        if first:
            root.mkdir(parents=True)
            (root / f"0=ocfl_object_{OCFL_VERSION}").write_text(
                f"ocfl_object_{OCFL_VERSION}\n"
            )
            inventory = {
                "id": object_id,
                "type": f"https://ocfl.io/{OCFL_VERSION}/spec/#inventory",
                "digestAlgorithm": CONTENT_ALGORITHM,
                "head": "v1",
                "contentDirectory": CONTENT_DIR,
                "manifest": {},
                "versions": {},
                "fixity": {FIXITY_ALGORITHM: {}},
            }
            version_name = "v1"
        else:
            inventory = json.loads((root / "inventory.json").read_text())
            version_name = f"v{int(inventory['head'][1:]) + 1}"

        content_root = root / version_name / CONTENT_DIR
        state: dict[str, list[str]] = {}

        for item in files:
            if not item.source.is_file():
                raise OcflError(f"missing content file: {item.source}")
            content_digest = _digest(item.source, CONTENT_ALGORITHM)
            fixity_digest = _digest(item.source, FIXITY_ALGORITHM)

            if content_digest not in inventory["manifest"]:
                # New content: place it under this version and record it.
                target = content_root / item.logical_path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item.source, target)
                content_path = f"{version_name}/{CONTENT_DIR}/{item.logical_path}"
                inventory["manifest"][content_digest] = [content_path]
                inventory["fixity"][FIXITY_ALGORITHM].setdefault(
                    fixity_digest, []
                ).append(content_path)
            # else: forward-delta — the bytes already exist under an earlier
            # version and are referenced, not duplicated.

            state.setdefault(content_digest, []).append(item.logical_path)

        # A version's state is its complete logical contents, so carry
        # forward everything the previous version held.
        if not first:
            previous = inventory["versions"][inventory["head"]]["state"]
            for digest, paths in previous.items():
                for path in paths:
                    if path not in state.get(digest, []):
                        state.setdefault(digest, []).append(path)

        inventory["versions"][version_name] = {
            "created": _utc_now(),
            "message": message,
            "user": {"name": user},
            "state": {d: sorted(p) for d, p in sorted(state.items())},
        }
        inventory["head"] = version_name

        self._write_inventory(root, inventory)
        self._write_inventory(root / version_name, inventory)
        return inventory

    @staticmethod
    def _write_inventory(directory: Path, inventory: dict) -> None:
        directory.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(inventory, indent=2, sort_keys=True) + "\n"
        (directory / "inventory.json").write_text(serialized)
        # The sidecar's algorithm must match digestAlgorithm.
        sidecar = _digest_bytes(serialized.encode("utf-8"), CONTENT_ALGORITHM)
        (directory / f"inventory.json.{CONTENT_ALGORITHM}").write_text(
            f"{sidecar}  inventory.json\n"
        )

    # -- reading and checking ----------------------------------------------

    def read_inventory(self, object_id: str) -> dict:
        return json.loads((self.object_path(object_id) / "inventory.json").read_text())

    def fixity_check(self, object_id: str) -> list[str]:
        """Verify stored content against both recorded digests (DR-0005).

        Returns a list of problems; empty means intact. Failures are returned
        rather than raised because a fixity failure is a recorded preservation
        event, never a silent re-copy (DR-0060).
        """
        root = self.object_path(object_id)
        inventory = self.read_inventory(object_id)
        problems: list[str] = []

        for digest, paths in inventory["manifest"].items():
            for rel in paths:
                path = root / rel
                if not path.is_file():
                    problems.append(f"missing content: {rel}")
                    continue
                actual = _digest(path, CONTENT_ALGORITHM)
                if actual != digest:
                    problems.append(
                        f"{CONTENT_ALGORITHM} mismatch for {rel}: "
                        f"expected {digest[:16]}…, got {actual[:16]}…"
                    )

        for digest, paths in inventory.get("fixity", {}).get(FIXITY_ALGORITHM, {}).items():
            for rel in paths:
                path = root / rel
                if path.is_file() and _digest(path, FIXITY_ALGORITHM) != digest:
                    problems.append(f"{FIXITY_ALGORITHM} mismatch for {rel}")

        return problems


def validate_object(root: StorageRoot, object_id: str) -> list[str]:
    """Check an object against the OCFL 1.1 requirements we depend on.

    This substitutes for the third-party conformance validation that WP 3.3
    expected a library to provide. It is deliberately a check of *our*
    dependencies, not a complete OCFL validator; see storage/README.md for
    what that means and what remains open.
    """
    problems: list[str] = []
    path = root.object_path(object_id)

    if not (path / f"0=ocfl_object_{OCFL_VERSION}").is_file():
        problems.append("missing object namaste declaration")

    inventory_file = path / "inventory.json"
    if not inventory_file.is_file():
        return problems + ["missing inventory.json"]

    raw = inventory_file.read_text()
    inventory = json.loads(raw)

    for field in ("id", "type", "digestAlgorithm", "head", "manifest", "versions"):
        if field not in inventory:
            problems.append(f"inventory missing required field {field!r}")
    if problems:
        return problems

    if inventory["digestAlgorithm"] != CONTENT_ALGORITHM:
        problems.append(
            f"digestAlgorithm is {inventory['digestAlgorithm']!r}, "
            f"expected {CONTENT_ALGORITHM!r} (DR-0075)"
        )
    if FIXITY_ALGORITHM not in inventory.get("fixity", {}):
        problems.append(f"missing {FIXITY_ALGORITHM} fixity block (DR-0075)")

    # Sidecar must exist and match.
    sidecar = path / f"inventory.json.{CONTENT_ALGORITHM}"
    if not sidecar.is_file():
        problems.append("missing inventory sidecar")
    else:
        expected = _digest_bytes(raw.encode("utf-8"), CONTENT_ALGORITHM)
        if sidecar.read_text().split()[0] != expected:
            problems.append("inventory sidecar digest does not match inventory")

    # Versions must be a complete v1..vN sequence with head last.
    names = sorted(inventory["versions"], key=lambda v: int(v[1:]))
    expected_names = [f"v{i}" for i in range(1, len(names) + 1)]
    if names != expected_names:
        problems.append(f"version sequence is {names}, expected {expected_names}")
    elif inventory["head"] != names[-1]:
        problems.append(f"head is {inventory['head']!r}, expected {names[-1]!r}")

    # Every digest a version state references must be in the manifest.
    for version_name, version in inventory["versions"].items():
        for digest in version["state"]:
            if digest not in inventory["manifest"]:
                problems.append(
                    f"{version_name} references digest not in manifest: {digest[:16]}…"
                )
        if not re.match(r"^\d{4}-\d{2}-\d{2}T", version.get("created", "")):
            problems.append(f"{version_name} has no valid created timestamp")

    # Each version directory must carry an inventory copy.
    for version_name in names:
        if not (path / version_name / "inventory.json").is_file():
            problems.append(f"{version_name} has no inventory copy")

    problems.extend(root.fixity_check(object_id))
    return problems
