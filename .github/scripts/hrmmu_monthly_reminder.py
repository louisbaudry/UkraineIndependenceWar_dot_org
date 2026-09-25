#!/usr/bin/env python3
"""Write the monthly reminder for `un-hrmmu-protection-of-civilians` (DR-0110).

Prints a Markdown comment body to stdout, for the scheduled workflow
`.github/workflows/hrmmu-monthly-reminder.yml` to post on issue #82.

DR-0110 Decision 3 authorises one run per month only after a person has
read that month's landing page, put its links into `run_locators` and
committed the change. This script prepares that step and nothing more: it
reads the UN mission's listing page, finds the newest edition, compares it
with the candidate file, and lists the links it found with their status,
size and SHA-256 for the person to check. It edits no file, registers
nothing and collects nothing.

The reminder is the point, so it must go out whatever happens: any failure
to reach the site or read the page is written into the comment, never
raised (the §28/PRES-007 habit of recording failures as outcomes). Standard
library only, so it runs on a bare GitHub runner.
"""

from __future__ import annotations

import datetime
import hashlib
import html
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

LISTING = "https://ukraine.ohchr.org/en/reports/protection-of-civilians"
BASE = "https://ukraine.ohchr.org"
CANDIDATE = Path(__file__).resolve().parents[2] / "sources" / "candidates" / "civilian-harm.yaml"
USER_AGENT = ("UIW-reminder/0.1 "
              "(+https://github.com/louisbaudry/UkraineIndependenceWar_dot_org)")
MENTION = "@louisbaudry"


def fetch(url: str, timeout: int = 90) -> tuple[int | None, bytes, str]:
    """Return (status, body, error). Never raises."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, response.read(), ""
    except urllib.error.HTTPError as e:
        return e.code, b"", f"HTTP {e.code}"
    except Exception as e:  # network, TLS, timeout: all go in the comment
        return None, b"", f"{type(e).__name__}: {e}"


def newest_edition(listing_html: str) -> str | None:
    """The listing is newest first; the first edition link is the newest."""
    match = re.search(
        r'href="(/en/Protection-of-Civilians-in-Armed-Conflict-[^"]+)"',
        listing_html)
    return BASE + match.group(1) if match else None


def pdf_links(page_html: str) -> list[str]:
    links = re.findall(r'href="([^"]+\.pdf)"', page_html, flags=re.IGNORECASE)
    seen: list[str] = []
    for link in links:
        link = html.unescape(link)
        if link.startswith("/"):
            link = BASE + link
        if link not in seen:
            seen.append(link)
    return seen


def pick(links: list[str], *tags: str) -> str | None:
    """The file names are irregular (`…(August)_ENG.pdf`, `…_August_UKR.pdf`),
    so match the language tag anywhere in the name, case-insensitively."""
    for link in links:
        name = link.rsplit("/", 1)[-1].upper()
        if any(tag in name for tag in tags):
            return link
    return None


def describe(url: str) -> str:
    status, body, error = fetch(url)
    if status == 200 and body:
        digest = hashlib.sha256(body).hexdigest()
        return f"| `{url}` | 200 | {len(body):,} | `{digest}` |"
    return f"| `{url}` | {status or '—'} | — | {error or 'empty body'} |"


def main() -> int:
    today = datetime.date.today().isoformat()
    out: list[str] = [
        f"{MENTION} monthly reminder for `un-hrmmu-protection-of-civilians` "
        f"(DR-0110), {today}.",
        "",
    ]
    try:
        current = CANDIDATE.read_text(encoding="utf-8")
    except OSError as e:
        current = ""
        out.append(f"⚠️ Could not read `{CANDIDATE.name}`: {e}")

    status, body, error = fetch(LISTING)
    edition = newest_edition(body.decode("utf-8", "replace")) if body else None
    if not edition:
        out += [
            f"⚠️ Could not find the newest edition on {LISTING} "
            f"(status {status or '—'}{', ' + error if error else ''}).",
            "",
            "Open that page yourself and follow the steps in this issue.",
        ]
        print("\n".join(out))
        return 0

    month = edition.rsplit("Armed-Conflict-", 1)[-1].replace("-", " ")
    if edition in current:
        out += [
            f"**No new edition yet.** The newest on the UN page is "
            f"**{month}**, and it is already in `run_locators`.",
            "",
            "Nothing to do this month unless it appears in the next few "
            "days. Check " + LISTING + " again later in the month.",
        ]
        print("\n".join(out))
        return 0

    page_status, page, page_error = fetch(edition)
    links = pdf_links(page.decode("utf-8", "replace")) if page else []
    english = pick(links, "_ENG", "ENG.PDF")
    ukrainian = pick(links, "_UKR", "UKR.PDF")

    out += [
        f"**New edition: {month}.** {edition}",
        "",
        "| URL | Status | Bytes | SHA-256 |",
        "| --- | --- | --- | --- |",
        describe(edition),
    ]
    for link in (english, ukrainian):
        if link:
            out.append(describe(link))
    out.append("")
    if not english:
        out.append("⚠️ No English PDF link found on the page.")
    if not ukrainian:
        out.append("⚠️ The Ukrainian PDF isn't linked yet; it usually "
                   "follows about a week after the English one. You can "
                   "run with the English PDF now and add the Ukrainian "
                   "later, or wait.")
    if page_status != 200:
        out.append(f"⚠️ Landing page returned {page_status or '—'} "
                   f"{page_error}.")

    locators = [edition] + [x for x in (english, ukrainian) if x]
    out += [
        "",
        "**Paste into `sources/candidates/civilian-harm.yaml`**, replacing "
        "the current values (check each link against the page first):",
        "",
        "```yaml",
        f"    locator_verified: {today}",
        "    run_locators:",
        *[f"      - {x}" for x in locators],
        "```",
        "",
        "Then: `python3 sources/register.py --check`, commit, merge; on "
        "the archive server `git pull` and run `collector/run.py --source "
        "un-hrmmu-protection-of-civilians` with `--dry-run` first.",
        "",
        "_Prepared by the scheduled workflow; it changes no file, "
        "registers nothing and collects nothing (DR-0110 Decision 3)._",
    ]
    print("\n".join(out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
