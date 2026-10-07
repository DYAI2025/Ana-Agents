"""validate_eval_evidence.py turns a run directory into PASS evidence or rejects it (ABI-016).

The fixture run below holds one real graded trial (the gold BI-EVAL-001 output) bound to the
current tree, so its only expected finding is incomplete case coverage. Each mutation must
add exactly its own finding code.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from ana_agents import REPO_ROOT

sys.path.insert(0, str(REPO_ROOT / "scripts"))
import run_brand_intel_evals as runner
import validate_eval_evidence as evidence
from ana_agents.skill_evals.brand_intel import load_suite
from skill_digest import content_digest, sha256_bytes

GOLD = Path(__file__).parent / "fixtures" / "gold-bi-eval-001.json"
DIGEST = content_digest(runner.SKILL_DIR)


def _run_dir(tmp_path: Path) -> Path:
    _, cases = load_suite(runner.SUITE)
    case = next(c for c in cases if c.case_id == "BI-EVAL-001")
    raw = runner.exchange_answer("fixture-model", GOLD.read_text(encoding="utf-8"))
    run = tmp_path / "run"
    (run / "raw").mkdir(parents=True)
    raw_path = run / "raw" / "BI-EVAL-001.trial1.json"
    raw_path.write_text(json.dumps(raw), encoding="utf-8")
    trials = []
    for n in (1, 2):
        graded = runner.grade_trial(case, raw)
        graded.update(trial=n, raw_ref="raw/BI-EVAL-001.trial1.json")
        graded["raw_sha256"] = sha256_bytes(raw_path.read_bytes())
        trials.append(graded)
    assert all(t["status"] == "PASS" for t in trials)
    report = {
        "run_id": "fixture",
        "executed": True,
        "evidence_class": "COMMITTED_TREE",
        "status": "PASS",
        "runtime": {"kind": "fixture", "resolved_models": ["fixture-model"]},
        "binding": {
            "skill_content_digest": DIGEST,
            "skill_tree_dirty": False,
            "suite_sha256": sha256_bytes(runner.SUITE.read_bytes()),
            "grading_sha256": sha256_bytes(runner.DEFAULT_GRADING.read_bytes()),
            "grader_sha256": sha256_bytes(Path(runner.grader_module.__file__).read_bytes()),
        },
        "results": [{"case_id": "BI-EVAL-001", "status": "PASS", "trials": trials}],
    }
    (run / "report.json").write_text(json.dumps(report), encoding="utf-8")
    return run


def codes(run: Path, **kw) -> set[str]:
    _, findings = evidence.validate(run, DIGEST, 2, check_commit=False, **kw)
    return {code for code, _ in findings}


def _edit(run: Path, fn) -> None:
    report = json.loads((run / "report.json").read_text())
    fn(report)
    (run / "report.json").write_text(json.dumps(report))


def test_well_formed_single_case_run_only_lacks_coverage(tmp_path):
    assert codes(_run_dir(tmp_path)) == {"EV_CASES", "EV_STATUS"}


MUTATIONS = {
    "not_executed": (lambda r: r.update(executed=False), "EV_NOT_EXECUTED"),
    "dirty_tree": (lambda r: r["binding"].update(skill_tree_dirty=True), "EV_DIRTY_TREE"),
    "other_digest": (
        lambda r: r["binding"].update(skill_content_digest="sha256:" + "0" * 64),
        "EV_DIGEST",
    ),
    "suite_drift": (lambda r: r["binding"].update(grading_sha256="0" * 64), "EV_SUITE_DRIFT"),
    "one_trial": (lambda r: r["results"][0]["trials"].pop(), "EV_TRIALS"),
    "verdict_flipped": (
        lambda r: r["results"][0]["trials"][0].update(status="FAIL"),
        "EV_REGRADE",
    ),
    "raw_hash": (
        lambda r: r["results"][0]["trials"][0].update(raw_sha256="0" * 64),
        "EV_RAW",
    ),
}


@pytest.mark.parametrize("name", sorted(MUTATIONS))
def test_mutation_is_rejected(tmp_path, name):
    mutate, code = MUTATIONS[name]
    run = _run_dir(tmp_path)
    _edit(run, mutate)
    assert code in codes(run) - {"EV_CASES"}


def test_commit_binding(tmp_path):
    assert evidence.digest_at_commit("0" * 40) is None
    head_digest = evidence.digest_at_commit("HEAD")
    assert head_digest is not None and head_digest.startswith("sha256:")
