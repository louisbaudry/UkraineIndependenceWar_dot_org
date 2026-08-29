-- Canonical store: core types and the assertion pattern.
--
-- Implements SPEC-0001 under DR-0054 (relational, assertion-centric,
-- append-only canonical store) and DR-0057 (PostgreSQL as the default
-- implementation candidate; the representation commitment survives an
-- engine change).
--
-- Depends on 01-enums-generated.sql for registry-derived types.

-- ---------------------------------------------------------------------------
-- Time
-- ---------------------------------------------------------------------------

-- A time-span with the four-bound fuzzy-interval pattern (CIDOC E52's
-- "ongoing throughout" / "at some time within"), implementing record §45's
-- approximate dates, ranges, and open intervals.
--
-- `absence` carries why a span is unknown rather than leaving nulls to mean
-- it (DR-0029, record §41). A span is either bounded or explicitly absent —
-- never silently empty.
CREATE TYPE timespan AS (
    begin_earliest  timestamptz,  -- earliest the span may have begun
    begin_latest    timestamptz,  -- latest it may have begun
    end_earliest    timestamptz,  -- earliest it may have ended
    end_latest      timestamptz,  -- latest it may have ended
    absence         absence_states
);

-- True when a span is well-formed: either it carries at least one bound, or
-- it declares why it has none.
CREATE FUNCTION timespan_ok(ts timespan) RETURNS boolean
LANGUAGE sql IMMUTABLE AS $$
    SELECT (
        ts.begin_earliest IS NOT NULL OR ts.begin_latest IS NOT NULL
        OR ts.end_earliest IS NOT NULL OR ts.end_latest IS NOT NULL
    ) <> (ts.absence IS NOT NULL)
    AND (ts.begin_earliest IS NULL OR ts.begin_latest IS NULL
         OR ts.begin_earliest <= ts.begin_latest)
    AND (ts.end_earliest IS NULL OR ts.end_latest IS NULL
         OR ts.end_earliest <= ts.end_latest);
$$;

-- ---------------------------------------------------------------------------
-- Quantity
-- ---------------------------------------------------------------------------

-- A quantitative assertion preserving what the source actually expressed
-- (DR-0030, record §43-44). The original expression is never overwritten by
-- a normalized value; "at least 17" never becomes "exactly 17".
CREATE TYPE quantity AS (
    original_expression text,     -- as stated, verbatim
    original_language   text,
    semantic_type       quantity_semantic_types,
    value_low           numeric,  -- interpretation of the expression
    value_high          numeric,  -- upper bound for ranges
    unit                text,
    significant_digits  integer,  -- resolution actually conveyed (§43)
    uncertainty         numeric,
    derivation_method   text,     -- set iff the value was computed
    absence             absence_states
);

CREATE FUNCTION quantity_ok(q quantity) RETURNS boolean
LANGUAGE sql IMMUTABLE AS $$
    SELECT
        -- Either the quantity says something, or it says why it says nothing.
        (q.semantic_type IS NOT NULL) <> (q.absence IS NOT NULL)
        -- A stated quantity keeps the words it was stated in (§44).
        AND (q.semantic_type IS NULL OR q.original_expression IS NOT NULL)
        -- Ranges need both bounds; non-ranges must not pretend to have them.
        AND (q.semantic_type IS DISTINCT FROM 'range'
             OR (q.value_low IS NOT NULL AND q.value_high IS NOT NULL))
        AND (q.value_low IS NULL OR q.value_high IS NULL
             OR q.value_low <= q.value_high);
$$;

-- ---------------------------------------------------------------------------
-- Agents — two registries, linked, never merged (DR-0004, DR-0059)
-- ---------------------------------------------------------------------------

-- Persons, organizations and software acting on the archive or the pipeline.
-- Never a historical actor: a collector is not a subject of history.
CREATE TABLE pipeline_agent (
    id              uuid PRIMARY KEY,
    kind            text NOT NULL CHECK (kind IN ('person', 'organization', 'software')),
    name            text NOT NULL,
    software_version text,          -- required for software agents (AI-002)
    model_identifier text,          -- provider/model for AI agents (§80)
    created_at      timestamptz NOT NULL DEFAULT now(),
    CONSTRAINT software_agents_are_versioned
        CHECK (kind <> 'software' OR software_version IS NOT NULL)
);

COMMENT ON TABLE pipeline_agent IS
    'Agents acting on the archive (DR-0059). Separate from world_actor by '
    'DR-0004; a real person appearing in both is linked by an evidence-backed '
    'same-person assertion, never merged.';

-- Historical persons and groups: subjects of the record, not operators of it.
-- Carries no name or identifier columns — appellations and identifiers attach
-- via assignment assertions (DR-0012, SPEC-0001 §2.2).
CREATE TABLE world_actor (
    id       uuid PRIMARY KEY,
    kind     text NOT NULL CHECK (kind IN ('person', 'group')),
    status   entity_statuses NOT NULL,
    created_at timestamptz NOT NULL DEFAULT now()
);

COMMENT ON TABLE world_actor IS
    'Historical actors (DR-0010). Deliberately has no name column: names are '
    'assignment assertions with provenance (DR-0012). Fabricated and disproved '
    'entities are retained as referents, never deleted (DR-0062).';

-- ---------------------------------------------------------------------------
-- Tier resolution (§12, SEC-003/004)
-- ---------------------------------------------------------------------------
--
-- "Several tiers apply; which governs?" The answer must be the most
-- restrictive, and it cannot be read off any ordering the database supplies:
-- both the enum order and the alphabetical order put `public` before
-- `subscriber`, so min() over {public, subscriber} yields `public` — the less
-- restrictive of the two, and precisely the wrong answer.
--
-- Restrictiveness is therefore declared. This mirrors RESTRICTIVENESS in
-- export/tiers.py; the test suite checks the two agree rather than trusting
-- them to stay aligned.

CREATE FUNCTION tier_restrictiveness(t access_tiers) RETURNS integer
LANGUAGE sql IMMUTABLE AS $$
    SELECT CASE t
        WHEN 'public' THEN 0
        WHEN 'subscriber' THEN 1
        -- Lateral grants to different named parties, not rungs: same rank,
        -- because neither covers the other's material.
        WHEN 'researcher-restricted' THEN 2
        WHEN 'investigator-restricted' THEN 2
        WHEN 'internal' THEN 3
        WHEN 'confidential' THEN 4
        WHEN 'private-preservation' THEN 5
    END;
$$;

CREATE FUNCTION most_restrictive_tier(tiers access_tiers[])
RETURNS access_tiers LANGUAGE sql IMMUTABLE AS $$
    SELECT CASE
        -- Nothing to go on. Unclassified is not the same as safe.
        WHEN tiers IS NULL OR cardinality(tiers) = 0 THEN 'confidential'
        -- Two different tiers tie at the top: both lateral grants apply and
        -- neither admits the other's material, so escalate.
        WHEN (SELECT count(DISTINCT t) FROM unnest(tiers) t
               WHERE tier_restrictiveness(t) =
                     (SELECT max(tier_restrictiveness(u)) FROM unnest(tiers) u)
             ) > 1 THEN 'internal'
        ELSE (SELECT t FROM unnest(tiers) t
               ORDER BY tier_restrictiveness(t) DESC LIMIT 1)
    END::access_tiers;
$$;

COMMENT ON FUNCTION most_restrictive_tier IS
    'Which tier governs when several apply (§12). Never derive this from the '
    'enum or alphabetical order: both rank `public` below `subscriber`, which '
    'is backwards for restrictiveness and errs toward disclosure.';

-- ---------------------------------------------------------------------------
-- The assertion core
-- ---------------------------------------------------------------------------
--
-- SPEC-0001 §2.1 fixes a common core carried by every assertion family, and
-- §2.2's granularity decision keeps families separate rather than collapsing
-- them into one polymorphic table, so payloads get real typing.
--
-- The core is defined here as a DOMAIN-documented column set. Every family
-- table repeats it; `assertion_core_columns` names the contract, and the test
-- suite fails if a family omits any of it — the constraint is enforced by
-- test rather than by inheritance, which would compromise foreign keys.

CREATE TABLE assertion_core_columns (
    column_name text PRIMARY KEY,
    rationale   text NOT NULL
);

INSERT INTO assertion_core_columns (column_name, rationale) VALUES
    ('id',            'Immutable internal identifier (record §15)'),
    ('valid_time',    'World time: when the asserted content holds (§45)'),
    ('asserted_at',   'Record time: when this entered the store (bitemporality)'),
    ('asserter_id',   'Which pipeline agent holds this belief (DR-0031, §30)'),
    ('epistemic_category', 'Which kind of assertion this is (DR-0025)'),
    ('likelihood',    'Calibrated probability band, where assessed (DR-0065)'),
    ('confidence',    'Analytic confidence, where assessed (DR-0026)'),
    ('basis',         'Evidence or inference this rests on (DR-0024 layers 3/6)'),
    ('supersedes_id', 'The assertion this one replaces (DR-0055)'),
    ('redacted_at',   'Tombstone: when content was removed (DR-0077)'),
    ('redaction_ground',  'Tombstone: under what ground (§77)'),
    ('redaction_authority', 'Tombstone: on whose authority');

COMMENT ON TABLE assertion_core_columns IS
    'The SPEC-0001 §2.1 core contract. Not data: a machine-checkable statement '
    'of what every assertion family must carry, verified by the test suite.';

-- ---------------------------------------------------------------------------
-- Append-only enforcement (DR-0055, DR-0077)
-- ---------------------------------------------------------------------------
--
-- Corrections are superseding assertions; nothing is edited in place. The one
-- exception is governed redaction, which must leave a tombstone.

CREATE FUNCTION forbid_mutation() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    IF TG_OP = 'DELETE' THEN
        RAISE EXCEPTION
            'DR-0055: % is append-only; assertions are never deleted. '
            'Use the governed redaction path (DR-0077), which leaves a tombstone.',
            TG_TABLE_NAME
            USING ERRCODE = 'restrict_violation';
    END IF;

    -- An UPDATE is permitted only to write a redaction tombstone, and only
    -- when the redaction fields move from unset to set. Content columns are
    -- checked by the family's own redaction function.
    IF OLD.redacted_at IS NULL AND NEW.redacted_at IS NOT NULL
       AND NEW.redaction_ground IS NOT NULL
       AND NEW.redaction_authority IS NOT NULL
       AND current_setting('uiw.redaction_in_progress', true) = 'on'
    THEN
        RETURN NEW;
    END IF;

    RAISE EXCEPTION
        'DR-0055: % is append-only; correct by superseding assertion, not by '
        'update. Redaction requires the governed path (DR-0077).',
        TG_TABLE_NAME
        USING ERRCODE = 'restrict_violation';
END;
$$;

COMMENT ON FUNCTION forbid_mutation() IS
    'Append-only guard (DR-0055). Attach to every assertion family. Permits '
    'only tombstone-writing updates inside a governed redaction (DR-0077).';

-- Applies the append-only guard to a family table. Called by each family's
-- DDL so the rule cannot be forgotten.
CREATE FUNCTION make_append_only(table_name text) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    EXECUTE format(
        'CREATE TRIGGER %I_append_only BEFORE UPDATE OR DELETE ON %I '
        'FOR EACH ROW EXECUTE FUNCTION forbid_mutation()',
        table_name, table_name
    );
END;
$$;
