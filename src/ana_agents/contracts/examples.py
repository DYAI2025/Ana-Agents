"""Load synthetic fixtures and run the negative-case manifest.

Negative cases are declared as mutations of a valid base chain
(contracts/examples/negative-cases.yaml). Each case states the exact set of expected
findings as (code, artifact_id[, keyword]). A case passes only if the produced set equals
the expected set: failing for an unrelated or additional reason is a false green and fails
the case. Cases with an empty expectation are positive controls.
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from ana_agents import CONTRACTS_DIR
from ana_agents.contracts.findings import Finding, all_codes
from ana_agents.contracts.hashing import compute_draft_hash
from ana_agents.contracts.semantic import parse_timestamp
from ana_agents.evidence.chain import validate_chain

EXAMPLES_DIR = CONTRACTS_DIR / "examples"
NEGATIVE_MANIFEST = EXAMPLES_DIR / "negative-cases.yaml"

Expectation = tuple[str, str | None, str | None]


@dataclass
class Chain:
    description: str
    evaluated_at: datetime
    artifacts: list[dict[str, Any]]


def load_chain(path: Path) -> Chain:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return Chain(data["description"], parse_timestamp(data["evaluated_at"]), data["artifacts"])


def _split_pointer(pointer: str) -> list[str]:
    if not pointer.startswith("/"):
        raise ValueError(f"JSON pointer must start with '/': {pointer!r}")
    return [p.replace("~1", "/").replace("~0", "~") for p in pointer[1:].split("/")]


def _parent(document: Any, pointer: str) -> tuple[Any, str]:
    parts = _split_pointer(pointer)
    node = document
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    return node, parts[-1]


def apply_ops(chain: Chain, ops: list[dict[str, Any]]) -> Chain:
    chain = Chain(chain.description, chain.evaluated_at, copy.deepcopy(chain.artifacts))
    for op in ops:
        kind = op["op"]
        if kind == "set_now":
            chain.evaluated_at = parse_timestamp(op["value"])
            continue
        matches = [a for a in chain.artifacts if a.get("artifact_id") == op["artifact"]]
        if len(matches) != 1:
            raise ValueError(f"op target {op['artifact']!r} not unique in base chain")
        target = matches[0]
        if kind == "drop":
            chain.artifacts.remove(target)
        elif kind == "rehash":
            target["draft_hash"] = compute_draft_hash(target)
        elif kind in ("set", "remove", "append"):
            parent, key = _parent(target, op["path"])
            if kind == "set":
                if isinstance(parent, list):
                    parent[int(key)] = copy.deepcopy(op["value"])
                else:
                    parent[key] = copy.deepcopy(op["value"])
            elif kind == "remove":
                if isinstance(parent, list):
                    del parent[int(key)]
                else:
                    del parent[key]
            else:
                container = parent[int(key)] if isinstance(parent, list) else parent[key]
                container.append(copy.deepcopy(op["value"]))
        else:
            raise ValueError(f"unknown op {kind!r}")
    return chain


@dataclass
class CaseResult:
    case_id: str
    expected: set[Expectation]
    actual: set[Expectation]
    findings: list[Finding] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.expected == self.actual


def _project(finding: Finding, with_keyword: bool) -> Expectation:
    return (finding.code, finding.artifact_id, finding.keyword if with_keyword else None)


def run_case(case: dict[str, Any], examples_dir: Path = EXAMPLES_DIR) -> CaseResult:
    unknown = {e["code"] for e in case["expect"]} - all_codes()
    if unknown:
        raise ValueError(f"{case['id']}: unknown finding codes {sorted(unknown)}")
    chain = apply_ops(load_chain(examples_dir / case["base"]), case.get("ops", []))
    findings = validate_chain(chain.artifacts, now=chain.evaluated_at)
    expected: set[Expectation] = set()
    actual: set[Expectation] = set()
    keyword_codes = {e["code"] for e in case["expect"] if "keyword" in e}
    for e in case["expect"]:
        expected.add((e["code"], e.get("artifact"), e.get("keyword")))
    for finding in findings:
        actual.add(_project(finding, finding.code in keyword_codes))
    return CaseResult(case["id"], expected, actual, findings)


def load_negative_cases(path: Path = NEGATIVE_MANIFEST) -> list[dict[str, Any]]:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    cases = data["cases"]
    ids = [c["id"] for c in cases]
    if len(ids) != len(set(ids)):
        raise ValueError("duplicate negative case ids")
    return cases
