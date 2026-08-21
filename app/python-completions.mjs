/**
 * A deliberately small, curated source of Python completion candidates.
 *
 * This module only matches a currently typed identifier prefix.  It does not
 * attempt spell checking, fuzzy matching, correction, or editing text: the
 * editor remains responsible for displaying a choice and inserting it only
 * after the learner explicitly accepts it.
 */
export const pythonCompletionCandidates = Object.freeze([
  "abs",
  "all",
  "any",
  "bool",
  "break",
  "class",
  "continue",
  "def",
  "dict",
  "elif",
  "else",
  "enumerate",
  "except",
  "filter",
  "finally",
  "float",
  "for",
  "from",
  "if",
  "import",
  "in",
  "input",
  "int",
  "isinstance",
  "len",
  "list",
  "map",
  "max",
  "min",
  "None",
  "not",
  "open",
  "or",
  "pass",
  "print",
  "range",
  "return",
  "reversed",
  "set",
  "sorted",
  "str",
  "sum",
  "try",
  "tuple",
  "while",
  "with",
  "zip",
]);

const pythonIdentifierPrefix = /^[A-Za-z_][A-Za-z0-9_]*$/;

/**
 * Returns the curated completions for an exact Python identifier prefix.
 *
 * Three characters is intentionally the minimum to keep the list quiet.
 * The result is a new array, so callers cannot mutate the curated catalog.
 */
export function findPythonPrefixCompletions(prefix) {
  if (
    typeof prefix !== "string" ||
    prefix.length < 3 ||
    !pythonIdentifierPrefix.test(prefix)
  ) {
    return [];
  }

  return pythonCompletionCandidates.filter(
    (candidate) => candidate.length > prefix.length && candidate.startsWith(prefix),
  );
}
