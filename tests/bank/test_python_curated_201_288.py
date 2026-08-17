"""Release checks for the beginner Python extension 201--288."""
from __future__ import annotations

import ast
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from backend.python_curated_201_288 import PYTHON_CURATED_201_288
from backend.exercise_bank import EXERCISES, _public_view, validate_submission


SOURCE = Path("backend/python_curated_201_288.py")
REQUIRED = {
    "id", "language", "title", "difficulty", "topics", "practice_frequency",
    "description", "constraints", "hints", "expected_complexity", "starter_code",
    "solution", "examples", "public_tests", "hidden_tests",
}


def _normalise(source: str) -> str:
    return re.sub(r"\s+", " ", source).strip().casefold()


def test_manifest_is_exactly_88_new_easy_exercises() -> None:
    items = PYTHON_CURATED_201_288
    assert len(items) == 88
    assert [item["id"] for item in items] == [f"python-curated-{number:03d}" for number in range(201, 289)]
    assert Counter(item["difficulty"] for item in items) == {"Easy": 88}
    assert len({item["title"].casefold() for item in items}) == 88
    assert all(item["language"] == "python" for item in items)


def test_every_exercise_has_the_complete_runner_schema_and_line_aware_copy() -> None:
    for item in PYTHON_CURATED_201_288:
        assert REQUIRED <= item.keys(), item["id"]
        assert item["topics"] and item["constraints"] and len(item["hints"]) == 3
        assert "line" in item["description"].casefold(), item["id"]
        assert "O(" in item["expected_complexity"]
        assert "def solve()" in item["solution"]
        is_class_drill = item.get("submission_mode") == "python_class"
        if is_class_drill:
            requirement = item["required_class"]
            assert set(requirement) == {"name", "methods"}
            assert requirement["name"] in item["starter_code"]
            assert f"class {requirement['name']}:" in item["solution"]
            # Run uses this learner-visible driver; Submit instead uses the
            # private per-fixture harness below.
            assert "def solve()" in item["starter_code"]
            assert (f"{requirement['name']}(" in item["starter_code"]
                    or f"{requirement['name']}." in item["starter_code"])
            for method in requirement["methods"]:
                if method != "__init__":
                    assert f".{method}(" in item["starter_code"]
        else:
            assert "def solve()" in item["starter_code"]
        assert len(item["examples"]) == 1
        assert len(item["public_tests"]) == 2 and len(item["hidden_tests"]) == 2
        for case in item["public_tests"] + item["hidden_tests"]:
            expected_keys = {"input", "expected_output", "harness"} if is_class_drill else {"input", "expected_output"}
            assert set(case) == expected_keys
            if is_class_drill:
                assert "submission_class" in case["harness"]
            assert case["input"].endswith("\n")


def test_module_is_data_only_and_contains_88_explicit_add_calls() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert "subprocess" not in source and "exec(" not in source
    assert not any(ord(char) > 127 or (ord(char) < 32 and char not in "\r\n\t") for char in source)
    tree = ast.parse(source)
    calls = [node.value for node in tree.body if isinstance(node, ast.Expr)
             and isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name)
             and node.value.func.id == "add"]
    assert len(calls) == 88
    assert [call.args[0].value for call in calls] == list(range(201, 289))


def test_no_duplicate_title_description_or_reference_solution_in_existing_python_catalog() -> None:
    current = PYTHON_CURATED_201_288
    current_ids = {item["id"] for item in current}
    existing = [
        item for item in EXERCISES.values()
        if item.get("language", "python") == "python" and item["id"] not in current_ids
    ]
    existing_titles = {_normalise(item["title"]) for item in existing}
    existing_descriptions = {_normalise(item["description"]) for item in existing}
    existing_solutions = {_normalise(item["solution"]) for item in existing}
    assert not existing_titles & {_normalise(item["title"]) for item in current}
    assert not existing_descriptions & {_normalise(item["description"]) for item in current}
    assert not existing_solutions & {_normalise(item["solution"]) for item in current}
    high_similarity = [
        (item["id"], prior["id"], SequenceMatcher(None, _normalise(item["description"]),
                                                     _normalise(prior["description"])).ratio())
        for item in current for prior in existing
        if SequenceMatcher(None, _normalise(item["description"]), _normalise(prior["description"])).ratio() >= 0.72
    ]
    assert not high_similarity, high_similarity


def test_representative_contracts_cover_numbers_text_lists_and_decisions() -> None:
    by_id = {item["id"]: item for item in PYTHON_CURATED_201_288}
    assert by_id["python-curated-204"]["public_tests"][1]["expected_output"] == "-3"
    assert by_id["python-curated-218"]["hidden_tests"][1]["expected_output"] == "42"
    assert "one integer per line" in by_id["python-curated-212"]["description"]
    assert by_id["python-curated-242"]["public_tests"][1]["expected_output"] == "19"
    assert by_id["python-curated-249"]["hidden_tests"][0]["expected_output"] == "Y"
    assert by_id["python-curated-253"]["public_tests"][0]["expected_output"] == "red-green-blue"
    assert by_id["python-curated-272"]["public_tests"][0]["expected_output"] == "6"
    assert by_id["python-curated-281"]["required_class"]["methods"] == ["__init__", "area", "perimeter"]
    assert by_id["python-curated-284"]["required_class"]["name"] == "Temperature"
    assert by_id["python-curated-288"]["hidden_tests"][1]["expected_output"] == "0"


def test_output_heavy_easy_exercises_fit_the_local_run_and_stdin_caps() -> None:
    """Keep valid beginner inputs and their printed answers inside the UI limits."""
    by_id = {item["id"]: item for item in PYTHON_CURATED_201_288}
    list_ids = ("python-curated-236", "python-curated-237", "python-curated-262",
                "python-curated-265", "python-curated-266")
    for exercise_id in list_ids:
        constraints = by_id[exercise_id]["constraints"]
        assert "1,200" in " ".join(constraints)
        assert "-1,000,000 and 1,000,000" in " ".join(constraints)

        # At most 1,200 signed seven-digit values plus 1,199 spaces and a
        # trailing newline are emitted.  The same line-based input is below
        # the 12,000-character custom-stdin limit.
        assert 1_200 * len("-1000000") + 1_199 + 1 <= 22_000
        assert len("1200\n") + 1_200 * len("-1000000") + 1_199 + 1 <= 12_000

    words = by_id["python-curated-253"]["constraints"]
    assert "n <= 500" in " ".join(words)
    assert "word length <= 20" in " ".join(words)
    # 500 20-character words joined with 499 hyphens; input uses one line
    # per word, so it remains under the same custom-stdin cap.
    assert 500 * 20 + 499 + 1 <= 22_000
    assert len("500\n") + 500 * (20 + 1) <= 12_000


def test_easy_class_cli_contracts_fit_the_local_run_and_stdin_caps() -> None:
    by_id = {item["id"]: item for item in PYTHON_CURATED_201_288}
    class_items = [by_id[f"python-curated-{number:03d}"] for number in range(281, 289)]
    for item in class_items:
        constraints = item["constraints"]
        assert "The complete CLI input is at most 12,000 characters" in constraints
        assert "The complete CLI output is at most 22,000 characters" in constraints

    assert "There are at most 500 commands" in by_id["python-curated-282"]["constraints"]
    assert "Task names contain 1 through 20 lowercase letters" in by_id["python-curated-283"]["constraints"]
    assert "There are at most 60 commands" in by_id["python-curated-283"]["constraints"]
    assert "There are at most 500 commands" in by_id["python-curated-285"]["constraints"]
    assert "The name contains 1 through 20 lowercase letters" in by_id["python-curated-287"]["constraints"]
    assert "There are at most 500 commands" in by_id["python-curated-287"]["constraints"]

    # Worst-case serialized CLI sizes implied by the natural q/value/word
    # limits. Newlines are included in each calculation.
    assert len("1000000\n500\n") + 500 * len("add 1000000\n") <= 12_000  # 282
    assert 500 * (len("501000000") + 1) <= 22_000
    assert len("60\n") + 60 * len("complete " + "x" * 20 + "\n") <= 12_000  # 283
    assert 21 * 30 * 30 <= 22_000  # 30 adds then 30 maximum-width pending results
    assert len("1000000\n500\n") + 500 * len("withdraw 1000000\n") <= 12_000  # 285
    assert 500 * (len("501000000") + 1) <= 22_000
    assert len("1000\n") + 1_000 * len("average\n") <= 12_000  # 286
    assert 1_000 * len("100\n") <= 22_000
    assert len("x" * 20 + "\n500\n") + 500 * len("status\n") <= 12_000  # 287
    assert 500 * len("x" * 20 + " 5 10\n") <= 22_000
    assert len("1000000\n1000\n") + 1_000 * len("remaining\n") <= 12_000  # 288
    assert 1_000 * len("1000000\n") <= 22_000


def test_every_reference_solution_passes_public_and_hidden_cases_in_isolated_python() -> None:
    with tempfile.TemporaryDirectory() as folder:
        program = Path(folder) / "reference.py"
        for exercise in PYTHON_CURATED_201_288:
            program.write_text(exercise["solution"], encoding="utf-8")
            for case in exercise["public_tests"] + exercise["hidden_tests"]:
                result = subprocess.run([sys.executable, "-I", str(program)], input=case["input"],
                                        text=True, capture_output=True, timeout=3, check=False)
                assert result.returncode == 0, (exercise["id"], result.stderr)
                assert result.stdout.rstrip("\r\n") == case["expected_output"].rstrip("\r\n"), exercise["id"]


def test_class_drills_use_private_harnesses_and_the_real_class_runner() -> None:
    class_items = [item for item in PYTHON_CURATED_201_288 if item.get("submission_mode") == "python_class"]
    assert [item["id"] for item in class_items] == [f"python-curated-{number:03d}" for number in range(281, 289)]
    previous = {item["id"]: EXERCISES.get(item["id"]) for item in class_items}
    try:
        EXERCISES.update({item["id"]: item for item in class_items})
        for item in class_items:
            public_view = _public_view(item, include_hidden=True)
            assert "harness" not in repr(public_view)
            result = validate_submission(item["id"], item["solution"])
            assert result["status"] == "passed", (item["id"], result)
            assert result["passed"] == result["total"] == 4
    finally:
        for exercise_id, prior in previous.items():
            if prior is None:
                EXERCISES.pop(exercise_id, None)
            else:
                EXERCISES[exercise_id] = prior
