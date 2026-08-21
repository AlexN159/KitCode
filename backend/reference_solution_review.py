"""Immutable quality-review snapshot for curated reference solutions.

The exercise bank deliberately keeps executable reference implementations with
the judge data.  This module records the editorial review boundary separately:
when a curated solution or its exercise contract changes, its language corpus
digest changes and it is no longer eligible to be described as a reviewed
*best answer* until this manifest is deliberately refreshed.
"""

from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
import json
from types import MappingProxyType
from typing import Any, Mapping


REVIEW_POLICY_ID = "kitcode-reference-best-v1"
"""The editorial rubric used for the reviewed curated corpus."""

REVIEW_POLICY = (
    "A best answer must first be correct for the exercise contract and meet "
    "the intended Big-O time bound. Among those answers, prefer lower "
    "auxiliary space. When time and space are equivalent, prefer the fewest "
    "clear, idiomatic lines. Do not code-golf: use a slightly longer answer "
    "when it materially improves naming, invariants, edge-case handling, or "
    "a human-facing API/readability requirement."
)


@dataclass(frozen=True)
class LanguageReviewSnapshot:
    """A reviewed, immutable snapshot of one language's curated corpus."""

    language: str
    exercise_count: int
    corpus_sha256: str


# These are intentionally literals rather than values calculated at import.
# Updating a reference or its contract must be accompanied by a conscious
# review and manifest refresh, rather than silently retaining the "best" label.
REVIEWED_CORPORA: Mapping[str, LanguageReviewSnapshot] = MappingProxyType({
    "python": LanguageReviewSnapshot(
        language="python",
        exercise_count=400,
        corpus_sha256="83e54f7ecc899ff8c9f1ae5f234e0161e24c663f351ad5e8c0c2cfeb5110d56d",
    ),
    "java": LanguageReviewSnapshot(
        language="java",
        exercise_count=150,
        corpus_sha256="d25047c698abca4193931a4e8167c9666f3f06b08b90229ffa027942b313b640",
    ),
    "sql": LanguageReviewSnapshot(
        language="sql",
        exercise_count=150,
        corpus_sha256="9e9de413bc02de221f11c4979b5a06ef56b2577ee8a9fe7da9c4236cfb785873",
    ),
})


@dataclass(frozen=True)
class ReferenceReviewStatus:
    """Whether a particular exercise may use the reviewed-best label."""

    reviewed: bool
    policy_id: str
    policy: str
    reason: str | None = None


def _language_of(exercise: Mapping[str, Any]) -> str:
    language = exercise.get("language", "python")
    return language if language in REVIEWED_CORPORA else ""


def corpus_digest(
    exercises: Mapping[str, Mapping[str, Any]] | list[Mapping[str, Any]],
    language: str,
) -> tuple[int, str]:
    """Return a stable digest of each reference and the contract it answers."""

    values = exercises.values() if isinstance(exercises, Mapping) else exercises
    reviewed_fields = (
        "id",
        "language",
        "title",
        "description",
        "constraints",
        "topics",
        "expected_complexity",
        "reference_complexity_note",
        "submission_mode",
        "required_class",
        "solution",
        "public_tests",
        "hidden_tests",
        "sql_setup",
        "setup_sql",
    )
    rows = [
        {field: exercise.get(field) for field in reviewed_fields}
        for exercise in values
        if _language_of(exercise) == language
    ]
    rows.sort(key=lambda row: str(row["id"]))
    encoded = json.dumps(
        rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return len(rows), sha256(encoded).hexdigest()


def reviewed_corpus_status(
    exercises: Mapping[str, Mapping[str, Any]] | list[Mapping[str, Any]],
    language: str,
) -> ReferenceReviewStatus:
    """Report whether the current language corpus still matches its review."""

    snapshot = REVIEWED_CORPORA.get(language)
    if snapshot is None:
        return ReferenceReviewStatus(False, REVIEW_POLICY_ID, REVIEW_POLICY, "Unsupported language.")
    count, digest = corpus_digest(exercises, language)
    if count != snapshot.exercise_count or digest != snapshot.corpus_sha256:
        return ReferenceReviewStatus(
            False,
            REVIEW_POLICY_ID,
            REVIEW_POLICY,
            "The curated reference corpus changed after this review snapshot.",
        )
    return ReferenceReviewStatus(True, REVIEW_POLICY_ID, REVIEW_POLICY)


def reference_solution_review_status(
    exercise: Mapping[str, Any],
    exercises: Mapping[str, Mapping[str, Any]] | list[Mapping[str, Any]],
) -> ReferenceReviewStatus:
    """Return reviewed status for one curated exercise in its full corpus.

    Generated exercises and records without a non-empty reference source never
    qualify, even when their language's curated corpus matches the snapshot.
    """

    if exercise.get("source") == "ai_generated":
        return ReferenceReviewStatus(False, REVIEW_POLICY_ID, REVIEW_POLICY, "AI-generated exercises are provisional.")
    if not isinstance(exercise.get("solution"), str) or not exercise["solution"].strip():
        return ReferenceReviewStatus(False, REVIEW_POLICY_ID, REVIEW_POLICY, "No curated reference solution is available.")
    language = _language_of(exercise)
    if not language:
        return ReferenceReviewStatus(False, REVIEW_POLICY_ID, REVIEW_POLICY, "Unsupported language.")
    return reviewed_corpus_status(exercises, language)
