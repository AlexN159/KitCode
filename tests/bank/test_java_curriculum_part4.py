"""Release gates for the final Java core curriculum tranche."""

from __future__ import annotations

import ast
import itertools
import math
from pathlib import Path
import random
import re
import subprocess
import tempfile

import pytest

from backend import main
from backend.java_curriculum_part4 import JAVA_CURRICULUM_PART4


SOURCE = Path("backend/java_curriculum_part4.py")


def _normalise(value: str) -> str:
    return "\n".join(line.rstrip() for line in value.replace("\r\n", "\n").strip().split("\n"))


@pytest.fixture(scope="module")
def release17_references():
    javac, java = main._java_tools()
    if not javac or not java:
        pytest.skip("JDK required")
    with tempfile.TemporaryDirectory(prefix="java-part4-audit-") as root:
        runners = {}
        for exercise in JAVA_CURRICULUM_PART4:
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
                return _normalise(result.stdout)

            runners[exercise["id"]] = run
        yield runners


def test_manifest_shape_levels_and_literal_fixture_count():
    assert [x["id"] for x in JAVA_CURRICULUM_PART4] == [
        f"java-curated-{n:03d}" for n in range(121, 141)
    ]
    assert [x["difficulty"] for x in JAVA_CURRICULUM_PART4].count("Easy") == 3
    assert [x["difficulty"] for x in JAVA_CURRICULUM_PART4].count("Medium") == 12
    assert [x["difficulty"] for x in JAVA_CURRICULUM_PART4].count("Hard") == 5
    assert all(
        len(x["public_tests"]) == 2 and len(x["hidden_tests"]) == 4
        for x in JAVA_CURRICULUM_PART4
    )
    assert len({x["title"] for x in JAVA_CURRICULUM_PART4}) == 20


def test_module_is_pure_ascii_data_with_literal_cases():
    source = SOURCE.read_text(encoding="utf-8")
    assert not any(
        word in source for word in ("subprocess", "sqlite", "requests", "lambda")
    )
    assert all(ord(char) < 128 for char in source)
    calls = [
        node
        for node in ast.walk(ast.parse(source))
        if isinstance(node, ast.Call)
        and isinstance(node.func, ast.Name)
        and node.func.id == "C"
    ]
    assert len(calls) == 120
    assert all(
        len(call.args) == 2
        and all(
            isinstance(arg, ast.Constant) and isinstance(arg.value, str)
            for arg in call.args
        )
        for call in calls
    )


def test_exact_title_source_uniqueness_and_semantic_progressions():
    from backend.exercise_bank import EXERCISES

    prior = [
        value
        for value in EXERCISES.values()
        if value.get("language") == "java"
        and value["id"] not in {item["id"] for item in JAVA_CURRICULUM_PART4}
    ]
    current_titles = {re.sub(r"[^a-z0-9]", "", item["title"].casefold()) for item in JAVA_CURRICULUM_PART4}
    prior_titles = {re.sub(r"[^a-z0-9]", "", item["title"].casefold()) for item in prior}
    assert not current_titles & prior_titles
    compact = lambda text: re.sub(r"\s+", "", text)
    assert not {compact(item["solution"]) for item in JAVA_CURRICULUM_PART4} & {
        compact(item["solution"]) for item in prior
    }
    # These are intentional advanced progressions, not duplicate contracts.
    progressions = {
        "java-curated-130": "java-curated-111",  # many kth ancestors vs one LCA
        "java-curated-135": "java-curated-118",  # weighted vs unit edit costs
    }
    by_id = {item["id"]: item for item in JAVA_CURRICULUM_PART4}
    prior_by_id = {item["id"]: item for item in prior}
    for advanced, foundation in progressions.items():
        assert by_id[advanced]["description"] != prior_by_id[foundation]["description"]


def test_release17_compile_once_and_execute_all_120(release17_references):
    for exercise in JAVA_CURRICULUM_PART4:
        run = release17_references[exercise["id"]]
        for case in exercise["public_tests"] + exercise["hidden_tests"]:
            assert run(case["input"]) == _normalise(case["expected_output"]), exercise["id"]


def test_random_graph_references_against_brute_oracles(release17_references):
    rng = random.Random(121125)
    for _ in range(24):
        n = rng.randint(1, 8)
        edges = [(rng.randrange(n), rng.randrange(n)) for __ in range(rng.randint(0, 13))]

        def components(removed=-1):
            seen = set()
            count = 0
            graph = [[] for __ in range(n)]
            for a, b in edges:
                if a != removed and b != removed:
                    graph[a].append(b)
                    graph[b].append(a)
            for start in range(n):
                if start == removed or start in seen:
                    continue
                count += 1
                seen.add(start)
                stack = [start]
                while stack:
                    for vertex in graph[stack.pop()]:
                        if vertex not in seen:
                            seen.add(vertex)
                            stack.append(vertex)
            return count

        base = components()
        articulation = sum(components(vertex) > base for vertex in range(n))
        payload = f"{n} {len(edges)}\n" + "".join(f"{a} {b}\n" for a, b in edges)
        assert release17_references["java-curated-121"](payload) == str(articulation)

        directed = [(rng.randrange(n), rng.randrange(n)) for __ in range(rng.randint(0, 14))]
        reach = [[row == col for col in range(n)] for row in range(n)]
        for a, b in directed:
            reach[a][b] = True
        for middle in range(n):
            for a in range(n):
                for b in range(n):
                    reach[a][b] |= reach[a][middle] and reach[middle][b]
        component = [-1] * n
        count = 0
        for a in range(n):
            if component[a] >= 0:
                continue
            for b in range(n):
                if reach[a][b] and reach[b][a]:
                    component[b] = count
            count += 1
        incoming = [False] * count
        for a, b in directed:
            if component[a] != component[b]:
                incoming[component[b]] = True
        payload = f"{n} {len(directed)}\n" + "".join(f"{a} {b}\n" for a, b in directed)
        assert release17_references["java-curated-122"](payload) == str(incoming.count(False))

        weighted = [
            (rng.randrange(n), rng.randrange(n), rng.randint(-5, 6))
            for __ in range(rng.randint(0, 15))
        ]
        source = rng.randrange(n)
        infinity = 10**12
        distance = [[infinity] * n for __ in range(n)]
        for vertex in range(n):
            distance[vertex][vertex] = 0
        for a, b, weight in weighted:
            distance[a][b] = min(distance[a][b], weight)
        for middle in range(n):
            for a in range(n):
                for b in range(n):
                    if distance[a][middle] < infinity and distance[middle][b] < infinity:
                        distance[a][b] = min(distance[a][b], distance[a][middle] + distance[middle][b])
        affected = sum(
            any(
                distance[source][cycle] < infinity
                and distance[cycle][cycle] < 0
                and distance[cycle][vertex] < infinity
                for cycle in range(n)
            )
            for vertex in range(n)
        )
        payload = f"{n} {len(weighted)} {source}\n" + "".join(
            f"{a} {b} {weight}\n" for a, b, weight in weighted
        )
        assert release17_references["java-curated-123"](payload) == str(affected)

        nonnegative = [
            (rng.randrange(n), rng.randrange(n), rng.randint(0, 12))
            for __ in range(rng.randint(0, 15))
        ]
        queries = [(rng.randrange(n), rng.randrange(n)) for __ in range(12)]
        answers = []
        for start, target in queries:
            shortest = [infinity] * n
            shortest[start] = 0
            for __ in range(n - 1):
                changed = False
                for a, b, weight in nonnegative:
                    if shortest[a] < infinity and shortest[a] + weight < shortest[b]:
                        shortest[b] = shortest[a] + weight
                        changed = True
                if not changed:
                    break
            answers.append("INF" if shortest[target] == infinity else str(shortest[target]))
        payload = f"{n} {len(nonnegative)} {len(queries)}\n" + "".join(
            f"{a} {b} {weight}\n" for a, b, weight in nonnegative
        ) + "".join(f"{a} {b}\n" for a, b in queries)
        assert release17_references["java-curated-124"](payload) == "\n".join(answers)

        # Exhaust every trail for a very small multigraph to verify the smallest start.
        small_n = rng.randint(1, 5)
        trail_edges = [
            (rng.randrange(small_n), rng.randrange(small_n))
            for __ in range(rng.randint(0, 7))
        ]

        def can_traverse(start):
            def search(vertex, used):
                if len(used) == len(trail_edges):
                    return True
                for edge_id, (a, b) in enumerate(trail_edges):
                    if edge_id in used:
                        continue
                    if a == vertex or b == vertex:
                        other = b if a == vertex else a
                        if search(other, used | {edge_id}):
                            return True
                return False

            return search(start, set())

        if not trail_edges:
            expected = "0"
        else:
            valid = [vertex for vertex in range(small_n) if can_traverse(vertex)]
            expected = str(min(valid)) if valid else "NONE"
        payload = f"{small_n} {len(trail_edges)}\n" + "".join(
            f"{a} {b}\n" for a, b in trail_edges
        )
        assert release17_references["java-curated-125"](payload) == expected


def test_random_tree_and_range_references_against_naive_models(release17_references):
    rng = random.Random(126132)
    for _ in range(18):
        n = rng.randint(1, 22)
        left = [-1] * n
        right = [-1] * n
        available = [0]
        for node in range(1, n):
            while True:
                parent = rng.choice(available)
                choices = [side for side in (0, 1) if (left[parent], right[parent])[side] < 0]
                if choices:
                    side = rng.choice(choices)
                    if side == 0:
                        left[parent] = node
                    else:
                        right[parent] = node
                    if left[parent] >= 0 and right[parent] >= 0:
                        available.remove(parent)
                    available.append(node)
                    break
        values = [rng.randint(-30, 30) for __ in range(n)]
        queue = [(0, 0, 0)]
        positioned = []
        while queue:
            node, column, row = queue.pop(0)
            positioned.append((column, row, node))
            if left[node] >= 0:
                queue.append((left[node], column - 1, row + 1))
            if right[node] >= 0:
                queue.append((right[node], column + 1, row + 1))
        expected = " ".join(str(values[node]) for _, _, node in sorted(positioned))
        payload = f"{n}\n" + "".join(
            f"{values[node]} {left[node]} {right[node]}\n" for node in range(n)
        )
        assert release17_references["java-curated-126"](payload) == expected

        boundary = [0]
        node = left[0]
        while node >= 0:
            if left[node] >= 0 or right[node] >= 0:
                boundary.append(node)
            node = left[node] if left[node] >= 0 else right[node]
        leaves = []
        stack = [0]
        while stack:
            node = stack.pop()
            if left[node] < 0 and right[node] < 0:
                if node != 0:
                    leaves.append(node)
            else:
                if right[node] >= 0:
                    stack.append(right[node])
                if left[node] >= 0:
                    stack.append(left[node])
        boundary.extend(leaves)
        right_boundary = []
        node = right[0]
        while node >= 0:
            if left[node] >= 0 or right[node] >= 0:
                right_boundary.append(node)
            node = right[node] if right[node] >= 0 else left[node]
        boundary.extend(reversed(right_boundary))
        expected_boundary = " ".join(str(values[node]) for node in boundary)
        assert release17_references["java-curated-127"](payload) == expected_boundary

        levels = {0: [(0, 0)]}
        for depth in range(n):
            if depth not in levels:
                break
            for node, position in levels[depth]:
                if left[node] >= 0:
                    levels.setdefault(depth + 1, []).append((left[node], 2 * position))
                if right[node] >= 0:
                    levels.setdefault(depth + 1, []).append((right[node], 2 * position + 1))
        width = max(max(position for _, position in level) - min(position for _, position in level) + 1 for level in levels.values())
        payload = f"{n}\n" + "".join(f"{left[node]} {right[node]}\n" for node in range(n))
        assert release17_references["java-curated-128"](payload) == str(width)

        parent = [-1] + [rng.randrange(node) for node in range(1, n)]
        initial = [rng.randint(-20, 20) for __ in range(n)]
        current = initial[:]
        operations = []
        answers = []
        for __ in range(24):
            vertex = rng.randrange(n)
            if rng.random() < 0.55:
                value = rng.randint(-20, 20)
                current[vertex] = value
                operations.append(f"U {vertex} {value}")
            else:
                total = 0
                for node in range(n):
                    ancestor = node
                    while ancestor >= 0 and ancestor != vertex:
                        ancestor = parent[ancestor]
                    if ancestor == vertex:
                        total += current[node]
                answers.append(total)
                operations.append(f"Q {vertex}")
        payload = (
            f"{n} {len(operations)}\n"
            + " ".join(map(str, initial))
            + "\n"
            + " ".join(map(str, parent))
            + "\n"
            + "\n".join(operations)
            + "\n"
        )
        assert release17_references["java-curated-129"](payload) == "\n".join(map(str, answers))

        queries = [(rng.randrange(n), rng.randint(0, n + 3)) for __ in range(20)]
        ancestors = []
        for vertex, distance in queries:
            for __ in range(distance):
                vertex = parent[vertex] if vertex >= 0 else -1
            ancestors.append(vertex)
        payload = (
            f"{n} {len(queries)}\n"
            + " ".join(map(str, parent))
            + "\n"
            + "".join(f"{vertex} {distance}\n" for vertex, distance in queries)
        )
        assert release17_references["java-curated-130"](payload) == "\n".join(map(str, ancestors))

        array = [rng.randint(-30, 30) for __ in range(n)]
        live = array[:]
        operations = []
        minima = []
        for __ in range(25):
            if rng.random() < 0.45:
                index = rng.randrange(n)
                value = rng.randint(-30, 30)
                live[index] = value
                operations.append(f"U {index} {value}")
            else:
                left_index = rng.randrange(n)
                right_index = rng.randrange(left_index, n)
                minima.append(min(live[left_index : right_index + 1]))
                operations.append(f"Q {left_index} {right_index}")
        payload = f"{n} {len(operations)}\n" + " ".join(map(str, array)) + "\n" + "\n".join(operations) + "\n"
        assert release17_references["java-curated-131"](payload) == "\n".join(map(str, minima))

        static_queries = []
        expected_minima = []
        for __ in range(20):
            left_index = rng.randrange(n)
            right_index = rng.randrange(left_index, n)
            static_queries.append((left_index, right_index))
            expected_minima.append(min(array[left_index : right_index + 1]))
        payload = f"{n} {len(static_queries)}\n" + " ".join(map(str, array)) + "\n" + "".join(
            f"{left_index} {right_index}\n" for left_index, right_index in static_queries
        )
        assert release17_references["java-curated-132"](payload) == "\n".join(map(str, expected_minima))


def test_random_dp_numeric_and_geometry_references_against_oracles(release17_references):
    rng = random.Random(133140)
    for _ in range(18):
        n = rng.randint(1, 8)
        dimensions = [rng.randint(1, 12) for __ in range(n + 1)]
        matrix_cost = [[0] * n for __ in range(n)]
        for length in range(2, n + 1):
            for left in range(n - length + 1):
                right = left + length - 1
                matrix_cost[left][right] = min(
                    matrix_cost[left][split]
                    + matrix_cost[split + 1][right]
                    + dimensions[left] * dimensions[split + 1] * dimensions[right + 1]
                    for split in range(left, right)
                )
        payload = f"{n}\n" + " ".join(map(str, dimensions)) + "\n"
        assert release17_references["java-curated-133"](payload) == str(matrix_cost[0][n - 1])

        values = [rng.randint(0, 8) for __ in range(rng.randint(0, 14))]
        target = rng.randint(0, 24)
        count = sum(
            sum(values[index] for index in range(len(values)) if mask >> index & 1) == target
            for mask in range(1 << len(values))
        )
        payload = f"{len(values)} {target}\n" + (" ".join(map(str, values)) + "\n" if values else "")
        assert release17_references["java-curated-134"](payload) == str(count % 1_000_000_007)

        first = "".join(rng.choice("abc") for __ in range(rng.randint(0, 7)))
        second = "".join(rng.choice("abc") for __ in range(rng.randint(0, 7)))
        insert, delete, replace = (rng.randint(1, 6) for __ in range(3))
        edit = [[0] * (len(second) + 1) for __ in range(len(first) + 1)]
        for row in range(len(first) + 1):
            edit[row][0] = row * delete
        for column in range(len(second) + 1):
            edit[0][column] = column * insert
        for row in range(1, len(first) + 1):
            for column in range(1, len(second) + 1):
                edit[row][column] = min(
                    edit[row - 1][column] + delete,
                    edit[row][column - 1] + insert,
                    edit[row - 1][column - 1] + (0 if first[row - 1] == second[column - 1] else replace),
                )
        payload = f"{first}\n{second}\n{insert} {delete} {replace}\n"
        assert release17_references["java-curated-135"](payload) == str(edit[-1][-1])

        subset = [rng.randint(-20, 20) for __ in range(rng.randint(0, 18))]
        wanted = rng.randint(-35, 35)
        difference = min(
            abs(wanted - sum(subset[index] for index in range(len(subset)) if mask >> index & 1))
            for mask in range(1 << len(subset))
        )
        payload = f"{len(subset)} {wanted}\n" + (" ".join(map(str, subset)) + "\n" if subset else "")
        assert release17_references["java-curated-136"](payload) == str(difference)

        lower = rng.randint(0, 180)
        upper = rng.randint(lower, lower + 90)

        def prime(value):
            return value >= 2 and all(value % divisor for divisor in range(2, math.isqrt(value) + 1))

        expected_primes = sum(prime(value) for value in range(lower, upper + 1))
        assert release17_references["java-curated-137"](f"{lower} {upper}\n") == str(expected_primes)

        points = []
        while len(points) < rng.randint(2, 10):
            point = (rng.randint(-12, 12), rng.randint(-12, 12))
            if point not in points:
                points.append(point)
        closest = min(
            (a - c) ** 2 + (b - d) ** 2
            for index, (a, b) in enumerate(points)
            for c, d in points[index + 1 :]
        )
        payload = f"{len(points)}\n" + "".join(f"{a} {b}\n" for a, b in points)
        assert release17_references["java-curated-139"](payload) == str(closest)

        start = min(points)
        hull = []
        current = start
        while True:
            hull.append(current)
            candidate = next(point for point in points if point != current)
            for point in points:
                if point == current:
                    continue
                cross = (candidate[0] - current[0]) * (point[1] - current[1]) - (
                    candidate[1] - current[1]
                ) * (point[0] - current[0])
                candidate_distance = (candidate[0] - current[0]) ** 2 + (candidate[1] - current[1]) ** 2
                point_distance = (point[0] - current[0]) ** 2 + (point[1] - current[1]) ** 2
                if cross > 0 or (cross == 0 and point_distance > candidate_distance):
                    candidate = point
            current = candidate
            if current == start:
                break
        perimeter = sum(
            math.hypot(hull[index][0] - hull[(index + 1) % len(hull)][0], hull[index][1] - hull[(index + 1) % len(hull)][1])
            for index in range(len(hull))
        )
        assert release17_references["java-curated-138"](payload) == f"{perimeter:.6f}"

        intervals = []
        for __ in range(rng.randint(0, 8)):
            left = rng.randint(-6, 5)
            intervals.append((left, rng.randint(left, 7)))
        candidates = sorted({right for _, right in intervals})
        optimum = 0
        for size in range(len(candidates) + 1):
            if any(
                all(any(left <= point <= right for point in chosen) for left, right in intervals)
                for chosen in itertools.combinations(candidates, size)
            ):
                optimum = size
                break
        payload = f"{len(intervals)}\n" + "".join(f"{left} {right}\n" for left, right in intervals)
        assert release17_references["java-curated-140"](payload) == str(optimum)
def test_resource_serialization_and_difficulty_regressions():
    by_id = {exercise["id"]: exercise for exercise in JAVA_CURRICULUM_PART4}

    assert by_id["java-curated-121"]["difficulty"] == "Hard"
    assert by_id["java-curated-122"]["difficulty"] == "Hard"
    assert by_id["java-curated-125"]["difficulty"] == "Easy"
    assert by_id["java-curated-137"]["difficulty"] == "Medium"
    assert by_id["java-curated-140"]["difficulty"] == "Easy"

    assert "dfs(" not in by_id["java-curated-121"]["solution"]
    assert "static void go" not in by_id["java-curated-122"]["solution"]
    assert "leaves(" not in by_id["java-curated-127"]["solution"]

    output_caps = {
        "java-curated-124": "q <= 1800",
        "java-curated-126": "n <= 1900",
        "java-curated-129": "q <= 1100",
        "java-curated-130": "q <= 3000",
        "java-curated-131": "q <= 1900",
        "java-curated-132": "q <= 1900",
    }
    for exercise_id, cap in output_caps.items():
        assert cap in " ".join(by_id[exercise_id]["constraints"])
        assert "24,000-character" in " ".join(by_id[exercise_id]["constraints"])

    assert "depth is at most 62" in " ".join(by_id["java-curated-128"]["constraints"])
    edit = by_id["java-curated-135"]
    assert "nextLine()" in edit["solution"]
    assert any(case["input"].startswith("\n") for case in edit["hidden_tests"])
    assert "10^12" in " ".join(by_id["java-curated-136"]["constraints"])
    assert "-10^9" in " ".join(by_id["java-curated-138"]["constraints"])
    assert "-10^9" in " ".join(by_id["java-curated-139"]["constraints"])


@pytest.mark.skipif(not all(main._java_tools()), reason="JDK required")
@pytest.mark.parametrize("exercise", JAVA_CURRICULUM_PART4, ids=lambda x: x["id"])
def test_all_reference_fixtures(exercise):
    cases = [("public", x) for x in exercise["public_tests"]] + [
        ("hidden", x) for x in exercise["hidden_tests"]
    ]
    result = main._validate_java_submission(cases, exercise["solution"], 4)
    assert result["status"] == "passed", result


@pytest.mark.skipif(not all(main._java_tools()), reason="JDK required")
def test_iterative_graph_solutions_survive_deep_chains():
    by_id = {exercise["id"]: exercise for exercise in JAVA_CURRICULUM_PART4}
    n = 20_000
    undirected = f"{n} {n - 1}\n" + "".join(
        f"{vertex} {vertex + 1}\n" for vertex in range(n - 1)
    )
    directed = undirected
    checks = [
        ("hidden", {"input": undirected, "expected_output": str(n - 2)}),
    ]
    result = main._validate_java_submission(
        checks, by_id["java-curated-121"]["solution"], 8
    )
    assert result["status"] == "passed", result
    result = main._validate_java_submission(
        [("hidden", {"input": directed, "expected_output": "1"})],
        by_id["java-curated-122"]["solution"],
        8,
    )
    assert result["status"] == "passed", result


@pytest.mark.skipif(not all(main._java_tools()), reason="JDK required")
def test_numeric_boundary_regressions():
    by_id = {exercise["id"]: exercise for exercise in JAVA_CURRICULUM_PART4}

    left = [-1] * 125
    right = [-1] * 125
    left[0], right[0] = 1, 2
    left_tip, right_tip, next_node = 1, 2, 3
    for _ in range(2, 63):
        left[left_tip] = next_node
        left_tip = next_node
        next_node += 1
        right[right_tip] = next_node
        right_tip = next_node
        next_node += 1
    width_input = "125\n" + "".join(
        f"{left[node]} {right[node]}\n" for node in range(125)
    )

    cases = {
        "java-curated-128": (width_input, "4611686018427387904"),
        "java-curated-136": (
            "2 -1000000000000\n1000000000000 1000000000000\n",
            "1000000000000",
        ),
        "java-curated-138": (
            "4\n-1000000000 -1000000000\n1000000000 -1000000000\n1000000000 1000000000\n-1000000000 1000000000\n",
            "8000000000.000000",
        ),
        "java-curated-139": (
            "2\n-1000000000 -1000000000\n1000000000 1000000000\n",
            "8000000000000000000",
        ),
    }
    for exercise_id, (input_text, expected_output) in cases.items():
        result = main._validate_java_submission(
            [("hidden", {"input": input_text, "expected_output": expected_output})],
            by_id[exercise_id]["solution"],
            5,
        )
        assert result["status"] == "passed", (exercise_id, result)
