# REQ-EVID — Evidence & Epistemics Requirements

**Class:** REQ (DR-0046 control) | **Version:** 1.0 | **Status:** Approved — Effective
**Approval:** founder/principal editor, 2026-08-16 | **Effective:** 2026-08-16
**Supersedes:** — | **Superseded by:** —
**Entries:** EVID-001 … EVID-015

---

### EVID-001 — Every assertion carries who asserts it, when, and on what basis
**Sources:** §30; Principle 2 · **Satisfied by:** DR-0024, DR-0031, SPEC-0001 §2.1
**Verification:** *Test* — schema requires asserter, `asserted_at`, and basis on
every assertion family; nulls rejected.

### EVID-002 — Documentary assertions, world assertions, and project conclusions are distinct objects
**Sources:** §32–33; Principles 3, 7 · **Satisfied by:** DR-0024, SPEC-0001 §4
**Verification:** *Inspection* — distinct object families exist per SPEC-0001.
*Test* — no shared type or table conflates the three.

### EVID-003 — Evidence relations are explicit and claim-relative; archived ≠ evidentially used
**Sources:** §29; Principles 5, 6 · **Satisfied by:** DR-0024
**Verification:** *Test* — every evidence relation references a proposition.
*Audit* — preserved sources bearing no evidence relation exist and are
normal, demonstrating the distinction holds in practice.

### EVID-004 — Evidential annotations target preserved captures with version pinning and selector redundancy
**Sources:** §24, §59 · **Satisfied by:** DR-0017, DR-0018, DR-0061
**Verification:** *Test* — every evidential annotation target resolves through a
holding to a version-pinned representation; targets naming only a live URL
are rejected at write time.

### EVID-005 — Quotations carry exact passage, source version, locus, omissions, and derivation; none minted from paraphrase
**Sources:** §58–59 · **Satisfied by:** DR-0019
**Verification:** *Test* — quotation entries require passage, source version and
locus. *Audit* — sample of 20 published quotations traced to source bytes at
the stated locus; paraphrase and summary entries carry their own distinct
types.

### EVID-006 — Likelihood and analytic confidence are recorded separately; bare numeric scores are prohibited
**Sources:** §42 · **Satisfied by:** DR-0026, DR-0065
**Verification:** *Test* — likelihood is a registry band identifier; confidence
is low/moderate/high; no free numeric confidence field exists anywhere in
the schema.

### EVID-007 — Contradictory assessments are preserved, never averaged
**Sources:** §40; Principle 9 · **Satisfied by:** DR-0026, DR-0055
**Verification:** *Test* — multiple conflicting assessments on one proposition
store and retrieve intact. *Inspection* — no aggregation function writes a
merged or averaged assessment value.

### EVID-008 — Source grades never determine proposition truth
**Sources:** §37 · **Satisfied by:** DR-0027
**Verification:** *Inspection* — no code path reads a source grade when
computing or setting likelihood, confidence, or status. *Audit* — sampled
assessments cite evidence and reasoning, never a grade.

### EVID-009 — Corroboration counts independent lines only; dependence relations are typed and recorded where consequential
**Sources:** §36 · **Satisfied by:** DR-0028, DR-0067
**Verification:** *Audit* — sample of corroboration claims; each identifies
distinct lines and addresses known dependence relations, including
registry-level declared dependence.

### EVID-010 — Missing values never default to negatives; absence states are typed; negatives carry provenance
**Sources:** §41; Principle 8 · **Satisfied by:** DR-0029
**Verification:** *Test* — schema rejects null wherever an absence state is
required; absence values validate against the registry vocabulary; explicit
negative assertions carry asserter and basis like any other assertion.

### EVID-011 — Quantitative assertions preserve original semantics; normalization never overwrites
**Sources:** §43–44 · **Satisfied by:** DR-0030
**Verification:** *Test* — quantity objects carry original expression and
semantic type; normalized values occupy separate fields. *Audit* — sampled
aggregations respect semantic type (a sum of at-leasts is an at-least).

### EVID-012 — Consequential conclusions preserve visible inference chains with typed defeaters
**Sources:** §34; Principle 7 · **Satisfied by:** DR-0032, DR-0033
**Verification:** *Audit* — every consequential published conclusion has an
argument structure recording premises, scheme, and any raised defeaters with
their type.

### EVID-013 — Important investigations maintain competing-hypothesis sets with discriminating evidence
**Sources:** §35 · **Satisfied by:** DR-0035
**Verification:** *Audit* — investigations designated important carry hypothesis
sets with at least two hypotheses and typed evidence relations including
discriminating evidence.

### EVID-014 — No computation adjudicates a project conclusion
**Sources:** §79 · **Satisfied by:** DR-0036, DR-0016
**Verification:** *Inspection* — no automated path sets a project conclusion's
status. *Audit* — every published conclusion traces to a human
inference-making record.

### EVID-015 — Prior epistemic states are never rewritten by later events
**Sources:** §63 · **Satisfied by:** DR-0048, DR-0055
**Verification:** *Test* — assessment changes create superseding records; no
in-place update path exists on assertion families.
