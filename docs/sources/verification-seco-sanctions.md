# Verification record — SECO sanctions list (Switzerland)

**Status:** Verification record for one candidate registration. Nothing
here is registered, nothing is collected into the project's archive, and
nothing is enacted by this document. Registering this candidate, like the
four before it, is the founder's act (CLAUDE.md standing ruling).
**Verified:** 2026-09-13, ~16:00–16:10 UTC, from this session's container.
**Candidate:** `seco-sanctions` in
[`sources/candidates/sanctions-authorities.yaml`](../../sources/candidates/sanctions-authorities.yaml).

This candidate had been tried once before
([2026-09-12](verification-bis-dpl-ofsi-consolidated.md) §5) and not found
— six blind guesses at plausible URL patterns and a site-search endpoint
all returned 404/500 or no usable links. This record replaces that
attempt: the locator was found by following the site's own navigation,
not by guessing another pattern.

## 1. What was done, in order

1. Fetched `https://www.seco.admin.ch/seco/en/home.html` in full (224 KB,
   not the truncated/redirect-only response earlier attempts got) and
   searched its actual rendered links for anything naming sanctions,
   rather than guessing a page slug.
2. Followed the one link that matched (`/en/sanctions-en`) to the site's
   real sanctions section, then followed its own link to
   `/en/searching-for-subjects-sanctions` — the page titled for exactly
   this purpose.
3. That page links the real download directly: a "Gesamtliste" (overall
   list) XML file, served from a *different host*
   (`sesam.search.admin.ch`, SECO's sanctions-search application) than
   the one every earlier guess had tried (`seco.admin.ch` or
   `www.sesam.search.admin.ch/.../pages/search.xhtml`).
4. Fetched the file twice, 2026-09-13, with SHA-256 computed both times.
5. Fetched the `de`, `fr`, and `it` language variants once each to check
   whether `lang=` changes the file's content.
6. **Rehearsal.** A throwaway PostgreSQL database was built from
   `schema/0*.sql`. The source was inserted directly (matching the
   BIS/OFSI rehearsal's approach, not through `sources/register.py`,
   since the candidate file did not yet carry `run_locators` at the point
   this rehearsal ran). The real `Collector`
   (`collector/pipeline.py`, two-agent split) was run with the real
   `HttpFetcher` against the live URL, into a throwaway OCFL root.
   Digest, byte count and documentary-assertion count were read back.
   Database and storage were then destroyed.

## 2. The file

| | |
| --- | --- |
| Locator | `https://www.sesam.search.admin.ch/sesam-search-web/pages/downloadXmlGesamtliste.xhtml?lang=en&action=downloadXmlGesamtlisteAction` |
| Size | 42 300 406 bytes |
| SHA-256 | `02122255f58baed2028cf513bbeffb6330fff781ccf4af9ffe9f336d10e0e7b1` |
| Content-Type | `text/xml` |
| Content-Disposition | `attachment; filename="consolidated-list_2026-09-04.xml"` |
| Root element | `<swiss-sanctions-list list-type="whole-list" date="2026-09-04">` |
| `<target>` elements | 17 312 |

Fetched twice, digest identical both times. The `de`, `fr`, and `it`
`lang=` variants were also fetched once each: all three produced the
identical 42 300 406-byte file with the identical SHA-256 — the parameter
does not change the file's content (each `<program-name>`/`<program-key>`
element already carries all four languages inline via its own `lang`
attribute), so one locator is registered rather than four.

Acquired end to end by the real collector in the rehearsal: 1 discovered,
1 acquired, 0 failed, 42 300 406 bytes — the stored digest matched the
independently-computed one exactly. Zero documentary assertions (DR-0066,
Principle 5), same as every collection to date.

## 3. What changed from the first attempt

The earlier session's six guesses (`/dam/seco/de/...sanktionsliste_de.xlsx`,
`/content/seco/en/home/.../sanktionen-embargos.html`,
`/sesam-search-web/pages/downloadXmlSanctionslist.xhtml`,
`/sanktionsmassnahmen`, a site-search query) all targeted `seco.admin.ch`
itself or guessed at the download-application's endpoint name. The real
file lives on `sesam.search.admin.ch` (a separate SECO application, not a
subpath of the main site) under an endpoint named for the German
"Gesamtliste" ("overall list"), not "sanctionslist" or
"sanktionsliste" — no pattern in the six guesses would have found it. The
difference this time was reading the actual page content returned by a
full fetch and following its real links, rather than constructing a URL
from the shape of other agencies' endpoints.

## What has not been verified

The rights position: `seco-sanctions` remains `may-preserve` with its
basis marked `UNVERIFIED` in the candidate file, unchanged by this record
— a locator being real says nothing about redistribution rights, which is
a POL-0001 §10 question. The declared dependence
(`seco-sanctions --common-evidentiary-origin--> eu-consolidated-list`)
was not re-examined; nothing in this file's content was read closely
enough to confirm or revise it.

---

**AI provenance (§80).** Drafted by Claude (`claude-sonnet-5`) on
2026-09-13, from fetches and one rehearsal performed in this session.
Every figure above comes from a response received here and is
reproducible from the URLs given. This is a verification record, not a
Decision Record; it enacts nothing and authorises no collection.
