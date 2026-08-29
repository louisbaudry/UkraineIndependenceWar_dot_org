-- Canonical store: Gate 3, the publication decision.
--
-- SPEC-0003 §2 (DR-0066): does accepted knowledge, or a preserved item,
-- appear on a public surface, and at which access tier (§12)? Preservation
-- status and access status remain independent (Principle 11).
--
-- The website is a projection (Principle 18). Nothing here is the archive;
-- it is the record of what the project said in public, when, in what
-- language, and on what evidence and methodology — which is the second half
-- of §86's question and the reason this layer exists at all.
--
-- Rules enforced here rather than left to discipline:
--
--   OPS-001   No path from Gate 1 to a public surface without recorded Gate 2
--             and Gate 3 decisions.
--   SEC-003   No universal is_public flag. Four independent dimensions.
--   SEC-004   A page cannot render material classified above its own tier.
--   §86       A revision pins its baseline, methodology, terminology and
--             template versions, so it is reproducible.
--   §90       Revision history from the first publication (DR-0052).
--   METH §10.1 A consequential conclusion published without the review its
--             tier requires carries the qualification, visibly.
--   §62       A project conclusion never renders as a legal finding.
--
-- Depends on 01-enums-generated.sql … 06-argument.sql.

-- ---------------------------------------------------------------------------
-- The decision
-- ---------------------------------------------------------------------------
--
-- Gate 3 is a distinct act from Gate 2. Accepting something as true and
-- deciding to say it in public are different decisions with different
-- consequences, and collapsing them is how archives end up publishing what
-- they merely believe.

CREATE TABLE publication_decision (
    id              uuid PRIMARY KEY,
    -- Exactly one subject: a conclusion the project holds, or a preserved
    -- holding shown as source material.
    assertion_id    uuid REFERENCES project_assertion(id),
    holding_id      uuid REFERENCES holding(id),
    decided_by      uuid NOT NULL REFERENCES pipeline_agent(id),
    decided_at      timestamptz NOT NULL DEFAULT now(),
    -- The four §12 dimensions, kept apart. SEC-003 forbids collapsing them
    -- into one flag: a thing can be publishable, sensitive, rights-restricted
    -- and evidentially undisclosable in any combination.
    access_tier     access_tiers NOT NULL,
    sensitivity     text,
    rights_basis    text NOT NULL,
    evidentiary_disclosure text,
    -- Why. A publication decision without a reason cannot be reviewed, and
    -- reversing it later needs to know what it rested on.
    rationale       text NOT NULL,
    -- A decision may be withdrawn. The row stays: §77 forbids silently
    -- unpublishing, and "we published this and later withdrew it" is part of
    -- the record.
    withdrawn_at    timestamptz,
    withdrawal_ground text,

    CONSTRAINT decisions_have_one_subject CHECK (
        num_nonnulls(assertion_id, holding_id) = 1
    ),
    CONSTRAINT withdrawal_is_complete CHECK (
        num_nonnulls(withdrawn_at, withdrawal_ground) IN (0, 2)
    )
);

-- Only a person publishes (§79). The same rule as Gate 2, for the same
-- reason, at the point where the consequences leave the building.
CREATE FUNCTION publication_is_decided_by_a_person() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE agent_kind text; gate2_state text;
BEGIN
    SELECT kind INTO agent_kind FROM pipeline_agent WHERE id = NEW.decided_by;
    IF agent_kind <> 'person' THEN
        RAISE EXCEPTION
            'Gate 3 requires a person (§79): agent kind was %', agent_kind;
    END IF;

    -- OPS-001, made structural: an assertion adopted from a proposal reaches
    -- the public surface only if that proposal was confirmed at Gate 2. Gate
    -- 2's own trigger already refuses the assertion, so this is belt and
    -- braces — but it is the check that would catch a row inserted around
    -- the Gate 2 path by a migration or an import.
    IF NEW.assertion_id IS NOT NULL THEN
        SELECT a.disposition::text INTO gate2_state
          FROM project_assertion pa
          LEFT JOIN acceptance a ON a.proposal_id = pa.adopted_from_id
         WHERE pa.id = NEW.assertion_id
           AND pa.adopted_from_id IS NOT NULL
         LIMIT 1;
        IF FOUND AND gate2_state IS DISTINCT FROM 'confirmed' THEN
            RAISE EXCEPTION
                'assertion % was adopted from a proposal with no confirming '
                'Gate 2 acceptance; no path runs from Gate 1 to a public '
                'surface without both gates (OPS-001)', NEW.assertion_id;
        END IF;
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER publication_person_check
    BEFORE INSERT ON publication_decision
    FOR EACH ROW EXECUTE FUNCTION publication_is_decided_by_a_person();

COMMENT ON TABLE publication_decision IS
    'Gate 3 (DR-0066). Distinct from Gate 2: accepting something as true and '
    'deciding to say it in public are different decisions. A withdrawn '
    'decision keeps its row — §77 forbids silent unpublishing.';

-- ---------------------------------------------------------------------------
-- Pages and their revisions — §90, DR-0052, OPS-004
-- ---------------------------------------------------------------------------
--
-- Revision history from the first publication, because the beginning is the
-- only moment history can start from the beginning (DR-0052).

CREATE TABLE published_page (
    id              uuid PRIMARY KEY,
    -- Stable path. The identifier a citation points at, so it outlives any
    -- particular rendering.
    path            text NOT NULL UNIQUE,
    -- BCP 47. A page is in one language; translations are separate pages
    -- linked by `translation_of` (I18N-001: translations are derived
    -- expressions, never overwriting the original).
    language        text NOT NULL,
    translation_of  uuid REFERENCES published_page(id),
    first_published timestamptz NOT NULL DEFAULT now(),

    CONSTRAINT a_page_is_not_its_own_translation
        CHECK (translation_of IS NULL OR translation_of <> id)
);

CREATE TYPE revision_kind AS ENUM (
    'initial',
    'update',        -- ordinary revision, no prior statement withdrawn
    'correction',    -- a prior statement was wrong and is corrected (§77)
    'retraction'     -- a prior conclusion is withdrawn (§77)
);

CREATE TABLE page_revision (
    id              uuid PRIMARY KEY,
    page_id         uuid NOT NULL REFERENCES published_page(id),
    revision        integer NOT NULL,
    kind            revision_kind NOT NULL,
    published_at    timestamptz NOT NULL DEFAULT now(),
    published_by    uuid NOT NULL REFERENCES pipeline_agent(id),

    -- §86: the exact rendered text. This is deliberately a display string in
    -- a store that otherwise holds identifiers (§61, I18N-003) — because the
    -- question is not "what does the project mean" but "what did the project
    -- actually say on the page". Canonical semantics live in the assertion
    -- layer; this is the artifact.
    rendered_text   text NOT NULL,
    text_digest     text NOT NULL,

    -- §86's reproducibility set. Without these a published statement cannot
    -- be reconstructed, which is the failure Principle 16 names.
    release_baseline text,
    methodology_version text NOT NULL,
    terminology_version text NOT NULL,
    template_version text NOT NULL,

    -- METH-0001 §10.1 (DR-0085 Q4): the qualification a reader must see.
    -- Null is legitimate only where nothing consequential is rendered; the
    -- trigger below decides, not the author.
    review_qualification text,

    -- Corrections and retractions say what they change and why (§77).
    supersedes_id   uuid REFERENCES page_revision(id),
    change_note     text,

    UNIQUE (page_id, revision),

    CONSTRAINT revisions_are_positive CHECK (revision >= 1),
    CONSTRAINT first_revision_is_initial
        CHECK ((revision = 1) = (kind = 'initial')),
    -- A correction or retraction that does not say what changed is not one
    -- (§77: being wrong and correcting the record leaves a trace).
    CONSTRAINT corrections_explain_themselves CHECK (
        kind NOT IN ('correction', 'retraction')
        OR (change_note IS NOT NULL AND supersedes_id IS NOT NULL)
    )
);

SELECT make_append_only('page_revision');

COMMENT ON TABLE page_revision IS
    'What the site said, when (§90). Carries the exact rendered text and the '
    'versions needed to reproduce it (§86) — the website is a projection '
    '(Principle 18), and this is its history, never the archive itself.';

-- Which assertions a revision rendered: §86''s "underlying dataset/
-- assertions", and the join SEC-004''s tier check runs over.
CREATE TABLE revision_assertion (
    revision_id     uuid NOT NULL REFERENCES page_revision(id),
    assertion_id    uuid NOT NULL REFERENCES project_assertion(id),
    PRIMARY KEY (revision_id, assertion_id)
);

-- Preserved material shown as source alongside a conclusion.
CREATE TABLE revision_holding (
    revision_id     uuid NOT NULL REFERENCES page_revision(id),
    holding_id      uuid NOT NULL REFERENCES holding(id),
    PRIMARY KEY (revision_id, holding_id)
);

-- ---------------------------------------------------------------------------
-- The tier check — SEC-004
-- ---------------------------------------------------------------------------
--
-- A page renders nothing classified above its own tier. Deferred, so a
-- revision and its contents arrive together.
--
-- Tier containment is declared, not computed from the enum's order: the
-- restricted tiers are lateral grants to named parties, not steps on a
-- ladder. This mirrors export/tiers.py, and the two are checked against each
-- other by the test suite rather than trusted to stay aligned by habit.

CREATE FUNCTION tier_admits(page_tier access_tiers, item_tier access_tiers)
RETURNS boolean LANGUAGE sql IMMUTABLE AS $$
    SELECT CASE page_tier
        WHEN 'public'       THEN item_tier = 'public'
        WHEN 'subscriber'   THEN item_tier IN ('public', 'subscriber')
        WHEN 'internal'     THEN item_tier IN ('public', 'subscriber', 'internal')
        WHEN 'researcher-restricted'
            THEN item_tier IN ('public', 'subscriber', 'researcher-restricted')
        WHEN 'investigator-restricted'
            THEN item_tier IN ('public', 'subscriber', 'investigator-restricted')
        -- `confidential` and `private-preservation` are not publication
        -- targets at all. A surface never carries them (SEC-001, §12).
        ELSE false
    END;
$$;

CREATE FUNCTION revision_respects_tiers() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE leak record; page_tier access_tiers; rev uuid; live integer;
BEGIN
    rev := NEW.revision_id;

    -- "No decision at all" is checked separately from tier resolution.
    -- most_restrictive_tier() fails closed on an empty set — it returns
    -- `confidential` rather than NULL — so an absent decision would
    -- otherwise look like a very restrictive one, and a revision rendering
    -- no holdings would slip through. The distinction matters: unclassified
    -- is not the same as restricted (DR-0029's rule applied to tiers).
    SELECT count(*) INTO live
      FROM revision_assertion ra
      JOIN publication_decision pd ON pd.assertion_id = ra.assertion_id
                                  AND pd.withdrawn_at IS NULL
     WHERE ra.revision_id = rev;

    IF live = 0 THEN
        RAISE EXCEPTION
            'revision % renders content with no live publication decision; '
            'nothing reaches a surface without Gate 3 (OPS-001)', rev;
    END IF;

    -- The page is only as open as its most restricted live decision permits.
    SELECT most_restrictive_tier(
               array_remove(array_agg(pd.access_tier), NULL)) INTO page_tier
      FROM revision_assertion ra
      JOIN publication_decision pd ON pd.assertion_id = ra.assertion_id
                                  AND pd.withdrawn_at IS NULL
     WHERE ra.revision_id = rev;

    -- Every holding shown must be admitted by that tier (SEC-004).
    SELECT h.id, h.access_tier INTO leak
      FROM revision_holding rh
      JOIN holding h ON h.id = rh.holding_id
     WHERE rh.revision_id = rev
       AND NOT tier_admits(page_tier, h.access_tier)
     LIMIT 1;

    IF FOUND THEN
        RAISE EXCEPTION
            'holding % is classified % and cannot appear on a % surface; a '
            'tier leak in any layer blocks release (SEC-004)',
            leak.id, leak.access_tier, page_tier;
    END IF;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER revision_assertion_tier_check
    AFTER INSERT ON revision_assertion
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION revision_respects_tiers();

CREATE CONSTRAINT TRIGGER revision_holding_tier_check
    AFTER INSERT ON revision_holding
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION revision_respects_tiers();

-- ---------------------------------------------------------------------------
-- The review qualification — METH-0001 §10.1, ruled by DR-0085 Q4
-- ---------------------------------------------------------------------------
--
-- The ruling put the qualification on the published surface, not in an
-- internal note: the reader relying on the conclusion was the one person the
-- drafted version left untold. This is where that becomes structural.

CREATE FUNCTION revision_carries_review_qualification() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE needed text; rev uuid;
BEGIN
    rev := NEW.revision_id;

    -- The strongest qualification any rendered conclusion requires. Ordering
    -- puts `unreviewed` first, so the page speaks to its weakest link.
    SELECT pc.review_qualification INTO needed
      FROM revision_assertion ra
      JOIN publishable_conclusion pc ON pc.id = ra.assertion_id
     WHERE ra.revision_id = rev
       AND pc.consequence_limb IS NOT NULL
       AND pc.review_qualification IS NOT NULL
     ORDER BY pc.review_state
     LIMIT 1;

    IF needed IS NULL THEN
        RETURN NULL;             -- nothing consequential rendered
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM page_revision
         WHERE id = rev AND review_qualification IS NOT NULL
           AND review_qualification <> ''
    ) THEN
        RAISE EXCEPTION
            'revision % renders a consequential conclusion but carries no '
            'review qualification. It requires: %  (METH-0001 §10.1, '
            'DR-0085 Q4)', rev, needed;
    END IF;
    RETURN NULL;
END;
$$;

CREATE CONSTRAINT TRIGGER revision_qualification_check
    AFTER INSERT ON revision_assertion
    DEFERRABLE INITIALLY DEFERRED
    FOR EACH ROW EXECUTE FUNCTION revision_carries_review_qualification();

-- ---------------------------------------------------------------------------
-- §62: a project conclusion never renders as a legal finding
-- ---------------------------------------------------------------------------
--
-- "Not proven guilty" is not "historically established not to have done it",
-- and a project conclusion is neither. The check is deliberately crude — a
-- word list cannot police prose — so it catches the specific formulations
-- that assert judicial status, and review catches the rest.

CREATE FUNCTION revision_does_not_claim_legal_findings() RETURNS trigger
LANGUAGE plpgsql AS $$
DECLARE offending text;
BEGIN
    SELECT phrase INTO offending
      FROM unnest(ARRAY[
            'is guilty of', 'found guilty', 'convicted of',
            'is criminally liable', 'constitutes a war crime',
            'is legally responsible'
      ]) AS phrase
     WHERE NEW.rendered_text ILIKE '%' || phrase || '%'
     LIMIT 1;

    IF FOUND THEN
        RAISE EXCEPTION
            'rendered text contains %, which asserts a legal finding. The '
            'project does not reach them; it may record and assess what '
            'competent authorities have found, always qualified as theirs '
            '(§62, METH-0001 §12)', quote_literal(offending);
    END IF;
    RETURN NEW;
END;
$$;

CREATE TRIGGER revision_legal_finding_check
    BEFORE INSERT ON page_revision
    FOR EACH ROW EXECUTE FUNCTION revision_does_not_claim_legal_findings();

-- ---------------------------------------------------------------------------
-- What the site said on date D — §86, §90
-- ---------------------------------------------------------------------------

CREATE FUNCTION site_as_of(record_time timestamptz)
RETURNS TABLE (
    path text, language text, revision integer, kind revision_kind,
    published_at timestamptz, text_digest text,
    methodology_version text, terminology_version text,
    release_baseline text, review_qualification text
)
LANGUAGE sql STABLE AS $$
    SELECT DISTINCT ON (p.path)
           p.path, p.language, r.revision, r.kind, r.published_at,
           r.text_digest, r.methodology_version, r.terminology_version,
           r.release_baseline, r.review_qualification
      FROM published_page p
      JOIN page_revision r ON r.page_id = p.id
     WHERE r.published_at <= record_time
     ORDER BY p.path, r.revision DESC;
$$;

COMMENT ON FUNCTION site_as_of IS
    'What exactly did we publicly say, in which language, on date Z, and on '
    'what methodology (§86). Answerable from the first page (DR-0052).';

-- Every page's full history, corrections and retractions included (§77).
CREATE VIEW page_history AS
    SELECT p.path, p.language, r.revision, r.kind, r.published_at,
           r.change_note, r.text_digest, r.review_qualification
      FROM published_page p
      JOIN page_revision r ON r.page_id = p.id
     ORDER BY p.path, r.revision;

-- Conclusions that reached a public surface, with what a reader was told.
-- The join a §86 audit starts from.
CREATE VIEW published_conclusion AS
    SELECT pa.id AS assertion_id,
           pa.proposition_id,
           pa.consequence_limb,
           pd.access_tier,
           pd.withdrawn_at,
           p.path,
           r.revision,
           r.published_at,
           r.review_qualification,
           r.methodology_version
      FROM project_assertion pa
      JOIN publication_decision pd ON pd.assertion_id = pa.id
      JOIN revision_assertion ra ON ra.assertion_id = pa.id
      JOIN page_revision r ON r.id = ra.revision_id
      JOIN published_page p ON p.id = r.page_id;
