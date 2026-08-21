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


def test_python_best_answers_use_the_documented_input_without_defensive_boilerplate() -> None:
    python_solutions = [
        exercise["solution"]
        for exercise in EXERCISES.values()
        if exercise.get("language", "python") == "python"
    ]

    assert all("if not tokens:" not in solution for solution in python_solutions)
    assert all("if not data:" not in solution for solution in python_solutions)
    assert all(
        "tokens = sys.stdin.read().split()" not in solution
        for solution in python_solutions
    )
    assert EXERCISES["number-001"]["solution"] == (
        "n = int(input())\n"
        "print('even' if n % 2 == 0 else 'odd')\n"
    )
    assert EXERCISES["array-001"]["solution"] == (
        "n = int(input())\n"
        "nums = list(map(int, input().split()))\n"
        "print(sum(nums))\n"
    )
    duplicate_copies = EXERCISES["drill-014"]
    assert duplicate_copies["title"] == "Duplicate Copies to Remove"
    assert duplicate_copies["description"] == (
        "Read n integers. Keep one copy of each distinct value and remove every "
        "additional copy. Print how many values are removed."
    )


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
