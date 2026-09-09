# SPEC-0007 — Public Identifiers and Resolution

**Class:** SPEC (DR-0046 control) | **Version:** 0.2 | **Status:** Draft — Candidate
**Approval:** — | **Effective:** —
**Supersedes:** — | **Superseded by:** —
**Change history:** 0.1 drafted 2026-09-09 from the five rulings on WP 3.4 (DR-0087…0091). 0.2 the same day: the check-character rule (§2.3) confirmed against a published NOID port and the `?info` record format (§6.2) fixed as an ERC record, closing the first two open questions of 0.1. Not yet implemented; §11 lists what must exist before anything is minted.
**Governed by:** DR-0087 (ARK scheme), DR-0088 (minting as assignment events), DR-0089 (register and dispositions), DR-0090 (objects and `.vN` states), DR-0091 (ARK-derived URIs); DR-0012, DR-0055, DR-0064, DR-0077, DR-0080, DR-0086; record §15–16; DATA-009/010, PRES-009, ARCH-001.
**Implemented by:** nothing yet. Intended home: `identifiers/` (minting, register, resolver), a new `schema/08-identifiers.sql`, and a tier rule in `export/tiers.py`.

### AI provenance (record §80)

Drafted 2026-09-09 by an AI assistant (Anthropic Claude Code agent session)
at the founder's direction, immediately after the founder ruled on
CDR-P3-31…35 one at a time. Candidate until approved. Where this document
fixes something the ARK draft leaves open (the check-character algorithm,
the `?info` record format), §2.3 and §6.2 say what it was checked against.

---

## 1. Why this exists

DR-0087…0091 decided *what* the project's public identifiers are. This
document says *exactly* how one is formed, when one is minted, what is
recorded, how it resolves in each of its five dispositions, and what a
future operator needs in order to rebuild the resolver from the archive
alone. The test is PRES-009's: with this document, the identifier register
from a dump, and an OCFL root, someone with no other context must be able to
answer every identifier the project ever published.

## 2. Identifier syntax

### 2.1 Form

```
ark:/NAAN/SHOULDER NAME CHECK [.vN]
        └───────── base name ─────────┘
```

| Part | Rule |
|---|---|
| `ark:/` | The label, always with the slash in the citation form. |
| `NAAN` | The project's Name Assigning Authority Number, five betanumeric characters, issued by the ARK maintenance agency. **Not yet issued** (§11). |
| `SHOULDER` | One primordial shoulder reserved for project minting: betanumeric consonants ending in the first digit (ARK draft convention). Chosen when the NAAN is issued and recorded in `registry.yaml`. A second shoulder is reserved, unused, for a successor institution (DR-0087; WP 3.4 §8 Q2). |
| `NAME` | Eight characters drawn uniformly at random from the betanumeric alphabet by a cryptographically secure generator. Random, not sequential: a sequence leaks minting order and counts (Cool URIs; §15 opacity). Collision is checked against the register before commit. |
| `CHECK` | One check character (§2.3). |
| `.vN` | Optional state qualifier (DR-0090; §7). |

The betanumeric alphabet is exactly

```
bcdfghjkmnpqrstvwxz0123456789
```

(twenty-nine characters; no vowels, no `l`). Names therefore never spell a
word in any language the project publishes in, and encode no type, name,
date, tier, status or classification (DR-0087).

### 2.2 Forms of the same identifier

| Form | Example shape | Use |
|---|---|---|
| **Citation form** | `ark:/NAAN/x1abcd2345k` | The identifier. Used in citations, CSL output (DR-0022), dumps, change sets and RDF. |
| **Project URL** | `https://ukraineindependencewar.org/ark:/NAAN/x1abcd2345k` | Resolves at the project's resolver. |
| **N2T URL** | `https://n2t.net/ark:/NAAN/x1abcd2345k` | Resolves through the ARK resolver chain to whichever resolver the NAAN record names. |

The hostname is identity-inert: all three name the same object.

### 2.3 Check character

The check character is the NOID check digit: over the string from the
first character of the NAAN to the last character of NAME, inclusive of
the `/`, each character's ordinal in the extended alphabet
`0123456789bcdfghjkmnpqrstvwxz` (characters outside it, such as `/`, count
as zero) is multiplied by its one-based position; the sum modulo 29
indexes the same alphabet to give CHECK. It is appended as the right-most
character of the base name, the position the ARK draft calls
conventional, and the draft's rule that the sum runs "back to the
beginning of the NAAN" fixes the string it covers. The rule detects every
single-character substitution and every adjacent transposition within
the alphabet; §10 tests that claim rather than trusting it.

Verified 2026-09-09 against the `checkdigit` method and `XDIGIT` alphabet
of the Ruby NOID port (`microservices/noid`), which implements the rule
above verbatim. The Perl reference module (`Noid.pm` on CPAN) was not
reachable from this environment; the suite must include one identifier
whose check character is confirmed against that reference before v1.0.

### 2.4 Normalisation

Before any lookup or comparison the resolver and the register apply the
ARK draft's normalisation: strip any hostname and query string; lower-case
the NAAN; **ignore hyphens anywhere** (they may be inserted for readability
in print and are never significant); collapse repeated slashes and periods;
strip terminal structural characters. Because names use only lower-case
betanumerics, case elsewhere is preserved by rule but never arises.

## 3. What may carry a public identifier

DR-0088 §3 fixes the eligible classes. This table binds each to its store:

| §15 class | Table today | Status |
|---|---|---|
| persons, organisations | `world_actor` | exists |
| events | — | **no table yet**; bound when created |
| assertions | `project_assertion`, `documentary_assertion` | exist |
| source captures / holdings | `holding` (and by qualifier its `preserved_object` versions) | exist |
| quotations | — | no table yet |
| investigations | — | no table yet |
| legal records (designation records, instruments) | — | no table yet |
| dataset releases | release baseline (`release/baseline.py` manifest) | exists as a file object, not a row; §4.4 |
| annotations | — (evidential targeting lives inside `documentary_assertion`; no Web Annotation table) | no table yet |
| published pages | `published_page` | exists |

A class without a table is bound by this document the day its table
appears: adding the table without adding it to §3 and to the tier rules
must fail the suite (§10). Internal-only tables — `pipeline_agent`,
`collector_run`, `acquisition_attempt`, `quarantine_item`, `proposal`,
`acceptance`, `review_record` and the rest — are **never** eligible; a
minting attempt against them is an error.

## 4. Minting (DR-0088)

### 4.1 Triggers

1. **Gate 3 publish.** When `Publisher.publish()` writes a `page_revision`,
   the transaction also mints, if not already minted: the page; every
   assertion in `revision_assertion`; every holding in `revision_holding`.
2. **Gate 3 decide.** A `publication_decision` on an assertion or holding
   mints it, so an object can be cited before a page carries it.
3. **Editorial cite.** An explicit `cite(subject)` action by a pipeline
   agent of kind `person`, for an eligible object not yet published,
   recording a rationale. This is how an annotation, quotation or holding
   referenced from outside a page gets its identifier.

Minting is **idempotent**: an object has at most one ARK, and a second
minting returns the existing one. Minting never happens at row creation
(DR-0088 alternative 2, rejected).

### 4.2 What is recorded

Minting writes, in one transaction:

- an **`identifier_assignment`** assertion (SPEC-0001 §2.2 family;
  DR-0012) with the §2.1 core columns, `subject` = the object's typed
  reference, `identifier_type` = `uiw-ark` (§8.1), `value` = the citation
  form, `asserter_id` = the project's own `pipeline_agent` row (kind
  `organization`), `basis` = the publication decision, revision or cite
  action that triggered it;
- a **register row** (§5) with disposition `active`.

**The `identifier_assignment` family does not exist in the DDL today**
(SPEC-0001 §2.2 defines it; `schema/` has no assignment tables of any
kind). §11 lists it as a prerequisite; its column contract is the §2.1
core plus `subject_table`, `subject_id`, `identifier_type`
(`identifier_types` reference) and `value`.

### 4.3 What is never done

Internal UUIDs are never rendered on any public surface, in any resolver
response, or in any RDF projection. A test greps every rendered page,
resolver body and projection for the UUID pattern (§10).

### 4.4 Releases

A release baseline is minted by `release/baseline.py --create` and the ARK
is written into the release manifest; the register row's subject is the
manifest's digest. A DataCite DOI, when one is minted under DR-0049, is
recorded as an external `identifier_assignment` on the same subject with
type `doi`; its landing page is the release's ARK page (DR-0091 §3).

## 5. The register (DR-0089)

Two tables, split so that table-level tier rules (SPEC-0006 §9A) can ship
the public part in every disclosure dump while keeping the subject mapping
internal:

```
public_identifier
    ark                 text PRIMARY KEY      -- normalised citation form
    minted_at           timestamptz NOT NULL
    assignment_id       uuid NOT NULL          -- the identifier_assignment row
    disposition         identifier_dispositions NOT NULL
    disposition_at      timestamptz NOT NULL
    disposition_basis   uuid                   -- merge/split event, redaction decision, tier decision
    successor_ark       text REFERENCES public_identifier(ark)   -- redirect only
    disambiguation_id   uuid                   -- disambiguation only

public_identifier_subject
    ark                 text PRIMARY KEY REFERENCES public_identifier(ark)
    subject_table       text NOT NULL
    subject_id          uuid NOT NULL
    UNIQUE (subject_table, subject_id)
```

`identifier_dispositions` is a closed registry vocabulary (§8.1):
`active`, `redirect`, `disambiguation`, `tombstone`, `restricted`.

**Invariants, enforced by trigger and checked by test:**

1. **No delete, ever.** The same append-only enforcement as DR-0055's
   assertion tables.
2. **Forward only.** `active` → any other; `restricted` → `active` only by
   a recorded tier decision that lowers restriction; `tombstone` → `active`
   only by a recorded reversal of the redaction under §77 (DR-0089 §2);
   `redirect` and `disambiguation` are terminal.
3. **Every disposition carries its basis.** A non-`active` row without
   `disposition_basis` is rejected.
4. **A redirect's successor must itself be registered**, and successor
   chains are followed to the first non-`redirect` row at resolution
   (bounded; a cycle is a constraint violation).
5. **A disambiguation record** contains exactly: the split event's date,
   the deciding agent, the successor ARKs, and the grounds citation
   (DR-0089 §5; closes SPEC-0002 §6 Q3).

**Tier rules.** `public_identifier` is declared `public` in
`export/tiers.py`: the existence of every minted identifier, and its
disposition, is public information by construction (that is what
`restricted` means). `public_identifier_subject` is declared `internal`.
Adding either table without a rule makes every dump refuse (SPEC-0006 §9A,
fail closed), which is the intended behaviour.

**Change sets.** Every disposition change since the previous release ships
in the release change set (DR-0048 §91 mappings), keyed by ARK.

## 6. Resolution

### 6.1 Contract

The resolver is a stateless HTTP service over `public_identifier`,
`public_identifier_subject` and the object stores. Its only configuration
is the NAAN, the shoulder, and the object renderers. Given a request path
beginning `/ark:/NAAN/`, it normalises (§2.4), strips any qualifier and
inflection, looks the base name up in the register, and answers by
disposition:

| Disposition | Response | Body |
|---|---|---|
| `active` | `200`, or `303 See Other` to a representation when content negotiation asks for RDF (DR-0091 §2) | The object's current state, with links to its history (§7) |
| `redirect` | `301 Moved Permanently` to the successor ARK's project URL | A short lineage note: "merged into … on … by …" (DR-0064) |
| `disambiguation` | `200` | The disambiguation record (§5 invariant 5); no automatic redirect, because there is no single successor |
| `tombstone` | `410 Gone` | The tombstone: fact, date, authority and grounds of removal, never the content (DR-0077) |
| `restricted` | `403 Forbidden` | A notice that the object exists, its access tier, and the absence state `withheld` (DR-0029); nothing else |
| never minted | `404 Not Found` | States that no such identifier was ever issued, so that a reader can tell a typo from a removal |

**A minted identifier never returns `404`.** That is DATA-009's test,
run against every row of the register.

### 6.2 Inflections

- **`?info`** is mandatory (ARK draft). It returns `200 text/plain` in
  every disposition, including `restricted` and `tombstone`, as an **ERC
  record in ANVL** (the format the ARK draft's `?info` inherits from
  Kunze's ERC and ANVL Internet-Drafts, both expired and both stable
  since 2005–2007): the record opens with `erc:`, carries the four kernel
  elements `who` (the project), `what` (a type-neutral description),
  `when` (minted date, ISO 8601), `where` (the project URL of the
  identifier), then `disposition`, `disposition-at`, and a `support-erc`
  block carrying the commitment statement (§9); a blank line ends it.
  ERC's missing-value tokens are used as the standard defines them:
  `(:unal)` (intentionally suppressed) for `what` on a `restricted`
  identifier, mapping DR-0029's `withheld`; `(:unav)` for a redacted
  `what` on a tombstone. Long values fold onto indented continuation
  lines; encoding is UTF-8.
- `?` and `??` are accepted as synonyms for `?info` (optional in the
  draft; cheap to honour).

### 6.3 Content negotiation

`Accept: text/html` (default) renders the page; `application/ld+json`,
`text/turtle` and `application/rdf+xml` return the object's RDF
representation for classes that have one (entities, registry entries),
via `303` from the object URI to a representation URI per DR-0091. Objects
without an RDF representation answer `406 Not Acceptable` to an RDF-only
request and `200` HTML otherwise.

### 6.4 Resolver chain

The NAAN record at N2T names the project resolver as primary. If the
project resolver is unreachable, N2T's own redirect fails; that is why the
register ships in every dump: a successor rebuilds the resolver from the
dump and updates the NAAN record. Nothing in the identifier changes.

## 7. States and qualifiers (DR-0090)

- The bare ARK resolves to the object's current state, with `Link`
  headers and page links to its history.
- `.vN` names an explicit state: for `published_page`, `page_revision`
  number N; for `holding`, OCFL version `vN`. Other classes have no `.vN`
  until this document lists them.
- An unknown N answers `404` with the object's known range in the body; the
  identifier is valid, the state is not.
- A qualified citation of a `redirect`ed predecessor resolves through the
  redirect to the successor's lineage explanation (DR-0090 §consequences).
- Memento (`Accept-Datetime` → TimeGate over `page_revision`; TimeMap per
  page) is **optional** in this version and, if implemented, must not
  change any identifier.

## 8. Registry and namespace changes

### 8.1 Additive changes (registry process, DR-0080)

- `identifier-types`: add member `uiw-ark` (issuing authority: the
  project; scope note: the project's own public identifier, DR-0087) and
  member `doi` (issuing authority: DataCite/registration agency; DR-0049).
- New closed vocabulary `identifier-dispositions` with the five members of
  §5, authorised by DR-0089.

### 8.2 Structural change (DR-0091, taken by DR)

When the NAAN is issued: the registry is minted its own ARK; the
`namespaces.base` in `registry.yaml` becomes
`https://ukraineindependencewar.org/ark:/NAAN/<registry-name>#` and the
`provisional` flag is cleared; SPEC-0005 is revised to v1.1 recording the
new §4 pattern (`{base}{entry-id}`, `{base}{scheme-id}--{member-id}` are
unchanged in shape). Until then nothing changes.

## 9. Commitment statement

Served by `?info` on every identifier. Draft wording for founder approval:

> **Identifier validity:** this identifier will never be reassigned or
> deleted. **Object permanence:** the object it names may be superseded,
> merged, split, restricted or redacted; in every case this identifier
> continues to resolve and says which. **Content invariance:** the
> unqualified identifier resolves to the object's current state, which
> may change by append-only supersession; a `.vN` qualified state, once
> published, does not change. **Change history:** every state and every
> disposition change is retained and reachable from this identifier.
> **Service:** resolved by the project and, as backup, by the ARK
> resolver chain; the register is preserved in every archive dump so that
> a successor can resume resolution.

## 10. Verification

| Check | Method |
|---|---|
| Check character detects every single-character substitution and adjacent transposition in a sample of 10,000 names | Test |
| Normalisation maps hyphenated, upper-cased-NAAN and hosted forms to the same key | Test |
| A minted ARK cannot be deleted; a backward disposition move without basis is rejected | Test, must be seen to fail when the trigger is removed |
| Every register row resolves to a non-`404` status matching its disposition (DATA-009) | Test over the register |
| No UUID pattern appears in any rendered page, resolver body or projection | Test |
| A table added to `schema/` that is eligible under §3 but absent from tier rules makes the dump refuse | Test (SPEC-0006 §9A) |
| The resolver can be rebuilt from a dump's register tables alone, with no project imports, and answers every identifier | Demonstration, in the style of `export/tests/reconstruct.py` (PRES-009) |
| `?info` returns `200` in all five dispositions | Test |

## 11. Prerequisites before the first identifier is minted

1. A NAAN issued to the project and a primordial shoulder chosen; both
   recorded in `registry.yaml`. The shared **test NAAN `99999`** is used by
   the suite until then, and never in a published identifier.
2. The `identifier_assignment` assertion family in the DDL (§4.2).
3. The two register tables and the `identifier_dispositions` vocabulary.
4. Tier rules for both register tables.
5. The project's own `pipeline_agent` row as asserter.
6. The N2T NAAN record pointing at the project resolver.

## 12. Open questions

1. **Check character against the Perl reference** — §2.3 is confirmed
   against a port; one fixture confirmed against `Noid.pm` closes this.
2. *(resolved in 0.2: `?info` is an ERC record in ANVL, §6.2)*
3. **NAAN timing** (WP 3.4 §8 Q1): request now or at first publication?
   Recommendation: now — it commits the project to nothing and unblocks
   §8.2.
4. **Minting for restricted-tier objects** (WP 3.4 §8 Q3): §4.1 trigger 2
   mints on any `publication_decision`, including at subscriber tiers, so
   the `restricted` disposition is reachable; confirm this is intended.
5. **Which classes get `.vN`** beyond pages and holdings.
6. **Memento** — in v1.0 or later.
7. Whether `public_identifier_subject` should be `internal` (proposed) or
   shipped in researcher-tier disclosures so external researchers can join
   dumps to identifiers.

## 13. Decision Record arising (candidate)

**CDR-P3-36 — Adoption of SPEC-0007 v1.0**, to be put to the founder once
§12 item 1 is closed and §11 items 2–5 are implemented and tested.
