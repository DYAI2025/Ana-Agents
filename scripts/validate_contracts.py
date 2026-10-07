#!/usr/bin/env python3
"""Validate the contract family end to end (offline).

1. Build the schema registry (metaschema, local refs, active format canary, envelope drift).
2. Load and validate the executable contact policy and artifact input graph.
3. Every positive example and valid chain must produce zero findings.
4. Every negative case must produce exactly its expected findings.

Exit status: 0 all checks passed, 1 any check failed, 2 the contract set itself is broken.
"""

from __future__ import annotations

import json
import sys

from ana_agents.contracts.examples import EXAMPLES_DIR, load_chain, load_negative_cases, run_case
from ana_agents.contracts.registry import SchemaRegistryError, default_registry
from ana_agents.contracts.semantic import (
    ContactPolicyError,
    default_contact_policy,
    validate_artifact,
    validate_eval_case,
)
from ana_agents.evidence.chain import InputGraphError, default_input_graph, validate_chain

SUPPORTING_BY_KEY = {
    "eval_id": "EvalCase",
    "claim_id": "EvidenceClaim",
    "source_id": "SourceRecord",
}


def main() -> int:
    try:
        registry = default_registry()
        policy = default_contact_policy()
        graph = default_input_graph()
    except (SchemaRegistryError, ContactPolicyError, InputGraphError) as exc:
        print(f"CONTRACT SET BROKEN: {exc}")
        return 2
    print(
        f"registry: {len(registry.schemas)} schemas, "
        f"{len(registry.pipeline_types)} pipeline types; "
        f"contact policy {policy.version} ({len(policy.rules)} rules); input graph {graph.version}"
    )
    failures = 0

    for path in sorted((EXAMPLES_DIR / "valid").glob("*.json")):
        doc = json.loads(path.read_text(encoding="utf-8"))
        if "artifact_type" in doc:
            findings = validate_artifact(doc)
        else:
            title = next(t for k, t in SUPPORTING_BY_KEY.items() if k in doc)
            findings = (
                validate_eval_case(doc) if title == "EvalCase" else registry.validate(doc, title)
            )
        status = "ok" if not findings else "FAIL"
        failures += bool(findings)
        print(f"  example {status:4} {path.relative_to(EXAMPLES_DIR)} ({len(findings)} findings)")
        for finding in findings:
            print(f"      {finding.code} {finding.artifact_id} {finding.path} {finding.message}")

    for path in sorted((EXAMPLES_DIR / "chains").glob("*.json")):
        chain = load_chain(path)
        findings = validate_chain(chain.artifacts, now=chain.evaluated_at)
        status = "ok" if not findings else "FAIL"
        failures += bool(findings)
        print(
            f"  chain   {status:4} {path.relative_to(EXAMPLES_DIR)} "
            f"({len(chain.artifacts)} artifacts)"
        )
        for finding in findings:
            print(f"      {finding.code} {finding.artifact_id} {finding.path} {finding.message}")

    cases = load_negative_cases()
    negatives = sum(1 for c in cases if c["expect"])
    case_failures = 0
    for case in cases:
        result = run_case(case)
        if not result.passed:
            case_failures += 1
            print(f"  case    FAIL {case['id']}: {case['description']}")
            print(f"      missing: {sorted(result.expected - result.actual, key=str)}")
            print(f"      extra:   {sorted(result.actual - result.expected, key=str)}")
    print(
        f"cases: {len(cases)} ({negatives} negative, {len(cases) - negatives} positive controls), "
        f"{case_failures} failed"
    )
    failures += case_failures
    print("RESULT:", "PASS" if failures == 0 else f"FAIL ({failures})")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
