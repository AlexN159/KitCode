"""Release gates for the curated Java 61--80 tranche."""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from backend import main
from backend.java_curriculum_part1 import JAVA_CURRICULUM_PART1
from backend.java_interview_bank import JAVA_INTERVIEW_EXERCISES
from backend.multilang_bank import MULTILANG_EXERCISES


SOURCE_PATH = Path("backend/java_curriculum_part1.py")

# Human-reviewed canonical concepts.  These are intentionally explicit rather
# than inferred from title words: variants such as two-sum-values are still
# semantic duplicates of two-sum-indices for a curated core catalogue.
PRIOR_CONCEPTS = {
    "two-sum", "valid-parentheses", "longest-unique-substring", "minimum-target-window",
    "binary-search-first-target", "rotated-search", "product-except-self", "max-subarray",
    "merge-intervals", "meeting-rooms", "min-stack", "next-greater", "daily-warmer",
    "flood-fill", "islands", "course-schedule", "unweighted-shortest-path", "tree-height",
    "validate-bst", "climb-stairs", "coin-change", "house-robber", "lis", "jump-game",
    "gas-station", "anagram", "group-anagrams", "top-k-frequent", "kth-largest", "queue",
    "spiral-matrix", "set-matrix-zeroes", "rotate-matrix", "word-search", "container-water",
    "three-sum", "longest-consecutive", "rotated-minimum", "integer-square-root", "decode-ways",
    "partition-labels", "reorganize-string", "reverse-linked-list", "lru", "array-sum",
    "array-maximum", "array-minimum", "count-even", "sum-odd", "count-positive", "array-range",
    "first-plus-last", "reverse-array", "nondecreasing-array", "reverse-text", "count-vowels",
    "palindrome", "count-words", "first-uppercase", "count-distinct-integers",
}

PART_CONCEPTS = {
    "sum-positive-values", "first-threshold-index", "interior-peak-count", "stable-move-zeroes",
    "signed-array-rotation", "stable-parity-partition", "next-permutation", "first-vowel-index",
    "longest-repeated-run", "word-initials", "reverse-word-order", "run-length-encode",
    "camel-to-snake", "adjacent-pair-cancellation", "unique-sorted-intersection",
    "first-nonrepeating-index", "postfix-evaluation", "stock-span", "sliding-window-maximum",
    "canonical-unix-path",
}


def _normalise(source: str) -> str:
    return re.sub(r"\s+", "", source)


def test_release_shape_and_literal_fixture_contract() -> None:
    assert [item["id"] for item in JAVA_CURRICULUM_PART1] == [f"java-curated-{n:03d}" for n in range(61, 81)]
    assert {item["difficulty"] for item in JAVA_CURRICULUM_PART1} == {"Easy", "Medium", "Hard"}
    assert sum(item["difficulty"] == "Easy" for item in JAVA_CURRICULUM_PART1) == 5
    assert sum(item["difficulty"] == "Medium" for item in JAVA_CURRICULUM_PART1) == 12
    assert sum(item["difficulty"] == "Hard" for item in JAVA_CURRICULUM_PART1) == 3
    assert all(len(item["public_tests"]) == 2 and len(item["hidden_tests"]) == 4 for item in JAVA_CURRICULUM_PART1)
    assert all(len(item["hints"]) == 3 and len(item["constraints"]) >= 1 for item in JAVA_CURRICULUM_PART1)
    assert all(case["input"] and "expected_output" in case for item in JAVA_CURRICULUM_PART1 for case in item["public_tests"] + item["hidden_tests"])


def test_manifest_prevents_semantic_overlap_and_titles_or_sources_do_not_repeat() -> None:
    assert len(PART_CONCEPTS) == len(JAVA_CURRICULUM_PART1)
    assert PRIOR_CONCEPTS.isdisjoint(PART_CONCEPTS)
    prior = [item for item in JAVA_INTERVIEW_EXERCISES + MULTILANG_EXERCISES if item.get("language") == "java"]
    prior_titles = {item["title"].casefold() for item in prior}
    prior_sources = {_normalise(item["solution"]) for item in prior}
    titles = [item["title"].casefold() for item in JAVA_CURRICULUM_PART1]
    sources = [_normalise(item["solution"]) for item in JAVA_CURRICULUM_PART1]
    assert not prior_titles.intersection(titles)
    assert not prior_sources.intersection(sources)
    assert len(set(titles)) == len(titles)
    assert len(set(sources)) == len(sources)


def test_module_is_import_pure_and_fixture_expectations_are_literal() -> None:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    assert "_revise" not in source and "_array_cases" not in source and "lambda" not in source
    assert "subprocess" not in source and "sqlite" not in source and "requests" not in source
    tree = ast.parse(source)
    fixture_calls = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "case"]
    assert len(fixture_calls) == 120
    assert all(len(node.args) == 2 and all(isinstance(arg, ast.Constant) and isinstance(arg.value, str) for arg in node.args) for node in fixture_calls)


@pytest.mark.skipif(not all(main._java_tools()), reason="Java curriculum checks require a local JDK")
@pytest.mark.parametrize("exercise", JAVA_CURRICULUM_PART1, ids=lambda item: item["id"])
def test_reference_program_passes_every_fixture(exercise: dict) -> None:
    tests = [("public", item) for item in exercise["public_tests"]]
    tests += [("hidden", item) for item in exercise["hidden_tests"]]
    result = main._validate_java_submission(tests, exercise["solution"], 4.0)
    assert result["status"] == "passed", result
