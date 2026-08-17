"""Focused release checks for curated Hard exercises 359--363."""
from __future__ import annotations

from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from backend.exercise_bank import EXERCISES
from backend.python_curated_359_363 import PYTHON_CURATED_359_363


SOURCE = Path("backend/python_curated_359_363.py")
REQUIRED = {"id", "language", "title", "difficulty", "topics", "practice_frequency",
            "description", "constraints", "hints", "expected_complexity", "starter_code",
            "solution", "examples", "public_tests", "hidden_tests"}


def _normalise(source: str) -> str:
    return re.sub(r"\s+", " ", source).strip().casefold()


def test_exact_hard_manifest_and_complete_schema() -> None:
    items = PYTHON_CURATED_359_363
    assert [item["id"] for item in items] == [f"python-curated-{number}" for number in range(359, 364)]
    assert Counter(item["difficulty"] for item in items) == {"Hard": 5}
    assert len({item["title"].casefold() for item in items}) == 5
    for item in items:
        assert REQUIRED <= item.keys()
        assert item["language"] == "python" and item["topics"]
        assert len(item["hints"]) >= 3 and item["constraints"] and item["expected_complexity"]
        assert len(item["public_tests"]) == 2 and len(item["hidden_tests"]) == 4
        cases = item["public_tests"] + item["hidden_tests"]
        assert len({(case["input"], case["expected_output"]) for case in cases}) == 6
        assert all(case["input"].endswith("\n") for case in cases)


def test_no_title_description_or_solution_collision_with_existing_python_catalog() -> None:
    current = PYTHON_CURATED_359_363
    current_ids = {item["id"] for item in current}
    prior = [item for item in EXERCISES.values()
             if item.get("language", "python") == "python" and item["id"] not in current_ids]
    for key in ("title", "description", "solution"):
        prior_values = {_normalise(item[key]) for item in prior}
        assert not prior_values & {_normalise(item[key]) for item in current}, key
    high_similarity = [(item["id"], previous["id"])
                       for item in current for previous in prior
                       if SequenceMatcher(None, _normalise(item["description"]),
                                          _normalise(previous["description"])).ratio() >= 0.72]
    assert not high_similarity, high_similarity


def test_source_has_expected_advanced_techniques() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    for token in ("MOD=1_000_000_007", "heavy", "roots", "insert", "events.sort"):
        assert token in source
    assert "subprocess" not in source and "exec(" not in source


def test_all_30_reference_fixtures_execute_in_isolated_python() -> None:
    with tempfile.TemporaryDirectory() as folder:
        program = Path(folder) / "reference.py"
        cases_run = 0
        for exercise in PYTHON_CURATED_359_363:
            program.write_text(exercise["solution"], encoding="utf-8")
            for case in exercise["public_tests"] + exercise["hidden_tests"]:
                result = subprocess.run([sys.executable, "-I", str(program)], input=case["input"],
                                        text=True, capture_output=True, timeout=4, check=False)
                assert result.returncode == 0, (exercise["id"], result.stderr)
                assert result.stdout.rstrip("\r\n") == case["expected_output"].rstrip("\r\n"), exercise["id"]
                cases_run += 1
        assert cases_run == 30
