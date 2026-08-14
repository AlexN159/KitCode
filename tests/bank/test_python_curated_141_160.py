"""Strict release gates for curated Python exercises 141--160."""
from __future__ import annotations

import ast
from collections import Counter
from math import factorial
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from backend.exercise_bank import EXERCISES
from backend.python_curated_141_160 import PYTHON_CURATED_141_160


SOURCE_PATH = Path("backend/python_curated_141_160.py")
CONCEPTS_BY_ID = {
    "python-curated-141": "linked-list-cycle-entry",
    "python-curated-142": "linked-list-middle-node",
    "python-curated-143": "linked-list-first-last-reorder",
    "python-curated-144": "height-balanced-tree",
    "python-curated-145": "tree-diameter",
    "python-curated-146": "tree-right-side-view",
    "python-curated-147": "root-leaf-path-sum",
    "python-curated-148": "tree-lowest-common-ancestor",
    "python-curated-149": "top-k-by-frequency",
    "python-curated-150": "running-lower-median",
    "python-curated-151": "directed-nonnegative-dijkstra",
    "python-curated-152": "graph-bipartite-decision",
    "python-curated-153": "strongly-connected-component-count",
    "python-curated-154": "first-redundant-undirected-edge",
    "python-curated-155": "maximum-nonadjacent-house-sum",
    "python-curated-156": "zero-one-knapsack",
    "python-curated-157": "word-break-decision",
    "python-curated-158": "equal-subset-partition",
    "python-curated-159": "distinct-lexicographic-permutations",
    "python-curated-160": "palindromic-partition-count",
}

# Human-reviewed nearest concepts in the existing 140.  This catches semantic
# repackaging that title/source equality cannot, especially the former two-list
# merge which was already subsumed by merge-k-sorted-streams.
PRIOR_NEARBY_CONCEPTS = {
    "reverse-linked-list", "remove-nth-linked-list-node", "tree-level-order",
    "validate-binary-search-tree", "merge-k-sorted-streams", "kth-largest-value",
    "median-sorted-list", "median-two-sorted-arrays", "grid-shortest-path",
    "dynamic-connectivity", "minimum-spanning-tree", "course-ordering",
    "island-component-count", "generate-parentheses", "palindrome-decision",
    "first-unique-character", "run-length-encoding", "move-zeroes", "rotate-array",
}


def run_solution(solution: str, payload: str, timeout: float = 3.0) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as folder:
        program = Path(folder) / "reference.py"
        program.write_text(solution, encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-I", str(program)], input=payload, text=True,
            capture_output=True, timeout=timeout, check=False,
        )


class CuratedPython141160Tests(unittest.TestCase):
    def test_shape_distribution_and_metadata(self) -> None:
        items = PYTHON_CURATED_141_160
        self.assertEqual([item["id"] for item in items], [f"python-curated-{i:03d}" for i in range(141, 161)])
        self.assertEqual(Counter(item["difficulty"] for item in items), {"Easy": 2, "Medium": 13, "Hard": 5})
        normalise = lambda value: re.sub(r"[^a-z0-9]+", "", value.lower())
        self.assertEqual(len({normalise(item["title"]) for item in items}), 20)
        self.assertEqual(set(CONCEPTS_BY_ID), {item["id"] for item in items})
        self.assertEqual(len(set(CONCEPTS_BY_ID.values())), 20)
        self.assertTrue(set(CONCEPTS_BY_ID.values()).isdisjoint(PRIOR_NEARBY_CONCEPTS))
        for item in items:
            self.assertEqual((len(item["public_tests"]), len(item["hidden_tests"])), (2, 4))
            self.assertEqual(len(item["hints"]), 3)
            self.assertTrue(item["description"] and item["constraints"] and item["examples"][0]["explanation"])
            for text in [item["title"], item["description"], item["expected_complexity"], *item["hints"], *item["constraints"]]:
                self.assertNotIn("\ufffd", text)
                self.assertFalse(any(ord(char) < 32 and char not in "\n\t" for char in text))
            for case in item["public_tests"] + item["hidden_tests"]:
                self.assertTrue(case["input"].endswith("\n"))
                self.assertIsInstance(case["expected_output"], str)

    def test_no_title_or_source_copy_from_existing_140(self) -> None:
        current_ids = {item["id"] for item in PYTHON_CURATED_141_160}
        prior = [item for item in EXERCISES.values() if item.get("language", "python") == "python" and item["id"] not in current_ids]
        normalise = lambda value: re.sub(r"\s+", "", value).casefold()
        self.assertFalse({item["title"].casefold() for item in prior} & {item["title"].casefold() for item in PYTHON_CURATED_141_160})
        self.assertFalse({normalise(item["solution"]) for item in prior} & {normalise(item["solution"]) for item in PYTHON_CURATED_141_160})

    def test_import_is_pure_literal_data_assembly(self) -> None:
        source = SOURCE_PATH.read_text(encoding="utf-8")
        self.assertNotIn("subprocess", source)
        self.assertNotIn("exec(", source)
        self.assertFalse({char for char in source if ord(char) > 127})
        tree = ast.parse(source)
        calls = [node.value for node in tree.body if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)]
        add_calls = [node for node in calls if isinstance(node.func, ast.Name) and node.func.id == "add"]
        self.assertEqual(len(add_calls), 20)
        for call in add_calls:
            cases = call.args[9]
            self.assertIsInstance(cases, ast.List)
            self.assertEqual(len(cases.elts), 6)
            for pair in cases.elts:
                self.assertIsInstance(pair, ast.Tuple)
                self.assertEqual(len(pair.elts), 2)
                self.assertTrue(all(isinstance(value, ast.Constant) and isinstance(value.value, str) for value in pair.elts))

    def test_positional_tree_contract_and_fixtures_agree(self) -> None:
        for number in range(144, 149):
            item = PYTHON_CURATED_141_160[number - 141]
            self.assertIn("complete positional-array", item["description"])
            self.assertTrue(any("# ancestor" in constraint for constraint in item["constraints"]))
            for case in item["public_tests"] + item["hidden_tests"]:
                lines = case["input"].splitlines()
                n = int(lines[0]); tokens = lines[1].split()
                self.assertEqual(len(tokens), n)
                for index, token in enumerate(tokens[1:], 1):
                    if token != "#":
                        self.assertNotEqual(tokens[(index - 1) // 2], "#")

    def test_serialized_middle_list_cases_cover_each_node_once(self) -> None:
        item = PYTHON_CURATED_141_160[1]
        for case in item["public_tests"] + item["hidden_tests"]:
            lines = case["input"].splitlines(); n = int(lines[0])
            self.assertEqual(len(lines[1].split()), n)
            nxt = list(map(int, lines[2].split())); self.assertEqual(len(nxt), n)
            current = int(lines[3]); visited = set()
            while current != -1:
                self.assertNotIn(current, visited); visited.add(current); current = nxt[current]
            self.assertEqual(len(visited), n)

    def test_output_heavy_contracts_fit_the_local_capture_limit(self) -> None:
        # A signed 32-bit token plus a separator needs at most 12 bytes.
        self.assertLessEqual(5_000 * 12, 64 * 1024)  # reorder, top-k, running median, Dijkstra
        permutation_bytes = factorial(6) * (6 * 11 + 5 + 1)
        self.assertLessEqual(permutation_bytes, 64 * 1024)
        self.assertIn("1 <= n <= 6", PYTHON_CURATED_141_160[18]["constraints"])

    def test_scc_reference_handles_a_chain_beyond_python_recursion_limit(self) -> None:
        n = 2_500
        payload = f"{n} {n - 1}\n" + "".join(f"{i} {i + 1}\n" for i in range(n - 1))
        result = run_solution(PYTHON_CURATED_141_160[12]["solution"], payload, timeout=5.0)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), str(n))

    def test_all_120_references_run_under_isolated_python(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            program = Path(folder) / "reference.py"
            for item in PYTHON_CURATED_141_160:
                program.write_text(item["solution"], encoding="utf-8")
                for case in item["public_tests"] + item["hidden_tests"]:
                    result = subprocess.run(
                        [sys.executable, "-I", str(program)], input=case["input"], text=True,
                        capture_output=True, timeout=3, check=False,
                    )
                    with self.subTest(item=item["id"], payload=case["input"]):
                        self.assertEqual(result.returncode, 0, result.stderr)
                        self.assertEqual(result.stdout.rstrip("\r\n"), case["expected_output"].rstrip("\r\n"))


if __name__ == "__main__":
    unittest.main()
