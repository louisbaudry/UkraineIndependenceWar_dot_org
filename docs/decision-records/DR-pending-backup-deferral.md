# DR-pending-backup-deferral — Independent backups deferred until the association exists

**Category:** operations / preservation | **Status:** **Approved**
**Decided:** 2026-09-24 by founder/principal editor, choosing option C of three put to them
**Origin:** compiling [`docs/infrastructure.md`](../infrastructure.md) (2026-09-24) found no regular or off-server backup recorded anywhere in the repository | **Supersedes:** — | **Superseded by:** —

> **AI provenance (§80).** Drafted 2026-09-24 by an AI assistant (Anthropic
> Claude Code agent session) at the founder's direction, recording a ruling
> the founder gave the same session. The drafter has never had access to
> the archive server. "No backup is recorded" means the **repository**
> records none. If backups the repository does not know about exist on the
> server, this record's factual premise is wrong and it should be
> superseded, not quietly ignored.

## Context

[OPS-005](../requirements/REQ-OPS-operations.md) requires that *"independent
backups exist and evolve toward geographic and provider redundancy"*,
verified by inspection (backups on infrastructure independent of the
primary) and by an annual restore test that restores an OCFL root and a
canonical dump.

As of 2026-09-24 the repository records:

- **one** set of `pg_dump` files (full and data-only), taken on 2026-09-21
  as part of the schema reload in [`DR-0105`](DR-0105-eur-lex-sanctions-registration.md)
  *Executed* §2, and kept in `~/uiw-backups/` **on the archive server itself**;
- **no** backup of the OCFL storage roots (`~/uiw-archive`);
- **no** copy with any provider other than IONOS
  ([`DR-0100`](DR-0100-jurisdiction-controller-and-hosting.md) Decision 3);
- **no** restore test.

Meanwhile the archive holds real preserved material: the sanctions sources
registered and collected from 2026-09-09 onward, and the two Telegram
channels backfilled under [`DR-0106`](DR-0106-strike-tracking-registration.md)
and [`DR-0107`](DR-0107-strike-tracking-full-backfill.md). As far as the
repository shows, all of it exists on one machine with one provider, so
OPS-005 is unmet.

The project has decided to form an association loi 1901
([`DR-0104`](DR-0104-legal-entity-formation.md)). It does not exist legally
yet, and until it does and takes over, the controller is the founder as a
natural person (DR-0100 Decision 2).

## Alternatives considered

1. **Back up to a second provider now, plus one recorded restore test.**
   A nightly `pg_dump` and a sync of the OCFL roots to storage outside
   IONOS, then one real restore. It meets OPS-005 as written. It costs a
   second provider, contracted by the founder personally, and a
   POL-0001-relevant choice: the copy holds personal data (sanctions
   listings of natural persons) and would need its own Art. 28 processor
   contract, and possibly a different country. Recommended by the drafter.
2. **Use IONOS's own backup product.** Quickest to set up. It is the same
   provider, so it does not meet the "independent infrastructure" that
   OPS-005's verification names. It would guard against disk or server
   loss, but not against losing the IONOS account.
3. **Defer until the association exists.** No cost or new processor
   relationship now, and the second provider would be contracted once, by
   the entity that will be the long-term controller, instead of by the
   founder personally and then moved over. The cost is the risk that any
   loss of the server or the IONOS account before then loses the archive's
   only copy. **Chosen.**

## Decision

1. **Setting up independent backups (OPS-005) is deferred until the
   association under DR-0104 legally exists.** "Legally exists" means its
   declaration is filed and published, so it can enter contracts in its own
   name. The trigger is that fact, not the controller handover, which is a
   separate POL-0001 §11 review.
2. **OPS-005 is knowingly unmet until then.** This record is where that is
   stated. No document may describe the archive as backed up, or as meeting
   OPS-005, before a later record says so.
3. **Nothing in this record forbids an ad-hoc `pg_dump` on the server**,
   like the one DR-0105 took before a schema change. Such dumps stay on the
   same machine, are not the independent backup OPS-005 requires, and do
   not discharge this deferral.
4. **The deferred work is tracked as one card on the project board**,
   labelled `kind:blocked-external` and `epic:infrastructure`, blocked on
   the association's formation. It reaches `kind:decision` when the trigger
   in Decision 1 is met.

## Consequences

1. **The archive has a single point of failure, accepted knowingly.** Losing
   the IONOS server, its disk, or the IONOS account before the association
   exists loses every preserved byte and the canonical database, with no
   copy anywhere. Material that is still online at its publisher could be
   re-collected, but it would be a new capture with a new capture time, not
   a restoration. A publisher that has since changed or removed something
   takes that version with it.
2. **The longer formation takes, the larger the exposure.** Every collection
   run between now and then adds material held only on the server. This
   record sets no deadline. Whether a long delay in forming the
   association should reopen this deferral is left to the founder, at any
   time, by superseding this record.
3. **When the trigger is met, option 1 above is the natural starting
   point.** The second provider's country and Art. 28 contract become
   questions for the association as controller, and they bear on POL-0001
   §11's material-change review.
4. **[`docs/infrastructure.md`](../infrastructure.md) §3.3 and its gap list
   cite this record**, so a reader of the infrastructure page sees that the
   gap was accepted, not overlooked.
