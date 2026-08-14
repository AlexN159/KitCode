"""Release gates for the curated Java 81--100 tranche."""
from __future__ import annotations

import ast
import re
from pathlib import Path

import pytest

from backend import main
from backend.java_curriculum_part1 import JAVA_CURRICULUM_PART1
from backend.java_curriculum_part2 import JAVA_CURRICULUM_PART2
from backend.java_practice_bank import JAVA_PRACTICE_EXERCISES
from backend.multilang_bank import MULTILANG_EXERCISES


SOURCE_PATH = Path("backend/java_curriculum_part2.py")

# These are deliberately semantic labels rather than a title-keyword heuristic.
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
    "sum-positive-values", "first-threshold-index", "interior-peak-count", "stable-move-zeroes",
    "signed-array-rotation", "stable-parity-partition", "next-permutation", "first-vowel-index",
    "longest-repeated-run", "word-initials", "reverse-word-order", "run-length-encode",
    "camel-to-snake", "adjacent-pair-cancellation", "unique-sorted-intersection",
    "first-nonrepeating-index", "postfix-evaluation", "stock-span", "sliding-window-maximum",
    "canonical-unix-path",
}
PART_CONCEPTS = {
    "integer-cube-root", "mountain-peak-index", "first-last-occurrence", "best-price-pair",
    "longest-ones-with-flips", "longest-two-distinct", "stock-trade-with-days",
    "circular-next-greater", "asteroid-collision", "bracket-decoder", "stack-pop-sequence",
    "kth-smallest-sorted-matrix", "inversion-count", "minimum-swaps-distinct-sort",
    "weighted-interval-scheduling", "task-cooldown", "minimum-window-subsequence",
    "earliest-longest-palindrome", "palindromic-substring-count", "wildcard-match",
}


def _normalise(source: str) -> str:
    return re.sub(r"\s+", "", source)


def test_release_shape_and_literal_fixture_contract() -> None:
    assert [x["id"] for x in JAVA_CURRICULUM_PART2] == [f"java-curated-{n:03d}" for n in range(81, 101)]
    assert [sum(x["difficulty"] == level for x in JAVA_CURRICULUM_PART2) for level in ("Easy", "Medium", "Hard")] == [2, 15, 3]
    assert all(len(x["public_tests"]) == 2 and len(x["hidden_tests"]) == 4 for x in JAVA_CURRICULUM_PART2)
    assert all(len(x["hints"]) == 3 and x["constraints"] and x["expected_complexity"] for x in JAVA_CURRICULUM_PART2)
    assert all(c["input"] is not None and "expected_output" in c for x in JAVA_CURRICULUM_PART2 for c in x["public_tests"] + x["hidden_tests"])


def test_manifest_blocks_prior_semantic_overlap_and_repetition() -> None:
    assert len(PART_CONCEPTS) == len(JAVA_CURRICULUM_PART2)
    assert PRIOR_CONCEPTS.isdisjoint(PART_CONCEPTS)
    prior = [x for x in JAVA_PRACTICE_EXERCISES + MULTILANG_EXERCISES if x.get("language") == "java"] + JAVA_CURRICULUM_PART1
    titles = [x["title"].casefold() for x in JAVA_CURRICULUM_PART2]
    sources = [_normalise(x["solution"]) for x in JAVA_CURRICULUM_PART2]
    assert not set(titles).intersection(x["title"].casefold() for x in prior)
    assert not set(sources).intersection(_normalise(x["solution"]) for x in prior)
    assert len(set(titles)) == len(titles)
    assert len(set(sources)) == len(sources)


def test_import_purity_literal_fixtures_no_mojibake_or_dead_sources() -> None:
    source = SOURCE_PATH.read_text(encoding="utf-8")
    assert not any(token in source for token in ("subprocess", "sqlite", "requests", "lambda", "Exit code:", "\ufffd", "\u00c2"))
    tree = ast.parse(source)
    fixtures = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == "case"]
    assert len(fixtures) == 120
    assert all(len(n.args) == 2 and all(isinstance(a, ast.Constant) and isinstance(a.value, str) for a in n.args) for n in fixtures)
    assert source.count("drill(") == 21  # helper declaration plus 20 one-and-only records


def test_output_heavy_contracts_fit_the_java_runner_limit() -> None:
    # MAX_OUTPUT is 24,000 bytes. A signed int plus a separator needs at most
    # 12 bytes, while decoded/source substrings are explicitly capped at 20k.
    circular, asteroids, decoded = JAVA_CURRICULUM_PART2[7], JAVA_CURRICULUM_PART2[8], JAVA_CURRICULUM_PART2[9]
    assert any("1,900" in constraint for constraint in circular["constraints"])
    assert any("1,900" in constraint for constraint in asteroids["constraints"])
    assert 1_900 * 12 < 24_000
    assert any("20,000 characters" in constraint for constraint in decoded["constraints"])


def test_complexities_include_reference_input_storage_and_difficulties_are_defensible() -> None:
    by_id = {item["id"]: item for item in JAVA_CURRICULUM_PART2}
    for exercise_id in ("java-curated-082", "java-curated-083", "java-curated-085"):
        assert "O(n) auxiliary space" in by_id[exercise_id]["expected_complexity"]
    assert "O(n^2) auxiliary space" in by_id["java-curated-092"]["expected_complexity"]
    assert by_id["java-curated-096"]["difficulty"] == "Medium"
    assert by_id["java-curated-098"]["difficulty"] == "Medium"
    assert by_id["java-curated-099"]["difficulty"] == "Medium"


@pytest.mark.skipif(not all(main._java_tools()), reason="Java curriculum checks require a local JDK")
@pytest.mark.parametrize("exercise", JAVA_CURRICULUM_PART2, ids=lambda x: x["id"])
def test_every_reference_program_passes_public_and_hidden_fixtures(exercise: dict) -> None:
    fixtures = [("public", x) for x in exercise["public_tests"]] + [("hidden", x) for x in exercise["hidden_tests"]]
    result = main._validate_java_submission(fixtures, exercise["solution"], 4.0)
    assert result["status"] == "passed", result
