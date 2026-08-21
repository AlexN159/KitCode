import ast

from backend.python_reference_formatting import (
    format_python_reference,
    has_statement_separator,
)


def test_expands_simple_and_compound_statement_separators_without_changing_ast():
    source = """def solve():
    total = 0; values = [1, 2]
    for value in values: total += value; print(total)
    if total: print('done'); return
"""
    formatted = format_python_reference(source)
    assert not has_statement_separator(formatted)
    assert ast.dump(ast.parse(formatted), include_attributes=False) == ast.dump(
        ast.parse(source), include_attributes=False
    )
    assert "for value in values:\n        total += value\n        print(total)" in formatted


def test_preserves_semicolons_and_hashes_inside_string_literals_and_comments():
    source = """def solve():
    text = 'a;#b'  # keep this comment
    print(text); return
"""
    formatted = format_python_reference(source)
    assert "'a;#b'  # keep this comment" in formatted
    assert "print(text)\n    return" in formatted
    assert has_statement_separator(formatted) is False


def test_expands_a_single_statement_compound_suite_too():
    source = """def solve():
    if ready: return
"""
    formatted = format_python_reference(source)
    assert "if ready:\n        return" in formatted
    assert ast.dump(ast.parse(formatted), include_attributes=False) == ast.dump(
        ast.parse(source), include_attributes=False
    )


def test_assembled_python_corpus_has_no_statement_separator_and_still_parses():
    from backend.exercise_bank import EXERCISES

    python_references = [
        exercise
        for exercise in EXERCISES.values()
        if exercise.get("language") == "python"
    ]
    assert len(python_references) == 400
    for exercise in python_references:
        source = exercise["solution"]
        assert not has_statement_separator(source), exercise["id"]
        ast.parse(source)
    assert all(
        ast.parse(exercise["solution"])
        for exercise in python_references
        if exercise.get("submission_mode") == "python_class"
    )
