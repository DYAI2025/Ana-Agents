#!/usr/bin/env python3
"""Validate that a recorded live eval run is execution evidence for a given skill digest.

ABI-016 / SPEC EVAL-006: a semantic/model PASS may only be claimed when the evaluation
actually executed. This check turns a run directory into evidence or rejects it:

  EV_NOT_EXECUTED      report does not declare executed=true
  EV_DIRTY_TREE        run was made from an uncommitted tree (exploratory only)
  EV_DIGEST            run is bound to a different skill content digest than expected
  EV_SUITE_DRIFT       suite, grading file or grader differ from the current ones
  EV_CASES             the run does not cover every case of the current suite
  EV_TRIALS            a case has fewer graded trials than --min-trials, or a NOT_RUN trial
  EV_RAW               a raw response file is missing or its sha256 differs
  EV_REGRADE           re-grading a raw response does not reproduce the recorded verdict
  EV_STATUS            the recorded overall/case status disagrees with the trial verdicts
  EV_COMMIT            git_head is unknown to this repository, or the skill tree at that
                       commit does not have the bound digest

Exit status: 0 the run is valid PASS evidence for the digest, 1 any finding, 2 usage error.
The runtime the run used is printed; this check does not turn a non-target runtime into
target-runtime evidence.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ana_agents.skill_evals.brand_intel import load_suite
from run_brand_intel_evals import (
    REPO_ROOT,
    SKILL_DIR,
    SUITE,
    grade_trial,
    suite_drift,
)
from skill_digest import content_digest, sha256_bytes


def digest_at_commit(commit: str) -> str | None:
    rel = SKILL_DIR.relative_to(REPO_ROOT).as_posix()
    with tempfile.TemporaryDirectory() as tmp:
        archive = subprocess.run(
            ["git", "archive", commit, rel], cwd=REPO_ROOT, capture_output=True, check=False
        )
        if archive.returncode != 0:
            return None
        subprocess.run(["tar", "-x", "-C", tmp], input=archive.stdout, check=True)
        return content_digest(Path(tmp) / rel)


def validate(run_dir: Path, expect_digest: str, min_trials: int, check_commit: bool = True):
    findings: list[tuple[str, str]] = []
    report = json.loads((run_dir / "report.json").read_text(encoding="utf-8"))
    binding = report.get("binding", {})
    if report.get("executed") is not True:
        findings.append(("EV_NOT_EXECUTED", "report.executed is not true"))
    if binding.get("skill_tree_dirty") is not False or report.get("evidence_class") != (
        "COMMITTED_TREE"
    ):
        findings.append(("EV_DIRTY_TREE", f"evidence_class={report.get('evidence_class')}"))
    if binding.get("skill_content_digest") != expect_digest:
        findings.append(
            ("EV_DIGEST", f"run {binding.get('skill_content_digest')} != {expect_digest}")
        )
    for line in suite_drift(binding):
        findings.append(("EV_SUITE_DRIFT", line))
    if check_commit:
        head = binding.get("git_head", "")
        at_commit = digest_at_commit(head) if head else None
        if at_commit != binding.get("skill_content_digest"):
            findings.append(("EV_COMMIT", f"skill digest at {head!r} is {at_commit}"))

    _, cases = load_suite(SUITE)
    by_id = {c.case_id: c for c in cases}
    results = {r["case_id"]: r for r in report.get("results", [])}
    if set(results) != set(by_id):
        findings.append(("EV_CASES", f"run covers {sorted(results)}, suite {sorted(by_id)}"))

    drifted = any(code == "EV_SUITE_DRIFT" for code, _ in findings)
    all_pass = True
    for case_id, result in sorted(results.items()):
        trials = result.get("trials", [])
        graded = [t for t in trials if t.get("status") in ("PASS", "FAIL")]
        if len(graded) < min_trials or len(graded) != len(trials):
            findings.append(("EV_TRIALS", f"{case_id}: {len(graded)} graded of {len(trials)}"))
        for trial in graded:
            raw_path = run_dir / trial.get("raw_ref", "")
            if not raw_path.is_file() or sha256_bytes(raw_path.read_bytes()) != trial.get(
                "raw_sha256"
            ):
                findings.append(("EV_RAW", f"{case_id} trial {trial.get('trial')}"))
                continue
            if case_id in by_id and not drifted:
                regraded = grade_trial(by_id[case_id], json.loads(raw_path.read_text("utf-8")))
                if (regraded["status"], regraded["failures"]) != (
                    trial["status"],
                    trial["failures"],
                ):
                    findings.append(("EV_REGRADE", f"{case_id} trial {trial.get('trial')}"))
        case_pass = bool(graded) and all(t["status"] == "PASS" for t in trials)
        all_pass = all_pass and case_pass
        if (result.get("status") == "PASS") != case_pass:
            findings.append(("EV_STATUS", f"{case_id}: recorded {result.get('status')}"))
    if (report.get("status") == "PASS") != (all_pass and set(results) == set(by_id)):
        findings.append(("EV_STATUS", f"overall recorded {report.get('status')}"))
    if report.get("status") != "PASS":
        findings.append(("EV_STATUS", f"run status is {report.get('status')}, not PASS"))
    return report, sorted(set(findings))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("run_dir", type=Path)
    ap.add_argument("--expect-digest", help="default: current content digest of the skill")
    ap.add_argument("--min-trials", type=int, default=2)
    args = ap.parse_args()
    expect = args.expect_digest or content_digest(SKILL_DIR)
    report, findings = validate(args.run_dir, expect, args.min_trials)
    for code, detail in findings:
        print(f"{code}  {detail}")
    runtime = report.get("runtime", {})
    print(
        f"run {report.get('run_id')}: runtime {runtime.get('kind')} "
        f"models {runtime.get('resolved_models')}; digest {expect}"
    )
    print("EVIDENCE_VALID" if not findings else f"EVIDENCE_INVALID ({len(findings)} findings)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
