import sqlite3

from backend.generated_sql_templates import SCHEMA_FAMILIES, choose_schema, visible_schema_description


def test_schema_families_are_small_static_sqlite_datasets() -> None:
    assert {family.id for family in SCHEMA_FAMILIES} == {"employees", "orders", "events", "inventory"}
    for family in SCHEMA_FAMILIES:
        assert len(family.fixtures) >= 2
        assert "INSERT" not in visible_schema_description(family).upper()
        for setup in family.server_only_setups:
            assert "CREATE TABLE" in setup.upper()
            assert "INSERT INTO" in setup.upper()
            db = sqlite3.connect(":memory:")
            try:
                db.executescript(setup)
            finally:
                db.close()


def test_choose_schema_is_stable_and_topic_aware() -> None:
    assert choose_schema("salary analysis", "drill-8").id == "employees"
    assert choose_schema("warehouse stock", "drill-8").id == "inventory"
    assert choose_schema("random", "same-seed") == choose_schema("random", "same-seed")
