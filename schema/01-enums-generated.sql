-- Registry-derived types for the canonical store.
--
-- GENERATED FILE — do not edit. Regenerate with schema/gen_enums.py.
-- Source of truth: registry/*.yaml (DR-0078), compiled per SPEC-0005.
--
-- This file is where DR-0078's enforcement surface becomes enforcement: a
-- value absent from the registry cannot enter the canonical store.
--
-- Registry: uiw-semantic-registry version 0.1.0 (effective)
--
-- Closed vocabularies (DR-0080) become enum types: changing them requires a
-- Decision Record, and a migration is the appropriate cost of that.
-- Open vocabularies become seeded lookup tables so that additions by
-- registry process do not require schema migrations.


-- Closed vocabularies -> enum types

-- absence-states (authorised by DR-0029)
CREATE TYPE absence_states AS ENUM (
    'indeterminate',
    'lost-or-destroyed',
    'no-evidence-found',
    'not-applicable',
    'not-researched',
    'redacted',
    'unavailable',
    'unknown',
    'withheld'
);

-- access-tiers (authorised by DR-0067, DR-0072)
CREATE TYPE access_tiers AS ENUM (
    'confidential',
    'internal',
    'investigator-restricted',
    'private-preservation',
    'public',
    'researcher-restricted',
    'subscriber'
);

-- analytic-confidence (authorised by DR-0026)
CREATE TYPE analytic_confidence AS ENUM (
    'high',
    'low',
    'moderate'
);

-- completeness-states (authorised by DR-0061)
CREATE TYPE completeness_states AS ENUM (
    'archival-copy',
    'derivative',
    'fragment',
    'metadata-only',
    'original',
    'screenshot',
    'transcript'
);

-- defeater-types (authorised by DR-0033)
CREATE TYPE defeater_types AS ENUM (
    'rebutting',
    'undercutting',
    'undermining'
);

-- dependence-relation-types (authorised by DR-0028)
CREATE TYPE dependence_relation_types AS ENUM (
    'cites',
    'common-evidentiary-origin',
    'derives-from',
    'reposts',
    'shares-underlying-document',
    'shares-underlying-witness',
    'syndicates'
);

-- document-statuses (authorised by DR-0046)
CREATE TYPE document_statuses AS ENUM (
    'approved',
    'draft',
    'effective',
    'proposed',
    'superseded',
    'withdrawn'
);

-- entity-statuses (authorised by DR-0062)
CREATE TYPE entity_statuses AS ENUM (
    'candidate',
    'canonical',
    'disproved',
    'fabricated'
);

-- epistemic-categories (authorised by DR-0025)
CREATE TYPE epistemic_categories AS ENUM (
    'assessment',
    'claim',
    'finding',
    'hypothesis',
    'observation',
    'project-conclusion'
);

-- interest-types (authorised by DR-0040)
CREATE TYPE interest_types AS ENUM (
    'appointment-rights',
    'beneficial-ownership',
    'contractual-control',
    'de-facto-control',
    'direct-ownership',
    'indirect-ownership',
    'legal-ownership',
    'managerial-control',
    'nominee-arrangement',
    'ultimate-beneficial-ownership',
    'voting-rights'
);

-- likelihood-bands (authorised by DR-0026, DR-0065)
CREATE TYPE likelihood_bands AS ENUM (
    'almost-certain',
    'almost-no-chance',
    'likely',
    'roughly-even-chance',
    'unlikely',
    'very-likely',
    'very-unlikely'
);

-- match-states (authorised by DR-0063)
CREATE TYPE match_states AS ENUM (
    'confirmed',
    'proposed',
    'rejected',
    'under-review',
    'withdrawn'
);

-- premis-event-types (authorised by DR-0060)
CREATE TYPE premis_event_types AS ENUM (
    'capture',
    'fixity-check',
    'format-identification',
    'ingestion',
    'message-digest-calculation',
    'migration-normalization',
    'virus-check'
);

-- quantity-semantic-types (authorised by DR-0030)
CREATE TYPE quantity_semantic_types AS ENUM (
    'approximate',
    'at-least',
    'at-most',
    'exact',
    'fewer-than',
    'greater-than',
    'range'
);

-- registration-statuses (authorised by DR-0080)
CREATE TYPE registration_statuses AS ENUM (
    'deprecated',
    'draft',
    'effective',
    'retired'
);

-- retention-tiers (authorised by DR-0068)
CREATE TYPE retention_tiers AS ENUM (
    'discard',
    'medium-term',
    'metadata-only',
    'permanent'
);

-- review-tiers (authorised by DR-0063)
CREATE TYPE review_tiers AS ENUM (
    'T1',
    'T2',
    'T3'
);

-- rights-permissions (authorised by DR-0002, DR-0067)
CREATE TYPE rights_permissions AS ENUM (
    'may-display',
    'may-preserve',
    'may-provide-to-subscribers',
    'may-redistribute',
    'unknown'
);

-- source-grades / item-credibility (authorised by DR-0027)
CREATE TYPE source_grades_item_credibility AS ENUM (
    '1',
    '2',
    '3',
    '4',
    '5',
    '6'
);

-- source-grades / source-reliability (authorised by DR-0027)
CREATE TYPE source_grades_source_reliability AS ENUM (
    'A',
    'B',
    'C',
    'D',
    'E',
    'F'
);

-- territorial-statuses (authorised by DR-0044, DR-0015)
CREATE TYPE territorial_statuses AS ENUM (
    'administration',
    'de-facto-control',
    'international-recognition',
    'non-recognition',
    'occupation',
    'sovereignty-claim'
);


-- Open vocabularies -> seeded lookup tables

-- classification-systems (open vocabulary, authorised by DR-0042)
-- Open per DR-0080: members may be added by registry process, so this
-- is a seeded lookup table rather than an enum type — adding a member
-- is a data change, not a migration.
CREATE TABLE classification_systems (
    id text PRIMARY KEY
);
INSERT INTO classification_systems (id) VALUES
    ('cn'),
    ('common-high-priority-list'),
    ('eccn'),
    ('eu-dual-use'),
    ('hs'),
    ('national-export-control'),
    ('wassenaar');

-- identifier-types (open vocabulary, authorised by DR-0012, DR-0045)
-- Open per DR-0080: members may be added by registry process, so this
-- is a seeded lookup table rather than an enum type — adding a member
-- is a data change, not a migration.
CREATE TABLE identifier_types (
    id text PRIMARY KEY
);
INSERT INTO identifier_types (id) VALUES
    ('aircraft-registration'),
    ('company-registration-number'),
    ('icao-24bit'),
    ('imo'),
    ('lei'),
    ('mmsi'),
    ('official-registry-id'),
    ('official-sanctions-id'),
    ('opensanctions'),
    ('tax-id'),
    ('wikidata');

-- source-types (open vocabulary, authorised by DR-0067)
-- Open per DR-0080: members may be added by registry process, so this
-- is a seeded lookup table rather than an enum type — adding a member
-- is a data change, not a migration.
CREATE TABLE source_types (
    id text PRIMARY KEY
);
INSERT INTO source_types (id) VALUES
    ('corporate-registry'),
    ('court-prosecutor'),
    ('feed'),
    ('government'),
    ('international-organisation'),
    ('investigative-media'),
    ('military-security-institution'),
    ('news-media'),
    ('ngo'),
    ('official-russian'),
    ('official-ukrainian'),
    ('podcast'),
    ('public-dataset'),
    ('sanctions-authority'),
    ('social-media'),
    ('telegram-channel'),
    ('telegram-group'),
    ('think-tank'),
    ('third-party-submission'),
    ('trade-transport-data'),
    ('video-platform'),
    ('web-archive');
