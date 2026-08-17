"""Release gates for the Hard object-oriented Python tranche 394--400."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from backend.exercise_bank import EXERCISES, _public_view, validate_submission
from backend.python_curated_394_400 import PYTHON_CURATED_394_400


SOURCE = Path("backend/python_curated_394_400.py")
REQUIRED = {"id", "language", "title", "difficulty", "topics", "practice_frequency", "description", "constraints", "hints", "expected_complexity", "starter_code", "solution", "examples", "public_tests", "hidden_tests", "submission_mode", "required_class"}


def normalise(value: str) -> str:
    return re.sub(r"[^a-z0-9]", "", value.casefold())


def test_exact_ids_schema_class_contracts_and_private_fixture_coverage() -> None:
    items = PYTHON_CURATED_394_400
    assert [item["id"] for item in items] == [f"python-curated-{number:03d}" for number in range(394, 401)]
    assert Counter(item["difficulty"] for item in items) == {"Hard": 7}
    assert len({normalise(item["title"]) for item in items}) == 7
    for item in items:
        assert REQUIRED <= item.keys()
        assert item["language"] == "python" and item["submission_mode"] == "python_class"
        assert len(item["hints"]) >= 3 and item["constraints"] and item["description"]
        assert len(item["public_tests"]) == 2 and len(item["hidden_tests"]) == 4
        requirement = item["required_class"]
        assert set(requirement) == {"name", "methods"} and requirement["methods"]
        assert f"class {requirement['name']}:" in item["starter_code"] and "def solve()" in item["starter_code"]
        assert f"class {requirement['name']}:" in item["solution"] and "if __name__" in item["solution"]
        fixtures = item["public_tests"] + item["hidden_tests"]
        assert len({(case["input"], case["expected_output"]) for case in fixtures}) == 6
        for case in fixtures:
            assert set(case) == {"input", "expected_output", "harness"}
            assert "submission_class" in case["harness"]


def test_reference_cli_demos_run_every_fixture() -> None:
    with tempfile.TemporaryDirectory() as directory:
        program = Path(directory) / "reference.py"
        for item in PYTHON_CURATED_394_400:
            program.write_text(item["solution"], encoding="utf-8")
            for case in item["public_tests"] + item["hidden_tests"]:
                result = subprocess.run([sys.executable, "-I", str(program)], input=case["input"], text=True, capture_output=True, timeout=4)
                assert result.returncode == 0, (item["id"], result.stderr)
                assert result.stdout.rstrip() == case["expected_output"].rstrip(), item["id"]


def test_real_runner_uses_every_private_harness_without_leaking_it() -> None:
    old = {item["id"]: EXERCISES.get(item["id"]) for item in PYTHON_CURATED_394_400}
    try:
        EXERCISES.update({item["id"]: item for item in PYTHON_CURATED_394_400})
        for item in PYTHON_CURATED_394_400:
            assert "harness" not in repr(_public_view(item, include_hidden=True))
            result = validate_submission(item["id"], item["solution"], timeout_seconds=4)
            assert result["status"] == "passed", (item["id"], result)
            assert result["passed"] == result["total"] == 6
    finally:
        for exercise_id, prior in old.items():
            if prior is None:
                EXERCISES.pop(exercise_id, None)
            else:
                EXERCISES[exercise_id] = prior


def test_spreadsheet_real_runner_handles_a_100k_dependency_chain_without_recursion() -> None:
    item = deepcopy(next(item for item in PYTHON_CURATED_394_400 if item["id"] == "python-curated-400"))
    depth = 100_000
    commands = ["value A0 1"] + [f"formula A{index} A{index - 1}" for index in range(1, depth + 1)] + [f"get A{depth}"]
    item["public_tests"] = [{"input": f"{len(commands)}\n" + "\n".join(commands) + "\n", "expected_output": "1", "harness": item["public_tests"][0]["harness"]}]
    item["hidden_tests"] = []
    previous = EXERCISES.get(item["id"])
    try:
        EXERCISES[item["id"]] = item
        result = validate_submission(item["id"], item["solution"], timeout_seconds=12)
        assert result["status"] == "passed", result
        assert result["passed"] == result["total"] == 1
    finally:
        if previous is None:
            EXERCISES.pop(item["id"], None)
        else:
            EXERCISES[item["id"]] = previous


def test_no_normalised_collisions_with_current_python_catalogue() -> None:
    prior = [item for item in EXERCISES.values() if item.get("language", "python") == "python" and item["id"] not in {current["id"] for current in PYTHON_CURATED_394_400}]
    for field in ("title", "description", "solution"):
        current = [normalise(item[field]) for item in PYTHON_CURATED_394_400]
        assert len(current) == len(set(current)), field
        assert not set(current) & {normalise(item[field]) for item in prior}, field


def test_module_is_data_only() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert "PYTHON_CURATED_394_400 = ITEMS" in source
    assert "exercise_bank" not in source
    assert all(ord(char) < 128 for char in source)
    vector = next(item for item in PYTHON_CURATED_394_400 if item["id"] == "python-curated-396")
    assert ".entries" not in vector["starter_code"]
    assert ".entries" not in vector["solution"].split("def solve():", 1)[1]
    assert all(".entries" not in fixture["harness"] for fixture in vector["public_tests"] + vector["hidden_tests"])
