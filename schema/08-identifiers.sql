-- ---------------------------------------------------------------------------
-- Public identifiers — SPEC-0007 (DR-0087…0091)
-- ---------------------------------------------------------------------------
--
-- Three things live here, and their separation is the design:
--
--   identifier_assignment      The assertion family SPEC-0001 §2.2 names and
--                              DR-0012 requires: an identifier is a
--                              provenance-bearing relationship, never a
--                              column. The project's own ARKs are assigned
--                              through it exactly like a Wikidata Q-id.
--   public_identifier          The register (DR-0089): one row per minted
--                              ARK, one current disposition, forward-only.
--   public_identifier_subject  Which internal object an ARK names. Kept in
--                              its own table so the register itself can sit
--                              at `public` tier while the mapping to
--                              internal UUIDs stays `internal` (SPEC-0007 §5).
--
-- Nothing in this file knows what a NAAN is worth or how a name is generated;
-- that is `identifiers/ark.py`. The database enforces the invariants that
-- would be catastrophic to get wrong: no identifier is deleted, none is
-- reissued, none moves backwards without a recorded basis, and a redirect
-- always lands.

-- ---------------------------------------------------------------------------
-- Citable classes (SPEC-0007 §3)
-- ---------------------------------------------------------------------------
--
-- Which tables may carry a public identifier. Seeded with the §15 classes
-- that exist; a class without a table is bound the day its table appears.
-- Internal-only tables are absent by design: a minting attempt against them
-- fails the foreign key.

CREATE TABLE citable_class (
    subject_table   text PRIMARY KEY,
    record_class    text NOT NULL,   -- the record §15 class it realises
    versioned       boolean NOT NULL DEFAULT false,  -- may take a .vN qualifier
    rationale       text NOT NULL
);

INSERT INTO citable_class VALUES
    ('world_actor',            'persons, organizations', false,
     'Historical actors (DR-0010).'),
    ('project_assertion',      'assertions',             false,
     'The project''s own findings and conclusions.'),
    ('documentary_assertion',  'assertions',             false,
     'What a source said, as recorded and located (DR-0024 layer 2).'),
    ('holding',                'source captures',        true,
     'A preserved holding; OCFL versions are its .vN states (DR-0090).'),
    ('published_page',         'published pages',        true,
     'A page; its revisions are its .vN states (DR-0090).');

COMMENT ON TABLE citable_class IS
    'Tables whose rows may carry a public identifier (SPEC-0007 §3). A '
    'documented contract, not data. Absent by design: every internal-only '
    'table; a minting attempt against one fails.';

-- ---------------------------------------------------------------------------
-- identifier_assignment — the assertion family (DR-0012, SPEC-0001 §2.2)
-- ---------------------------------------------------------------------------

CREATE TABLE identifier_assignment (
    -- ---- SPEC-0001 §2.1 core ----
    id                  uuid PRIMARY KEY,
    valid_time          timespan NOT NULL,
    asserted_at         timestamptz NOT NULL DEFAULT now(),
    asserter_id         uuid NOT NULL REFERENCES pipeline_agent(id),
    epistemic_category  epistemic_categories NOT NULL,
    likelihood          likelihood_bands,
    confidence          analytic_confidence,
    basis               jsonb,
    supersedes_id       uuid REFERENCES identifier_assignment(id),
    redacted_at         timestamptz,
    redaction_ground    text,
    redaction_authority text,
    -- ---- family payload ----
    subject_table       text NOT NULL REFERENCES citable_class(subject_table),
    subject_id          uuid NOT NULL,
    identifier_type     text NOT NULL REFERENCES identifier_types(id),
    value               text NOT NULL,

    CONSTRAINT valid_time_well_formed CHECK (timespan_ok(valid_time)),

    -- An identifier is a fact about who calls a thing what; it carries no
    -- likelihood of its own (DR-0026). Whether two identifiers name the same
    -- referent is a match assertion, not an identifier assignment (§16, §72).
    CONSTRAINT identifier_assignments_carry_no_band
        CHECK (likelihood IS NULL AND confidence IS NULL),

    CONSTRAINT tombstone_is_complete CHECK (
        num_nonnulls(redacted_at, redaction_ground, redaction_authority) IN (0, 3)
    )
);

SELECT make_append_only('identifier_assignment');

-- The project's own identifier is assigned once per object and never to two
-- objects. External identifiers carry no such constraint: the same registry
-- number may be claimed for several candidates until resolution (DR-0063).
CREATE UNIQUE INDEX one_ark_per_object
    ON identifier_assignment (subject_table, subject_id)
    WHERE identifier_type = 'uiw-ark' AND redacted_at IS NULL;
CREATE UNIQUE INDEX one_object_per_ark
    ON identifier_assignment (value)
    WHERE identifier_type = 'uiw-ark';

-- The subject must exist in the table the assignment names. A foreign key
-- cannot express "one of several tables", so a trigger checks it.
CREATE FUNCTION identifier_subject_exists() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE found boolean;
BEGIN
    EXECUTE format('SELECT EXISTS (SELECT 1 FROM %I WHERE id = $1)',
                   NEW.subject_table)
       INTO found USING NEW.subject_id;
    IF NOT found THEN
        RAISE EXCEPTION
            'identifier_assignment: no row % in % (SPEC-0007 §4.2)',
            NEW.subject_id, NEW.subject_table
            USING ERRCODE = 'foreign_key_violation';
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER identifier_assignment_subject_exists
    BEFORE INSERT ON identifier_assignment
    FOR EACH ROW EXECUTE FUNCTION identifier_subject_exists();

COMMENT ON TABLE identifier_assignment IS
    'Identifiers attach via assignment events with actor, time and basis '
    '(DR-0012, DATA-001, DATA-010). The project''s own ARKs use the same '
    'family (DR-0088): identifier_type = uiw-ark, asserter = the project.';

-- ---------------------------------------------------------------------------
-- Disambiguation records (DR-0089 §5; closes SPEC-0002 §6 Q3)
-- ---------------------------------------------------------------------------

CREATE TABLE disambiguation_record (
    id                uuid PRIMARY KEY,
    split_at          timestamptz NOT NULL,
    -- A snapshot of the deciding agent's public_title at the moment of the
    -- split, computed by the same statement that inserts this row from
    -- pipeline_agent — never a free-text value a caller supplies (DR-0092).
    -- Null when the agent has no public title: the split stays fully
    -- recorded (disambiguation_decision, below), and the public response
    -- says the deciding agent is recorded without naming or describing
    -- them. Fixed at insert: a title changed later does not rewrite what a
    -- past decision's byline said (append-only, DR-0055's discipline
    -- applied to a derived column).
    decided_by_title  text,
    grounds           text NOT NULL,
    CONSTRAINT grounds_are_stated CHECK (length(trim(grounds)) > 0)
);

COMMENT ON TABLE disambiguation_record IS
    'What a split identifier resolves to (DR-0064, DR-0089 §5): the split '
    'date, the successors (disambiguation_successor), the grounds, and a '
    'public byline if the deciding agent chose one (DR-0092) — nothing '
    'more. Public tier as a whole: no column here may ever be, or become, '
    'an internal reference. The deciding agent''s identity is recorded '
    'separately in disambiguation_decision (internal tier), precisely so '
    'that a raw agent id can never sit in a table a disclosure dump '
    'carries whole.';

-- Kept apart from disambiguation_record on purpose (DR-0092). A preservation
-- dump carries pipeline_agent (names included); a disclosure dump carries
-- disambiguation_record (decided_by_title included) but never this table.
-- Putting the raw agent id in disambiguation_record itself would let anyone
-- holding both dumps join them and identify an agent who chose to stay
-- unnamed — the one thing an opt-in byline is supposed to prevent.
CREATE TABLE disambiguation_decision (
    record_id   uuid PRIMARY KEY REFERENCES disambiguation_record(id),
    decided_by  uuid NOT NULL REFERENCES pipeline_agent(id)
);

COMMENT ON TABLE disambiguation_decision IS
    'Internal-tier link from a disambiguation record to the agent who '
    'decided it (DR-0089 §5). Exists so the decision is traceable for '
    'internal audit without the link ever reaching a public dump '
    '(DR-0092) — see disambiguation_record''s comment.';

-- Delete/update guards for this table are attached below, once
-- forbid_delete() and forbid_update() are defined (§ Invariants).

-- ---------------------------------------------------------------------------
-- The register (DR-0089)
-- ---------------------------------------------------------------------------

CREATE TABLE public_identifier (
    -- Normalised citation form: ark:/NAAN/name, no qualifier, no hyphens.
    ark                 text PRIMARY KEY,
    minted_at           timestamptz NOT NULL DEFAULT now(),
    assignment_id       uuid NOT NULL UNIQUE REFERENCES identifier_assignment(id),
    disposition         identifier_dispositions NOT NULL DEFAULT 'active',
    disposition_at      timestamptz NOT NULL DEFAULT now(),
    -- The merge/split event, redaction decision, or tier decision behind a
    -- non-active disposition. Required whenever the disposition is not
    -- `active` (DR-0089 invariant 3).
    disposition_basis   uuid,
    successor_ark       text REFERENCES public_identifier(ark),
    disambiguation_id   uuid REFERENCES disambiguation_record(id),

    CONSTRAINT ark_is_normalised CHECK (
        ark ~ '^ark:/[0-9bcdfghjkmnpqrstvwxz]{5}/[0-9bcdfghjkmnpqrstvwxz]+$'
    ),
    CONSTRAINT non_active_dispositions_carry_a_basis CHECK (
        disposition = 'active' OR disposition_basis IS NOT NULL
    ),
    CONSTRAINT redirect_has_a_successor CHECK (
        (disposition = 'redirect') = (successor_ark IS NOT NULL)
    ),
    CONSTRAINT redirect_is_not_to_self CHECK (successor_ark IS DISTINCT FROM ark),
    CONSTRAINT disambiguation_has_a_record CHECK (
        (disposition = 'disambiguation') = (disambiguation_id IS NOT NULL)
    )
);

CREATE TABLE public_identifier_subject (
    ark             text PRIMARY KEY REFERENCES public_identifier(ark),
    subject_table   text NOT NULL REFERENCES citable_class(subject_table),
    subject_id      uuid NOT NULL,
    UNIQUE (subject_table, subject_id)
);

CREATE TABLE disambiguation_successor (
    record_id       uuid NOT NULL REFERENCES disambiguation_record(id),
    successor_ark   text NOT NULL REFERENCES public_identifier(ark),
    PRIMARY KEY (record_id, successor_ark)
);

COMMENT ON TABLE public_identifier IS
    'The identifier register (DR-0089). One row per minted ARK; one current '
    'disposition; forward-only; never deleted. Public by construction: the '
    'existence and disposition of every identifier is public information.';
COMMENT ON TABLE public_identifier_subject IS
    'Which internal row an ARK names. Internal tier: internal UUIDs are never '
    'a public surface (SPEC-0007 §4.3).';

-- The subject recorded for an ARK must be the subject of its assignment.
CREATE FUNCTION public_identifier_subject_matches() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE a record;
BEGIN
    SELECT ia.subject_table, ia.subject_id, ia.value, ia.identifier_type
      INTO a
      FROM public_identifier p
      JOIN identifier_assignment ia ON ia.id = p.assignment_id
     WHERE p.ark = NEW.ark;
    IF a.identifier_type <> 'uiw-ark' OR a.value <> NEW.ark THEN
        RAISE EXCEPTION 'public_identifier %: its assignment is not a uiw-ark assignment of that value', NEW.ark;
    END IF;
    IF a.subject_table <> NEW.subject_table OR a.subject_id <> NEW.subject_id THEN
        RAISE EXCEPTION
            'public_identifier_subject %: subject differs from its assignment (%/% vs %/%)',
            NEW.ark, NEW.subject_table, NEW.subject_id, a.subject_table, a.subject_id;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER public_identifier_subject_matches
    BEFORE INSERT ON public_identifier_subject
    FOR EACH ROW EXECUTE FUNCTION public_identifier_subject_matches();

-- ---------------------------------------------------------------------------
-- Invariants 1, 2 and 4: never deleted, forward-only, redirects land
-- ---------------------------------------------------------------------------

CREATE FUNCTION forbid_delete() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION
        'DR-0089: % rows are never deleted; an identifier that was ever '
        'published resolves forever (DATA-009). Change its disposition.',
        TG_TABLE_NAME
        USING ERRCODE = 'restrict_violation';
END;
$$;

CREATE TRIGGER public_identifier_never_deleted
    BEFORE DELETE ON public_identifier
    FOR EACH ROW EXECUTE FUNCTION forbid_delete();
CREATE TRIGGER public_identifier_subject_never_deleted
    BEFORE DELETE ON public_identifier_subject
    FOR EACH ROW EXECUTE FUNCTION forbid_delete();
CREATE TRIGGER disambiguation_record_never_deleted
    BEFORE DELETE ON disambiguation_record
    FOR EACH ROW EXECUTE FUNCTION forbid_delete();
CREATE TRIGGER disambiguation_decision_never_deleted
    BEFORE DELETE ON disambiguation_decision
    FOR EACH ROW EXECUTE FUNCTION forbid_delete();

-- A disambiguation record, decided_by_title included, is fixed at the
-- moment of the split (DR-0092): it is never edited afterwards, the same
-- discipline DR-0055 applies to assertions. The same holds for the
-- internal decision link — a decider does not change after the fact.
CREATE FUNCTION forbid_update() RETURNS trigger
LANGUAGE plpgsql AS $$
BEGIN
    RAISE EXCEPTION
        'DR-0092: % rows are fixed at insert and never updated.',
        TG_TABLE_NAME
        USING ERRCODE = 'restrict_violation';
END;
$$;

CREATE TRIGGER disambiguation_record_never_updated
    BEFORE UPDATE ON disambiguation_record
    FOR EACH ROW EXECUTE FUNCTION forbid_update();
CREATE TRIGGER disambiguation_decision_never_updated
    BEFORE UPDATE ON disambiguation_decision
    FOR EACH ROW EXECUTE FUNCTION forbid_update();
CREATE TRIGGER disambiguation_successor_never_deleted
    BEFORE DELETE ON disambiguation_successor
    FOR EACH ROW EXECUTE FUNCTION forbid_delete();

-- Which moves are permitted (DR-0089 invariant 2):
--   active        -> redirect | disambiguation | tombstone | restricted
--   restricted    -> active (tier lowered) | redirect | disambiguation | tombstone
--   tombstone     -> active (redaction reversed under §77)
--   redirect, disambiguation: terminal
-- Every move needs a basis; the identity columns never change.
CREATE FUNCTION identifier_disposition_moves_forward() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE hops integer := 0; cursor_ark text;
BEGIN
    IF NEW.ark <> OLD.ark OR NEW.minted_at <> OLD.minted_at
       OR NEW.assignment_id <> OLD.assignment_id THEN
        RAISE EXCEPTION 'DR-0089: an identifier''s identity columns never change'
            USING ERRCODE = 'restrict_violation';
    END IF;
    IF NEW.disposition = OLD.disposition THEN
        RAISE EXCEPTION 'DR-0089: a disposition changes or the row is left alone'
            USING ERRCODE = 'restrict_violation';
    END IF;
    IF OLD.disposition IN ('redirect', 'disambiguation') THEN
        RAISE EXCEPTION 'DR-0089: % is terminal for %', OLD.disposition, OLD.ark
            USING ERRCODE = 'restrict_violation';
    END IF;
    IF OLD.disposition = 'tombstone' AND NEW.disposition <> 'active' THEN
        RAISE EXCEPTION 'DR-0089: a tombstone returns only to active, by a recorded reversal (§77)'
            USING ERRCODE = 'restrict_violation';
    END IF;
    IF NEW.disposition_basis IS NULL THEN
        RAISE EXCEPTION 'DR-0089: every disposition change records its basis'
            USING ERRCODE = 'restrict_violation';
    END IF;
    IF NEW.disposition_at < OLD.disposition_at THEN
        RAISE EXCEPTION 'DR-0089: dispositions move forward in time'
            USING ERRCODE = 'restrict_violation';
    END IF;

    -- A redirect chain must end. Follow successors from the new target; if
    -- the walk comes back to this row, the chain is a cycle.
    IF NEW.disposition = 'redirect' THEN
        cursor_ark := NEW.successor_ark;
        WHILE cursor_ark IS NOT NULL LOOP
            IF cursor_ark = NEW.ark THEN
                RAISE EXCEPTION 'DR-0089: redirect cycle through %', NEW.ark
                    USING ERRCODE = 'restrict_violation';
            END IF;
            hops := hops + 1;
            IF hops > 64 THEN
                RAISE EXCEPTION 'DR-0089: redirect chain from % exceeds 64 hops', NEW.ark
                    USING ERRCODE = 'restrict_violation';
            END IF;
            SELECT successor_ark INTO cursor_ark
              FROM public_identifier WHERE ark = cursor_ark;
        END LOOP;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER public_identifier_moves_forward
    BEFORE UPDATE ON public_identifier
    FOR EACH ROW EXECUTE FUNCTION identifier_disposition_moves_forward();

-- The subject mapping is fixed at minting.
CREATE TRIGGER public_identifier_subject_fixed
    BEFORE UPDATE ON public_identifier_subject
    FOR EACH ROW EXECUTE FUNCTION forbid_delete();

-- ---------------------------------------------------------------------------
-- Resolution in SQL (SPEC-0007 §6.1)
-- ---------------------------------------------------------------------------
--
-- The resolver service is a thin layer over this function, so that the
-- answer to "what does this identifier resolve to" is in the archive, not
-- in application code that may not survive (PRES-009).

CREATE TYPE identifier_resolution AS (
    ark                 text,
    disposition         identifier_dispositions,
    terminal_ark        text,       -- after following redirects
    hops                integer,
    disambiguation_id   uuid,
    disposition_basis   uuid,
    minted_at           timestamptz,
    disposition_at      timestamptz
);

CREATE FUNCTION resolve_identifier(query_ark text)
RETURNS identifier_resolution LANGUAGE plpgsql STABLE AS $$
DECLARE r public_identifier%ROWTYPE; out identifier_resolution; hops integer := 0;
BEGIN
    SELECT * INTO r FROM public_identifier WHERE ark = query_ark;
    IF NOT FOUND THEN
        RETURN NULL;              -- never minted: the one case that is a 404
    END IF;
    out.ark := r.ark; out.disposition := r.disposition;
    out.disambiguation_id := r.disambiguation_id;
    out.disposition_basis := r.disposition_basis;
    out.minted_at := r.minted_at; out.disposition_at := r.disposition_at;
    out.terminal_ark := r.ark;
    WHILE r.disposition = 'redirect' AND hops <= 64 LOOP
        hops := hops + 1;
        SELECT * INTO r FROM public_identifier WHERE ark = r.successor_ark;
        out.terminal_ark := r.ark;
    END LOOP;
    out.hops := hops;
    RETURN out;
END;
$$;

COMMENT ON FUNCTION resolve_identifier(text) IS
    'DATA-009: returns a row for every identifier ever minted, following '
    'redirects to their terminal identifier. NULL only for a name that was '
    'never issued.';

-- Every minted identifier resolves. The test suite asserts this over the
-- whole register; the view makes the check one query.
CREATE VIEW identifier_register_health AS
    SELECT p.ark, p.disposition,
           (resolve_identifier(p.ark)).terminal_ark AS terminal_ark,
           s.subject_table, s.subject_id
      FROM public_identifier p
      LEFT JOIN public_identifier_subject s ON s.ark = p.ark;
