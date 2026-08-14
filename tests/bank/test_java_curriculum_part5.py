"""Release gates for the final Java 141--150 core tranche."""
from __future__ import annotations

import ast
from functools import lru_cache
import random
import re
from pathlib import Path
import subprocess
import tempfile

import pytest

from backend import main
from backend.java_curriculum_part1 import JAVA_CURRICULUM_PART1
from backend.java_curriculum_part2 import JAVA_CURRICULUM_PART2
from backend.java_curriculum_part3 import JAVA_CURRICULUM_PART3
from backend.java_curriculum_part4 import JAVA_CURRICULUM_PART4
from backend.java_curriculum_part5 import JAVA_CURRICULUM_PART5
from backend.java_interview_bank import JAVA_INTERVIEW_EXERCISES
from backend.multilang_bank import MULTILANG_EXERCISES


SOURCE = Path("backend/java_curriculum_part5.py")
CONCEPTS = {
    "three-word-autocomplete", "closed-interval-overlap", "dag-cheapest-route",
    "kmp-pattern-positions", "sudoku-4x4", "tarjan-offline-lca",
    "rollback-dsu-script", "circular-stone-merge", "dinic-max-flow",
    "aho-corasick-pattern-counts",
}


def normalise(code: str) -> str:
    return re.sub(r"\s+", "", code)


def normalise_output(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.replace("\r\n", "\n").strip().split("\n"))


@pytest.fixture(scope="module")
def release17_references():
    javac, java = main._java_tools()
    if not javac or not java:
        pytest.skip("JDK required")
    with tempfile.TemporaryDirectory(prefix="java-part5-audit-") as root:
        runners = {}
        for exercise in JAVA_CURRICULUM_PART5:
            folder = Path(root) / exercise["id"]
            folder.mkdir()
            source = folder / "Main.java"
            source.write_text(exercise["solution"], encoding="utf-8")
            compiled = subprocess.run(
                [javac, "--release", "17", "-encoding", "UTF-8", "-d", str(folder), str(source)],
                text=True,
                capture_output=True,
                timeout=8,
            )
            assert compiled.returncode == 0, (exercise["id"], compiled.stderr)

            def run(input_text, folder=folder):
                result = subprocess.run(
                    [java, "-Xms16m", "-Xmx128m", "-XX:+UseSerialGC", "-cp", str(folder), "Main"],
                    input=input_text,
                    text=True,
                    capture_output=True,
                    timeout=8,
                )
                assert result.returncode == 0, result.stderr
                return normalise_output(result.stdout)

            runners[exercise["id"]] = run
        yield runners


def test_release_shape_and_literal_contracts() -> None:
    assert [x["id"] for x in JAVA_CURRICULUM_PART5] == [f"java-curated-{n:03d}" for n in range(141, 151)]
    assert [sum(x["difficulty"] == level for x in JAVA_CURRICULUM_PART5) for level in ("Easy", "Medium", "Hard")] == [0, 6, 4]
    assert len(CONCEPTS) == len(JAVA_CURRICULUM_PART5)
    assert all(len(x["public_tests"]) == 2 and len(x["hidden_tests"]) == 4 for x in JAVA_CURRICULUM_PART5)
    assert all(len(x["hints"]) == 3 and x["constraints"] and x["expected_complexity"] for x in JAVA_CURRICULUM_PART5)


def test_no_import_oracle_dead_revisions_or_mojibake() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    assert not any(token in source for token in ("subprocess", "sqlite", "requests", "lambda", "Exit code:", "\ufffd", "\u00c2"))
    assert all(ord(character) < 128 for character in source)
    tree = ast.parse(source)
    fixtures = [node for node in ast.walk(tree) if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == "C"]
    assert len(fixtures) == 60
    assert all(len(node.args) == 2 and all(isinstance(arg, ast.Constant) and isinstance(arg.value, str) for arg in node.args) for node in fixtures)
    assert source.count("D(") == 11  # helper plus the ten records only


def test_distinct_from_every_prior_java_reference() -> None:
    previous = JAVA_INTERVIEW_EXERCISES + MULTILANG_EXERCISES + JAVA_CURRICULUM_PART1 + JAVA_CURRICULUM_PART2 + JAVA_CURRICULUM_PART3 + JAVA_CURRICULUM_PART4
    previous = [x for x in previous if x.get("language") == "java"]
    titles = [x["title"].casefold() for x in JAVA_CURRICULUM_PART5]
    solutions = [normalise(x["solution"]) for x in JAVA_CURRICULUM_PART5]
    assert not set(titles).intersection(x["title"].casefold() for x in previous)
    assert not set(solutions).intersection(normalise(x["solution"]) for x in previous)
    assert len(set(titles)) == len(titles) == 10
    assert len(set(solutions)) == len(solutions) == 10

    by_id = {exercise["id"]: exercise for exercise in JAVA_CURRICULUM_PART5}
    previous_by_id = {exercise["id"]: exercise for exercise in previous}
    # Batch Tarjan LCA is a deliberate multi-query progression from the one-query
    # parent-array LCA exercise, not the same input or output contract.
    assert by_id["java-curated-146"]["description"] != previous_by_id["java-curated-111"]["description"]


def test_repaired_contract_regressions() -> None:
    by_id = {exercise["id"]: exercise for exercise in JAVA_CURRICULUM_PART5}
    autocomplete = by_id["java-curated-141"]
    assert "nonempty prefix" in " ".join(autocomplete["constraints"])
    assert "24,000" in " ".join(autocomplete["constraints"])
    assert "Arrays.sort(words)" in autocomplete["solution"]
    assert "keep(" not in autocomplete["solution"]
    rollback = " ".join(by_id["java-curated-147"]["constraints"])
    assert "current history" in rollback and "3,000" in rollback
    assert "s != t" in " ".join(by_id["java-curated-149"]["constraints"])


def test_release17_compile_once_and_execute_all_60(release17_references) -> None:
    for exercise in JAVA_CURRICULUM_PART5:
        run = release17_references[exercise["id"]]
        for case in exercise["public_tests"] + exercise["hidden_tests"]:
            assert run(case["input"]) == normalise_output(case["expected_output"]), exercise["id"]


def test_random_search_string_and_graph_algorithms_against_naive_oracles(release17_references) -> None:
    rng = random.Random(141146)
    for _ in range(24):
        word_count = rng.randint(0, 14)
        words = set()
        while len(words) < word_count:
            words.add("".join(rng.choice("abc") for __ in range(rng.randint(1, 7))))
        words = list(words)
        prefix = "".join(rng.choice("abc") for __ in range(rng.randint(1, 4)))
        matches = sorted(word for word in words if word.startswith(prefix))[:3]
        expected = " ".join(matches) if matches else "NONE"
        payload = f"{len(words)}\n" + (" ".join(words) + "\n" if words else "") + prefix + "\n"
        assert release17_references["java-curated-141"](payload) == expected

        intervals = []
        for __ in range(rng.randint(0, 12)):
            left = rng.randint(-8, 7)
            intervals.append((left, rng.randint(left, 9)))
        if intervals:
            coordinates = range(min(left for left, _ in intervals), max(right for _, right in intervals) + 1)
            overlap = [(sum(left <= point <= right for left, right in intervals), point) for point in coordinates]
            best = max(value for value, _ in overlap)
            first = min(point for value, point in overlap if value == best)
            expected = f"{best} {first}"
        else:
            expected = "0 NONE"
        payload = f"{len(intervals)}\n" + "".join(f"{left} {right}\n" for left, right in intervals)
        assert release17_references["java-curated-142"](payload) == expected

        n = rng.randint(1, 10)
        edges = [
            (left, right, rng.randint(-9, 10))
            for left in range(n)
            for right in range(left + 1, n)
            if rng.random() < 0.3
        ]
        source, target = rng.randrange(n), rng.randrange(n)
        infinity = 10**12
        distance = [infinity] * n
        distance[source] = 0
        for vertex in range(n):
            if distance[vertex] < infinity:
                for left, right, cost in edges:
                    if left == vertex:
                        distance[right] = min(distance[right], distance[left] + cost)
        expected = "INF" if distance[target] == infinity else str(distance[target])
        payload = f"{n} {len(edges)} {source} {target}\n" + "".join(
            f"{left} {right} {cost}\n" for left, right, cost in edges
        )
        assert release17_references["java-curated-143"](payload) == expected

        text = "".join(rng.choice("abc ") for __ in range(rng.randint(0, 35)))
        pattern = "".join(rng.choice("abc ") for __ in range(rng.randint(1, 7)))
        starts = [index for index in range(len(text) - len(pattern) + 1) if text.startswith(pattern, index)]
        expected = " ".join(map(str, starts)) if starts else "NONE"
        assert release17_references["java-curated-144"](f"{text}\n{pattern}\n") == expected

        parent = [-1] + [rng.randrange(vertex) for vertex in range(1, n)]
        queries = [(rng.randrange(n), rng.randrange(n)) for __ in range(20)]

        def lca(first, second):
            ancestors = set()
            while first >= 0:
                ancestors.add(first)
                first = parent[first]
            while second not in ancestors:
                second = parent[second]
            return second

        payload = (
            f"{n} {len(queries)}\n"
            + " ".join(map(str, parent))
            + "\n"
            + "".join(f"{first} {second}\n" for first, second in queries)
        )
        assert release17_references["java-curated-146"](payload) == "\n".join(
            str(lca(first, second)) for first, second in queries
        )

        patterns = ["".join(rng.choice("abc") for __ in range(rng.randint(1, 6))) for __ in range(rng.randint(1, 10))]
        lowercase_text = "".join(rng.choice("abc") for __ in range(rng.randint(1, 35)))
        counts = [
            sum(lowercase_text.startswith(pattern, index) for index in range(len(lowercase_text) - len(pattern) + 1))
            for pattern in patterns
        ]
        payload = f"{lowercase_text} {len(patterns)}\n" + "\n".join(patterns) + "\n"
        assert release17_references["java-curated-150"](payload) == "\n".join(map(str, counts))


def test_random_rollback_stone_and_flow_algorithms_against_brute_oracles(release17_references) -> None:
    rng = random.Random(147149)
    for _ in range(24):
        n = rng.randint(1, 9)
        history = []
        snapshot_ids = []
        operations = []
        expected = []
        for __ in range(35):
            choice = rng.random()
            if choice < 0.5:
                first, second = rng.randrange(n), rng.randrange(n)
                history.append((first, second))
                operations.append(f"U {first} {second}")
            elif choice < 0.68:
                snapshot_ids.append(len(history))
                operations.append("S")
                expected.append(str(len(history)))
            elif choice < 0.82 and snapshot_ids:
                snapshot = rng.choice(snapshot_ids)
                history = history[:snapshot]
                snapshot_ids = [value for value in snapshot_ids if value <= snapshot]
                operations.append(f"R {snapshot}")
            else:
                parent = list(range(n))

                def find(vertex):
                    while parent[vertex] != vertex:
                        vertex = parent[vertex]
                    return vertex

                count = n
                for first, second in history:
                    first, second = find(first), find(second)
                    if first != second:
                        parent[second] = first
                        count -= 1
                operations.append("C")
                expected.append(str(count))
        payload = f"{n} {len(operations)}\n" + "\n".join(operations) + "\n"
        assert release17_references["java-curated-147"](payload) == "\n".join(expected)

        stones = tuple(rng.randint(1, 8) for __ in range(rng.randint(1, 7)))

        @lru_cache(None)
        def merge(state):
            if len(state) == 1:
                return 0
            costs = []
            for index in range(len(state)):
                following = (index + 1) % len(state)
                combined = state[index] + state[following]
                if following == 0:
                    next_state = (combined,) + state[1:-1]
                else:
                    next_state = state[:index] + (combined,) + state[following + 1 :]
                costs.append(combined + merge(next_state))
            return min(costs)

        payload = f"{len(stones)}\n" + " ".join(map(str, stones)) + "\n"
        assert release17_references["java-curated-148"](payload) == str(merge(stones))

        vertices = rng.randint(2, 7)
        source, sink = 0, vertices - 1
        edges = [
            (left, right, rng.randint(0, 9))
            for left in range(vertices)
            for right in range(vertices)
            if left != right and rng.random() < 0.22
        ]
        minimum_cut = min(
            sum(
                capacity
                for left, right, capacity in edges
                if mask >> left & 1 and not (mask >> right & 1)
            )
            for mask in range(1 << vertices)
            if mask & 1 and not (mask >> sink & 1)
        )
        payload = f"{vertices} {len(edges)} {source} {sink}\n" + "".join(
            f"{left} {right} {capacity}\n" for left, right, capacity in edges
        )
        assert release17_references["java-curated-149"](payload) == str(minimum_cut)


@pytest.mark.skipif(not all(main._java_tools()), reason="Java curriculum checks require a local JDK")
@pytest.mark.parametrize("exercise", JAVA_CURRICULUM_PART5, ids=lambda x: x["id"])
def test_references_compile_once_and_pass_all_six_fixtures(exercise: dict) -> None:
    fixtures = [("public", x) for x in exercise["public_tests"]] + [("hidden", x) for x in exercise["hidden_tests"]]
    result = main._validate_java_submission(fixtures, exercise["solution"], 8.0)
    assert result["status"] == "passed", result
