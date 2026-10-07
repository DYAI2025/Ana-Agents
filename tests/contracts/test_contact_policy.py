"""Executable contact policy (D3; INTEL-007, INTEL-008, INTEL-010)."""

from __future__ import annotations

import itertools
import shutil

import pytest
import yaml

from ana_agents import CONTRACTS_DIR
from ana_agents.contracts.semantic import (
    CONTACT_POLICY_PATH,
    ContactPolicyError,
    default_contact_policy,
    load_contact_policy,
)

SOURCE_CLASSES = ["official_published", "public_found", "inferred", "private", "unknown"]
VERIFICATIONS = ["verified", "unverified", "catch_all", "unknown"]


def expected_readiness(source_class: str, verification: str, business: bool) -> str:
    """Independent restatement of the approved decision D3, used as the test oracle."""
    if source_class in ("private", "unknown") or not business:
        return "NO_SEND"
    if source_class == "official_published" and verification == "verified":
        return "ELIGIBLE_FOR_GATES"
    return "REVIEW_REQUIRED"


@pytest.mark.parametrize(
    ("source_class", "verification", "business"),
    list(itertools.product(SOURCE_CLASSES, VERIFICATIONS, [True, False])),
)
def test_policy_matches_decision_d3_for_every_combination(source_class, verification, business):
    readiness, _ = default_contact_policy().evaluate(source_class, verification, business)
    assert readiness == expected_readiness(source_class, verification, business)


def test_exactly_one_combination_is_eligible():
    policy = default_contact_policy()
    eligible = [
        combo
        for combo in itertools.product(SOURCE_CLASSES, VERIFICATIONS, [True, False])
        if policy.evaluate(*combo)[0] == "ELIGIBLE_FOR_GATES"
    ]
    assert eligible == [("official_published", "verified", True)]


def test_dimensions_match_schema_enums():
    from ana_agents.contracts.registry import default_registry

    defs = default_registry().schemas["Common"]["$defs"]
    assert defs["contact_source_class"]["enum"] == SOURCE_CLASSES
    assert defs["contact_verification"]["enum"] == VERIFICATIONS
    assert defs["contact_readiness"]["enum"] == ["ELIGIBLE_FOR_GATES", "REVIEW_REQUIRED", "NO_SEND"]


def test_most_restrictive_wins_over_rule_order(tmp_path):
    data = yaml.safe_load(CONTACT_POLICY_PATH.read_text())
    data["rules"].reverse()
    path = tmp_path / "contact-policy.yaml"
    path.write_text(yaml.safe_dump(data))
    reversed_policy = load_contact_policy(path)
    for combo in itertools.product(SOURCE_CLASSES, VERIFICATIONS, [True, False]):
        assert reversed_policy.evaluate(*combo)[0] == expected_readiness(*combo)


def test_no_matching_rule_falls_back_to_no_send(tmp_path):
    data = yaml.safe_load(CONTACT_POLICY_PATH.read_text())
    data["rules"] = [r for r in data["rules"] if r["readiness"] != "ELIGIBLE_FOR_GATES"]
    path = tmp_path / "contact-policy.yaml"
    path.write_text(yaml.safe_dump(data))
    readiness, rules = load_contact_policy(path).evaluate("official_published", "verified", True)
    assert (readiness, rules) == ("NO_SEND", ())


@pytest.mark.parametrize(
    ("mutate", "label"),
    [
        (lambda d: d.__setitem__("default_readiness", "ELIGIBLE_FOR_GATES"), "permissive default"),
        (
            lambda d: d.__setitem__("review_resolution_mechanism", "auto"),
            "invented review mechanism",
        ),
        (
            lambda d: d["rules"][0]["when"].__setitem__("source_class", "leaked"),
            "unknown dimension value",
        ),
        (lambda d: d["rules"][0].__setitem__("readiness", "SEND_ALLOWED"), "send authority value"),
        (
            lambda d: d.__setitem__(
                "readiness_order", ["NO_SEND", "REVIEW_REQUIRED", "ELIGIBLE_FOR_GATES"]
            ),
            "inverted order",
        ),
    ],
)
def test_malformed_policy_is_rejected(tmp_path, mutate, label):
    data = yaml.safe_load(CONTACT_POLICY_PATH.read_text())
    mutate(data)
    path = tmp_path / "contact-policy.yaml"
    path.write_text(yaml.safe_dump(data))
    with pytest.raises(ContactPolicyError):
        load_contact_policy(path)


def test_markdown_does_not_restate_the_mapping():
    """contact-policy.md explains; the YAML is the only mapping (no competing table)."""
    text = (CONTRACTS_DIR / "policies" / "contact-policy.md").read_text()
    assert "contact-policy.yaml" in text
    for rule in yaml.safe_load(CONTACT_POLICY_PATH.read_text())["rules"]:
        assert rule["id"] not in text


def test_policy_file_copy_loads(tmp_path):
    copy_path = tmp_path / "contact-policy.yaml"
    shutil.copy(CONTACT_POLICY_PATH, copy_path)
    assert load_contact_policy(copy_path).version == default_contact_policy().version
