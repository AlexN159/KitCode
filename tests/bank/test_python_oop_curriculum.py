"""Cross-level release gates for the class-based Python curriculum."""
from __future__ import annotations

from collections import Counter

from backend.exercise_bank import EXERCISES, _public_view, validate_submission
from backend.python_curated_201_288 import PYTHON_CURATED_201_288
from backend.python_curated_289_353 import PYTHON_CURATED_289_353
from backend.python_curated_394_400 import PYTHON_CURATED_394_400


def _class_items():
    all_items = PYTHON_CURATED_201_288 + PYTHON_CURATED_289_353 + PYTHON_CURATED_394_400
    return [item for item in all_items if item.get("submission_mode") == "python_class"]


def _temporarily_register(items):
    previous = {item["id"]: EXERCISES.get(item["id"]) for item in items}
    EXERCISES.update({item["id"]: item for item in items})
    return previous


def _restore(previous):
    for exercise_id, prior in previous.items():
        if prior is None:
            EXERCISES.pop(exercise_id, None)
        else:
            EXERCISES[exercise_id] = prior


def test_cross_level_class_manifest_and_safe_learner_payloads():
    items = _class_items()
    assert len(items) == 23
    assert Counter(item["difficulty"] for item in items) == {"Easy": 8, "Medium": 8, "Hard": 7}
    assert [item["id"] for item in items if item["difficulty"] == "Easy"] == [f"python-curated-{number:03d}" for number in range(281, 289)]
    assert [item["id"] for item in items if item["difficulty"] == "Medium"] == [f"python-curated-{number:03d}" for number in range(346, 354)]
    assert [item["id"] for item in items if item["difficulty"] == "Hard"] == [f"python-curated-{number:03d}" for number in range(394, 401)]
    for item in items:
        requirement = item["required_class"]
        assert any(topic in {"classes", "oop"} for topic in item["topics"]), item["id"]
        assert isinstance(requirement, dict) and requirement["name"].isidentifier() and requirement["methods"]
        assert f"class {requirement['name']}:" in item["starter_code"]
        assert "pass" in item["starter_code"] and "def solve()" in item["starter_code"] and "if __name__" in item["starter_code"]
        assert f"class {requirement['name']}:" in item["solution"] and "def solve()" in item["solution"] and "if __name__" in item["solution"]
        for fixture in item["public_tests"] + item["hidden_tests"]:
            assert isinstance(fixture.get("harness"), str) and "submission_class" in fixture["harness"]
        safe = _public_view(item, include_hidden=True)
        assert "harness" not in repr(safe)


def test_all_class_references_pass_the_real_private_harnesses():
    items = _class_items()
    previous = _temporarily_register(items)
    try:
        for item in items:
            result = validate_submission(item["id"], item["solution"], timeout_seconds=4)
            assert result["status"] == "passed", (item["id"], result)
            assert result["passed"] == result["total"] == len(item["public_tests"]) + len(item["hidden_tests"])
    finally:
        _restore(previous)


def test_oop_curriculum_has_the_promised_language_features_and_error_paths():
    by_id = {item["id"]: item for item in _class_items()}
    sources = {exercise_id: item["starter_code"] + "\n" + item["solution"] for exercise_id, item in by_id.items()}
    assert "@classmethod" in sources["python-curated-284"]
    assert "@property" in sources["python-curated-346"] and "raise ValueError" in sources["python-curated-346"]
    assert "class LineItem" in sources["python-curated-347"] and "class Book" in sources["python-curated-353"]
    assert "class Circle(Shape)" in sources["python-curated-350"] and "issubclass" in by_id["python-curated-350"]["public_tests"][0]["harness"]
    assert "__iter__" in sources["python-curated-349"] and "__contains__" in sources["python-curated-349"]
    assert "__lt__" in sources["python-curated-351"] and "__eq__" in sources["python-curated-351"]
    assert "__add__" in sources["python-curated-396"] and "__matmul__" in sources["python-curated-396"] and "__repr__" in sources["python-curated-397"]
    assert "self.total" in sources["python-curated-282"] and "self.value" in sources["python-curated-288"]
    assert "raise ValueError" in sources["python-curated-399"] and "raise ValueError" in sources["python-curated-400"]


def test_hard_class_cli_demos_fit_the_desktop_runner_contract():
    hard = [item for item in _class_items() if item["difficulty"] == "Hard"]
    assert [item["id"] for item in hard] == [f"python-curated-{number:03d}" for number in range(394, 401)]
    for item in hard:
        contract = " ".join(item["constraints"])
        assert "12,000 characters" in contract, item["id"]
        assert "22,000 characters" in contract, item["id"]
    by_id = {item["id"]: " ".join(item["constraints"]) for item in hard}
    assert "at most 500 commands" in by_id["python-curated-394"]
    assert "n <= 800" in by_id["python-curated-395"]
    assert "250 stored entries" in by_id["python-curated-396"]
    assert "300 coefficients" in by_id["python-curated-397"]
    assert "at most 800 operations" in by_id["python-curated-398"]
    assert "at most 800 task" in by_id["python-curated-399"]
    assert "at most 500 commands" in by_id["python-curated-400"]


def test_a_real_class_drill_rejects_procedural_and_dummy_bypass_attempts():
    exercise = next(item for item in _class_items() if item["id"] == "python-curated-281")
    previous = _temporarily_register([exercise])
    try:
        procedural = validate_submission(exercise["id"], "print('12 14')\n")
        assert procedural["status"] == "failed"
        assert "top-level class named Rectangle" in procedural["message"]
        dummy = validate_submission(exercise["id"], "class Rectangle:\n    def __init__(self, width, height): pass\n    def area(self): return 0\n    def perimeter(self): return 0\n")
        assert dummy["status"] == "failed"
        assert dummy["passed"] == 0
        assert any(not result["passed"] for result in dummy["results"])
    finally:
        _restore(previous)
