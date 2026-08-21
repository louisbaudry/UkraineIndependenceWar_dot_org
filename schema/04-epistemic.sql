-- Canonical store: the epistemic layer, first families.
--
-- Demonstrates the SPEC-0001 §2.1 assertion core on two families: documentary
-- assertions (what a source says, DR-0024 layer 2) and evidence relations
-- (claim-relative support, layer 3). Further families repeat the same core.
--
-- Implements DR-0024, DR-0025, DR-0026, DR-0029, DR-0031, DR-0055, DR-0065.
--
-- Depends on 01-enums-generated.sql, 02-core.sql, 03-pipeline.sql.

-- A proposition: content that can be asserted, believed, supported, attacked.
-- Deliberately not "a fact" — propositions carry no truth value of their own
-- (Principle 3; CRMinf I4 per DR-0031).
CREATE TABLE proposition (
    id          uuid PRIMARY KEY,
    statement   text NOT NULL,
    created_at  timestamptz NOT NULL DEFAULT now()
);

-- ---------------------------------------------------------------------------
-- Documentary assertions — what a source says (DR-0024 layer 2)
-- ---------------------------------------------------------------------------
--
-- Owned by the source, not the project. Entering the graph by adoption
-- (CRMinf I7 pattern) never makes the project hold the belief.

CREATE TABLE documentary_assertion (
    -- ---- SPEC-0001 §2.1 core ----
    id                  uuid PRIMARY KEY,
    valid_time          timespan NOT NULL,
    asserted_at         timestamptz NOT NULL DEFAULT now(),
    asserter_id         uuid NOT NULL REFERENCES pipeline_agent(id),
    epistemic_category  epistemic_categories NOT NULL,
    likelihood          likelihood_bands,
    confidence          analytic_confidence,
    basis               jsonb,
    supersedes_id       uuid REFERENCES documentary_assertion(id),
    redacted_at         timestamptz,
    redaction_ground    text,
    redaction_authority text,
    -- ---- family payload ----
    proposition_id      uuid NOT NULL REFERENCES proposition(id),
    holding_id          uuid NOT NULL REFERENCES holding(id),
    -- Where in the source this is said. Evidential annotations target
    -- preserved captures, never live URLs (DR-0018, EVID-004).
    locator             jsonb NOT NULL,
    -- Who the source attributes the statement to; distinct from the asserter,
    -- which is the pipeline agent that recorded it.
    attributed_to       text,

    CONSTRAINT valid_time_well_formed CHECK (timespan_ok(valid_time)),

    -- A documentary assertion records what a source says; it is a `claim`,
    -- never a project conclusion (§32, Principle 3).
    CONSTRAINT sources_make_claims_not_conclusions
        CHECK (epistemic_category = 'claim'),

    -- Likelihood and confidence belong to assessments, not to the bare fact
    -- that a source said something (DR-0026, §32).
    CONSTRAINT documentary_assertions_carry_no_project_judgment
        CHECK (likelihood IS NULL AND confidence IS NULL),

    -- Tombstones are complete or absent (DR-0077).
    CONSTRAINT tombstone_is_complete CHECK (
        num_nonnulls(redacted_at, redaction_ground, redaction_authority) IN (0, 3)
    )
);

SELECT make_append_only('documentary_assertion');

COMMENT ON TABLE documentary_assertion IS
    'What a source says (DR-0024 layer 2). "The source says X" and "X is true" '
    'are different propositions (§32); this table records only the first.';

-- ---------------------------------------------------------------------------
-- Evidence relations — claim-relative support (DR-0024 layer 3)
-- ---------------------------------------------------------------------------
--
-- Being in the corpus is not being evidentially used (Principle 5). A source
-- becomes evidence only through an explicit relation to a proposition
-- (§29, Principle 6, EVID-003).

CREATE TYPE evidence_relation_kind AS ENUM (
    'supports',
    'contradicts',
    'bears-on',
    'discriminates'   -- distinguishes between competing hypotheses (DR-0035)
);

CREATE TABLE evidence_relation (
    -- ---- SPEC-0001 §2.1 core ----
    id                  uuid PRIMARY KEY,
    valid_time          timespan NOT NULL,
    asserted_at         timestamptz NOT NULL DEFAULT now(),
    asserter_id         uuid NOT NULL REFERENCES pipeline_agent(id),
    epistemic_category  epistemic_categories NOT NULL,
    likelihood          likelihood_bands,
    confidence          analytic_confidence,
    basis               jsonb,
    supersedes_id       uuid REFERENCES evidence_relation(id),
    redacted_at         timestamptz,
    redaction_ground    text,
    redaction_authority text,
    -- ---- family payload ----
    proposition_id      uuid NOT NULL REFERENCES proposition(id),
    holding_id          uuid REFERENCES holding(id),
    documentary_assertion_id uuid REFERENCES documentary_assertion(id),
    relation            evidence_relation_kind NOT NULL,
    reasoning           text,

    CONSTRAINT valid_time_well_formed CHECK (timespan_ok(valid_time)),

    -- Evidence is always evidence *of something* from *something* (§29).
    CONSTRAINT evidence_has_a_source CHECK (
        holding_id IS NOT NULL OR documentary_assertion_id IS NOT NULL
    ),

    -- A likelihood band belongs to an assessment with a stated basis; it
    -- never attaches without one (DR-0065 rule 6).
    CONSTRAINT bands_require_a_basis CHECK (
        likelihood IS NULL OR (basis IS NOT NULL OR reasoning IS NOT NULL)
    ),

    CONSTRAINT tombstone_is_complete CHECK (
        num_nonnulls(redacted_at, redaction_ground, redaction_authority) IN (0, 3)
    )
);

SELECT make_append_only('evidence_relation');

-- ---------------------------------------------------------------------------
-- Cross-family view (SPEC-0001 §2.1)
-- ---------------------------------------------------------------------------
--
-- Families stay separate so payloads get real typing; cross-family questions
-- go through this thin union rather than a polymorphic table.

CREATE VIEW assertion AS
      SELECT 'documentary_assertion' AS family, id, valid_time, asserted_at,
             asserter_id, epistemic_category, likelihood, confidence, basis,
             supersedes_id, redacted_at, redaction_ground, redaction_authority,
             proposition_id
        FROM documentary_assertion
    UNION ALL
      SELECT 'evidence_relation', id, valid_time, asserted_at,
             asserter_id, epistemic_category, likelihood, confidence, basis,
             supersedes_id, redacted_at, redaction_ground, redaction_authority,
             proposition_id
        FROM evidence_relation;

COMMENT ON VIEW assertion IS
    'Thin union over assertion families (SPEC-0001 §2.1). Answers "what did we '
    'hold at time T" by filtering asserted_at and supersession.';

-- What the project held at a given record time: assertions entered by then
-- and not yet superseded by then (bitemporality; EVID-015, §63).
CREATE FUNCTION assertions_as_of(record_time timestamptz)
RETURNS TABLE (
    family text, id uuid, epistemic_category epistemic_categories,
    proposition_id uuid, likelihood likelihood_bands
)
LANGUAGE sql STABLE AS $$
    SELECT a.family, a.id, a.epistemic_category, a.proposition_id, a.likelihood
      FROM assertion a
     WHERE a.asserted_at <= record_time
       AND NOT EXISTS (
           SELECT 1 FROM assertion s
            WHERE s.supersedes_id = a.id
              AND s.asserted_at <= record_time
       );
$$;
