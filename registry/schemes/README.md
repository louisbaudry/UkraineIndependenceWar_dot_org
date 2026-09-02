# Argument schemes

Reasoning patterns with attached **critical questions**, per
[DR-0034](../../docs/decision-records/DR-0034-argument-scheme-library.md).

Answering a scheme's critical questions — or failing to — is recorded as
argument structure (DR-0032/0033). This is OSINT verification practice
(Berkeley Protocol, DR-0008) expressed as data, and it operationalises
record §53: attributing deception requires answering *specific* questions
with evidence, not gesturing at falsity.

## The critical questions are not decoration

Since METH-0001 §6.2 (ruled by DR-0085 Q2), an **unanswered critical question
caps analytic confidence at `moderate`**, and Gate 2 enforces that in the
schema (`schema/05-editorial.sql`, `enforce_confidence_cap`). A scheme's
questions therefore define what a conclusion drawn under it can claim: leave
one open and `high` confidence is structurally unavailable.

Each question declares `defeater_type_if_unanswered` — the kind of doubt it
leaves standing (DR-0033). That declaration is what makes the cap defensible
rather than arbitrary: the scheme itself says in advance what an open
question means.

## The library

DR-0034's named set, complete:

| Scheme | Concludes | Sits before / after |
|---|---|---|
| [witness-testimony](witness-testimony.yaml) | An event occurred, from an account of it | — |
| [expert-opinion](expert-opinion.yaml) | A proposition holds, from a specialist's judgment | — |
| [sign-indicator](sign-indicator.yaml) | A state of affairs obtains, from an indicator of it | Feeds attribution |
| [document-authenticity](document-authenticity.yaml) | A document is what it purports to be | **Before** any argument from its contents |
| [image-video-verification](image-video-verification.yaml) | A visual record depicts what it is presented as | **Before** geolocation |
| [geolocation](geolocation.yaml) | Imagery depicts a particular place | After verification |
| [coordination-attribution](coordination-attribution.yaml) | A common hand directs coordinated actors | After sign-indicator; the §52 ladder |

Two distinctions run through the set and are worth naming once:

**Authenticity is not veracity** (§38). `document-authenticity` and
`image-video-verification` conclude only that a thing is what it purports
to be. A claim about what it *shows* is a separate argument in which the
authenticity conclusion is a premise. Collapsing the two is how a genuine
document becomes a false claim.

**Independence is researched, never assumed** (DR-0028, §36). Every scheme
carries a question about whether its corroborating lines share an origin.
Three analyses of one dataset are one line; five lists naming the same
person may be one designation propagating.

## Status

The first two schemes were seeded 2026-08-16 as exemplars. The remaining
five were drafted 2026-08-26, additive under DR-0080, and are **untested
against real investigations** — the archive holds no material yet.
SPEC-0004 §11 Q4 and WP 0.6 §7 Q1 anticipate revision once it does. A
question that turns out never to discriminate, or a scheme that real cases
keep straining, is a registry change with a rationale, not a failure.

Schemes are referenced from `critical_question_answer.scheme_id` and
`.question_id` by identifier. Nothing yet checks that a referenced
question exists in the registry; that cross-check is a known gap.
