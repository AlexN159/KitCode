"""Presentation-format regressions for the Java and SQL reference corpus."""

from backend.exercise_bank import EXERCISES
from backend.reference_solution_formatting import (
    SQL_AUXILIARY_SPACE_NOTE,
    format_java_reference,
    format_sql_reference,
)


def test_java_formatter_is_token_aware_for_for_headers_and_literals() -> None:
    source = '''public class Main { public static void main(String[] a) { for(int i=0;i<2;i++){System.out.println("a;b");} char c=';'; // keep ; here
} }'''

    formatted = format_java_reference(source)

    assert 'for(int i=0;i<2;i++){' in formatted
    assert 'System.out.println("a;b");' in formatted
    assert "char c=';';" in formatted
    assert "// keep ; here" in formatted


def test_stored_java_and_sql_references_are_readable_and_idempotently_formatted() -> None:
    java = [item["solution"] for item in EXERCISES.values() if item["language"] == "java"]
    sql = [item["solution"] for item in EXERCISES.values() if item["language"] == "sql"]

    assert len(java) == len(sql) == 150
    assert all(solution.count("\n") >= 9 for solution in java)
    assert all(solution.count("\n") >= 3 for solution in sql)
    assert all(format_java_reference(solution) == solution for solution in java)
    assert all(format_sql_reference(solution) == solution for solution in sql)
    assert all(
        item["reference_complexity_note"] == SQL_AUXILIARY_SPACE_NOTE
        for item in EXERCISES.values()
        if item["language"] == "sql"
    )


def test_having_count_drill_is_distinct_from_the_basic_group_count() -> None:
    basic = EXERCISES["sql-group-032"]
    filtered = EXERCISES["sql-having-092"]

    assert basic["solution"] != filtered["solution"]
    assert "exactly two" in filtered["description"].lower()
    assert "HAVING" in filtered["solution"]
    three_and_two = filtered["hidden_tests"][1]
    assert "('E','A')" in three_and_two["setup_sql"]
    assert three_and_two["expected_output"] == "Z\t2"
