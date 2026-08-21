"""Lossless-enough readability normalization for trusted Python references.

Curriculum declarations sometimes put several simple-suite statements on one
physical line.  This formatter only expands statement separators; unlike an
AST unparser it preserves comments, string spelling, and the surrounding
hand-authored source.  It is intentionally narrow: it is not a general Python
formatter.
"""
from __future__ import annotations

import ast
import io
import re
import tokenize


_COMPOUND_HEADER = re.compile(
    r"(?:async\s+)?(?:if|elif|else|for|while|def|class|try|except|finally|with|match|case)\b"
)


def _line_operators(source: str) -> dict[int, list[tuple[int, str]]]:
    """Locate only real punctuation tokens, never lookalikes in strings."""

    operators: dict[int, list[tuple[int, str]]] = {}
    for token in tokenize.generate_tokens(io.StringIO(source).readline):
        if token.type == tokenize.OP and token.string in {";", ":"}:
            operators.setdefault(token.start[0] - 1, []).append(
                (token.start[1], token.string)
            )
    return operators


def _header_colon(line: str, stop_column: int) -> int | None:
    """Find the top-level suite colon for a one-line compound statement."""

    if not _COMPOUND_HEADER.match(line.lstrip(" \t")):
        return None
    depth = 0
    for token in tokenize.generate_tokens(io.StringIO(line).readline):
        if token.type != tokenize.OP:
            continue
        if token.string in "([{":
            depth += 1
        elif token.string in ")]}":
            depth -= 1
        elif token.string == ":" and depth == 0 and token.start[1] < stop_column:
            return token.start[1]
    return None


def format_python_reference(source: str) -> str:
    """Expand real ``;`` statement separators while preserving Python meaning.

    An inline compound suite such as ``if ready: save(); return`` becomes a
    conventional indented suite.  Other statements retain their existing
    indentation.  The AST comparison is a safety belt for the checked-in
    corpus: a formatting bug raises at assembly rather than changing a judged
    reference silently.
    """

    original_tree = ast.dump(ast.parse(source), include_attributes=False)
    lines = source.splitlines()
    changed = False
    for line_number, operators in _line_operators(source).items():
        semicolons = [column for column, symbol in operators if symbol == ";"]
        line = lines[line_number]
        leading = line[: len(line) - len(line.lstrip(" \t"))]
        first_separator = min(semicolons) if semicolons else len(line)
        colon = _header_colon(line, first_separator)
        if colon is not None:
            trailing = line[colon + 1 :].strip()
            if not trailing or trailing.startswith("#"):
                colon = None
        if not semicolons and colon is None:
            continue
        statement_indent = leading + "    " if colon is not None else leading
        replacements = {column: "\n" + statement_indent for column in semicolons}
        if colon is not None:
            replacements[colon] = ":\n" + statement_indent
        changed = True
        pieces: list[str] = []
        cursor = 0
        for column in sorted(replacements):
            pieces.extend((line[cursor:column], replacements[column]))
            cursor = column + 1
            # The replacement already provides the indentation for the next
            # statement.  Retaining the cosmetic space after ``;`` or ``:``
            # would create an accidental extra indent.
            while cursor < len(line) and line[cursor] in " \t":
                cursor += 1
        pieces.append(line[cursor:])
        lines[line_number] = "".join(pieces)
    if not changed:
        return source
    formatted = "\n".join(lines) + ("\n" if source.endswith("\n") else "")
    if ast.dump(ast.parse(formatted), include_attributes=False) != original_tree:
        raise ValueError("Python reference formatter changed program structure.")
    return formatted


def has_statement_separator(source: str) -> bool:
    """Return whether source contains a real (not string-literal) semicolon."""

    return any(
        symbol == ";"
        for operators in _line_operators(source).values()
        for _, symbol in operators
    )
