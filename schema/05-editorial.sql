-- Canonical store: Gate 2, editorial acceptance.
--
-- SPEC-0003 §2 and §7: does anything extracted from a preserved item become
-- canonical knowledge? Nothing crosses on automated confidence alone.
-- Extractions and matches arrive as **proposals** and become canonical only by
-- human acceptance at the risk tier the content demands.
--
-- The layers Gate 2 produces are DR-0024's 4 and 5: project assertions (the
-- project's own voice) and epistemic assessments (likelihood and confidence
-- with a stated basis). Layer 6, arguments, is 06-argument.sql.
--
-- Four METH-0001 rules are enforced here rather than left to discipline:
--
--   §1.5   Consequence is recorded with the limb that triggered it, so "is
--          this consequential?" is answerable from the row rather than from
--          someone's memory.
--   §6.2   An open critical question caps analytic confidence at `moderate`.
--   §7     A consequential conclusion requires a competing-hypothesis set.
--   §10.1  A conclusion needing T1/T2 review that got only self-review is
--          `unreviewed`, and publication must carry that qualification.
--
-- Implements DR-0024, DR-0036, DR-0055, DR-0063, DR-0066, METH-0001, and
-- AI-001/AI-003.
--
-- Depends on 01-enums-generated.sql … 04-epistemic.sql.

-- ---------------------------------------------------------------------------
-- Consequence (METH-0001 §1.5)
-- ---------------------------------------------------------------------------
--
-- The record uses "consequential" throughout without defining it; METH-0001
-- §1.5 defines it once, as a three-part test with any limb sufficing. Storing
-- *which* limb fired makes the classification reviewable — a later reader can
-- disagree with the reasoning rather than only with the verdict.

CREATE TYPE consequence_limb AS ENUM (
    'names-identifiable-party',   -- limb 1: a person or entity, by name or by
                                  --         any identifier resolving to one
    'feeds-legal-layer',          -- limb 2: designation mapping, ownership
                                  --         path, sanctions/export assessment
    'materially-relied-on'        -- limb 3: a figure, chronology or
                                  --         attribution others would act on
);

-- ---------------------------------------------------------------------------
-- Proposals — what automation may produce, and nothing more
-- ---------------------------------------------------------------------------
--
-- AI-003: an AI-proposed assertion is a belief held by a software agent until
-- a human adopts it, and adoption is a separate recorded act that changes who
-- holds the belief. This table is that "until".

CREATE TABLE proposal (
    id              uuid PRIMARY KEY,
    -- What kind of thing is being proposed. Free-form rather than an enum:
    -- the registry governs vocabularies, and proposal kinds are an
    -- implementation concern that will grow with the extractors.
    kind            text NOT NULL,
    -- The agent that produced it. Constrained below: only software and
    -- organizations propose. A person recording their own judgment writes a
    -- project assertion directly and is accountable for it.
    proposed_by     uuid NOT NULL REFERENCES pipeline_agent(id),
    proposed_at     timestamptz NOT NULL DEFAULT now(),
    -- What it was derived from. At least one must be present: a proposal with
    -- no origin cannot be reviewed, because there is nothing to check it
    -- against (DR-0018, EVID-004).
    holding_id      uuid REFERENCES holding(id),
    documentary_assertion_id uuid REFERENCES documentary_assertion(id),
    -- The proposed content, and the features the extractor relied on.
    -- `feature_basis` is what a reviewer interrogates (DR-0063).
    content         jsonb NOT NULL,
    feature_basis   jsonb NOT NULL,
    -- Consequential proposals demand a person's acceptance at T1/T2; routine
    -- ones may be accepted batch-wise at T3 (DR-0063, §78).
    review_tier     review_tiers NOT NULL,
    -- Lifecycle per DR-0063. Terminal states are reached only through an
    -- `acceptance` row; this column is a denormalized convenience kept true by
    -- the trigger below, not an independently writable field.
    state           match_states NOT NULL DEFAULT 'proposed',
    -- AI provenance (§80, AI-002) for consequential model outputs. Routine
    -- disposable calls are exempt by documented rule, never by omission —
    -- hence the constraint rather than a nullable field left to habit.
    ai_provenance   jsonb,

    CONSTRAINT proposals_have_an_origin CHECK (
        holding_id IS NOT NULL OR documentary_assertion_id IS NOT NULL
    )
);

-- Only automation proposes. A person forming a judgment is not proposing it
-- to themselves; they assert it and answer for it (§79).
CREATE FUNCTION proposal_agent_is_not_a_person() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE agent_kind text;
BEGIN
    SELECT kind INTO agent_kind FROM pipeline_agent WHERE id = NEW.proposed_by;
    IF agent_kind = 'person' THEN
        RAISE EXCEPTION
            'a person does not propose to themselves: record a project '
            'assertion, which carries their accountability (§79, AI-003)';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER proposal_agent_check
    BEFORE INSERT ON proposal
    FOR EACH ROW EXECUTE FUNCTION proposal_agent_is_not_a_person();

-- A software proposal at T1 or T2 must carry its AI provenance. §80's list is
-- checked at the application layer; the schema enforces that *something* is
-- there, so an omission is loud rather than silent.
CREATE FUNCTION consequential_ai_carries_provenance() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE agent_kind text;
BEGIN
    SELECT kind INTO agent_kind FROM pipeline_agent WHERE id = NEW.proposed_by;
    IF agent_kind = 'software'
       AND NEW.review_tier IN ('T1', 'T2')
       AND NEW.ai_provenance IS NULL THEN
        RAISE EXCEPTION
            'a software proposal at tier % must carry ai_provenance '
            '(§80, AI-002); routine calls are exempt by documented rule, '
            'not by omission', NEW.review_tier;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER proposal_ai_provenance_check
    BEFORE INSERT ON proposal
    FOR EACH ROW EXECUTE FUNCTION consequential_ai_carries_provenance();

COMMENT ON TABLE proposal IS
    'What automation may produce (AI-003). A proposal is a belief held by a '
    'software agent; it becomes canonical only through an acceptance row, '
    'which changes who holds the belief.';

-- ---------------------------------------------------------------------------
-- Acceptance — the human act at Gate 2
-- ---------------------------------------------------------------------------
--
-- SPEC-0003 §7: acceptance records the accepting agent, the risk tier applied,
-- what was accepted and what was rejected. **Rejections are retained** — they
-- are audit trail and matcher input alike, and a rejection nobody can consult
-- gets re-proposed forever.

CREATE TABLE acceptance (
    id              uuid PRIMARY KEY,
    proposal_id     uuid NOT NULL REFERENCES proposal(id),
    -- The person who accepted or rejected. Not nullable, not a software
    -- agent: this column is where AI-001 becomes structural.
    decided_by      uuid NOT NULL REFERENCES pipeline_agent(id),
    decided_at      timestamptz NOT NULL DEFAULT now(),
    disposition     match_states NOT NULL,
    -- The tier actually applied, which may exceed the proposal's own — a
    -- reviewer may decide something is more consequential than the extractor
    -- judged. It may never fall below it.
    tier_applied    review_tiers NOT NULL,
    -- Why. For a rejection this is the record others consult; for an
    -- acceptance at T1/T2 it is the discriminating evidence relied on
    -- (DR-0063: name similarity alone never confirms).
    reasoning       text NOT NULL,
    -- Batch acceptance is permitted at T3 only (DR-0063). A batch id groups
    -- decisions taken in one act so an audit can sample them.
    batch_id        uuid,

    CONSTRAINT disposition_is_terminal
        CHECK (disposition IN ('confirmed', 'rejected', 'withdrawn')),
    CONSTRAINT batches_are_routine_only
        CHECK (batch_id IS NULL OR tier_applied = 'T3')
);

SELECT make_append_only('acceptance');

-- The load-bearing rule of Gate 2: only a person decides (AI-001, §79).
CREATE FUNCTION acceptance_is_by_a_person() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE agent_kind text; proposed_tier review_tiers;
BEGIN
    SELECT kind INTO agent_kind FROM pipeline_agent WHERE id = NEW.decided_by;
    IF agent_kind <> 'person' THEN
        RAISE EXCEPTION
            'Gate 2 acceptance requires a person (AI-001, §79): agent kind '
            'was %. No computation adjudicates (DR-0036)', agent_kind;
    END IF;

    -- A reviewer may raise the tier but never lower it. Lowering it would let
    -- a consequential item be waved through as routine, which is the whole
    -- failure mode the tiers exist to prevent.
    SELECT review_tier INTO proposed_tier FROM proposal WHERE id = NEW.proposal_id;
    IF NEW.tier_applied > proposed_tier THEN
        RAISE EXCEPTION
            'tier applied (%) is lower than the tier proposed (%); a reviewer '
            'may raise the tier, never lower it (§78)',
            NEW.tier_applied, proposed_tier;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER acceptance_person_check
    BEFORE INSERT ON acceptance
    FOR EACH ROW EXECUTE FUNCTION acceptance_is_by_a_person();

-- Keep the proposal's denormalized state true to its decisions.
CREATE FUNCTION sync_proposal_state() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    UPDATE proposal SET state = NEW.disposition WHERE id = NEW.proposal_id;
    RETURN NEW;
END;
$$;

CREATE TRIGGER acceptance_syncs_proposal
    AFTER INSERT ON acceptance
    FOR EACH ROW EXECUTE FUNCTION sync_proposal_state();

COMMENT ON TABLE acceptance IS
    'The Gate 2 decision (SPEC-0003 §7). Rejections are retained as '
    'consultable records: a rejection nobody can look up gets re-proposed '
    'forever.';

-- ---------------------------------------------------------------------------
-- Project assertions — DR-0024 layer 4, the project's own voice
-- ---------------------------------------------------------------------------

CREATE TABLE project_assertion (
    -- ---- SPEC-0001 §2.1 core ----
    id                  uuid PRIMARY KEY,
    valid_time          timespan NOT NULL,
    asserted_at         timestamptz NOT NULL DEFAULT now(),
    asserter_id         uuid NOT NULL REFERENCES pipeline_agent(id),
    epistemic_category  epistemic_categories NOT NULL,
    likelihood          likelihood_bands,
    confidence          analytic_confidence,
    basis               jsonb,
    supersedes_id       uuid REFERENCES project_assertion(id),
    redacted_at         timestamptz,
    redaction_ground    text,
    redaction_authority text,
    -- ---- family payload ----
    proposition_id      uuid NOT NULL REFERENCES proposition(id),
    -- The proposal this was adopted from, where it came from one. Null for a
    -- judgment a person formed directly, which is equally legitimate.
    adopted_from_id     uuid REFERENCES proposal(id),
    -- METH-0001 §1.5. Null limb means "not consequential"; a limb means it is,
    -- and says which test it met.
    consequence_limb    consequence_limb,
    reasoning           text,

    CONSTRAINT valid_time_well_formed CHECK (timespan_ok(valid_time)),

    -- The project speaks in its own voice here: findings, assessments,
    -- conclusions and hypotheses. It never records a source's claim as its
    -- own — that is a documentary assertion (§32, EVID-002).
    CONSTRAINT project_does_not_launder_source_claims
        CHECK (epistemic_category <> 'claim'),

    -- A band belongs to an assessment with its evidence and reasoning; it
    -- never attaches bare (DR-0065 rule 6, EVID-006).
    CONSTRAINT bands_require_a_basis CHECK (
        likelihood IS NULL OR basis IS NOT NULL OR reasoning IS NOT NULL
    ),

    CONSTRAINT tombstone_is_complete CHECK (
        num_nonnulls(redacted_at, redaction_ground, redaction_authority) IN (0, 3)
    )
);

SELECT make_append_only('project_assertion');

-- AI-001, made structural. An assertion whose asserter is a software agent
-- cannot exist without a confirming acceptance by a person.
CREATE FUNCTION project_assertion_accountability() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE agent_kind text; confirmed boolean;
BEGIN
    SELECT kind INTO agent_kind FROM pipeline_agent WHERE id = NEW.asserter_id;
    IF agent_kind = 'person' THEN
        RETURN NEW;                       -- a person answers for their own work
    END IF;

    IF NEW.adopted_from_id IS NULL THEN
        RAISE EXCEPTION
            'a non-human asserter must adopt from a proposal accepted by a '
            'person (AI-001, AI-003): adopted_from_id is null';
    END IF;

    SELECT EXISTS (
        SELECT 1 FROM acceptance
         WHERE proposal_id = NEW.adopted_from_id AND disposition = 'confirmed'
    ) INTO confirmed;

    IF NOT confirmed THEN
        RAISE EXCEPTION
            'proposal % has no confirming acceptance; AI output never becomes '
            'canonical without human accountability (AI-001, §79)',
            NEW.adopted_from_id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER project_assertion_accountability_check
    BEFORE INSERT ON project_assertion
    FOR EACH ROW EXECUTE FUNCTION project_assertion_accountability();

COMMENT ON TABLE project_assertion IS
    'What the project says in its own voice (DR-0024 layer 4). Distinct from '
    'what a source said, permanently (§32–33, EVID-002).';

-- ---------------------------------------------------------------------------
-- Critical-question coverage — METH-0001 §6.2, ruled by DR-0085 Q2
-- ---------------------------------------------------------------------------
--
-- Argument schemes carry critical questions (DR-0034). Each is answered, or
-- recorded as unanswered with the defeater type it then implies. An open
-- question caps analytic confidence at `moderate`: the rule that makes the
-- discipline bite rather than being a checklist one notes and moves past.

CREATE TABLE critical_question_answer (
    id              uuid PRIMARY KEY,
    assertion_id    uuid NOT NULL REFERENCES project_assertion(id),
    -- Registry identifiers: the scheme (e.g. `scheme-geolocation`) and the
    -- question within it (e.g. `cq-distinctiveness`).
    scheme_id       text NOT NULL,
    question_id     text NOT NULL,
    -- Null answer = the question stands open. An argued dismissal is an
    -- answer: METH-0001 §6.2 caps confidence only while a question is
    -- untouched, not while it is answered unfavourably.
    answer          text,
    -- What kind of doubt an unanswered question leaves, per the scheme.
    unanswered_defeater defeater_types,
    answered_by     uuid REFERENCES pipeline_agent(id),
    recorded_at     timestamptz NOT NULL DEFAULT now(),

    UNIQUE (assertion_id, scheme_id, question_id),

    -- An open question must say what doubt it leaves; that is the scheme's
    -- own declaration and is the reason the cap is defensible.
    CONSTRAINT open_questions_declare_their_defeater CHECK (
        answer IS NOT NULL OR unanswered_defeater IS NOT NULL
    ),
    CONSTRAINT answers_have_an_author CHECK (
        answer IS NULL OR answered_by IS NOT NULL
    )
);

COMMENT ON TABLE critical_question_answer IS
    'Critical-question coverage per assertion (DR-0034). An open question '
    'caps analytic confidence at moderate (METH-0001 §6.2, DR-0085 Q2).';

-- The cap itself. Deferred to statement end so questions and the assertion
-- can be written in either order within one transaction.
CREATE FUNCTION enforce_confidence_cap() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE open_count integer; target uuid;
BEGIN
    -- IF rather than CASE: plpgsql plans the whole expression against NEW's
    -- actual row type, so a CASE naming both tables' columns fails to compile
    -- on whichever table it was not fired from.
    IF TG_TABLE_NAME = 'project_assertion' THEN
        target := NEW.id;
    ELSE
        target := NEW.assertion_id;
    END IF;

    SELECT count(*) INTO open_count
      FROM critical_question_answer
     WHERE assertion_id = target AND answer IS NULL;

    -- The cap binds a *live* claim. A superseded assertion may stand at
    -- `high` in the record forever: it was what the project held at the time,
    -- and rewriting it would be exactly the retrospective edit EVID-015
    -- forbids.
    --
    -- This is what lets a doubt raised months later be recorded at all. The
    -- system must never refuse to hear an objection in order to protect a
    -- confidence claim — that would be the worst possible failure mode for an
    -- evidentiary archive. Instead the objection is admitted on condition
    -- that the over-confident claim is superseded in the same breath, which
    -- is the append-only correction pattern used everywhere else (DR-0055).
    IF open_count > 0 AND EXISTS (
        SELECT 1 FROM project_assertion pa
         WHERE pa.id = target
           AND pa.confidence = 'high'
           AND NOT EXISTS (
               SELECT 1 FROM project_assertion s WHERE s.supersedes_id = pa.id
           )
    ) THEN
        RAISE EXCEPTION
            'assertion % has % unanswered critical question(s) and still '
            'stands at high confidence; the cap is moderate (METH-0001 §6.2, '
            'DR-0085 Q2). Answer the question, argue it away, or supersede '
            'the assertion at moderate or lower in this transaction — the '
            'objection is not being refused, the stale confidence is',
            target, open_count;
    END IF;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER project_assertion_confidence_cap
    AFTER INSERT ON project_assertion
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION enforce_confidence_cap();

CREATE CONSTRAINT TRIGGER critical_question_confidence_cap
    AFTER INSERT OR UPDATE ON critical_question_answer
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION enforce_confidence_cap();

-- ---------------------------------------------------------------------------
-- Review records — METH-0001 §10.1, ruled by DR-0085 Q4
-- ---------------------------------------------------------------------------
--
-- §83: second-person review is not automatically independent review, and two
-- signatures need not mean two independent judgments. While the project is one
-- person, no conclusion can receive what T1 and T2 ask for — so the record
-- says `unreviewed`, and publication carries that qualification visibly.

CREATE TYPE review_state AS ENUM (
    'unreviewed',   -- self-review only; the tier's requirement is unmet
    'reviewed',     -- a second party examined the reasoning
    'independent'   -- the reviewer formed a judgment from the evidence
                    -- *before* seeing the conclusion (§83, METH §10.3)
);

CREATE TABLE review_record (
    id              uuid PRIMARY KEY,
    assertion_id    uuid NOT NULL REFERENCES project_assertion(id),
    tier_required   review_tiers NOT NULL,
    state           review_state NOT NULL,
    reviewed_by     uuid REFERENCES pipeline_agent(id),
    reviewed_at     timestamptz NOT NULL DEFAULT now(),
    notes           text,

    -- A review with no reviewer is not a review. `unreviewed` is the state
    -- that legitimately has none.
    CONSTRAINT reviews_have_a_reviewer CHECK (
        state = 'unreviewed' OR reviewed_by IS NOT NULL
    )
);

-- The reviewer is never the asserter. That is what "second party" means, and
-- it is the one part of §83 a database can check.
CREATE FUNCTION reviewer_is_a_second_party() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE author uuid;
BEGIN
    IF NEW.state = 'unreviewed' THEN
        RETURN NEW;
    END IF;
    SELECT asserter_id INTO author FROM project_assertion WHERE id = NEW.assertion_id;
    IF author = NEW.reviewed_by THEN
        RAISE EXCEPTION
            'the asserter cannot be the reviewer: a second look by the same '
            'mind is not an independent judgment (§83). Record `unreviewed` '
            'and publish qualified (METH-0001 §10.1)';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER review_second_party_check
    BEFORE INSERT ON review_record
    FOR EACH ROW EXECUTE FUNCTION reviewer_is_a_second_party();

COMMENT ON TABLE review_record IS
    'What review a conclusion actually received (§83). `unreviewed` is a '
    'legitimate, publishable state — presenting it as reviewed is not '
    '(METH-0001 §10.1, DR-0085 Q4).';

-- What a publication surface must render alongside a conclusion. A view
-- rather than a column, so it cannot drift out of step with the reviews.
CREATE VIEW publishable_conclusion AS
    SELECT pa.id,
           pa.proposition_id,
           pa.epistemic_category,
           pa.likelihood,
           pa.confidence,
           pa.consequence_limb,
           coalesce(r.state, 'unreviewed')::review_state AS review_state,
           r.tier_required,
           -- The qualification the reader sees. METH-0001 §10.1: publication
           -- is not blocked; presenting the conclusion as reviewed is.
           CASE
               WHEN pa.consequence_limb IS NULL THEN NULL
               WHEN coalesce(r.state, 'unreviewed') = 'unreviewed'
                   THEN 'Unreviewed at tier ' || coalesce(r.tier_required::text, 'T2')
                        || ': this conclusion has not received the independent '
                        || 'review its consequence requires.'
               WHEN r.state = 'reviewed'
                   THEN 'Reviewed by a second party; not independently reassessed.'
               ELSE 'Independently reassessed.'
           END AS review_qualification
      FROM project_assertion pa
      LEFT JOIN LATERAL (
          SELECT state, tier_required FROM review_record
           WHERE assertion_id = pa.id
           ORDER BY state DESC, reviewed_at DESC LIMIT 1
      ) r ON true
     WHERE pa.redacted_at IS NULL;

COMMENT ON VIEW publishable_conclusion IS
    'A conclusion with the review qualification a publication surface must '
    'render (METH-0001 §10.1). Derived, so it cannot drift out of step with '
    'the review records.';
