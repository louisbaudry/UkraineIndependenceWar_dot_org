# Phase III / Study 5 — Identifier Design
## Working Paper 3.5

**Project:** Ukraine's Second War of Independence
**Status:** CANDIDATE — AI-drafted, awaiting founder review.
**Version:** 3.5
**Mandate:** Q-12 and record §15 — how citable research objects receive stable public identifiers and permanent resolvable URLs; whether annotations are independently citable, and through what resolver. DR-0022 left "identifier syntax and resolvers for citable project objects" as "a separate, later decision"; this is the study that decision requires.
**Constraints inherited:** record §15–16 (immutable internal IDs, stable public identifiers, permanent resolvable URLs, typed external mappings; "do not freeze a custom identifier syntax without researching established patterns first"; internal objects do not automatically need public identifiers), §77 (corrections leave a trace), §89 (releases carry a persistent identifier where mature), Principle 18 and PRES-009 (the archive is reconstructible without the website), ARCH-001 (no shared identity between pipeline and world registries), DATA-009 (every published identifier resolves forever, including merged, split and redacted objects), DATA-010, DR-0012 (identifiers attach via assignment events), DR-0017/0018 (Web Annotation targeting; targets are preserved captures, version-pinned), DR-0045, DR-0049 (DataCite DOIs for releases at maturity), DR-0055/0077 (append-only; governed redaction leaves a tombstone), DR-0062/0064 (entity statuses; merge and split leave permanent redirects, a split's redirect resolves to a disambiguation record), DR-0080 (structural changes need a DR), DR-0083 (the RDF namespace is provisional), SPEC-0006 §9A and DR-0086 (access tiers; most-restrictive wins).

### AI provenance (record §80)

Drafted 2026-09-08 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction, after the founder chose the study-first route
over drafting SPEC-0007 directly. External standards were checked against
their primary texts by web retrieval where reachable (§7 says which were
not). Candidate until approved.

---

## 1. What §15 actually asks for

Record §15 names four distinct things, and the project already has one of
them:

| §15 element | State today |
|---|---|
| Immutable internal IDs | **Done.** Every table uses a `uuid` primary key (SPEC-0001 §2.1; `schema/`). Minted with UUID version 4. |
| Typed external identifier mappings | **Done in principle.** `identifier-assignment` assertions with a registry identifier-type (DR-0012, DR-0045, DATA-010). |
| Stable public project identifiers | **Absent.** Nothing is minted for citation. The only published handle is `published_page.path`, a text column the schema comment calls "the identifier a citation points at". |
| Permanent resolvable URLs | **Absent.** No resolver exists; the RDF namespace is a provisional string in `registry.yaml` (DR-0083). |

Three enacted commitments already dictate the *behaviour* of whatever
scheme is chosen, without choosing it:

- **DATA-009:** the resolver returns a resource, a documented redirect, or a
  tombstone for every identifier ever published. No published identifier
  dead-ends.
- **DR-0064:** merges and splits leave permanent redirects; a split's
  redirect resolves to a disambiguation record; mappings ship in release
  change sets.
- **DR-0077 / DR-0055:** redaction leaves a tombstone recording fact, date,
  authority and grounds, never the content.

So the identifier design is not "pick a syntax". It is: pick a scheme whose
persistence semantics can carry *resource / redirect / disambiguation /
tombstone*, separate the identifier from the hostname so PRES-009 holds,
decide when an object earns a public identifier, and fix the namespace that
SPEC-0005 is waiting on.

## 2. Established patterns

Verified against primary texts on 2026-09-08 unless marked otherwise.

### 2.1 Persistent-identifier schemes

| Scheme | Governance and cost | Resolution | Opacity and persistence semantics |
|---|---|---|---|
| **ARK** (`ark:/NAAN/name[qualifiers]`) | Internet-Draft `draft-kunze-ark-43` (May 2026), no formal IETF endorsement; maintained by the ARK Alliance. Free to mint; a Name Assigning Authority Number (NAAN) is requested once from the maintenance agency. No metadata requirements. >650 organisations, ~15 billion ARKs. | Any host may serve as Name Mapping Authority; the hostname is "identity inert" (two ARKs differing only in host are the same identifier). `n2t.net` offers a resolver chain keyed on NAAN, and organisations may act as alternative or backup resolvers. | Names are to be semantically opaque; a check character is recommended. `?info` returns a metadata record **and a commitment statement** — persistence policy is part of the scheme. Qualifiers (`/` hierarchy, `.` variants) address components and versions. |
| **DOI** | ISO 26324; minted through a registration agency (DataCite for datasets) with membership fees and per-DOI charges. DR-0049 already places DOIs at release maturity. | Handle System via `doi.org`. | DataCite requires a **publicly available landing page** with citation metadata and machine-readable tags; "the underlying content does not need to be public but the metadata must be open"; withdrawn items get a tombstone page. (The DOI Handbook itself was unreachable in this environment; syntax details are not re-verified — §7.) |
| **Handle** (`prefix/local-name`) | RFC 3650 (Informational, 2003); the IESG recorded that IETF discussion "has not resulted in IETF consensus". A naming-authority prefix is obtained from the Global Handle Registry; running one means operating a local handle server. | Two-tier: Global Handle Registry, then local handle service. | No opacity rule; persistence is whatever the operator does. |
| **URN** (`urn:NID:NSS`) | RFC 8141 (Standards Track, 2017). Formal namespace identifiers need IANA expert review; informal ones are auto-assigned as `urn-N`. Free. | **None inherent.** "Resolution for URNs is more flexible and varied"; a separate resolution service is always required. | Namespace-defined. |
| **UUID v7** | RFC 9562 (Standards Track, May 2024), obsoletes RFC 4122. | n/a — a key, not a citation form. | Time-ordered (48-bit ms timestamp + randomness), giving B-tree locality that v4 lacks; "implementations SHOULD utilize UUIDv7 instead of UUIDv1 and UUIDv6 if possible". 36 characters, no check character. |

### 2.2 URL discipline

- **"Cool URIs don't change"** (W3C, Berners-Lee): leave out of a URI the
  author, status ("draft", "latest"), access level, file extension,
  software mechanism, subject classification and organisational structure;
  a creation date is the one thing that safely may stay. "Designing mostly
  means leaving information out."
- **Cool URIs for the Semantic Web** (W3C Interest Group Note, 2008):
  one URI must not name both a thing and a document about it. **Hash URIs**
  suit "small and stable sets of resources that evolve together" —
  ontologies and vocabularies. **Slash URIs with 303** suit large, evolving
  datasets, at the cost of a redirect per lookup. Content negotiation
  serves HTML or RDF from the same identifier.
- **Memento** (RFC 7089, Informational, 2013): `Accept-Datetime`
  negotiation over a resource's prior states (Original Resource, Memento,
  TimeGate, TimeMap; link relations `original`, `timegate`, `timemap`,
  `memento`). This is the standard answer to the record's own warning that
  "the same URL may later serve different content".

### 2.3 Practice the project already consumes

Wikidata (`Q42`), OpenSanctions and GLEIF identifiers are opaque or
near-opaque strings with a short type-agnostic prefix, resolved by their
issuer. They enter the project as external identifier assignments
(DR-0045, DATA-010) and are not models to copy, but they illustrate the
working norm: opaque, issuer-scoped, resolved by the issuer.

## 3. Analysis against the project's requirements

**3.1 The identifier must outlive the hostname.** PRES-009 and Principle 18
require the archive to be reconstructible without the website; DR-0058
requires the dump to be software-independent. A public identifier whose
identity *is* a URL on `ukraineindependencewar.org` fails both the day the
domain lapses or the project passes to a successor. ARK's identity-inert
hostname is the only scheme in §2.1 designed around this without a paid
central registry: the citation is `ark:/NAAN/name`; the URL is whichever
resolver currently serves it. DOIs and Handles achieve the same through a
central registry the project must pay for and cannot operate itself. URNs
achieve it but resolve nowhere. Plain project URLs do not achieve it at
all.

**3.2 The scheme must express four dispositions.** DATA-009 and DR-0064
need every identifier to resolve to one of: the object; a redirect (merge);
a disambiguation record (split); a tombstone (redaction). A fifth follows
from SPEC-0006 §9A and DR-0086: an object in a restricted tier must still
*resolve* — to a notice that it exists and is restricted, using the
`withheld` absence state of DR-0029 — rather than vanish, because a
dead-ending identifier is exactly what DATA-009 forbids. This rules out
DataCite DOIs as the primary scheme: its rule that "the metadata must be
open" cannot be met for restricted-tier objects (SEC-003/004), and DOIs are
in any case reserved by DR-0049 for public dataset releases. ARK's `?info`
commitment statement is the natural carrier for the disposition; every
other scheme needs the same register built alongside it anyway.

**3.3 Opacity is mandatory, not stylistic.** DR-0062 keeps fabricated and
disproved entities as referents; §54 covers invented personas; DR-0064
merges entities; access tiers change; names are assertions, not columns
(DR-0012). Any identifier carrying a name, a type, a tier, a status, a
date of the historical event, or a classification (all on the Cool-URIs
exclusion list) will eventually be wrong for its object and cannot be
changed. Names must therefore be opaque. A check character is worth its
one extra character: identifiers will be cited in print, court filings and
translations, where transcription errors are silent.

**3.4 Internal and public identity stay separate.** §15 says internal
objects do not automatically need public identifiers; ARCH-001 forbids a
shared identity between the two agent registries. The internal UUID is a
key, never a citation. A public identifier is a *fact about* an object —
"the project assigned this name on this date" — which is precisely what
DR-0012 models as an `identifier-assignment` assertion with the project as
asserter. Treating the project's own identifiers as assignment events means
the identifier register is ordinary provenance-bearing data, ships in dumps
and change sets (DR-0048, DR-0058), and reconstructs the resolver from the
archive alone (PRES-009).

**3.5 When an object earns a public identifier.** Two candidate rules:
(a) mint at creation for every object; (b) mint at first publication or
first citation, through Gate 3. Rule (a) produces millions of identifiers
the project has never committed to and fills the register with unpublished
pipeline internals, contradicting §15's "not automatically". Rule (b) ties
minting to the moment the project takes public responsibility for the
object — a publication decision (DR-0066 Gate 3) or an explicit editorial
act for objects cited in a publication without a page of their own
(assertions, quotations, holdings, annotations). Rule (b) is recommended.

**3.6 Annotations (the Q-12 question proper).** Evidential annotations are
already required to target preserved, version-pinned captures (DR-0018),
and the Web Annotation model gives every serialised annotation an IRI.
Nothing in the model distinguishes an annotation from any other citable
object except that Q-23 (whether it carries epistemic status) is still
open. Q-23 does not gate identity: an annotation is citable because it is
a thing the project asserted and someone may need to point at, whatever
epistemic status it later carries. Recommendation: annotations are citable
objects under the same scheme and the same minting rule as everything
else; there is no separate annotation resolver. Serving them over the Web
Annotation *Protocol* (LDP containers) is a later, product-level choice.

**3.7 Versions.** An identifier names the object, not a state of it
(Cool URIs; DR-0055's append-only store means the object's current state is
the head of a supersession chain). Two complementary mechanisms serve a
particular state: an ARK **qualifier** for an explicitly versioned thing
(page revision `N`, holding version `vN` in OCFL), and **Memento** datetime
negotiation on the resolver for "as the project held it at time T", which
`page_revision` and the bitemporal `asserted_at` column already make
answerable. The qualifier form is a decision; Memento is an
implementation item.

**3.8 The RDF namespace.** SPEC-0005 and DR-0083 wait on Q-12 for the
namespace URI. The Semantic-Web note's criterion is decisive: the registry
is a small, stable set that evolves together → **hash URIs**; entities,
holdings, assertions and pages are a large, evolving set → **slash URIs**
with 303 or direct content negotiation. Both should hang off ARKs so the
namespace survives re-hosting: the registry itself receives an ARK, and its
concept URIs are that ARK's resolver URL plus `#entry-id` (the fragment is
stripped before resolution, so the `?info` and content-negotiation
behaviour of the registry object is untouched). Changing the provisional
namespace is a structural change under DR-0080, but DR-0083 notes the cost
only bites once an external consumer exists; there is none yet. This is
the cheap moment.

**3.9 DOIs remain where DR-0049 put them.** A DataCite DOI for a public
dataset release is an *additional* identifier — an external identifier
assignment on the release object — whose landing page is the release's ARK
resolver page. Nothing here reopens DR-0049 or Q-31 (registration route).

## 4. Alternatives considered

| Option | Why not (or why) |
|---|---|
| **A. ARK under a project NAAN; project-run resolver; N2T registered as backup** | **Recommended.** Free; no central dependency; hostname-inert identity satisfies PRES-009; commitment statements match DATA-009's dispositions; opaque names with check characters; qualifiers for versions. Cost: one NAAN request, a resolver table and a small HTTP service, and the discipline of never exposing UUIDs. |
| B. Opaque project URLs with Cool-URIs discipline, no scheme | Identity bound to the domain; no third-party resolver chain; no commitment-statement convention; every successor must re-derive the rules. Strictly worse than A for the same work. |
| C. DOIs for all citable objects | Fees per object; public-metadata rule conflicts with restricted tiers; registrant obligations sit with a registration agency the project does not control; DR-0049 already scopes DOIs to releases. |
| D. Handle prefix and local handle server | DOI's substrate without DOI's ecosystem; infrastructure to run; no opacity or persistence conventions; Informational RFC without IETF consensus. |
| E. A formal URN namespace | IANA expert review for a namespace that then resolves nowhere; the project would still build everything in A. |
| F. Publish the internal UUIDs | Immutable but 36 characters, no check character, no persistence semantics, and collapses the §15 internal/public distinction and DR-0012's assignment model. |

## 5. Recommendation

Adopt **ARK** as the public identifier scheme, with the rules below. Each
is a separate candidate DR (§6) so the founder can rule on them one at a
time.

1. **Scheme.** Public identifiers are ARKs under a NAAN requested for the
   project. Names are opaque, betanumeric, with a terminal check character;
   they encode no type, name, date, tier, status or classification. The
   project operates its own resolver on its domain and registers it with
   N2T so the ARK resolver chain can find it and, at succession, a
   successor can take it over. The URL form is a resolver convenience; the
   citation form is `ark:/NAAN/name`.
2. **Minting is an assignment event.** A public identifier is an
   `identifier-assignment` assertion (DR-0012) with the project as asserter
   and a registry identifier-type for the project's own ARKs. It is minted
   at the object's first publication decision (Gate 3) or by explicit
   editorial act for objects cited without a page of their own. Internal
   UUIDs are never published as identifiers. Eligible classes: the §15 list
   (persons, organisations, events, assertions, source captures/holdings,
   quotations, investigations, legal records, dataset releases) plus
   annotations and published pages.
3. **The identifier register and the five dispositions.** Every minted
   identifier has exactly one current disposition — `active`, `redirect`
   (merge), `disambiguation` (split), `tombstone` (redaction, DR-0077), or
   `restricted` (exists; access-tier notice with `withheld`) — held as
   data, shipped in every dump and release change set, and served by the
   resolver together with an ARK `?info` commitment statement. Dispositions
   only ever move forward (an `active` identifier may become any of the
   others; nothing returns to `active` except by a recorded decision
   reversing a redaction under §77). No identifier is ever deleted or
   reissued.
4. **Identifiers name objects; qualifiers name states.** An ARK without a
   qualifier resolves to the object's current state with links to its
   history. Explicitly versioned things (page revisions, OCFL holding
   versions) are cited with an ARK qualifier of the form `.vN`. The
   resolver may additionally offer Memento datetime negotiation; that is
   implementation, not identity.
5. **All project URIs derive from ARKs.** The registry receives an ARK; its
   SKOS concept URIs are that ARK's resolver URL with `#entry-id` (hash
   URIs, per the Semantic-Web note's small-stable-set criterion), replacing
   the provisional namespace in `registry.yaml` and closing SPEC-0005 §7 Q1
   and DR-0083's open item. Entities and other citable objects use slash
   URIs with content negotiation. DR-0049's DOIs for releases are external
   identifier assignments whose landing page is the release's ARK page.

Two implementation notes fall out of the study without needing a DR: new
internal UUIDs should be minted as version 7 (RFC 9562's recommendation;
better index locality; no change to any published surface), and
`published_page.path` becomes a *resolver target* of a page's ARK rather
than the citation identifier the schema comment currently claims.

## 6. Candidate Decision Records

- **CDR-P3-36 — ARK as the public identifier scheme.** §5 rule 1. Records
  that §15's research-first obligation has been met (this paper, §2) and
  resolves the scheme half of Q-12. Supersedes nothing; DR-0022's deferral
  is discharged.
- **CDR-P3-37 — Public identifiers are minted as assignment events at
  publication.** §5 rule 2. Extends DR-0012 to the project's own
  identifiers; fixes the eligible classes, including annotations (the
  other half of Q-12); satisfies §15's "not automatically" clause.
- **CDR-P3-38 — The identifier register and its five dispositions.** §5
  rule 3. Gives DATA-009 its verification object, implements DR-0064's
  redirects and disambiguation records and DR-0077's tombstones on the
  public surface, and adds the `restricted` disposition required by
  SPEC-0006 §9A. Also fixes SPEC-0002 §6 Q3 (disambiguation-record content:
  the split event's date, deciding agent, successor identifiers, and the
  grounds citation — nothing more).
- **CDR-P3-39 — Identifiers name objects; `.vN` qualifiers name states.**
  §5 rule 4.
- **CDR-P3-40 — Project URIs derive from ARKs; the registry namespace is
  the registry's ARK with hash fragments.** §5 rule 5. A structural change
  under DR-0080 to the provisional namespace, taken before any external
  consumer exists; closes SPEC-0005 §7 Q1 and DR-0083's open item.

If approved, these five DRs are the input to **SPEC-0007 — Public
Identifiers and Resolution**, which would specify the name-generation
algorithm and check-character rule, the register schema and its place in
the dump format (SPEC-0006 change), the resolver's HTTP contract including
`?info` and content negotiation, the Gate 3 minting hook, and the migration
of `registry.yaml` and SPEC-0005 to the new namespace.

## 7. What was and was not verified

Verified by web retrieval on 2026-09-08 against the primary text: the ARK
Internet-Draft (`draft-kunze-ark-43`, published 2026-05-08, expires
2026-11-09), RFC 9562, RFC 3650, RFC 8141, RFC 7089, the W3C "Cool URIs
don't change" essay, the W3C "Cool URIs for the Semantic Web" note, the
DataCite landing-page requirements, and the ARK Alliance's comparison page
(source of the fee, organisation-count and ARK-count figures).

Not verified: the DOI Handbook was unreachable (HTTP 404 at three
addresses), so DOI syntax statements rest on general knowledge and on RFC
3650; the ARK "shoulder" convention for delegated sub-namespaces and the
exact check-character algorithm (NOID) were not re-read and are therefore
left to SPEC-0007 rather than fixed here. No NAAN has been requested; the
paper assumes one can be obtained, as the draft states, without fee.

## 8. Open questions raised

1. **NAAN timing.** Request the NAAN now (it commits the project to nothing
   and secures the number) or at first publication?
2. **Shoulders for succession.** Whether to reserve a sub-namespace
   ("shoulder") so a successor institution can mint under the same NAAN
   without collision — cheap now, hard later; needs the unverified
   convention checked in SPEC-0007.
3. **Minting for restricted-tier objects.** Rule 2 mints at publication;
   a restricted object is never published. Should citation by a
   subscriber-tier product count as publication for minting purposes, so
   that the `restricted` disposition is reachable at all?
4. **Web Annotation Protocol.** Whether annotations are ever served as LDP
   containers per the WAP, or only through the general resolver.
5. **Memento.** Whether the resolver implements TimeGate/TimeMap from the
   first release or after; interacts with Q-06 (site-snapshot mechanics).
6. **Internal UUID v7.** Whether existing v4 keys are left as they are
   (recommended — they are never published) with v7 for new rows only.

## 9. Sources

- ARK: [draft-kunze-ark-43](https://datatracker.ietf.org/doc/html/draft-kunze-ark) (IETF Datatracker); [ARK Alliance — comparing ARKs and other identifiers](https://arks.org/about/comparing-arks-and-other-identifiers/)
- UUID: [RFC 9562](https://www.rfc-editor.org/rfc/rfc9562.html)
- Handle: [RFC 3650](https://www.rfc-editor.org/rfc/rfc3650.html)
- URN: [RFC 8141](https://www.rfc-editor.org/rfc/rfc8141.html)
- Memento: [RFC 7089](https://www.rfc-editor.org/rfc/rfc7089.html)
- W3C: [Cool URIs don't change](https://www.w3.org/Provider/Style/URI); [Cool URIs for the Semantic Web](https://www.w3.org/TR/cooluris/)
- DataCite: [Landing pages](https://support.datacite.org/docs/landing-pages)
- Record §15–16, §77, §89; Principle 18; DATA-009/010; ARCH-001; PRES-009; DR-0012, 0017, 0018, 0022, 0029, 0045, 0048, 0049, 0055, 0058, 0062, 0064, 0066, 0077, 0080, 0083, 0086; SPEC-0001 §2, SPEC-0002 §5–6, SPEC-0005 §4 and §7, SPEC-0006 §9A; WP 0.4 §6 Q1 (origin of Q-12)
