#!/usr/bin/env python3
"""ARK syntax: names, check characters, normalisation, qualifiers.

Implements SPEC-0007 §2 under DR-0087. Deliberately knows nothing about the
database: an ARK is a string with rules, and those rules must be re-derivable
from the specification alone by someone who no longer has this code
(PRES-009).

Three things happen here and nowhere else:

  * **Names are random, not sequential.** A sequence leaks minting order and
    running counts, and record §15 forbids an identifier that encodes
    anything about its object. Randomness from `secrets`, not `random`.

  * **A check character travels with every name.** Identifiers will be
    transcribed from print, from court filings, and through translation.
    The check character turns a silent misreading into a loud one.

  * **Comparison is normalised.** Hyphens are insignificant in ARKs and may
    be inserted anywhere for readability, so `ark:/99999/t1bc-df23k` and
    `ark:/99999/t1bcdf23k` are the same identifier and must never be two
    rows in the register.
"""

from __future__ import annotations

import re
import secrets

# The betanumeric alphabet: digits plus consonants, no vowels and no `l`.
# No name spells a word, and the characters most often confused in
# handwriting and OCR are simply absent.
BETANUMERIC = "0123456789bcdfghjkmnpqrstvwxz"

# The check character is computed over this ordering, which is the same set.
# Kept as its own name because the two roles are conceptually distinct: one
# is the alphabet names are drawn from, the other the mapping ordinals are
# read against.
XDIGIT = BETANUMERIC

NAME_LENGTH = 8          # before the check character
NAAN_LENGTH = 5

_ARK = re.compile(
    r"^ark:/?/?(?P<naan>[0-9a-z]{%d})/(?P<name>[0-9a-z]+)$" % NAAN_LENGTH
)
_QUALIFIER = re.compile(r"^(?P<base>.*?)(?P<qualifier>\.v\d+)?$")


class ArkError(ValueError):
    """A malformed ARK, or one that fails its check character."""


def check_character(naan: str, name: str) -> str:
    """The NOID check character for `naan/name`.

    Each character's ordinal in XDIGIT is multiplied by its one-based
    position; characters outside the alphabet — `/` is the only one that
    occurs — count as zero; the sum modulo 29 indexes XDIGIT.

    The string covered runs from the first character of the NAAN to the last
    character of the name, inclusive of the separating `/`, which is what the
    ARK draft means by computing "back to the beginning of the NAAN".
    """
    covered = f"{naan}/{name}"
    total = sum(
        (XDIGIT.index(ch) if ch in XDIGIT else 0) * position
        for position, ch in enumerate(covered, start=1)
    )
    return XDIGIT[total % len(XDIGIT)]


def mint_name(naan: str, shoulder: str, *, length: int = NAME_LENGTH) -> str:
    """A fresh opaque name with its check character appended.

    Collision is a caller's concern: the register's primary key is the
    authority on uniqueness, and a retry there is cheaper than a reservation
    protocol here.
    """
    body = shoulder + "".join(secrets.choice(BETANUMERIC) for _ in range(length))
    return body + check_character(naan, body)


def format_ark(naan: str, name: str) -> str:
    return f"ark:/{naan}/{name}"


def normalise(ark: str) -> str:
    """The comparison form (SPEC-0007 §2.4).

    Strips any hostname and query string, lower-cases the NAAN, removes
    hyphens wherever they appear, collapses repeated slashes and periods,
    and drops terminal structural characters. The result is what the
    register stores and what every lookup is keyed by.
    """
    text = ark.strip()
    text = text.split("?", 1)[0].split("#", 1)[0]

    # A hostname may precede the label; the label is where identity starts.
    marker = text.lower().find("ark:")
    if marker == -1:
        raise ArkError(f"not an ARK: {ark!r} (no 'ark:' label)")
    text = text[marker:]

    text = text.replace("-", "")
    text = re.sub(r"/{2,}", "/", text.replace("ark://", "ark:/"))
    text = re.sub(r"\.{2,}", ".", text)
    text = text.rstrip("/.")

    label, _, rest = text.partition(":")
    naan, _, name = rest.lstrip("/").partition("/")
    if not name:
        raise ArkError(f"not an ARK: {ark!r} (no name after the NAAN)")
    return f"{label.lower()}:/{naan.lower()}/{name}"


def split_qualifier(ark: str) -> tuple[str, int | None]:
    """Separate a normalised ARK from its `.vN` state qualifier (DR-0090)."""
    match = _QUALIFIER.match(ark)
    base, qualifier = match.group("base"), match.group("qualifier")
    return base, int(qualifier[2:]) if qualifier else None


def parse(ark: str, *, verify: bool = True) -> tuple[str, str, int | None]:
    """(naan, name, version) for an ARK in any of its forms.

    `verify=False` skips the check character, for the one legitimate case:
    reading back an identifier the register already holds, where the stored
    value is the authority and a rejection would hide data rather than
    protect it.
    """
    base, version = split_qualifier(normalise(ark))
    match = _ARK.match(base)
    if not match:
        raise ArkError(f"malformed ARK: {ark!r}")
    naan, name = match.group("naan"), match.group("name")
    if verify and check_character(naan, name[:-1]) != name[-1]:
        raise ArkError(
            f"check character fails for {ark!r} — the identifier was "
            "mistyped or truncated, not merely unknown"
        )
    return naan, name, version


def is_valid(ark: str) -> bool:
    try:
        parse(ark)
    except ArkError:
        return False
    return True
