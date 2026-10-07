"""Draft hash semantics: send-payload-v1 (ADR-003, OPS-003)."""

from __future__ import annotations

import copy
import json

import pytest

from ana_agents.contracts.hashing import (
    HASH_ALGORITHM,
    NON_PAYLOAD_FIELDS,
    SEND_PAYLOAD_FIELDS,
    canonical_bytes,
    compute_draft_hash,
    send_payload,
)
from ana_agents.contracts.registry import default_registry


@pytest.fixture
def draft(artifacts):
    return artifacts["ed-001"]


def test_fixture_hash_matches_declared(draft):
    assert compute_draft_hash(draft) == draft["draft_hash"]
    assert draft["hash_algorithm"] == HASH_ALGORITHM


def test_key_order_and_serialization_do_not_change_hash(draft):
    reordered = json.loads(json.dumps(dict(reversed(list(draft.items())))))
    reordered["recipient"] = dict(reversed(list(draft["recipient"].items())))
    reordered["links"] = [dict(reversed(list(link.items()))) for link in draft["links"]]
    assert list(reordered) != list(draft)
    assert compute_draft_hash(reordered) == compute_draft_hash(draft)
    pretty = json.loads(json.dumps(draft, indent=4, sort_keys=True))
    assert compute_draft_hash(pretty) == compute_draft_hash(draft)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("artifact_id", "ed-999"),
        ("schema_version", "9.9.9"),
        ("contract_version", "9.9.9"),
        ("produced_at", "2030-01-01T00:00:00Z"),
        ("producer", {"kind": "runtime", "id": "someone-else"}),
        ("run_id", "run-other"),
        ("input_artifact_ids", ["x"]),
        ("claim_usage", []),
        ("draft_hash", "sha256:" + "0" * 64),
    ],
)
def test_metadata_only_change_keeps_hash(draft, field, value):
    changed = copy.deepcopy(draft)
    changed[field] = value
    assert compute_draft_hash(changed) == compute_draft_hash(draft)


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(lambda d: d.__setitem__("subject", d["subject"] + "!"), id="subject"),
        pytest.param(
            lambda d: d["recipient"].__setitem__("email", "other@brand.example.com"),
            id="recipient-email",
        ),
        pytest.param(
            lambda d: d["recipient"].__setitem__("contact_id", "contact-2"), id="recipient-contact"
        ),
        pytest.param(
            lambda d: d.__setitem__("body_text", d["body_text"] + " "),
            id="body_text-trailing-space",
        ),
        pytest.param(
            lambda d: d.__setitem__("body_html_light", "<p>changed</p>"), id="body_html_light"
        ),
        pytest.param(
            lambda d: d.__setitem__("body_html_light", None), id="body_html_light-removed"
        ),
        pytest.param(
            lambda d: d["links"][0].__setitem__("url", "https://creator.example.org/other"),
            id="link-url",
        ),
        pytest.param(lambda d: d["links"][0].__setitem__("label", "Other"), id="link-label"),
        pytest.param(
            lambda d: d["links"].append({"url": "https://creator.example.org/x", "label": "x"}),
            id="link-added",
        ),
        pytest.param(lambda d: d.__setitem__("sender_identity_id", "sender-other"), id="sender"),
    ],
)
def test_send_payload_change_changes_hash(draft, mutate):
    changed = copy.deepcopy(draft)
    mutate(changed)
    assert compute_draft_hash(changed) != compute_draft_hash(draft)


def test_link_order_is_significant(draft):
    draft["links"].append({"url": "https://creator.example.org/second", "label": "Second"})
    swapped = copy.deepcopy(draft)
    swapped["links"].reverse()
    assert compute_draft_hash(swapped) != compute_draft_hash(draft)


def test_unicode_is_hashed_exactly_without_normalization(draft):
    composed = copy.deepcopy(draft)
    composed["subject"] = "Café"
    decomposed = copy.deepcopy(draft)
    decomposed["subject"] = "Café"
    assert compute_draft_hash(composed) != compute_draft_hash(decomposed)


def test_canonical_bytes_are_deterministic():
    assert canonical_bytes({"b": 1, "a": [2, "ä"]}) == '{"a":[2,"ä"],"b":1}'.encode()
    with pytest.raises(ValueError):
        canonical_bytes({"x": float("nan")})


def test_payload_projection_contains_only_send_fields(draft):
    payload = send_payload(draft)
    assert set(payload) == {*SEND_PAYLOAD_FIELDS, "payload_version"}


def test_every_email_draft_field_is_classified():
    """Drift guard: a new EmailDraft field must be classified as payload or metadata, and
    a new payload field requires a new hash version (ADR-003)."""
    declared = default_registry().declared_properties("EmailDraft")
    classified = set(SEND_PAYLOAD_FIELDS) | NON_PAYLOAD_FIELDS
    assert declared == classified
    assert set(SEND_PAYLOAD_FIELDS).isdisjoint(NON_PAYLOAD_FIELDS)


def test_missing_payload_field_is_an_error(draft):
    del draft["links"]
    with pytest.raises(ValueError):
        compute_draft_hash(draft)
