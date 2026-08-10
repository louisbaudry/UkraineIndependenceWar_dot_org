# DR-0006 — WARC for high-value web capture; WACZ evaluation required

**Category:** preservation | **Status:** Approved | **Decided:** 2026-08-10 by founder/principal editor
**Origin:** CDR-W1-6, WP 0.2 §2.4/§7 | **Supersedes:** — | **Superseded by:** —

## Context

Phase I §7 calls for preserving web captures "in richer formats such as WARC for
selected high-value sources." Screenshot- or text-only capture loses the
server-response evidence (headers, timestamps, exact payloads) that gives web
preservation evidentiary weight.

## Alternatives considered

1. WARC for high-value capture + mandatory WACZ evaluation before toolchain
   freeze (chosen).
2. WARC only, WACZ optional later (rejected: WACZ's signable packaging is directly
   relevant to evidentiary aims and cheap to evaluate now).
3. Defer to collection-system design (rejected: the format commitment usefully
   constrains that design).

## Decision

**WARC (ISO 28500)** is the capture format for selected high-value web sources.
Before the capture toolchain is frozen, **WACZ** (packaged, cryptographically
signable web-archive collections, Webrecorder ecosystem) must be evaluated —
including the maturity and jurisdictional meaning of its signing (WP 0.2 §8 Q4).

Not all sources receive WARC capture: selection follows the multi-stage retention
model (record §9); lighter capture forms remain valid for lower tiers, recorded
honestly as such (§26).

## Consequences

- Capture tooling must produce or wrap WARC for the high-value tier.
- The WACZ evaluation is a standing Phase II research task.
- Capture records' per-record digests integrate with DR-0005 fixity.
