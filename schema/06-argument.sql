-- Canonical store: DR-0024 layer 6 — arguments, defeaters, hypothesis sets.
--
-- DR-0032: arguments are CRMinf argumentation activities whose content follows
-- the AIF pattern — propositions connected by typed scheme applications.
-- DR-0033: conflict relations are typed rebutting / undercutting / undermining.
-- DR-0035: hypothesis sets are first-class; ACH matrices are derived views
-- over the evidence relations, never separate data.
--
-- Two rules are enforced here rather than left to discipline:
--
--   DR-0036  No computation adjudicates. There is deliberately no column for
--            a computed acceptability status; §40's "unresolved" is a
--            legitimate end-state and stays visible.
--   METH §7  A consequential conclusion requires a competing-hypothesis set
--            with a genuine alternative (DR-0085 Q3).
--
-- Depends on 01-enums-generated.sql … 05-editorial.sql.

-- ---------------------------------------------------------------------------
-- Hypothesis sets — DR-0035
-- ---------------------------------------------------------------------------

CREATE TABLE hypothesis_set (
    id          uuid PRIMARY KEY,
    question    text NOT NULL,       -- the defined question, §74–75
    opened_by   uuid NOT NULL REFERENCES pipeline_agent(id),
    opened_at   timestamptz NOT NULL DEFAULT now(),
    -- Why a set exists at all: METH-0001 §7's three triggers. Recorded so an
    -- audit can check the mandate was applied, not merely honoured where
    -- convenient.
    trigger     text NOT NULL CHECK (trigger IN (
        'single-explanation',    -- one explanation is being built toward
        'consequential',         -- the conclusion meets METH-0001 §1.5
        'strong-prior'           -- the project already expects an answer
    ))
);

COMMENT ON TABLE hypothesis_set IS
    'Competing hypotheses for a defined question (DR-0035). Mandatory in all '
    'three trigger cases including strong prior expectation — the case where '
    'confirmation bias actually operates (METH-0001 §7, DR-0085 Q3).';

CREATE TABLE hypothesis (
    id              uuid PRIMARY KEY,
    set_id          uuid NOT NULL REFERENCES hypothesis_set(id),
    proposition_id  uuid NOT NULL REFERENCES proposition(id),
    -- Marks the alternative that competes with the one being built toward.
    -- The known failure mode is the strawman: an alternative written to
    -- satisfy the rule rather than to compete. The schema cannot detect that;
    -- review treats such a set as absent (METH-0001 §7).
    is_alternative  boolean NOT NULL DEFAULT false,
    added_at        timestamptz NOT NULL DEFAULT now(),

    UNIQUE (set_id, proposition_id)
);

-- A set with one hypothesis is not a set. Deferred, so both rows can be
-- written in one transaction.
CREATE FUNCTION hypothesis_set_has_alternatives() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE n integer; alternatives integer; target uuid;
BEGIN
    -- IF, not CASE: see the note on enforce_confidence_cap in 05-editorial.
    IF TG_TABLE_NAME = 'hypothesis_set' THEN
        target := NEW.id;
    ELSE
        target := NEW.set_id;
    END IF;
    SELECT count(*), count(*) FILTER (WHERE is_alternative)
      INTO n, alternatives
      FROM hypothesis WHERE set_id = target;

    IF n < 2 OR alternatives < 1 THEN
        RAISE EXCEPTION
            'hypothesis set % has % hypothesis(es) and % alternative(s); a '
            'set needs at least two, one of them a genuine alternative '
            '(DR-0035, METH-0001 §7)', target, n, alternatives;
    END IF;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER hypothesis_set_completeness
    AFTER INSERT ON hypothesis_set
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION hypothesis_set_has_alternatives();

-- ---------------------------------------------------------------------------
-- The METH-0001 §7 mandate, made structural
-- ---------------------------------------------------------------------------
--
-- A consequential conclusion requires a hypothesis set. The link is here
-- rather than as a column on project_assertion so that one set can serve
-- several conclusions drawn from the same question.

CREATE TABLE conclusion_hypothesis_set (
    assertion_id    uuid NOT NULL REFERENCES project_assertion(id),
    set_id          uuid NOT NULL REFERENCES hypothesis_set(id),
    PRIMARY KEY (assertion_id, set_id)
);

CREATE FUNCTION consequential_conclusions_compete_hypotheses() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE has_set boolean;
BEGIN
    IF NEW.consequence_limb IS NULL
       OR NEW.epistemic_category NOT IN ('project-conclusion', 'finding') THEN
        RETURN NULL;
    END IF;

    SELECT EXISTS (
        SELECT 1 FROM conclusion_hypothesis_set WHERE assertion_id = NEW.id
    ) INTO has_set;

    IF NOT has_set THEN
        RAISE EXCEPTION
            'consequential conclusion % has no hypothesis set; competing '
            'hypotheses are mandatory for consequential conclusions '
            '(METH-0001 §7, DR-0085 Q3)', NEW.id;
    END IF;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER consequential_needs_hypothesis_set
    AFTER INSERT ON project_assertion
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION consequential_conclusions_compete_hypotheses();

-- ---------------------------------------------------------------------------
-- ACH matrix — a derived view, never separate data (DR-0035)
-- ---------------------------------------------------------------------------
--
-- Heuer's matrix reads off the evidence relations that layer 3 already holds.
-- Copies drift; views stay consistent.

CREATE VIEW ach_matrix AS
    SELECT hs.id             AS set_id,
           hs.question,
           h.id              AS hypothesis_id,
           h.proposition_id,
           h.is_alternative,
           er.id             AS evidence_id,
           er.relation,
           er.holding_id,
           er.documentary_assertion_id
      FROM hypothesis_set hs
      JOIN hypothesis h  ON h.set_id = hs.id
      LEFT JOIN evidence_relation er ON er.proposition_id = h.proposition_id
                                    AND er.redacted_at IS NULL;

COMMENT ON VIEW ach_matrix IS
    'Heuer ACH matrix derived from evidence relations (DR-0035). The '
    'analytically useful query is which evidence `discriminates`: evidence '
    'consistent with every hypothesis distinguishes nothing, however much of '
    'it there is.';

-- Which evidence actually tells the hypotheses apart — the object of the
-- exercise, and simultaneously the research-gap inventory (§74–75).
CREATE VIEW discriminating_evidence AS
    SELECT set_id, question, hypothesis_id, evidence_id, relation
      FROM ach_matrix
     WHERE relation = 'discriminates';

-- ---------------------------------------------------------------------------
-- Arguments — DR-0032, AIF-patterned
-- ---------------------------------------------------------------------------

CREATE TABLE argument (
    id              uuid PRIMARY KEY,
    -- What it concludes. An argument always concludes something the project
    -- says; arguments for what a source said are that source's, not ours.
    assertion_id    uuid NOT NULL REFERENCES project_assertion(id),
    -- The registry scheme applied, e.g. `scheme-geolocation`. Null where no
    -- scheme fits: METH-0001 §6.1 requires premises and warrant to be
    -- recorded anyway, and the gap proposed to the registry.
    scheme_id       text,
    -- Toulmin's warrant: the inference rule relied on. DR-0037 makes the
    -- scaffold a drafting and review discipline; the warrant is the slot most
    -- often left implicit, so it is a column rather than prose.
    warrant         text NOT NULL,
    made_by         uuid NOT NULL REFERENCES pipeline_agent(id),
    made_at         timestamptz NOT NULL DEFAULT now()

    -- Deliberately absent: any computed acceptability or resolution status.
    -- Formal semantics may run as analytic aids and their output is advisory
    -- (DR-0036, EVID-014). A column here would become the editor.
);

SELECT make_append_only('argument');

-- An inference-making record is a human act (DR-0036: tooling may rank, flag
-- and warn; it may never conclude).
CREATE FUNCTION argument_is_made_by_a_person() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE agent_kind text;
BEGIN
    SELECT kind INTO agent_kind FROM pipeline_agent WHERE id = NEW.made_by;
    IF agent_kind <> 'person' THEN
        RAISE EXCEPTION
            'an argument is a human inference-making record (DR-0036, '
            'EVID-014): agent kind was %. Analysis by software is advisory '
            'input, recorded as a proposal', agent_kind;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER argument_person_check
    BEFORE INSERT ON argument
    FOR EACH ROW EXECUTE FUNCTION argument_is_made_by_a_person();

CREATE TABLE argument_premise (
    id              uuid PRIMARY KEY,
    argument_id     uuid NOT NULL REFERENCES argument(id),
    -- A premise rests on something the archive holds: a documentary
    -- assertion, an evidence relation, or a prior project assertion.
    documentary_assertion_id uuid REFERENCES documentary_assertion(id),
    evidence_relation_id     uuid REFERENCES evidence_relation(id),
    project_assertion_id     uuid REFERENCES project_assertion(id),
    -- Where none of the above applies — a background assumption. Naming it as
    -- a premise is the point: an unattacked assumption should be visible.
    assumption      text,

    CONSTRAINT premises_are_grounded CHECK (
        num_nonnulls(documentary_assertion_id, evidence_relation_id,
                     project_assertion_id, assumption) = 1
    )
);

-- ---------------------------------------------------------------------------
-- Defeaters — DR-0033
-- ---------------------------------------------------------------------------

CREATE TABLE defeater (
    id              uuid PRIMARY KEY,
    argument_id     uuid NOT NULL REFERENCES argument(id),
    kind            defeater_types NOT NULL,
    statement       text NOT NULL,
    raised_by       uuid NOT NULL REFERENCES pipeline_agent(id),
    raised_at       timestamptz NOT NULL DEFAULT now(),
    -- An answer, when one is given. Null means the defeater stands, and the
    -- argument is visibly contested — a legitimate end-state (§40, DR-0033).
    -- The method has no step that makes a live objection go away.
    answer          text,
    answered_by     uuid REFERENCES pipeline_agent(id),
    answered_at     timestamptz,

    CONSTRAINT answers_are_complete CHECK (
        num_nonnulls(answer, answered_by, answered_at) IN (0, 3)
    )
);

COMMENT ON TABLE defeater IS
    'Typed attacks on an argument (DR-0033). The distinction is load-bearing: '
    'answering a forgery claim (undermining) with counter-evidence about the '
    'event (rebutting) addresses nothing.';

-- Contested conclusions, surfaced rather than resolved. §40: unresolved is a
-- legitimate end-state, and nothing here adjudicates it.
CREATE VIEW contested_conclusion AS
    SELECT pa.id AS assertion_id,
           pa.proposition_id,
           pa.consequence_limb,
           a.id  AS argument_id,
           count(*) FILTER (WHERE d.answer IS NULL) AS unanswered_defeaters,
           array_agg(DISTINCT d.kind) FILTER (WHERE d.answer IS NULL)
               AS unanswered_kinds
      FROM project_assertion pa
      JOIN argument a ON a.assertion_id = pa.id
      JOIN defeater d ON d.argument_id = a.id
     WHERE pa.redacted_at IS NULL
     GROUP BY pa.id, pa.proposition_id, pa.consequence_limb, a.id
    HAVING count(*) FILTER (WHERE d.answer IS NULL) > 0;

COMMENT ON VIEW contested_conclusion IS
    'Conclusions with live objections (§40). An analytic aid: it reports what '
    'is unanswered and adjudicates nothing (DR-0036).';
