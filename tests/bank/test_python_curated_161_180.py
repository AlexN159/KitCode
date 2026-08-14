"""Strict release checks for curated Python exercises 161--180."""
from __future__ import annotations

import ast
from collections import Counter
from pathlib import Path
import re
import subprocess
import sys
import tempfile

from backend.exercise_bank import EXERCISES
from backend.python_curated_141_160 import PYTHON_CURATED_141_160
from backend.python_curated_161_180 import PYTHON_CURATED_161_180


SOURCE = Path("backend/python_curated_161_180.py")
CONCEPTS = {
    "kmp-overlap-count", "z-array", "bellman-ford-negative-cycle", "floyd-warshall-queries",
    "prim-spanning-forest", "articulation-points", "bridges", "euler-trail-feasibility",
    "fenwick-updates", "segment-tree-min", "sparse-table-min", "weighted-edit-distance",
    "regex-match", "digit-dp-adjacent", "bitmask-tsp", "matrix-chain", "huffman-cost",
    "minimum-topological-layers", "aho-corasick-counts", "burst-balloons",
}
PRIOR_NEAR_CONCEPTS = {
    "plain-edit-distance", "dijkstra", "course-ordering", "kruskal-mst", "dynamic-connectivity",
    "count-islands", "kmp-not-present", "range-prefix-sum", "binary-search", "n-queens",
    "palindrome-partition-count", "zero-one-knapsack", "word-break", "distinct-permutations",
}


def _normalise(source: str) -> str:
    return re.sub(r"\s+", "", source).casefold()


def _run(solution: str, payload: str, timeout: float = 5.0) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as folder:
        program = Path(folder) / "solution.py"
        program.write_text(solution, encoding="utf-8")
        return subprocess.run([sys.executable, "-I", str(program)], input=payload, text=True,
                              capture_output=True, timeout=timeout, check=False)


def test_shape_manifest_metadata_and_semantic_separation() -> None:
    assert [x["id"] for x in PYTHON_CURATED_161_180] == [f"python-curated-{i:03d}" for i in range(161, 181)]
    assert Counter(x["difficulty"] for x in PYTHON_CURATED_161_180) == {"Medium": 9, "Hard": 11}
    assert len(CONCEPTS) == 20 and CONCEPTS.isdisjoint(PRIOR_NEAR_CONCEPTS)
    assert len({x["title"].casefold() for x in PYTHON_CURATED_161_180}) == 20
    for item in PYTHON_CURATED_161_180:
        assert len(item["public_tests"]) == 2 and len(item["hidden_tests"]) == 4
        assert len(item["hints"]) == 3 and item["constraints"] and item["description"]
        assert all(case["input"].endswith("\n") for case in item["public_tests"] + item["hidden_tests"])


def test_titles_and_sources_are_unique_against_python_1_160() -> None:
    current_ids = {x["id"] for x in PYTHON_CURATED_161_180}
    prior = [
        x for x in EXERCISES.values()
        if x.get("language", "python") == "python" and x["id"] not in current_ids
    ]
    assert not {x["title"].casefold() for x in prior} & {x["title"].casefold() for x in PYTHON_CURATED_161_180}
    assert not {_normalise(x["solution"]) for x in prior} & {_normalise(x["solution"]) for x in PYTHON_CURATED_161_180}


def test_import_is_pure_and_all_expected_outputs_are_literal() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert ".replace(" not in source and "subprocess" not in source and "exec(" not in source
    assert not any(ord(char) > 127 or (ord(char) < 32 and char not in "\r\n\t") for char in source)
    tree = ast.parse(source)
    calls = [node.value for node in tree.body if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call)
             and isinstance(node.value.func, ast.Name) and node.value.func.id == "add"]
    assert len(calls) == 20
    for call in calls:
        cases = call.args[9]
        assert isinstance(cases, ast.List) and len(cases.elts) == 6
        assert all(isinstance(pair, ast.Tuple) and len(pair.elts) == 2
                   and all(isinstance(value, ast.Constant) and isinstance(value.value, str) for value in pair.elts)
                   for pair in cases.elts)


def test_output_heavy_contracts_fit_the_python_runner_limit() -> None:
    by_id = {x["id"]: x for x in PYTHON_CURATED_161_180}
    assert any("8,000" in value for value in by_id["python-curated-162"]["constraints"])
    assert any("4,500" in value for value in by_id["python-curated-164"]["constraints"])
    assert any("8,000" in value for value in by_id["python-curated-166"]["constraints"])
    assert any("4,000 bridges" in value for value in by_id["python-curated-167"]["constraints"])
    for exercise_id in ("python-curated-169", "python-curated-170"):
        assert any("3,500" in value for value in by_id[exercise_id]["constraints"])
    assert any("5,000" in value for value in by_id["python-curated-171"]["constraints"])
    assert any("8,000" in value for value in by_id["python-curated-179"]["constraints"])


def test_low_link_references_handle_a_chain_beyond_default_recursion_depth() -> None:
    n = 2_500
    payload = f"{n} {n - 1}\n" + "".join(f"{i} {i + 1}\n" for i in range(n - 1))
    articulation = _run(PYTHON_CURATED_161_180[5]["solution"], payload)
    bridges = _run(PYTHON_CURATED_161_180[6]["solution"], payload)
    assert articulation.returncode == 0, articulation.stderr
    assert articulation.stdout.split() == [str(i) for i in range(1, n - 1)]
    assert bridges.returncode == 0, bridges.stderr
    assert len(bridges.stdout.splitlines()) == n - 1


def test_all_120_references_under_isolated_python() -> None:
    with tempfile.TemporaryDirectory() as folder:
        program = Path(folder) / "reference.py"
        for exercise in PYTHON_CURATED_161_180:
            program.write_text(exercise["solution"], encoding="utf-8")
            for case in exercise["public_tests"] + exercise["hidden_tests"]:
                result = subprocess.run([sys.executable, "-I", str(program)], input=case["input"], text=True,
                                        capture_output=True, timeout=3, check=False)
                assert result.returncode == 0, (exercise["id"], result.stderr)
                assert result.stdout.rstrip("\r\n") == case["expected_output"].rstrip("\r\n"), exercise["id"]
