-- Schema test suite.
--
-- Each test executes a verification criterion from a REQ document, naming the
-- requirement it verifies. This closes the record §99 chain at its last link:
-- requirement -> verification criterion -> executable test.
--
-- Run: psql -d uiw -v ON_ERROR_STOP=1 -f schema/tests/test_schema.sql

\set QUIET on
SET client_min_messages = warning;

CREATE OR REPLACE FUNCTION t_pass(req text, what text) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    RAISE INFO 'PASS  % — %', req, what;
END; $$;

-- Asserts that a statement fails. Used for the many requirements phrased as
-- "the schema rejects X".
CREATE OR REPLACE FUNCTION t_rejects(req text, what text, stmt text) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    BEGIN
        EXECUTE stmt;
    EXCEPTION WHEN others THEN
        PERFORM t_pass(req, what);
        RETURN;
    END;
    RAISE EXCEPTION 'FAIL  % — % : statement was accepted but must be rejected', req, what;
END; $$;

CREATE OR REPLACE FUNCTION t_true(req text, what text, cond boolean) RETURNS void
LANGUAGE plpgsql AS $$
BEGIN
    IF cond THEN PERFORM t_pass(req, what);
    ELSE RAISE EXCEPTION 'FAIL  % — %', req, what;
    END IF;
END; $$;

\set QUIET off

-- ---------------------------------------------------------------------------
-- Fixtures
-- ---------------------------------------------------------------------------

INSERT INTO pipeline_agent (id, kind, name, software_version) VALUES
    ('11111111-0000-0000-0000-000000000001', 'person', 'founder', NULL),
    ('11111111-0000-0000-0000-000000000002', 'software', 'collector', '0.1.0');

INSERT INTO source (
    id, source_type, name, collection_method, default_retention_tier,
    default_access_tier, rights_permission
) VALUES (
    '22222222-0000-0000-0000-000000000001', 'government', 'Test source',
    'feed', 'permanent', 'public', 'may-preserve'
);

INSERT INTO preserved_object (
    id, object_level, sha512, sha256, ocfl_root, ocfl_object_id, ocfl_version,
    ingested_at
) VALUES (
    '33333333-0000-0000-0000-000000000001', 'representation',
    decode(repeat('ab', 64), 'hex'), decode(repeat('cd', 32), 'hex'),
    'permanent', 'holding-1', 'v1', now()
);

INSERT INTO holding (
    id, completeness, retention_tier, access_tier, rights_permission,
    ocfl_object_id
) VALUES (
    '44444444-0000-0000-0000-000000000001', 'original', 'permanent',
    'public', 'may-preserve', 'holding-1'
);

INSERT INTO holding_representation VALUES
    ('44444444-0000-0000-0000-000000000001',
     '33333333-0000-0000-0000-000000000001', 'original');

INSERT INTO proposition (id, statement) VALUES
    ('55555555-0000-0000-0000-000000000001', 'A test proposition.');

INSERT INTO documentary_assertion (
    id, valid_time, asserter_id, epistemic_category, proposition_id,
    holding_id, locator
) VALUES (
    '66666666-0000-0000-0000-000000000001',
    ROW('2022-02-24'::timestamptz, NULL, NULL, NULL, NULL)::timespan,
    '11111111-0000-0000-0000-000000000002', 'claim',
    '55555555-0000-0000-0000-000000000001',
    '44444444-0000-0000-0000-000000000001',
    '{"selector": "TextQuote", "exact": "..."}'::jsonb
);

-- ---------------------------------------------------------------------------
-- DATA-001 / DR-0012 — names attach via assignment events, not columns
-- ---------------------------------------------------------------------------

SELECT t_true('DATA-001', 'world_actor carries no name or identifier column',
    NOT EXISTS (
        SELECT 1 FROM information_schema.columns
         WHERE table_name = 'world_actor'
           AND column_name ~ '(name|identifier|alias|label)'
    ));

-- ---------------------------------------------------------------------------
-- ARCH-001 / DR-0004, DR-0059 — the two registries never join implicitly
-- ---------------------------------------------------------------------------

SELECT t_true('ARCH-001', 'no foreign key links pipeline_agent and world_actor',
    NOT EXISTS (
        SELECT 1
          FROM information_schema.referential_constraints rc
          JOIN information_schema.key_column_usage k
            ON k.constraint_name = rc.constraint_name
          JOIN information_schema.constraint_column_usage u
            ON u.constraint_name = rc.constraint_name
         WHERE (k.table_name = 'pipeline_agent' AND u.table_name = 'world_actor')
            OR (k.table_name = 'world_actor' AND u.table_name = 'pipeline_agent')
    ));

-- ---------------------------------------------------------------------------
-- EVID-015 / DR-0055 — append-only: no in-place update, no delete
-- ---------------------------------------------------------------------------

SELECT t_rejects('EVID-015', 'UPDATE on an assertion is refused',
    $$UPDATE documentary_assertion SET attributed_to = 'edited'
       WHERE id = '66666666-0000-0000-0000-000000000001'$$);

SELECT t_rejects('EVID-015', 'DELETE of an assertion is refused',
    $$DELETE FROM documentary_assertion
       WHERE id = '66666666-0000-0000-0000-000000000001'$$);

-- Correction is by superseding assertion, and that path works.
INSERT INTO documentary_assertion (
    id, valid_time, asserter_id, epistemic_category, proposition_id,
    holding_id, locator, supersedes_id
) VALUES (
    '66666666-0000-0000-0000-000000000002',
    ROW('2022-02-24'::timestamptz, NULL, NULL, NULL, NULL)::timespan,
    '11111111-0000-0000-0000-000000000001', 'claim',
    '55555555-0000-0000-0000-000000000001',
    '44444444-0000-0000-0000-000000000001',
    '{"selector": "TextQuote", "exact": "corrected"}'::jsonb,
    '66666666-0000-0000-0000-000000000001'
);

SELECT t_true('EDIT-002', 'correction by supersession is recorded and traceable',
    (SELECT supersedes_id FROM documentary_assertion
      WHERE id = '66666666-0000-0000-0000-000000000002') IS NOT NULL);

-- ---------------------------------------------------------------------------
-- DR-0077 — redaction is the sole exception, and needs a complete tombstone
-- ---------------------------------------------------------------------------

SELECT t_rejects('DR-0077', 'redaction without the governed flag is refused',
    $$UPDATE documentary_assertion
         SET redacted_at = now(), redaction_ground = 'privacy removal',
             redaction_authority = 'founder'
       WHERE id = '66666666-0000-0000-0000-000000000001'$$);

SET uiw.redaction_in_progress = 'on';

SELECT t_rejects('DR-0077', 'redaction with an incomplete tombstone is refused',
    $$UPDATE documentary_assertion SET redacted_at = now()
       WHERE id = '66666666-0000-0000-0000-000000000001'$$);

UPDATE documentary_assertion
   SET redacted_at = now(),
       redaction_ground = 'privacy removal (POL-0001 §6)',
       redaction_authority = 'founder'
 WHERE id = '66666666-0000-0000-0000-000000000001';

SET uiw.redaction_in_progress = 'off';

SELECT t_true('DR-0077', 'governed redaction leaves a complete tombstone',
    (SELECT redacted_at IS NOT NULL AND redaction_ground IS NOT NULL
            AND redaction_authority IS NOT NULL
       FROM documentary_assertion
      WHERE id = '66666666-0000-0000-0000-000000000001'));

-- ---------------------------------------------------------------------------
-- EVID-010 / DR-0029 — absence is typed; null never silently means "no"
-- ---------------------------------------------------------------------------

SELECT t_true('EVID-010', 'a span with neither bounds nor absence is invalid',
    NOT timespan_ok(ROW(NULL, NULL, NULL, NULL, NULL)::timespan));

SELECT t_true('EVID-010', 'a span cannot be both bounded and absent',
    NOT timespan_ok(ROW('2022-01-01'::timestamptz, NULL, NULL, NULL,
                        'unknown'::absence_states)::timespan));

SELECT t_true('EVID-010', 'an explicitly unknown span is valid',
    timespan_ok(ROW(NULL, NULL, NULL, NULL, 'unknown'::absence_states)::timespan));

SELECT t_rejects('EVID-010', 'an assertion with a malformed span is refused',
    $$INSERT INTO documentary_assertion (
        id, valid_time, asserter_id, epistemic_category, proposition_id,
        holding_id, locator
      ) VALUES (
        '66666666-0000-0000-0000-000000000009',
        ROW(NULL, NULL, NULL, NULL, NULL)::timespan,
        '11111111-0000-0000-0000-000000000001', 'claim',
        '55555555-0000-0000-0000-000000000001',
        '44444444-0000-0000-0000-000000000001', '{}'::jsonb)$$);

-- ---------------------------------------------------------------------------
-- EVID-011 / DR-0030 — quantities keep the semantics they were stated in
-- ---------------------------------------------------------------------------

SELECT t_true('EVID-011', '"at least 17" is representable as an at-least',
    quantity_ok(ROW('щонайменше 17', 'uk', 'at-least'::quantity_semantic_types,
                    17, NULL, 'persons', 2, NULL, NULL, NULL)::quantity));

SELECT t_true('EVID-011', 'a stated quantity must keep its original expression',
    NOT quantity_ok(ROW(NULL, NULL, 'exact'::quantity_semantic_types,
                        17, NULL, NULL, NULL, NULL, NULL, NULL)::quantity));

SELECT t_true('EVID-011', 'a range needs both bounds',
    NOT quantity_ok(ROW('17-20', 'en', 'range'::quantity_semantic_types,
                        17, NULL, NULL, NULL, NULL, NULL, NULL)::quantity));

SELECT t_true('EVID-011', 'an absent quantity says why it is absent',
    quantity_ok(ROW(NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL,
                    'no-evidence-found'::absence_states)::quantity));

-- ---------------------------------------------------------------------------
-- EVID-006 / DR-0026, DR-0065 — likelihood and confidence discipline
-- ---------------------------------------------------------------------------

SELECT t_rejects('EVID-006',
    'a documentary assertion cannot carry a project judgment',
    $$INSERT INTO documentary_assertion (
        id, valid_time, asserter_id, epistemic_category, proposition_id,
        holding_id, locator, likelihood
      ) VALUES (
        '66666666-0000-0000-0000-00000000000a',
        ROW('2022-01-01'::timestamptz, NULL, NULL, NULL, NULL)::timespan,
        '11111111-0000-0000-0000-000000000001', 'claim',
        '55555555-0000-0000-0000-000000000001',
        '44444444-0000-0000-0000-000000000001', '{}'::jsonb, 'likely')$$);

SELECT t_rejects('DR-0065', 'a likelihood band without a stated basis is refused',
    $$INSERT INTO evidence_relation (
        id, valid_time, asserter_id, epistemic_category, proposition_id,
        holding_id, relation, likelihood
      ) VALUES (
        '77777777-0000-0000-0000-000000000001',
        ROW('2022-01-01'::timestamptz, NULL, NULL, NULL, NULL)::timespan,
        '11111111-0000-0000-0000-000000000001', 'assessment',
        '55555555-0000-0000-0000-000000000001',
        '44444444-0000-0000-0000-000000000001', 'supports', 'likely')$$);

SELECT t_true('EVID-006', 'no numeric confidence column exists anywhere',
    NOT EXISTS (
        SELECT 1 FROM information_schema.columns
         WHERE column_name LIKE '%confidence%'
           AND data_type IN ('numeric', 'double precision', 'real', 'integer')
    ));

-- ---------------------------------------------------------------------------
-- LEGAL-001 / DR-0038 — no boolean sanctioned property anywhere
-- ---------------------------------------------------------------------------

SELECT t_true('LEGAL-001', 'no boolean sanctioned column exists',
    NOT EXISTS (
        SELECT 1 FROM information_schema.columns
         WHERE column_name ~ 'sanction' AND data_type = 'boolean'
    ));

-- ---------------------------------------------------------------------------
-- EVID-003 / DR-0024 — evidence is claim-relative
-- ---------------------------------------------------------------------------

SELECT t_true('EVID-003', 'every evidence relation references a proposition',
    (SELECT is_nullable FROM information_schema.columns
      WHERE table_name = 'evidence_relation' AND column_name = 'proposition_id')
    = 'NO');

SELECT t_true('EVID-003', 'a preserved holding may exist with no evidence relation',
    EXISTS (
        SELECT 1 FROM holding h
         WHERE NOT EXISTS (
             SELECT 1 FROM evidence_relation e WHERE e.holding_id = h.id)
    ));

-- ---------------------------------------------------------------------------
-- SPEC-0001 §2.1 — every assertion family carries the full core
-- ---------------------------------------------------------------------------

SELECT t_true('SPEC-0001',
    'every assertion family carries the complete §2.1 core',
    NOT EXISTS (
        SELECT 1
          FROM (VALUES ('documentary_assertion'), ('evidence_relation')) AS f(tbl)
         CROSS JOIN assertion_core_columns c
         WHERE NOT EXISTS (
             SELECT 1 FROM information_schema.columns col
              WHERE col.table_name = f.tbl AND col.column_name = c.column_name
         )
    ));

-- ---------------------------------------------------------------------------
-- PRES-012, SEC-002 — pipeline safety constraints
-- ---------------------------------------------------------------------------

SELECT t_rejects('PRES-012',
    'a source expecting graphic content cannot default to public',
    $$INSERT INTO source (
        id, source_type, name, collection_method, default_retention_tier,
        default_access_tier, rights_permission, expects_graphic_content
      ) VALUES (
        '22222222-0000-0000-0000-00000000000b', 'social-media', 'Graphic',
        'api', 'permanent', 'public', 'may-preserve', true)$$);

SELECT t_rejects('SEC-002',
    'quarantined material cannot be admitted without a clean security check',
    $$INSERT INTO quarantine_item (
        id, received_at, byte_size, sha256, security_check_outcome,
        gate1_decision, gate1_decided_at, gate1_decided_by
      ) VALUES (
        '88888888-0000-0000-0000-000000000001', now(), 100,
        decode(repeat('ef', 32), 'hex'), 'malicious', 'admitted', now(),
        '11111111-0000-0000-0000-000000000001')$$);

SELECT t_rejects('PRES-007',
    'a failed acquisition must explain itself',
    $$INSERT INTO acquisition_attempt (
        id, source_id, locator, attempted_at, outcome
      ) VALUES (
        '99999999-0000-0000-0000-000000000001',
        '22222222-0000-0000-0000-000000000001', 'https://example.invalid',
        now(), 'failure')$$);

SELECT t_rejects('DR-0061',
    'a metadata-only holding cannot claim to hold an original',
    $$INSERT INTO holding (
        id, completeness, retention_tier, access_tier, rights_permission
      ) VALUES (
        '44444444-0000-0000-0000-00000000000b', 'original', 'metadata-only',
        'public', 'may-preserve')$$);

-- ---------------------------------------------------------------------------
-- Bitemporality — "what did we hold at time T" (EVID-015, §63)
-- ---------------------------------------------------------------------------

SELECT t_true('EVID-015',
    'a superseded assertion is still visible as of its own record time',
    (SELECT count(*) FROM assertions_as_of(
        (SELECT asserted_at FROM documentary_assertion
          WHERE id = '66666666-0000-0000-0000-000000000001'))) >= 1);

SELECT t_true('EVID-015',
    'the superseding assertion replaces it as of now',
    NOT EXISTS (
        SELECT 1 FROM assertions_as_of(now())
         WHERE id = '66666666-0000-0000-0000-000000000001'));

-- ---------------------------------------------------------------------------
-- DR-0078 — enum types match the registry exactly
-- ---------------------------------------------------------------------------

SELECT t_true('DATA-008', 'likelihood bands match the registry',
    (SELECT array_agg(e.enumlabel::text ORDER BY e.enumlabel)
       FROM pg_enum e JOIN pg_type t ON t.oid = e.enumtypid
      WHERE t.typname = 'likelihood_bands')
    = ARRAY['almost-certain','almost-no-chance','likely','roughly-even-chance',
            'unlikely','very-likely','very-unlikely']);

SELECT t_rejects('DATA-008', 'a value absent from the registry cannot enter',
    $$SELECT 'probably-maybe'::likelihood_bands$$);
