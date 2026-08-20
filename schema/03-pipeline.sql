-- Canonical store: the pipeline layer.
--
-- Sources, captures, preserved objects, preservation events and holdings —
-- what a first collector needs. Implements SPEC-0003 (three-gate pipeline),
-- DR-0060 (PREMIS subset), DR-0061 (the holding), DR-0067 (source registry),
-- DR-0068 (retention tiers), DR-0070 (collector runs), DR-0075 (digests).
--
-- Depends on 01-enums-generated.sql and 02-core.sql.

-- ---------------------------------------------------------------------------
-- Source registry (DR-0067)
-- ---------------------------------------------------------------------------

CREATE TABLE source (
    id                      uuid PRIMARY KEY,
    source_type             text NOT NULL REFERENCES source_types(id),
    name                    text NOT NULL,
    locator                 text,          -- URL, handle, feed
    publisher               text,
    jurisdiction            text,
    primary_languages       text[],
    coverage_start          date,

    -- Collection policy
    collection_method       text NOT NULL,
    collection_cadence      text,
    scope_rules             text,
    exclusions              text,

    -- Preservation policy (DR-0006, DR-0068)
    capture_format          text NOT NULL DEFAULT 'http',
    default_retention_tier  retention_tiers NOT NULL,

    -- Access and rights defaults. Four independent dimensions (§12): tier,
    -- sensitivity, rights, evidentiary disclosure — never one flag (SEC-003).
    default_access_tier     access_tiers NOT NULL,
    default_sensitivity     text,
    expects_graphic_content boolean NOT NULL DEFAULT false,
    rights_permission       rights_permissions NOT NULL,
    rights_basis            text,

    -- Triage only. Barred from determining truth (DR-0027, EVID-008).
    grade_source_reliability source_grades_source_reliability,
    grade_item_credibility   source_grades_item_credibility,

    lifecycle_state         text NOT NULL DEFAULT 'active'
        CHECK (lifecycle_state IN ('active', 'paused', 'retired')),
    lifecycle_reason        text,
    created_at              timestamptz NOT NULL DEFAULT now(),

    -- WARC capture is the high-value tier (DR-0006); a source expecting
    -- graphic content must not default to public (PRES-012, POL-0001 §5.9).
    CONSTRAINT graphic_sources_not_public_by_default
        CHECK (NOT expects_graphic_content OR default_access_tier <> 'public')
);

COMMENT ON COLUMN source.grade_source_reliability IS
    'Admiralty-style triage grade. DR-0027 bars it from propagating into any '
    'proposition''s truth status, likelihood or confidence. No query computing '
    'an assessment may read this column.';

-- Declared dependence between sources (DR-0028, DR-0067). Stating known
-- republishing once, rather than rediscovering it per item: five publications
-- repeating one report are not five independent confirmations (§36).
CREATE TABLE source_dependence (
    id              uuid PRIMARY KEY,
    dependent_id    uuid NOT NULL REFERENCES source(id),
    depends_on_id   uuid NOT NULL REFERENCES source(id),
    relation        dependence_relation_types NOT NULL,
    note            text,
    asserted_at     timestamptz NOT NULL DEFAULT now(),
    asserter_id     uuid NOT NULL REFERENCES pipeline_agent(id),
    CONSTRAINT no_self_dependence CHECK (dependent_id <> depends_on_id)
);

-- ---------------------------------------------------------------------------
-- Collector runs (DR-0070)
-- ---------------------------------------------------------------------------
--
-- The unit of coverage accounting. Per-item records cannot express "the
-- collector was down for six days" — an absence with no items to attach to.

CREATE TABLE collector_run (
    id                  uuid PRIMARY KEY,
    source_id           uuid NOT NULL REFERENCES source(id),
    collector_agent_id  uuid NOT NULL REFERENCES pipeline_agent(id),
    configuration       jsonb NOT NULL,
    started_at          timestamptz NOT NULL,
    ended_at            timestamptz,
    items_discovered    integer NOT NULL DEFAULT 0,
    items_acquired      integer NOT NULL DEFAULT 0,
    items_skipped       integer NOT NULL DEFAULT 0,
    items_failed        integer NOT NULL DEFAULT 0,
    bytes_preserved     bigint NOT NULL DEFAULT 0,
    skip_reasons        jsonb,
    failure_details     jsonb,
    outage_note         text,   -- §57: recorded so absence is never mistaken
                                -- for absence in the world
    CONSTRAINT counts_are_not_negative CHECK (
        items_discovered >= 0 AND items_acquired >= 0
        AND items_skipped >= 0 AND items_failed >= 0 AND bytes_preserved >= 0
    )
);

-- ---------------------------------------------------------------------------
-- Acquisition and Gate 1 (DR-0066, DR-0069)
-- ---------------------------------------------------------------------------
--
-- Every acquisition attempt is recorded, including failures — a failed
-- acquisition can itself be historically significant (§28, PRES-007).

CREATE TABLE acquisition_attempt (
    id              uuid PRIMARY KEY,
    source_id       uuid NOT NULL REFERENCES source(id),
    collector_run_id uuid REFERENCES collector_run(id),
    locator         text NOT NULL,
    attempted_at    timestamptz NOT NULL,
    outcome         text NOT NULL
        CHECK (outcome IN ('success', 'failure', 'refused', 'not-found')),
    error_detail    text,
    retry_of_id     uuid REFERENCES acquisition_attempt(id),
    -- Set when the loss is established as permanent rather than pending retry.
    permanent_loss  boolean NOT NULL DEFAULT false,
    historically_significant boolean NOT NULL DEFAULT false,
    CONSTRAINT failures_explain_themselves
        CHECK (outcome = 'success' OR error_detail IS NOT NULL)
);

COMMENT ON TABLE acquisition_attempt IS
    'Every attempt, not merely every success (§28). Retries, later successes '
    'and permanent losses are all recorded; significant failures are preserved '
    'permanently (PRES-007).';

-- Material held before Gate 1. Explicitly NOT part of the archive: archive
-- integrity guarantees are never claimed for unvetted material (DR-0069).
CREATE TABLE quarantine_item (
    id                  uuid PRIMARY KEY,
    acquisition_attempt_id uuid REFERENCES acquisition_attempt(id),
    submitted_by_pseudonym text,   -- confidential identity lives elsewhere
                                   -- (SEC-001, DR-0059)
    submitter_claims    text,      -- kept separate from project conclusions (§11)
    received_at         timestamptz NOT NULL,
    byte_size           bigint NOT NULL,
    sha256              bytea NOT NULL,
    security_check_at   timestamptz,
    security_check_outcome text
        CHECK (security_check_outcome IN ('clean', 'malicious', 'unreadable', 'inconclusive')),
    gate1_decision      text
        CHECK (gate1_decision IN ('admitted', 'rejected')),
    gate1_decided_at    timestamptz,
    gate1_decided_by    uuid REFERENCES pipeline_agent(id),
    gate1_rationale     text,
    CONSTRAINT admission_requires_a_clean_check CHECK (
        gate1_decision IS DISTINCT FROM 'admitted'
        OR security_check_outcome = 'clean'
    ),
    CONSTRAINT decisions_are_attributed CHECK (
        gate1_decision IS NULL
        OR (gate1_decided_at IS NOT NULL AND gate1_decided_by IS NOT NULL)
    )
);

COMMENT ON TABLE quarantine_item IS
    'Pre-archival zone (DR-0069). Not an archival holding: carries no §26 '
    'completeness claim until it passes Gate 1.';

-- ---------------------------------------------------------------------------
-- Preserved objects (DR-0060, DR-0075)
-- ---------------------------------------------------------------------------

CREATE TABLE preserved_object (
    id                  uuid PRIMARY KEY,
    object_level        text NOT NULL CHECK (object_level IN ('representation', 'file')),
    parent_id           uuid REFERENCES preserved_object(id),  -- file -> representation
    original_name       text,
    format_identifier   text,
    byte_size           bigint,

    -- DR-0075: SHA-512 addresses content in OCFL; SHA-256 satisfies DR-0005
    -- and preserves continuity. Two algorithms disagreeing is itself a signal.
    sha512              bytea NOT NULL,
    sha256              bytea NOT NULL,

    -- OCFL placement (DR-0073, DR-0074, DR-0076)
    ocfl_root           text NOT NULL CHECK (ocfl_root IN ('permanent', 'medium-term')),
    ocfl_object_id      text NOT NULL,
    ocfl_version        text NOT NULL,

    ingested_at         timestamptz NOT NULL,
    CONSTRAINT files_have_a_parent_representation CHECK (
        object_level <> 'file' OR parent_id IS NOT NULL
    ),
    CONSTRAINT digests_are_the_right_length CHECK (
        length(sha512) = 64 AND length(sha256) = 32
    )
);

-- Preservation events (DR-0060). Outcomes include failure: a fixity failure
-- is a recorded event, never a silent re-copy.
CREATE TABLE preservation_event (
    id              uuid PRIMARY KEY,
    event_type      premis_event_types NOT NULL,
    object_id       uuid REFERENCES preserved_object(id),
    quarantine_item_id uuid REFERENCES quarantine_item(id),
    agent_id        uuid NOT NULL REFERENCES pipeline_agent(id),
    occurred_at     timestamptz NOT NULL,
    outcome         text NOT NULL CHECK (outcome IN ('success', 'failure')),
    outcome_detail  text,
    CONSTRAINT failures_explain_themselves
        CHECK (outcome = 'success' OR outcome_detail IS NOT NULL),
    CONSTRAINT events_have_a_subject CHECK (
        (object_id IS NOT NULL) <> (quarantine_item_id IS NOT NULL)
    )
);

-- ---------------------------------------------------------------------------
-- Holdings (DR-0061, DR-0074)
-- ---------------------------------------------------------------------------
--
-- What the archive possesses of one documentary item: the bridge between
-- documentary identity (an LRMoo Item) and preserved bytes (PREMIS
-- representations), carrying the §26 completeness statement.
--
-- An OCFL object corresponds to a holding (DR-0074).

CREATE TABLE holding (
    id                  uuid PRIMARY KEY,
    -- item_id will reference the documentary layer's LRMoo Item once that
    -- layer lands; left as an opaque identifier so the pipeline layer can be
    -- used before the documentary layer exists.
    item_id             uuid,
    completeness        completeness_states NOT NULL,
    retention_tier      retention_tiers NOT NULL,
    access_tier         access_tiers NOT NULL,
    rights_permission   rights_permissions NOT NULL,

    -- §26: external custodians' copies are holdings with a non-project
    -- custodian and no preserved representation of their own.
    custodian           text NOT NULL DEFAULT 'project',
    ocfl_object_id      text,
    created_at          timestamptz NOT NULL DEFAULT now(),

    CONSTRAINT project_holdings_have_storage CHECK (
        custodian <> 'project'
        OR retention_tier IN ('discard', 'metadata-only')
        OR ocfl_object_id IS NOT NULL
    ),
    CONSTRAINT external_holdings_have_no_storage CHECK (
        custodian = 'project' OR ocfl_object_id IS NULL
    ),
    -- Metadata-only holdings hold no bytes, so they cannot claim to be an
    -- original or an archival copy (§26, DR-0068).
    CONSTRAINT metadata_only_holds_nothing CHECK (
        retention_tier <> 'metadata-only' OR completeness = 'metadata-only'
    )
);

CREATE TABLE holding_representation (
    holding_id  uuid NOT NULL REFERENCES holding(id),
    object_id   uuid NOT NULL REFERENCES preserved_object(id),
    role        text NOT NULL CHECK (role IN ('original', 'derivative')),
    PRIMARY KEY (holding_id, object_id)
);

-- Exactly one original per holding: the acquired object. Derivatives are
-- later OCFL versions of the same object (DR-0074).
CREATE UNIQUE INDEX one_original_per_holding
    ON holding_representation (holding_id) WHERE role = 'original';

-- Capture series: successive captures of one locator are *different*
-- holdings, related here rather than buried in OCFL version history
-- (DR-0074, Memento pattern per DR-0023).
CREATE TABLE capture_series_member (
    series_id   uuid NOT NULL,
    holding_id  uuid NOT NULL REFERENCES holding(id),
    locator     text NOT NULL,
    captured_at timestamptz NOT NULL,
    PRIMARY KEY (series_id, holding_id)
);

CREATE INDEX capture_series_by_time ON capture_series_member (series_id, captured_at);
