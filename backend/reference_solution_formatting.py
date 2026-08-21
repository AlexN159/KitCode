"""Deterministic presentation formatting for trusted reference solutions.

The exercise sources intentionally keep many reference programs compact so the
curriculum modules stay reviewable.  Learners, however, should receive normal
source code and a meaningful line count.  These formatters run only over the
trusted, checked-in Java and SQLite reference corpus during bank assembly.
"""
from __future__ import annotations

from sqlglot import parse_one


SQL_AUXILIARY_SPACE_NOTE = (
    "Auxiliary space depends on the database engine and query plan; this "
    "reviewed query avoids unnecessary sorts and materialization."
)


def format_java_reference(source: str) -> str:
    """Format Java without touching tokens inside strings, chars, or comments.

    This is deliberately a small lexer rather than a regex/semicolon splitter:
    semicolons in ``for`` headers and literals must remain in place.  The
    curriculum uses conventional brace-delimited Java, which makes structural
    indentation deterministic without reordering or transforming expressions.
    """
    lines: list[str] = []
    current: list[str] = []
    indent = 0
    parens = 0
    state = "code"
    index = 0

    def emit() -> None:
        text = "".join(current).strip()
        current.clear()
        if text:
            lines.append("    " * indent + text)

    def append_space() -> None:
        if current and not current[-1].isspace():
            current.append(" ")

    while index < len(source):
        char = source[index]
        following = source[index + 1] if index + 1 < len(source) else ""

        if state == "string":
            current.append(char)
            if char == "\\" and following:
                current.append(following)
                index += 2
                continue
            if char == '"':
                state = "code"
            index += 1
            continue
        if state == "char":
            current.append(char)
            if char == "\\" and following:
                current.append(following)
                index += 2
                continue
            if char == "'":
                state = "code"
            index += 1
            continue
        if state == "line-comment":
            if char in "\r\n":
                emit()
                state = "code"
            else:
                current.append(char)
            index += 1
            continue
        if state == "block-comment":
            current.append(char)
            if char == "*" and following == "/":
                current.append(following)
                index += 2
                emit()
                state = "code"
                continue
            index += 1
            continue

        if char == '"':
            current.append(char)
            state = "string"
        elif char == "'":
            current.append(char)
            state = "char"
        elif char == "/" and following == "/":
            append_space()
            current.extend((char, following))
            state = "line-comment"
            index += 1
        elif char == "/" and following == "*":
            append_space()
            current.extend((char, following))
            state = "block-comment"
            index += 1
        elif char.isspace():
            if char in "\r\n":
                emit()
            else:
                append_space()
        elif char == "(":
            current.append(char)
            parens += 1
        elif char == ")":
            current.append(char)
            parens = max(0, parens - 1)
        elif char == "{":
            current.append(char)
            emit()
            indent += 1
        elif char == "}":
            emit()
            indent = max(0, indent - 1)
            current.append(char)
            if following not in ";,)]":
                emit()
        elif char == ";":
            current.append(char)
            if parens == 0:
                emit()
        else:
            current.append(char)
        index += 1

    emit()
    return "\n".join(lines) + "\n"


def format_sql_reference(source: str) -> str:
    """Render a checked-in SQLite SELECT/CTE reference using sqlglot's AST."""
    return parse_one(source, read="sqlite").sql(dialect="sqlite", pretty=True) + "\n"
