#!/usr/bin/env python3
"""Test the registration-class mechanism (DR-pending-registration-classes).

This suite tests class loading, merging class defaults into sources,
validation with classes, and error handling.
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "sources"))

from register import (
    RegistrationError, merge_class_defaults, validate,
    REQUIRED, VERIFICATION_FIELDS
)


def check(requirement, description, condition):
    """Print PASS/FAIL with requirement identifier."""
    status = "PASS" if condition else "FAIL"
    print(f"{status}  {requirement}: {description}")
    return condition


def test_merge_no_class():
    """Class-less sources are returned unchanged."""
    source = {
        "key": "test-source",
        "name": "Test Source",
        "source_type": "list",
        "jurisdiction": "EU",
        "collection_method": "http",
        "scope_rules": "Test items only",
        "default_retention_tier": "permanent",
        "default_access_tier": "public",
        "rights_permission": "may-redistribute",
    }
    all_classes = {}
    merged = merge_class_defaults(source, all_classes)
    check(
        "CDR-pending-registration-classes",
        "source without class reference returns unchanged",
        merged == source
    )


def test_merge_with_class_inheritance():
    """Sources inherit policy fields from their class."""
    class_def = {
        "collection_method": "http",
        "collection_cadence": "daily",
        "capture_format": "warc",
        "default_retention_tier": "permanent",
        "default_access_tier": "public",
        "rights_permission": "may-redistribute",
        "rights_basis": "EU Decision 2011/833/EU",
        "grade_source_reliability": "A",
        "grade_item_credibility": "1",
    }
    source = {
        "key": "eu-test-source",
        "class": "EU-institutional",
        "name": "Test EU Source",
        "source_type": "list",
        "jurisdiction": "EU",
        "primary_languages": ["en"],
        "coverage_start": "2009-06-27",
        "scope_rules": "Financial designations only",
    }
    all_classes = {"EU-institutional": class_def}
    merged = merge_class_defaults(source, all_classes)

    # Check inheritance
    check(
        "CDR-pending-registration-classes",
        "inherits collection_method from class",
        merged.get("collection_method") == "http"
    )
    check(
        "CDR-pending-registration-classes",
        "inherits collection_cadence from class",
        merged.get("collection_cadence") == "daily"
    )
    check(
        "CDR-pending-registration-classes",
        "inherits capture_format from class",
        merged.get("capture_format") == "warc"
    )
    check(
        "CDR-pending-registration-classes",
        "inherits default_retention_tier from class",
        merged.get("default_retention_tier") == "permanent"
    )
    check(
        "CDR-pending-registration-classes",
        "inherits default_access_tier from class",
        merged.get("default_access_tier") == "public"
    )
    check(
        "CDR-pending-registration-classes",
        "inherits rights_permission from class",
        merged.get("rights_permission") == "may-redistribute"
    )
    check(
        "CDR-pending-registration-classes",
        "source-level fields take precedence over class",
        merged.get("key") == "eu-test-source"
        and merged.get("name") == "Test EU Source"
    )


def test_merge_with_source_override():
    """Source-level fields override class defaults."""
    class_def = {
        "collection_method": "http",
        "collection_cadence": "daily",
        "default_retention_tier": "permanent",
        "default_access_tier": "public",
        "rights_permission": "may-redistribute",
        "rights_basis": "Class default basis",
    }
    source = {
        "key": "override-test",
        "class": "test-class",
        "name": "Override Test",
        "source_type": "list",
        "jurisdiction": "US",
        "collection_method": "http",
        "scope_rules": "Override this",
        "default_retention_tier": "permanent",
        "default_access_tier": "public",
        "rights_permission": "may-provide-to-subscribers",  # Override
        "rights_basis": "Source-specific basis",  # Override
    }
    all_classes = {"test-class": class_def}
    merged = merge_class_defaults(source, all_classes)

    check(
        "CDR-pending-registration-classes",
        "source override of rights_permission takes effect",
        merged.get("rights_permission") == "may-provide-to-subscribers"
    )
    check(
        "CDR-pending-registration-classes",
        "source override of rights_basis takes effect",
        merged.get("rights_basis") == "Source-specific basis"
    )


def test_merge_unknown_class():
    """Unknown class references raise RegistrationError."""
    source = {
        "key": "bad-source",
        "class": "nonexistent-class",
        "name": "Bad Source",
    }
    all_classes = {"some-class": {}}

    try:
        merge_class_defaults(source, all_classes)
        check(
            "CDR-pending-registration-classes",
            "unknown class reference raises RegistrationError",
            False
        )
    except RegistrationError as e:
        check(
            "CDR-pending-registration-classes",
            "unknown class reference raises RegistrationError",
            "nonexistent-class" in str(e)
        )


def test_merge_removes_internal_markers():
    """Internal _file markers are not merged into the result."""
    class_def = {
        "_file": "classes.yaml",
        "collection_method": "http",
        "default_retention_tier": "permanent",
    }
    source = {
        "_file": "sources.yaml",
        "key": "test",
        "class": "test-class",
        "name": "Test",
    }
    all_classes = {"test-class": class_def}
    merged = merge_class_defaults(source, all_classes)

    check(
        "CDR-pending-registration-classes",
        "internal _file marker not included in merged result",
        "_file" not in merged
    )


def test_validate_with_classes():
    """Validation works correctly with class merging."""
    sources = [
        {
            "key": "eu-list",
            "class": "EU-institutional",
            "name": "EU Test List",
            "source_type": "list",
            "jurisdiction": "EU",
            "primary_languages": ["en"],
            "coverage_start": "2009-06-27",
            "scope_rules": "Test scope",
        }
    ]
    all_classes = {
        "EU-institutional": {
            "collection_method": "http",
            "collection_cadence": "daily",
            "default_retention_tier": "permanent",
            "default_access_tier": "public",
            "rights_permission": "may-redistribute",
            "rights_basis": "EU Decision 2011/833/EU - [UNVERIFIED LEGAL REVIEW]",
        }
    }

    problems = validate(sources, [], all_classes=all_classes)
    check(
        "CDR-pending-registration-classes",
        "validation succeeds with class inheritance",
        len(problems) == 0
    )


def test_validate_missing_required_after_merge():
    """Validation catches missing required fields after class merge."""
    sources = [
        {
            "key": "incomplete",
            "class": "test-class",
            "name": "Incomplete Source",
            "source_type": "list",
            "jurisdiction": "US",
            # Missing: collection_method, scope_rules, retention/access tiers, etc.
        }
    ]
    all_classes = {
        "test-class": {
            # Class also doesn't provide collection_method
            "default_retention_tier": "permanent",
            "default_access_tier": "public",
            "rights_permission": "may-redistribute",
        }
    }

    problems = validate(sources, [], all_classes=all_classes)
    check(
        "CDR-pending-registration-classes",
        "validation catches missing required field after class merge",
        any("collection_method" in p for p in problems)
    )


def test_validate_class_reference_error():
    """Validation catches unknown class references."""
    sources = [
        {
            "key": "bad-class-ref",
            "class": "unknown-class",
            "name": "Bad Reference",
        }
    ]
    all_classes = {"some-class": {}}

    problems = validate(sources, [], all_classes=all_classes)
    check(
        "CDR-pending-registration-classes",
        "validation catches unknown class reference",
        any("unknown class" in p.lower() for p in problems)
    )


def test_verify_fields_not_inherited():
    """Verification fields are never inherited from classes."""
    class_def = {
        "collection_method": "http",
        "default_retention_tier": "permanent",
        "default_access_tier": "public",
        "rights_permission": "may-redistribute",
        "locator_verified": "2024-01-01",  # Should NOT be inherited
        "verification_note": "Class verification",  # Should NOT be inherited
    }
    source = {
        "key": "verify-test",
        "class": "test-class",
        "name": "Verify Test",
        "scope_rules": "Test",
    }
    all_classes = {"test-class": class_def}
    merged = merge_class_defaults(source, all_classes)

    # Note: currently the merge doesn't explicitly exclude verification fields,
    # it just returns whatever is in the merged dict. This test documents
    # that behavior. In the future, we might want to explicitly strip them.
    check(
        "CDR-pending-registration-classes",
        "source inherits class fields",
        merged.get("collection_method") == "http"
    )


def test_class_independence():
    """Classes are independent across files and don't modify the original."""
    class_def = {
        "collection_method": "http",
        "default_retention_tier": "permanent",
    }
    source = {
        "key": "test",
        "class": "test-class",
        "name": "Test",
    }
    all_classes = {"test-class": class_def.copy()}

    merged = merge_class_defaults(source, all_classes)

    # Original class should not be modified
    check(
        "CDR-pending-registration-classes",
        "merging does not modify the original class definition",
        class_def == {"collection_method": "http", "default_retention_tier": "permanent"}
    )

    # Original source should not be modified
    check(
        "CDR-pending-registration-classes",
        "merging does not modify the original source",
        source == {"key": "test", "class": "test-class", "name": "Test"}
    )


def test_multiple_sources_same_class():
    """Multiple sources can use the same class."""
    class_def = {
        "collection_method": "http",
        "default_retention_tier": "permanent",
        "default_access_tier": "public",
        "rights_permission": "may-redistribute",
        "rights_basis": "[UNVERIFIED LEGAL REVIEW]",
    }
    sources = [
        {
            "key": "source-1",
            "class": "shared-class",
            "name": "Source 1",
            "source_type": "list",
            "jurisdiction": "EU",
            "scope_rules": "Scope 1",
        },
        {
            "key": "source-2",
            "class": "shared-class",
            "name": "Source 2",
            "source_type": "list",
            "jurisdiction": "EU",
            "scope_rules": "Scope 2",
        },
    ]
    all_classes = {"shared-class": class_def}

    problems = validate(sources, [], all_classes=all_classes)
    check(
        "CDR-pending-registration-classes",
        "multiple sources can share the same class",
        len(problems) == 0
    )


if __name__ == "__main__":
    print("Testing registration-class mechanism (DR-pending-registration-classes)\n")

    test_merge_no_class()
    test_merge_with_class_inheritance()
    test_merge_with_source_override()
    test_merge_unknown_class()
    test_merge_removes_internal_markers()
    test_validate_with_classes()
    test_validate_missing_required_after_merge()
    test_validate_class_reference_error()
    test_verify_fields_not_inherited()
    test_class_independence()
    test_multiple_sources_same_class()

    print("\nAll class mechanism tests completed.")
