"""Integrity gate for the reviewed curated reference-solution snapshot."""

from collections import Counter

from backend.exercise_bank import EXERCISES
from backend.reference_solution_review import (
    REVIEWED_CORPORA,
    REVIEW_POLICY,
    REVIEW_POLICY_ID,
    corpus_digest,
    reference_solution_review_status,
    reviewed_corpus_status,
)


def test_review_snapshot_covers_the_complete_curated_language_corpora() -> None:
    counts = Counter(item.get("language", "python") for item in EXERCISES.values())
    assert counts == {"python": 400, "java": 150, "sql": 150}
    assert {language: snapshot.exercise_count for language, snapshot in REVIEWED_CORPORA.items()} == counts

    for language, snapshot in REVIEWED_CORPORA.items():
        count, digest = corpus_digest(EXERCISES, language)
        assert count == snapshot.exercise_count
        assert digest == snapshot.corpus_sha256
        assert reviewed_corpus_status(EXERCISES, language).reviewed is True


def test_every_curated_reference_is_bound_to_the_best_answer_review_policy() -> None:
    assert REVIEW_POLICY_ID == "kitcode-reference-best-v1"
    assert "Big-O time" in REVIEW_POLICY
    assert "auxiliary space" in REVIEW_POLICY
    assert "fewest" in REVIEW_POLICY
    assert "readability" in REVIEW_POLICY

    for exercise in EXERCISES.values():
        status = reference_solution_review_status(exercise, EXERCISES)
        assert status.reviewed is True, (exercise["id"], status.reason)
        assert status.policy_id == REVIEW_POLICY_ID


def test_any_reference_source_change_invalidates_its_language_review_snapshot() -> None:
    altered = dict(EXERCISES)
    original = dict(altered["number-001"])
    original["solution"] += "\n# review-invalidating change\n"
    altered["number-001"] = original

    status = reference_solution_review_status(original, altered)
    assert status.reviewed is False
    assert status.reason == "The curated reference corpus changed after this review snapshot."

    changed_contract = dict(EXERCISES)
    contract_record = dict(changed_contract["number-001"])
    contract_record["expected_complexity"] = "O(n) time, O(1) space"
    changed_contract["number-001"] = contract_record
    assert reference_solution_review_status(
        contract_record,
        changed_contract,
    ).reviewed is False
