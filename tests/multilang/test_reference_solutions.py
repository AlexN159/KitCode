"""End-to-end canonical checks for every Java and SQL drill.

These intentionally exercise the same compile/database runners used by the API,
so adding a catalogue record with an invalid reference or fixture cannot ship.
"""
from __future__ import annotations

import pytest

from backend import exercise_bank, main


SQL_EXERCISES = [item for item in exercise_bank.EXERCISES.values() if item["language"] == "sql"]
JAVA_EXERCISES = [item for item in exercise_bank.EXERCISES.values() if item["language"] == "java"]


@pytest.mark.parametrize("exercise", SQL_EXERCISES, ids=lambda item: item["id"])
def test_sql_reference_solution_passes(exercise: dict) -> None:
    result = main._validate_multilanguage_submission(exercise, exercise["solution"], "sql", 4.0)
    assert result["status"] == "passed", result


@pytest.mark.skipif(not all(main._java_tools()), reason="Java reference checks require a local JDK")
@pytest.mark.parametrize("exercise", JAVA_EXERCISES, ids=lambda item: item["id"])
def test_java_reference_solution_passes(exercise: dict) -> None:
    tests = [("public", case) for case in exercise["public_tests"]]
    tests += [("hidden", case) for case in exercise["hidden_tests"]]
    result = main._validate_java_submission(tests, exercise["solution"], 4.0)
    assert result["status"] == "passed", result
