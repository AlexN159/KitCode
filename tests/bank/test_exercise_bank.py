"""Regression checks for the local practice exercise catalogue."""
import os
from pathlib import Path
import tempfile
import time
import unittest
from collections import Counter

from backend.exercise_bank import EXERCISES, _public_view, catalog_summary, get_catalog, get_exercise, validate_submission


class ExerciseBankTests(unittest.TestCase):
    def _with_class_exercise(self, exercise_id: str = "test-class-adder"):
        """Install a tiny private class-contract drill for runner tests."""
        exercise = {
            "id": exercise_id,
            "title": "Test class adder",
            "language": "python",
            "difficulty": "Easy",
            "topics": ["classes"],
            "practice_frequency": "once",
            "expected_complexity": "O(1)",
            "submission_mode": "python_class",
            "required_class": {"name": "Adder", "methods": ["add"]},
            "public_tests": [{
                "input": "2 5\n",
                "expected_output": "7",
                "harness": "left, right = map(int, sys.stdin.read().split())\nprint(submission_class().add(left, right))",
            }],
            "hidden_tests": [{
                "input": "9 4\n",
                "expected_output": "13",
                "harness": "left, right = map(int, sys.stdin.read().split())\nprint(submission_class().add(left, right))",
            }],
        }
        previous = EXERCISES.get(exercise_id)
        EXERCISES[exercise_id] = exercise
        self.addCleanup(lambda: EXERCISES.__setitem__(exercise_id, previous) if previous is not None else EXERCISES.pop(exercise_id, None))
        return exercise

    def test_class_runner_rejects_procedural_output_without_required_class(self) -> None:
        self._with_class_exercise()
        result = validate_submission("test-class-adder", "import sys\na, b = map(int, sys.stdin.read().split())\nprint(a + b)\n")
        self.assertEqual(result["status"], "failed")
        self.assertIn("top-level class named Adder", result["message"])
        self.assertEqual(result["total"], 0)

    def test_class_runner_rejects_missing_required_method(self) -> None:
        self._with_class_exercise()
        result = validate_submission("test-class-adder", "class Adder:\n    pass\n")
        self.assertEqual(result["status"], "failed")
        self.assertIn("must define: add", result["message"])

    def test_class_runner_imports_and_invokes_the_class_through_its_harness(self) -> None:
        self._with_class_exercise()
        code = "class Adder:\n    def add(self, left, right):\n        return left + right\n\nif __name__ == '__main__':\n    raise RuntimeError('the harness must import this module')\n"
        result = validate_submission("test-class-adder", code)
        self.assertEqual(result["status"], "passed", result)
        self.assertEqual(result["passed"], 2)

    def test_class_runner_does_not_allow_a_procedural_main_to_bypass_the_harness(self) -> None:
        self._with_class_exercise()
        code = "import sys\n\nclass Adder:\n    def add(self, left, right):\n        return -1\n\nif __name__ == '__main__':\n    left, right = map(int, sys.stdin.read().split())\n    print(left + right)\n"
        result = validate_submission("test-class-adder", code)
        self.assertEqual(result["status"], "failed")
        self.assertFalse(result["results"][0]["passed"])
        self.assertEqual(result["results"][0]["actual_output"].strip(), "-1")

    def test_class_runner_rejects_unguarded_import_time_output_and_exit(self) -> None:
        self._with_class_exercise()
        code = (
            "class Adder:\n"
            "    def add(self, left, right):\n"
            "        return -1\n\n"
            "print('7')\n"
            "raise SystemExit(0)\n"
        )
        result = validate_submission("test-class-adder", code)
        self.assertEqual(result["status"], "failed")
        self.assertEqual(result["passed"], 0)
        self.assertTrue(all(not entry["passed"] for entry in result["results"]))

    def test_class_harnesses_and_private_fixtures_are_not_learner_visible(self) -> None:
        exercise = self._with_class_exercise()
        exercise["hidden_tests"] = [{
            "input": "PRIVATE_CLASS_INPUT_802\n",
            "expected_output": "irrelevant",
            "harness": "raise RuntimeError('PRIVATE_CLASS_HARNESS_802')",
        }]
        detail = get_exercise("test-class-adder")
        self.assertNotIn("harness", repr(detail))
        self.assertNotIn("PRIVATE_CLASS_INPUT_802", repr(detail))
        self.assertNotIn("PRIVATE_CLASS_HARNESS_802", repr(detail))
        self.assertNotIn("harness", repr(_public_view(exercise, include_hidden=True)))

        result = validate_submission("test-class-adder", "class Adder:\n    def add(self, left, right):\n        return left + right\n")
        private = [entry for entry in result["results"] if entry["visibility"] == "hidden"]
        self.assertEqual(len(private), 1)
        self.assertNotIn("PRIVATE_CLASS_INPUT_802", repr(private))
        self.assertNotIn("PRIVATE_CLASS_HARNESS_802", repr(private))
        self.assertEqual(private[0]["error"], "Program exited with an error on a private test.")

    def test_release_catalogue_has_exact_language_counts(self) -> None:
        """Keep curated progress comparable and prevent accidental padding/removal."""
        languages = Counter(item.get("language", "python") for item in EXERCISES.values())
        self.assertEqual(len(EXERCISES), 700)
        self.assertEqual(languages, {"python": 400, "java": 150, "sql": 150})
        python_difficulties = Counter(
            item["difficulty"]
            for item in EXERCISES.values()
            if item.get("language") == "python"
        )
        self.assertEqual(python_difficulties, {"Easy": 176, "Medium": 130, "Hard": 94})

    def test_catalogue_has_breadth_and_complete_public_payloads(self) -> None:
        summary = catalog_summary()
        self.assertGreaterEqual(summary["total"], 140)
        self.assertGreaterEqual(summary["by_difficulty"]["Easy"], 20)
        self.assertGreaterEqual(summary["by_difficulty"]["Medium"], 20)
        self.assertGreaterEqual(summary["by_difficulty"]["Hard"], 5)
        required = {"id", "title", "difficulty", "topics", "description", "constraints", "examples", "starter_code", "hints", "solution", "expected_complexity", "public_tests", "hidden_tests"}
        for item in EXERCISES.values():
            self.assertTrue(required.issubset(item))
            self.assertTrue(item["examples"])
            self.assertGreaterEqual(len(item["hints"]), 3)
            self.assertTrue(item["public_tests"])
            self.assertTrue(item["hidden_tests"])

    def test_catalogue_listing_and_detail_keep_hidden_cases_private(self) -> None:
        listing = get_catalog()
        self.assertEqual(len(listing), len(EXERCISES))
        detail = get_exercise("two-sum-indices")
        self.assertIsNotNone(detail)
        self.assertNotIn("hidden_tests", detail)
        self.assertEqual(get_exercise("missing"), None)

    def test_array_input_copy_explains_count_values_and_target_lines(self) -> None:
        common_hints = [
            "In Python, `n = int(input())` reads the count from line 1; equivalent whitespace-based parsing is also valid.",
            "Read line 2 with `nums = list(map(int, input().split()))`, or use another whitespace-based parser.",
            "Use n to check how many values belong to the list, then print only the requested result.",
        ]
        minimum = EXERCISES["array-003"]
        self.assertEqual(
            minimum["description"],
            "Line 1 contains the count n. Line 2 contains n space-separated integers. Print the smallest integer.",
        )
        self.assertEqual(minimum["hints"], common_hints)
        self.assertEqual(minimum["examples"], [{"input": "4\n-2 9 3 1\n", "output": "-2"}])

        frequency = EXERCISES["array-013"]
        self.assertEqual(
            frequency["description"],
            "Line 1 contains the count n. Line 2 contains n space-separated integers. "
            "Line 3 contains the target t. Print how many of the integers equal t.",
        )
        self.assertEqual(
            frequency["hints"],
            common_hints[:2]
            + ["Read the target from line 3 with `target = int(input())`, or use another whitespace-based parser."],
        )
        self.assertEqual(
            frequency["examples"],
            [{"input": "5\n1 2 2 3 2\n2\n", "output": "3"}],
        )

    def test_validator_reports_a_failing_public_case(self) -> None:
        result = validate_submission("number-001", "print('wrong')")
        self.assertEqual(result["status"], "failed")
        self.assertGreaterEqual(result["total"], 5)
        self.assertIn("expected_output", result["results"][0])

    def test_validator_does_not_inherit_host_secrets(self) -> None:
        secret = "bank-test-secret-do-not-leak"
        previous = os.environ.get("OPENAI_API_KEY")
        os.environ["OPENAI_API_KEY"] = secret
        try:
            result = validate_submission("number-001", "import os\nprint(os.getenv('OPENAI_API_KEY', 'missing'))")
        finally:
            if previous is None:
                os.environ.pop("OPENAI_API_KEY", None)
            else:
                os.environ["OPENAI_API_KEY"] = previous
        rendered = repr(result)
        self.assertNotIn(secret, rendered)
        self.assertNotIn("OPENAI_API_KEY", rendered)
        self.assertEqual(result["results"][0]["actual_output"].strip(), "missing")

    def test_advanced_exercises_have_stronger_hidden_coverage(self) -> None:
        advanced = [item for key, item in EXERCISES.items() if key.startswith("advanced-")]
        self.assertEqual(len(advanced), 20)
        for item in advanced:
            self.assertGreaterEqual(len(item["public_tests"]), 2)
            self.assertGreaterEqual(len(item["hidden_tests"]), 3)

    def test_every_exercise_has_a_private_test_floor(self) -> None:
        for exercise_id, item in EXERCISES.items():
            with self.subTest(exercise_id=exercise_id):
                self.assertGreaterEqual(len(item["public_tests"]), 2)
                self.assertGreaterEqual(len(item["hidden_tests"]), 2)
                if item["difficulty"] in {"Medium", "Hard"}:
                    self.assertGreaterEqual(len(item["hidden_tests"]), 4)

    def test_timeout_cleans_up_spawned_child_process(self) -> None:
        """A timed-out learner must not leave a delayed child behind."""
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "should-not-exist.txt"
            child = (
                "import pathlib,time; time.sleep(0.7); "
                f"pathlib.Path({str(marker)!r}).write_text('orphan')"
            )
            code = (
                "import subprocess, sys\n"
                f"subprocess.Popen([sys.executable, '-c', {child!r}])\n"
                "while True: pass\n"
            )
            result = validate_submission("number-001", code, timeout_seconds=0.2)
            self.assertEqual(result["status"], "failed")
            self.assertIn("Timed out", result["results"][0].get("error", ""))
            time.sleep(0.9)
            self.assertFalse(marker.exists(), "timed-out submission left an orphan child process")

    def test_large_output_is_capped_without_retaining_full_stream(self) -> None:
        result = validate_submission("number-001", "print('x' * 2_000_000)")
        self.assertEqual(result["status"], "failed")
        first = result["results"][0]
        self.assertIn("safety limit", first.get("error", ""))
        self.assertNotIn("actual_output", first)
        self.assertLess(len(repr(result)), 10_000)

    def test_private_failure_never_returns_hidden_input_or_stderr(self) -> None:
        exercise = EXERCISES["number-001"]
        original = list(exercise["hidden_tests"])
        sentinel = "UNIQUE_PRIVATE_INPUT_SENTINEL_94721\n"
        exercise["hidden_tests"] = [{"input": sentinel, "expected_output": "even"}]
        try:
            result = validate_submission("number-001", "import sys\nraise RuntimeError(sys.stdin.read())")
        finally:
            exercise["hidden_tests"] = original
        private = [item for item in result["results"] if item["visibility"] == "hidden"]
        self.assertTrue(private)
        rendered_private = repr(private)
        self.assertNotIn(sentinel.strip(), rendered_private)
        self.assertTrue(all(item.get("error") == "Program exited with an error on a private test." for item in private))

    def test_every_reference_solution_passes_every_case(self) -> None:
        for exercise_id, exercise in EXERCISES.items():
            # Python owns the dependency-free bank validator.  Java and SQL
            # execute through the API runtime, where their compiler/database
            # guards and language-specific runners are covered separately.
            if exercise.get("language", "python") != "python":
                continue
            with self.subTest(exercise_id=exercise_id):
                result = validate_submission(exercise_id, exercise["solution"])
                self.assertEqual(result["status"], "passed", result)

    def test_multilanguage_records_have_private_fixtures_and_safe_metadata(self) -> None:
        languages = {item.get("language") for item in EXERCISES.values()}
        self.assertTrue({"python", "java", "sql"}.issubset(languages))
        for item in EXERCISES.values():
            with self.subTest(exercise_id=item["id"]):
                self.assertIn(item["language"], {"python", "java", "sql"})
                if item["language"] == "java":
                    self.assertIn("public class Main", item["solution"])
                if item["language"] == "sql":
                    self.assertTrue(all("setup_sql" in test for test in item["public_tests"] + item["hidden_tests"]))
                    detail = get_exercise(item["id"])
                    self.assertTrue(any(str(value).startswith("Schema:") for value in detail["constraints"]))
                    self.assertNotIn("setup_sql", repr(detail))

    def test_sql_public_details_are_dialect_neutral_while_fixtures_stay_private(self) -> None:
        """The dialect picker must not be undermined by SQLite-only drill copy."""
        sql_items = [item for item in EXERCISES.values() if item["language"] == "sql"]
        self.assertEqual(len(sql_items), 150)
        required_instruction = "Write one read-only SELECT or WITH query in the selected dialect."
        for item in sql_items:
            with self.subTest(exercise_id=item["id"]):
                detail = get_exercise(item["id"])
                public_copy = repr(detail).lower()
                self.assertIn(required_instruction, detail["constraints"])
                self.assertIn(required_instruction, detail["starter_code"])
                self.assertIn("translated for local sqlite compatibility", public_copy)
                self.assertNotIn("sqlite-compatible sql", public_copy)
                self.assertNotIn("read-only sqlite", public_copy)
                self.assertNotIn("write one sqlite", public_copy)
                self.assertNotIn("sqlite", [topic.casefold() for topic in detail["topics"]])
                self.assertNotIn("setup_sql", public_copy)
                self.assertTrue(all("setup_sql" in case for case in item["public_tests"] + item["hidden_tests"]))

    def test_java_and_sql_drills_do_not_pad_the_catalogue_with_duplicate_answers(self) -> None:
        seen: dict[tuple[str, str], str] = {}
        for item in EXERCISES.values():
            language = item.get("language", "python")
            if language not in {"java", "sql"}:
                continue
            normalized = " ".join(item["solution"].split())
            key = (language, normalized)
            self.assertNotIn(key, seen, f"{item['id']} duplicates {seen.get(key)}")
            seen[key] = item["id"]


if __name__ == "__main__":
    unittest.main()
