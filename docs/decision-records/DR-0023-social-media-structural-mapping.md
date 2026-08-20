# DR-0023 — Social-media structural mapping

**Category:** architecture | **Status:** Approved | **Decided:** 2026-08-11 by founder/principal editor
**Origin:** CDR-W3-7, WP 0.4 §3.4/§5 | **Supersedes:** — | **Superseded by:** —

## Context

Record §25 requires preserving inexpensive structural context (reply chains,
forwards, nearby posts, threads); §8 makes social platforms first-class sources.
WP 0.3 left the mapping of social-media structures open (its question 7).

## Alternatives considered

1. Map onto the adopted stack: accounts→actor identifiers, posts→manifestations,
   relations→typed documentary links (chosen).
2. A dedicated social-media ontology (rejected for now: the adopted stack
   expresses the requirements; a platform-specific model can be layered later if
   analytics demand it, per §55–56's deferral).

## Decision

- **Accounts** are actor identifiers/appellations assigned by events (DR-0012) —
  an account is never itself a person, and account→actor attribution is an
  evidence-backed identity assertion.
- **Posts** are manifestations (platform embodiments) of expressions (DR-0011).
- **Reply, forward, quote-post, and thread membership** are typed documentary
  relations captured as inexpensive structural context at acquisition (§25),
  alongside engagement metadata where available (§55).
- **Capture series** of changing/deleted posts follow the Memento pattern over
  preserved captures (WP 0.2 §4.5, DR-0018).

## Consequences

- Impersonation and fabricated-account cases (§17) are representable: the
  account identifier exists; its attribution assertions carry their own
  evidence and status.
- Coordination analysis (§56) later builds on these relations without remodeling.
- Richer propagation analytics remain deferred (§55), losslessly.
