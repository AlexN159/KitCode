"""Release gates for the final 25 SQL curriculum records."""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import sqlite3
import subprocess
import sys

from backend.sql_curriculum_part2 import SQL_CURRICULUM_PART2, validate_reference_cases
from backend.sql_curriculum_part2_oracles import ORACLE_OUTPUTS


def _render(query: str, setup: str) -> str:
    db = sqlite3.connect(":memory:")
    try:
        db.executescript(setup)
        return "\n".join("\t".join("NULL" if value is None else str(value) for value in row) for row in db.execute(query).fetchall())
    finally:
        db.close()


def test_catalogue_shape_and_static_import() -> None:
    assert [x["id"] for x in SQL_CURRICULUM_PART2] == [f"sql-curated-{n:03d}" for n in range(126, 151)]
    assert Counter(x["difficulty"] for x in SQL_CURRICULUM_PART2) == {"Easy": 3, "Medium": 14, "Hard": 8}
    assert len({x["title"].casefold() for x in SQL_CURRICULUM_PART2}) == 25
    assert len({x["solution"].casefold() for x in SQL_CURRICULUM_PART2}) == 25
    assert set(ORACLE_OUTPUTS) == {x["id"] for x in SQL_CURRICULUM_PART2}
    source = Path("backend/sql_curriculum_part2.py").read_text(encoding="utf-8").split("def validate_reference_cases", 1)[0]
    assert "import sqlite3" not in source
    check = subprocess.run([sys.executable, "-c", "import sqlite3; sqlite3.connect=lambda *a,**k: (_ for _ in ()).throw(RuntimeError()); import backend.sql_curriculum_part2 as m; print(len(m.SQL_CURRICULUM_PART2))"], capture_output=True, text=True, check=True)
    assert check.stdout.strip() == "25"


def test_all_six_static_fixtures_replay_and_have_hidden_novelty() -> None:
    validate_reference_cases()
    for record in SQL_CURRICULUM_PART2:
        cases = record["public_tests"] + record["hidden_tests"]
        assert len(cases) == 6 and len(record["public_tests"]) == 2
        assert len(ORACLE_OUTPUTS[record["id"]]) == 6
        outputs = [case["expected_output"] for case in cases]
        assert len(set(outputs)) >= 3, record["id"]
        assert any(value not in outputs[:2] for value in outputs[2:]), record["id"]
        assert len({case["setup_sql"] for case in cases}) == 6
        assert all(_render(record["solution"], case["setup_sql"]) == case["expected_output"] for case in cases)
        assert len(record["hints"]) == 3 and len(set(record["hints"])) == 3
        assert all(len(hint.split()) >= 4 for hint in record["hints"])


def test_ascii_source_has_no_fixture_leak_or_mojibake() -> None:
    source = Path("backend/sql_curriculum_part2.py").read_text(encoding="utf-8")
    assert all(ord(char) < 128 for char in source)
    assert "setup_sql" not in str({key: value for key, value in SQL_CURRICULUM_PART2[0].items() if key not in {"public_tests", "hidden_tests", "sql_setup"}})


def test_documented_tie_and_exclusion_contract_edges() -> None:
    records = {record["id"]: record for record in SQL_CURRICULUM_PART2}
    sessions = records["sql-curated-132"]
    tied_login_setup = sessions["public_tests"][0]["setup_sql"] + (
        "INSERT INTO events VALUES (18,1,'login','2024-02-10 09:20');"
    )
    assert _render(sessions["solution"], tied_login_setup) == (
        "1\t1\t2024-02-10 09:00\t2024-02-10 09:20\t3\n"
        "1\t2\t2024-02-10 10:05\t2024-02-10 10:05\t1\n"
        "2\t1\t2024-02-11 09:00\t2024-02-11 09:00\t1\n"
        "2\t2\t2024-02-11 09:45\t2024-02-11 09:45\t1"
    )
    reachability = records["sql-curated-148"]
    direct_return_setup = reachability["public_tests"][0]["setup_sql"] + (
        "INSERT INTO flights VALUES (6,'A','A','2024-04-01 14:00','2024-04-01 15:00',50);"
    )
    assert _render(reachability["solution"], direct_return_setup) == "B\nC\nD"
