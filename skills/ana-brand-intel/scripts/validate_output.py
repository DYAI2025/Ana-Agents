#!/usr/bin/env python3
"""Pre-flight check of an ana-brand-intel answer before it is returned.

Standard library only. Run it on the answer file whenever the runtime offers code
execution:

    python3 scripts/validate_output.py answer.json

It catches structural mistakes the canonical repository validators would reject anyway, so
they can be fixed before the answer leaves the skill: invalid JSON (with the position of the
first error), wrong top-level shape, non-canonical or duplicated artifact types, missing
envelope fields, mixed run ids, non-canonical epistemic classes, FACT without a source,
artifacts emitted after a stop outcome, and more than three hypotheses.

It is a pre-flight, not validation: a clean result is NOT a schema, evidence-chain or
policy PASS. The canonical validators in DYAI2025/Ana-Agents stay authoritative.

Exit status: 0 no problems, 1 problems found, 2 usage error.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

OUTPUT_TYPES = ("BrandResearch", "ContactProfile", "AnaBrandFit", "CollaborationHypothesis")
ENVELOPE = (
    "artifact_id",
    "artifact_type",
    "schema_version",
    "contract_version",
    "produced_at",
    "producer",
    "run_id",
    "input_artifact_ids",
)
EPISTEMIC = {"FACT", "SUPPORTED_INFERENCE", "HYPOTHESIS", "UNKNOWN"}
RESEARCH_STOPS = {"INSUFFICIENT_EVIDENCE", "CONFLICTING_EVIDENCE"}
FIT_STOPS = {"NO_FIT", "INSUFFICIENT_EVIDENCE", "CONFLICTING_EVIDENCE"}


def check_text(text: str) -> list[str]:
    try:
        answer = json.loads(text)
    except json.JSONDecodeError as exc:
        line = text.splitlines()[exc.lineno - 1] if exc.lineno <= len(text.splitlines()) else ""
        return [
            f"invalid JSON at line {exc.lineno} column {exc.colno} (char {exc.pos}): {exc.msg}; "
            f"near {line[max(0, exc.colno - 60) : exc.colno + 20]!r}. Check that every "
            "object and array is closed before the next top-level key."
        ]
    return check_answer(answer)


def check_answer(answer: object) -> list[str]:
    problems: list[str] = []
    if not isinstance(answer, dict):
        return ["top level must be an object with 'artifacts' and 'operator_summary'"]
    extra = set(answer) - {"artifacts", "operator_summary"}
    if extra:
        problems.append(
            f"unexpected top-level keys {sorted(extra)}; a key inside an artifact may have "
            "been placed at the wrong nesting level"
        )
    artifacts = answer.get("artifacts")
    if not isinstance(artifacts, list):
        return [*problems, "'artifacts' must be a list"]
    summary = answer.get("operator_summary")
    if not isinstance(summary, str) or not summary.strip():
        problems.append("'operator_summary' must be a non-empty string")

    by_type: dict[str, dict] = {}
    run_ids = set()
    for index, artifact in enumerate(artifacts):
        where = f"artifacts[{index}]"
        if not isinstance(artifact, dict):
            problems.append(f"{where} is not an object")
            continue
        kind = artifact.get("artifact_type")
        if kind not in OUTPUT_TYPES:
            problems.append(f"{where}: artifact_type {kind!r} is not a Brand Intel output")
            continue
        if kind in by_type:
            problems.append(f"{where}: second {kind}")
        by_type.setdefault(kind, artifact)
        missing = [k for k in ENVELOPE if k not in artifact]
        if missing:
            problems.append(f"{where} ({kind}): missing envelope fields {missing}")
        stray = {"operator_summary", "artifacts"} & set(artifact)
        if stray:
            problems.append(f"{where} ({kind}): top-level key {sorted(stray)} nested inside")
        if artifact.get("producer") != {"kind": "skill", "id": "ana-brand-intel"}:
            problems.append(f"{where} ({kind}): producer must be skill/ana-brand-intel")
        run_ids.add(artifact.get("run_id"))
    if len(run_ids) > 1:
        problems.append(f"artifacts use several run_id values {sorted(map(str, run_ids))}")

    research = by_type.get("BrandResearch")
    if research is None:
        problems.append("BrandResearch is missing")
    else:
        for i, claim in enumerate(research.get("claims") or []):
            status = claim.get("epistemic_status") if isinstance(claim, dict) else None
            if status not in EPISTEMIC:
                problems.append(f"claims[{i}]: epistemic_status {status!r} is not canonical")
            elif status == "FACT" and not claim.get("source_ids"):
                problems.append(f"claims[{i}]: FACT without source_ids")
        if research.get("research_outcome") in RESEARCH_STOPS:
            later = sorted(set(by_type) - {"BrandResearch"})
            if later:
                problems.append(f"research stop emits {later}; only BrandResearch may follow")

    fit = by_type.get("AnaBrandFit")
    hypotheses = by_type.get("CollaborationHypothesis")
    if fit is not None and fit.get("fit_outcome") in FIT_STOPS and hypotheses is not None:
        problems.append(f"fit outcome {fit['fit_outcome']} must not be followed by hypotheses")
    if hypotheses is not None:
        items = hypotheses.get("hypotheses")
        if not isinstance(items, list) or not 1 <= len(items) <= 3:
            problems.append("CollaborationHypothesis.hypotheses must hold 1 to 3 items")
    return problems


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_output.py ANSWER.json")
        return 2
    problems = check_text(Path(argv[1]).read_text(encoding="utf-8"))
    for problem in problems:
        print(f"PREFLIGHT  {problem}")
    print(
        f"preflight: {len(problems)} problems "
        "(a clean pre-flight is not a schema or evidence-chain PASS)"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
