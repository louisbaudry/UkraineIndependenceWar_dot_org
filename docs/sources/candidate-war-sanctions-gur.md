# Candidate source — War & Sanctions (GUR), "Components" section

**Status:** Candidate — not registered, not collected, not evaluated against live content.
**Logged:** 2026-09-01, at the founder's direction, following a link the founder received
(source of the link: a third party, unspecified).

## What this note is based on

This session had **no network access** to `war-sanctions.gur.gov.ua` — the domain is
blocked by this environment's egress proxy — so nothing below about the page's actual
content, structure, or fields is first-hand observation. It is background knowledge about
the publicly known War & Sanctions project, stated as such, not verified against the live
page. **This must be re-checked from the live site before any of it is relied on.**

Publicly, War & Sanctions (war-sanctions.gur.gov.ua) is a database maintained by
Ukraine's Main Directorate of Intelligence (GUR, Ministry of Defence of Ukraine),
tracking entities and individuals linked to Russia's war effort, and — in the
"Components" section specifically — foreign-made electronic components (chips,
processors, connectors) recovered from destroyed Russian weapons systems (missiles,
drones, guided munitions), typically with manufacturer, country of origin, and the
weapon system(s) the part was found in.

## Why it could matter to this project

If the above is accurate, this is squarely inside the project's stated scope
(README: "sanctions-evasion, export-control ... research infrastructure"):

- It is a component-level supply-chain evidence source for sanctions-evasion analysis
  — which Western-origin parts are still reaching Russian weapons, through what
  apparent diversion routes.
- It would corroborate (or could be corroborated by) independent trackers already
  known to do similar component-in-wreckage analysis — e.g. KSE Institute, RUSI,
  Conflict Armament Research — which matters for [DR-0028](../decision-records/DR-0028-corroboration-and-dependence.md)-style
  corroboration/dependence analysis.
- It is a primary-ish output of a party to the conflict, not a neutral third party —
  see caveats below.

## Caveats that any future registration must carry, not silently drop

- **GUR is a directorate of Ukraine's Ministry of Defence** — an intelligence service
  of a belligerent state, not a neutral investigative body. Per this project's stated
  commitment to "rigorous evidentiary standards ... careful distinctions among source
  claims, evidence, inference ... and project conclusions," anything sourced from it
  needs the `official Ukrainian` / `government` source type (SPEC-0003 §3 identity
  field), an explicit rights-assessment entry (likely `unknown` pending review per
  DR-0029), and should never be treated as self-corroborating with other Ukrainian
  government output.
- Component identification (a part number traced to a manufacturer and country) is a
  factual claim distinct from any attribution or narrative GUR attaches to it; Gate 2
  editorial acceptance would need to separate "this part number was found in this
  wreckage" from any framing GUR adds.
- Terms of use, licensing, and update cadence for the site are unknown — need to be
  read directly from the live page, not assumed.

## What would need to happen before this becomes a real registry entry

1. Fetch and review the live page from an environment with network access to
   `war-sanctions.gur.gov.ua` (this session's environment blocks the domain).
2. Check for an existing crosswalk against known independent trackers (KSE Institute,
   RUSI, CAR) to assess declared-dependence relationships up front (DR-0028).
3. Decide — as a founder decision, not an inline judgment call — where source registry
   *instances* actually live (this repository has no such store yet; see
   [docs/sources/README.md](README.md)).
4. Only then does DR-0071(a) allow the pipeline to collect from it at all.

## Recommendation

Worth exploring further — it's a plausible, on-scope evidentiary source — but treat this
note as "flagged for follow-up," not as a source now in scope for collection.
