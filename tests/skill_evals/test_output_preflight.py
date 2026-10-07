"""Package-local output pre-flight (skills/ana-brand-intel/scripts/validate_output.py).

The real failure that motivated it, run bi-sub-r4 BI-EVAL-011 trial 1 (unclosed artifact and
artifacts array), must be rejected; the gold output must pass; each rule has a canary.
"""

from __future__ import annotations

import copy
import json
import subprocess
import sys
from pathlib import Path

import pytest

from ana_agents import REPO_ROOT

SKILL = REPO_ROOT / "skills" / "ana-brand-intel"
SCRIPT = SKILL / "scripts" / "validate_output.py"
GOLD = Path(__file__).parent / "fixtures" / "gold-bi-eval-001.json"
R4_MALFORMED = SKILL / "reports" / "evals" / "bi-sub-r4" / "raw" / "BI-EVAL-011.trial1.json"

sys.path.insert(0, str(SCRIPT.parent))
import validate_output  # noqa: E402


@pytest.fixture
def gold():
    return json.loads(GOLD.read_text(encoding="utf-8"))


def _art(answer, kind):
    return next(a for a in answer["artifacts"] if a["artifact_type"] == kind)


def test_gold_passes_cli(tmp_path):
    answer = tmp_path / "a.json"
    answer.write_text(GOLD.read_text(encoding="utf-8"), encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), str(answer)], capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout
    assert "0 problems" in result.stdout


def test_recorded_malformed_answer_is_rejected(tmp_path):
    raw = json.loads(R4_MALFORMED.read_text(encoding="utf-8"))
    content = raw["choices"][0]["message"]["content"]
    problems = validate_output.check_text(content)
    assert len(problems) == 1 and problems[0].startswith("invalid JSON at line"), problems
    answer = tmp_path / "a.json"
    answer.write_text(content, encoding="utf-8")
    result = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), str(answer)], capture_output=True, text=True
    )
    assert result.returncode == 1


def test_misnested_summary_is_rejected(gold):
    hyp = _art(gold, "CollaborationHypothesis")
    hyp["operator_summary"] = gold.pop("operator_summary")
    problems = validate_output.check_answer(gold)
    assert any("nested inside" in p for p in problems)
    assert any("operator_summary" in p and "non-empty" in p for p in problems)


CANARIES = {
    "email_draft": (
        lambda a: a["artifacts"].append({**_art(a, "AnaBrandFit"), "artifact_type": "EmailDraft"}),
        "not a Brand Intel output",
    ),
    "duplicate_type": (
        lambda a: a["artifacts"].append(copy.deepcopy(_art(a, "AnaBrandFit"))),
        "second AnaBrandFit",
    ),
    "missing_envelope": (lambda a: _art(a, "ContactProfile").pop("run_id"), "missing envelope"),
    "mixed_run_ids": (lambda a: _art(a, "ContactProfile").update(run_id="run-x"), "several run_id"),
    "runtime_producer": (
        lambda a: _art(a, "AnaBrandFit").update(producer={"kind": "runtime", "id": "x"}),
        "producer must be",
    ),
    "non_canonical_class": (
        lambda a: _art(a, "BrandResearch")["claims"][0].update(epistemic_status="LIKELY"),
        "not canonical",
    ),
    "fact_without_source": (
        lambda a: _art(a, "BrandResearch")["claims"][0].update(source_ids=[]),
        "FACT without source_ids",
    ),
    "research_stop_followed": (
        lambda a: _art(a, "BrandResearch").update(research_outcome="INSUFFICIENT_EVIDENCE"),
        "research stop emits",
    ),
    "hypothesis_after_no_fit": (
        lambda a: _art(a, "AnaBrandFit").update(fit_outcome="NO_FIT"),
        "must not be followed by hypotheses",
    ),
    "four_hypotheses": (
        lambda a: _art(a, "CollaborationHypothesis")["hypotheses"].extend(
            copy.deepcopy(_art(a, "CollaborationHypothesis")["hypotheses"]) * 3
        ),
        "1 to 3 items",
    ),
    "no_research": (
        lambda a: a["artifacts"].remove(_art(a, "BrandResearch")),
        "BrandResearch is missing",
    ),
}


def test_gold_has_no_problems(gold):
    assert validate_output.check_answer(gold) == []


@pytest.mark.parametrize("name", sorted(CANARIES))
def test_canary(gold, name):
    mutate, expected = CANARIES[name]
    mutate(gold)
    problems = validate_output.check_answer(gold)
    assert any(expected in p for p in problems), problems
