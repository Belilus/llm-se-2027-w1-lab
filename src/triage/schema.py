"""Typed records on both sides of the model boundary.

Everything in this module is fully typed. Values only get here after
`extract.py` has validated the raw model output against `TriageRecord`.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

IssueType = Literal["bug", "enhancement", "documentation", "question", "meta"]
Severity = Literal["low", "medium", "high", "critical"]

ISSUE_TYPES: tuple[IssueType, ...] = ("bug", "enhancement", "documentation", "question", "meta")
SEVERITIES: tuple[Severity, ...] = ("low", "medium", "high", "critical")

MAX_BODY_CHARS = 8_000
MAX_RAW_OUTPUT_CHARS = 2_000


class Issue(BaseModel):
    """The only issue fields triage is allowed to read.

    Labels, comments and every `gold_*` field are deliberately absent: labels
    are where the gold answers come from, and comments do not exist yet when a
    new issue arrives.
    """

    model_config = ConfigDict(frozen=True)

    repo: str
    number: int = Field(gt=0)
    title: str
    body: str = ""


class TriageRecord(BaseModel):
    """One structured triage record. Identity fields come from the input, never the model."""

    model_config = ConfigDict(frozen=True, extra="forbid", strict=True)

    repo: str
    number: int = Field(gt=0)
    issue_type: IssueType
    component: str | None = Field(max_length=40)
    severity: Severity
    has_reproduction_steps: bool
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str = Field(min_length=1, max_length=200)
    model: str


class TriageFailure(BaseModel):
    """Emitted when the model output could not be validated after one retry."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    repo: str
    number: int
    reason: str
    raw_output: str = Field(max_length=MAX_RAW_OUTPUT_CHARS)
    model: str


TriageResult = TriageRecord | TriageFailure
