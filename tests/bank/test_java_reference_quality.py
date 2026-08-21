"""Focused quality regressions for curated Java reference implementations."""

from backend.exercise_bank import EXERCISES


def test_word_search_reference_uses_path_space_not_a_grid_sized_visited_copy() -> None:
    exercise = EXERCISES["java-int-word-search"]

    assert exercise["expected_complexity"] == (
        "O(rows × cols × 4^word length) time, O(word length) space"
    )
    assert "boolean[][]v" not in exercise["solution"]
    assert "char saved=g[x][y];" in exercise["solution"]
    assert "g[x][y]=0;" in exercise["solution"]
    assert "g[x][y]=saved;" in exercise["solution"]
    assert "return ok;" in exercise["solution"]
