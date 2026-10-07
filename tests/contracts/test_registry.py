"""Schema registry: offline refs, active format checking, deterministic dispatch."""

from __future__ import annotations

import json
import shutil

import pytest
from jsonschema import Draft202012Validator

from ana_agents.contracts import findings as F
from ana_agents.contracts.registry import (
    DEFAULT_SCHEMA_DIR,
    SchemaRegistry,
    SchemaRegistryError,
    default_registry,
)

EXPECTED_SCHEMAS = {
    "Common",
    "ArtifactEnvelope",
    "SourceRecord",
    "EvidenceClaim",
    "LeadTriage",
    "CreatorTruthPack",
    "BrandResearch",
    "ContactProfile",
    "AnaBrandFit",
    "CollaborationHypothesis",
    "CommercialCheck",
    "OutreachStrategy",
    "EmailDraft",
    "QAGateReport",
    "HumanApproval",
    "SendPermission",
    "SendReceipt",
    "ReplyHandoff",
    "OutcomeRecord",
    "EvalCase",
    "ContactPolicy",
}


def _copy_schemas(tmp_path):
    target = tmp_path / "schemas"
    shutil.copytree(DEFAULT_SCHEMA_DIR, target)
    return target


def test_all_canonical_schemas_load_as_draft_2020_12():
    registry = default_registry()
    assert set(registry.schemas) == EXPECTED_SCHEMAS
    for schema in registry.schemas.values():
        assert schema["$schema"] == "https://json-schema.org/draft/2020-12/schema"
        Draft202012Validator.check_schema(schema)


def test_supporting_types_are_not_pipeline_artifacts():
    registry = default_registry()
    assert {"SourceRecord", "EvidenceClaim", "EvalCase"}.isdisjoint(registry.pipeline_types)
    assert len(registry.pipeline_types) == 15


def test_unresolvable_local_ref_is_rejected(tmp_path):
    schema_dir = _copy_schemas(tmp_path)
    path = schema_dir / "lead-triage.schema.json"
    schema = json.loads(path.read_text())
    schema["properties"]["rationale"] = {"$ref": "common.schema.json#/$defs/does_not_exist"}
    path.write_text(json.dumps(schema))
    with pytest.raises(SchemaRegistryError) as excinfo:
        SchemaRegistry(schema_dir)
    assert excinfo.value.code == "REGISTRY_UNRESOLVABLE_REF"


def test_ref_to_missing_local_file_is_rejected(tmp_path):
    schema_dir = _copy_schemas(tmp_path)
    path = schema_dir / "lead-triage.schema.json"
    schema = json.loads(path.read_text())
    schema["properties"]["rationale"] = {"$ref": "no-such-file.schema.json"}
    path.write_text(json.dumps(schema))
    with pytest.raises(SchemaRegistryError) as excinfo:
        SchemaRegistry(schema_dir)
    assert excinfo.value.code == "REGISTRY_UNRESOLVABLE_REF"


def test_remote_ref_is_rejected_without_network(tmp_path):
    schema_dir = _copy_schemas(tmp_path)
    path = schema_dir / "lead-triage.schema.json"
    schema = json.loads(path.read_text())
    schema["properties"]["rationale"] = {"$ref": "https://example.com/remote.schema.json"}
    path.write_text(json.dumps(schema))
    with pytest.raises(SchemaRegistryError) as excinfo:
        SchemaRegistry(schema_dir)
    assert excinfo.value.code == "REGISTRY_NONLOCAL_REF"


def test_wrong_draft_is_rejected(tmp_path):
    schema_dir = _copy_schemas(tmp_path)
    path = schema_dir / "lead-triage.schema.json"
    schema = json.loads(path.read_text())
    schema["$schema"] = "http://json-schema.org/draft-07/schema#"
    path.write_text(json.dumps(schema))
    with pytest.raises(SchemaRegistryError) as excinfo:
        SchemaRegistry(schema_dir)
    assert excinfo.value.code == "REGISTRY_WRONG_DRAFT"


def test_envelope_enum_drift_is_rejected(tmp_path):
    schema_dir = _copy_schemas(tmp_path)
    (schema_dir / "outcome-record.schema.json").unlink()
    with pytest.raises(SchemaRegistryError) as excinfo:
        SchemaRegistry(schema_dir)
    assert excinfo.value.code == "REGISTRY_ENVELOPE_TYPE_DRIFT"


def test_format_check_canary_detects_inactive_checker(monkeypatch):
    """If date-time checking silently degrades to annotation-only, construction fails."""
    checker = Draft202012Validator.FORMAT_CHECKER
    monkeypatch.delitem(checker.checkers, "date-time")
    with pytest.raises(SchemaRegistryError) as excinfo:
        SchemaRegistry()
    assert excinfo.value.code == "REGISTRY_FORMAT_CHECK_INACTIVE"


@pytest.mark.parametrize(
    ("value", "valid"),
    [
        ("2026-10-07T12:00:00Z", True),
        ("2026-10-07T12:00:00.123+05:30", True),
        ("2026-02-30T10:00:00Z", False),
        ("2026-10-07T12:00:00", False),
        ("2026-10-07 12:00:00Z", False),
        ("yesterday", False),
    ],
)
def test_timestamp_format_is_asserted(value, valid, artifacts):
    lead = artifacts["lt-001"]
    lead["produced_at"] = value
    found = default_registry().validate_artifact(lead)
    if valid:
        assert found == []
    else:
        assert [(f.code, f.keyword, f.path) for f in found] == [
            (F.SCHEMA_INVALID, "format", "/produced_at")
        ]


def test_dispatch_rejects_unknown_and_supporting_types(artifacts):
    registry = default_registry()
    source = artifacts["br-001"]["sources"][0]
    assert [f.code for f in registry.validate_artifact(source)] == [
        F.REGISTRY_UNKNOWN_ARTIFACT_TYPE
    ]
    disguised = dict(source, artifact_type="SourceRecord")
    assert [f.code for f in registry.validate_artifact(disguised)] == [
        F.REGISTRY_UNKNOWN_ARTIFACT_TYPE
    ]
    assert [f.code for f in registry.validate_artifact([])] == [F.REGISTRY_NOT_AN_OBJECT]


def test_dispatch_is_by_artifact_type(artifacts):
    draft = artifacts["ed-001"]
    draft["artifact_type"] = "LeadTriage"  # now judged by the LeadTriage schema
    found = default_registry().validate_artifact(draft)
    assert any(f.keyword == "required" for f in found)


def test_genuine_extra_property_is_still_reported_alongside_other_errors(artifacts):
    fit = artifacts["fit-001"]
    fit["fit_score"] = 0.9
    fit["produced_at"] = "not-a-time"
    keywords = {f.keyword for f in default_registry().validate_artifact(fit)}
    assert keywords == {"format", "unevaluatedProperties"}


def test_source_record_accepts_real_urls_not_only_example_domains():
    registry = default_registry()
    record = {
        "source_id": "src-real",
        "url": "https://www.some-real-brand.de/en/about?ref=1",
        "source_class": "official_brand_site",
        "trust": "UNTRUSTED_EXTERNAL",
        "retrieved_at": "2026-10-07T10:00:00Z",
    }
    assert registry.validate(record, "SourceRecord") == []
    record["url"] = "not a url"
    assert [f.keyword for f in registry.validate(record, "SourceRecord")] == ["format"]
