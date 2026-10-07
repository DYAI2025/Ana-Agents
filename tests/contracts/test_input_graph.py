"""The executable input graph and its ADR-003 restatement must not drift apart."""

from __future__ import annotations

import re

import pytest
import yaml

from ana_agents import REPO_ROOT
from ana_agents.evidence.chain import INPUT_GRAPH_PATH, InputGraphError, load_input_graph

ADR = REPO_ROOT / "docs" / "decisions" / "ADR-003-canonical-contract-encoding.md"


def adr_graph() -> dict[str, set[str]]:
    text = ADR.read_text(encoding="utf-8")
    block = re.search(r"<!-- input-graph:begin -->(.*?)<!-- input-graph:end -->", text, re.S)
    assert block, "ADR-003 must contain the input-graph block"
    graph: dict[str, set[str]] = {}
    for line in block.group(1).splitlines():
        if "<-" not in line:
            continue
        left, right = (part.strip() for part in line.split("<-", 1))
        names = {n.strip() for n in right.split(",")} - {"none", ""}
        graph[left] = names
    return graph


def test_adr_restatement_matches_executable_graph():
    graph = load_input_graph()
    assert adr_graph() == {name: set(allowed) for name, allowed in graph.allowed.items()}


def test_source_record_is_never_an_input():
    graph = load_input_graph()
    for allowed in graph.allowed.values():
        assert not {"SourceRecord", "EvidenceClaim"} & allowed


@pytest.mark.parametrize("target", ["EmailDraft", "SendPermission", "SendReceipt"])
def test_send_path_never_accepts_raw_research(target):
    graph = load_input_graph()
    assert not {"BrandResearch", "CreatorTruthPack", "LeadTriage"} & graph.allowed[target]


def test_no_type_accepts_outcome_record():
    graph = load_input_graph()
    assert all("OutcomeRecord" not in allowed for allowed in graph.allowed.values())


def test_contact_profile_is_not_a_fit_input():
    assert "ContactProfile" not in load_input_graph().allowed["AnaBrandFit"]


def _write(tmp_path, mutate):
    data = yaml.safe_load(INPUT_GRAPH_PATH.read_text())
    mutate(data)
    path = tmp_path / "graph.yaml"
    path.write_text(yaml.safe_dump(data))
    return path


@pytest.mark.parametrize(
    "mutate",
    [
        pytest.param(
            lambda d: d["types"]["EmailDraft"]["allowed"].append("OutcomeRecord"),
            id="outcome-feedback",
        ),
        pytest.param(
            lambda d: d["types"]["EmailDraft"]["allowed"].append("SourceRecord"), id="raw-source"
        ),
        pytest.param(lambda d: d["types"].pop("SendReceipt"), id="missing-type"),
        pytest.param(
            lambda d: d["types"]["EmailDraft"]["required"].append("CommercialCheck"),
            id="required-not-allowed",
        ),
    ],
)
def test_widened_or_broken_graph_is_rejected(tmp_path, mutate):
    with pytest.raises(InputGraphError):
        load_input_graph(_write(tmp_path, mutate))
