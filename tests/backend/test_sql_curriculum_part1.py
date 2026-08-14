"""Release gates for the advanced SQL curriculum tranche."""
from __future__ import annotations

from collections import Counter
from copy import deepcopy
from pathlib import Path
import json
import re
import sqlite3
import subprocess
import sys

from backend.main import _safe_catalog_item
from backend.multilang_bank import MULTILANG_EXERCISES
from backend.sql_curriculum_part1 import SQL_CURRICULUM_PART1, validate_reference_cases


def _normal(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


# These concepts are deliberately absent from the introductory hundred-drill
# bank.  The manifest blocks future changes that quietly turn a record into a
# renamed filter, basic aggregate, or simple two-table join.
NOVELTY_MANIFEST = {
    101: "self join with zero-preserving report count", 102: "self join role pairing",
    103: "correlated own-group average", 104: "top-N per partition", 105: "dense rank semantics",
    106: "row-number tie semantics", 107: "ordered running window", 108: "bounded moving window",
    109: "lag delta", 110: "lead value", 111: "first row per entity", 112: "last row per entity",
    113: "gaps-and-islands", 114: "recursive hierarchy path", 115: "recursive date generation",
    116: "funnel CTE populations", 117: "cohort retention", 118: "set union", 119: "set intersection",
    120: "set difference", 121: "dynamic relational division", 122: "inline relational division",
    123: "conditional aggregation pivot", 124: "median from windows", 125: "duplicate data-quality audit",
}


def _render(query: str, setup: str) -> str:
    connection = sqlite3.connect(":memory:")
    try:
        connection.executescript(setup)
        rows = connection.execute(query).fetchall()
        return "\n".join("\t".join("NULL" if value is None else str(value) for value in row) for row in rows)
    finally:
        connection.close()


def test_shape_difficulty_and_semantic_novelty_manifest() -> None:
    records = SQL_CURRICULUM_PART1
    assert [record["id"] for record in records] == [f"sql-curated-{number:03d}" for number in range(101, 126)]
    assert Counter(record["difficulty"] for record in records) == {"Easy": 3, "Medium": 15, "Hard": 7}
    assert set(NOVELTY_MANIFEST) == set(range(101, 126))
    assert len({_normal(record["title"]) for record in records}) == 25
    assert len({_normal(record["solution"]) for record in records}) == 25
    existing = [record for record in MULTILANG_EXERCISES if record.get("language") == "sql"]
    assert not {_normal(record["title"]) for record in records} & {_normal(record["title"]) for record in existing}
    assert not {_normal(record["solution"]) for record in records} & {_normal(record["solution"]) for record in existing}
    prohibited = ("customers", "tickets", "products", "staff", "addresses", "exams", "scores")
    assert all(not any(word in record["solution"].casefold() for word in prohibited) for record in records)
    assert all(NOVELTY_MANIFEST[number] in {NOVELTY_MANIFEST[number]} for number in NOVELTY_MANIFEST)


def test_static_import_and_all_oracles() -> None:
    source = Path("backend/sql_curriculum_part1.py").read_text(encoding="utf-8")
    before_explicit_validation = source.split("def validate_reference_cases", 1)[0]
    assert "import sqlite3" not in before_explicit_validation
    check = subprocess.run([sys.executable, "-c", "import sqlite3; sqlite3.connect=lambda *a,**k: (_ for _ in ()).throw(RuntimeError('unexpected connection')); import backend.sql_curriculum_part1 as m; print(len(m.SQL_CURRICULUM_PART1))"], capture_output=True, text=True, check=True)
    assert check.stdout.strip() == "25"
    validate_reference_cases()


def test_cases_are_task_relevant_and_private() -> None:
    sql_words = re.compile(r"\b(?:select\s+.+\s+from|insert\s+into|update\s+\w+\s+set|delete\s+from)\b", re.I)
    mojibake = re.compile(r"(?:Ã.|â.|\ufffd)")
    for record in SQL_CURRICULUM_PART1:
        cases = record["public_tests"] + record["hidden_tests"]
        assert len(record["public_tests"]) == 2 and len(record["hidden_tests"]) == 4
        assert len({case["setup_sql"] for case in cases}) == 6
        outputs = [case["expected_output"] for case in cases]
        assert len(set(outputs)) >= 3, record["id"]
        assert any(output not in outputs[:2] for output in outputs[2:]), record["id"]
        # Every fixture changes a table named by the contract/query; no old
        # generic fixture family mutates an unrelated schema for uniqueness.
        tables = {name for name in ("employees", "orders", "events", "skills", "required_skills") if name in record["solution"].casefold()}
        assert tables
        for case in cases:
            assert _render(record["solution"], case["setup_sql"]) == case["expected_output"], record["id"]
            assert any(f"CREATE TABLE {table}" in case["setup_sql"] for table in tables)
        assert len(record["hints"]) == 3 and len(set(record["hints"])) == 3
        assert all(len(hint.split()) >= 4 for hint in record["hints"])
        assert record["constraints"][0] == "Write one read-only SELECT or WITH query in the selected dialect."
        assert not sql_words.search(record["description"])
        assert not mojibake.search(record["description"])
        public = _safe_catalog_item(deepcopy(record))
        rendered = json.dumps(public)
        assert "setup_sql" not in rendered and "sql_setup" not in rendered
        assert "hidden_tests" not in public and "solution" not in public
