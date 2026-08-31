# Source registration

Candidate sources for the first real collection, drafted against the DR-0067
registry schema. **Nothing here is registered.** These are proposals for the
founder to accept, amend, or reject — per source, not as a block.

```bash
python3 sources/register.py --check                      # validate only
python3 sources/register.py --dry-run                    # what it would authorise
python3 sources/register.py --commit --dbname uiw \
        --agent <your-pipeline_agent-uuid> \
        --only ofac-sdn eu-consolidated-list             # register these two
```

Registering a source is **the act that authorises collecting from it**
(OPS-001). It is not a configuration change, and the gap between "drafted"
and "registered" exists so that authorising is deliberate.

## What is proposed

Seven sanctions and export-control authorities — the thematic area the
founder chose. Institutional publishers, stable formats, near-zero
special-category personal data, so DR-0071's interim constraints barely bite
and POL-0001's structuring limits are straightforward to honour.

| Key | Authority | Jurisdiction | Cadence | Grade |
|---|---|---|---|---|
| `eur-lex-sanctions` | EUR-Lex restrictive measures | EU | daily | A1 |
| `eu-consolidated-list` | EU Consolidated Financial Sanctions List | EU | daily | A1 |
| `ofac-sdn` | OFAC SDN + Consolidated | US | daily | A1 |
| `bis-entity-list` | BIS Entity / Denied Persons | US | weekly | A1 |
| `uk-ofsi-consolidated` | OFSI Consolidated List | GB | daily | A1 |
| `seco-sanctions` | SECO sanctions list | CH | weekly | A1 |
| `ua-nsdc-sanctions` | NSDC decisions and enacting decrees | UA | weekly | B2 |

Grades are **triage only** — they set scrutiny depth and review priority and
are architecturally barred from touching any proposition's truth, likelihood
or confidence (DR-0027, EVID-008).

## The judgment calls, so you can disagree with the reasoning

**Why EUR-Lex and the consolidated list are both registered.** They are not
redundant. The instrument is the legal act; the consolidated list is an
administrative compilation of it. DR-0038 makes instruments carry lifecycles,
and a designation's history is reconstructible from instruments in a way it is
not from a snapshot list. Their dependence is declared (below), so they never
count as two lines.

**Why whole-file captures rather than parsing on ingest.** Each list is
captured whole, forming a capture series (DR-0074), and nothing is parsed into
structured fields at collection time. Designation records name individuals with
dates and places of birth; DR-0071(b) forbids automatic promotion of personal
data into queryable structure. Structuring is a Gate 2 decision under POL-0001
§4, taken per record, not a side effect of fetching.

**Why `ua-nsdc-sanctions` is graded B2, not A1.** It is a party to the conflict
publishing about its adversary. The grade means "read with the care a
belligerent source deserves" — it does not mean less likely to be true, and it
cannot reach any assessment. A1 for the EU and US lists is not a claim that
those bodies are right; it is a claim that they reliably publish what they
have decided.

**Why Switzerland is included.** Its non-EU status makes divergence between
Swiss and EU measures evidentially interesting in itself (§68–70, financial
flows). Where it mirrors the EU it is one line, not two — declared below.

**Why `may-preserve` for SECO and NSDC.** Their rights positions are
unverified. The conservative default is preserve-only, no redistribution,
until someone checks (§14). Claiming redistribution rights the project has not
confirmed is the kind of error that is cheap to avoid and expensive to make.

**What is deliberately excluded.** Interpretive guidance, FAQs, press releases
and enforcement notices. They have a different evidentiary character from legal
instruments and belong in their own registrations with their own scope rules —
not folded into these.

## Declared dependence (DR-0028)

Stated once here rather than rediscovered per item. **Five lists naming the
same person are not five independent confirmations** — in part they are one
designation propagating (§36).

| Dependent | Relation | Depends on |
|---|---|---|
| `eu-consolidated-list` | derives-from | `eur-lex-sanctions` |
| `uk-ofsi-consolidated` | common-evidentiary-origin | `eu-consolidated-list` |
| `seco-sanctions` | common-evidentiary-origin | `eu-consolidated-list` |

Declaring dependence is an analytic judgment, so `--commit` requires
`--agent`: the claim carries an asserter like any other assertion.

Not declared, deliberately: OFAC and the EU list. They designate
independently and often diverge, and asserting dependence where none is
established would understate corroboration as badly as assuming independence
overstates it.

## What registering these commits you to

`--dry-run` prints this; it is repeated here because each item is a real
obligation rather than a formality.

- **Reading capacity in de, fr, it and uk at Gate 2.** No translations are
  seeded (DR-0081). Registering `ua-nsdc-sanctions` in particular commits the
  project to Ukrainian.
- **Permanent retention for all seven**, meaning indefinite fixity checking
  on a 180-day cadence (DR-0005).
- **Resolving the unverified rights positions** for `seco-sanctions` and
  `ua-nsdc-sanctions` (§14).
- **A first collection run against locators none of which have been fetched.**

## Every locator here is unverified

This environment's proxy blocks general internet hosts, so **no URL below has
been fetched**. Each is drawn from documentation and prior knowledge, not from
a successful request. Some are probably wrong: sanctions authorities move
endpoints, and several of these publish through interfaces that have changed
more than once since 2014.

That is expected and handled. A 404 on first collection is a **recorded failed
acquisition** (PRES-007), not a system fault, and the coverage record will say
plainly what was sought and not obtained (DR-0070, §57). Correcting a locator
is a routine registry edit.

Treat the first run as locator verification. It is the cheapest way to find
out which of these are right.

## Verification

22 tests. The refusals are the substance:

- a candidate missing any policy field is refused rather than defaulted —
  DR-0067's point is that collection policy is *stated*, and a silent default
  is a policy nobody chose;
- an open-ended scope is refused (DR-0071(a));
- a redistribution claim whose basis nobody flagged as unreviewed is refused
  (§14), because silence there reads as "checked and fine";
- a graphic-content source defaulting to public is refused (PRES-012);
- a dependence declaration with no reasoning is refused (DR-0028);
- **registration collects nothing** — a full registry and an empty archive is
  the correct state immediately afterwards.

The scope and rights checks were verified by sabotage: removing either lets
the corresponding bad candidate through and the suite fails.

**Not verified:** that any of these sources exists at the address given, that
the formats are as assumed, or that the rights positions are correct. Those
are questions a network answers, and this environment cannot.
