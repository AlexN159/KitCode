import assert from "node:assert/strict";
import test from "node:test";

import {
  findPythonPrefixCompletions,
  pythonCompletionCandidates,
} from "../../app/python-completions.mjs";

test("curated Python completions require an exact prefix of at least three characters", () => {
  assert.deepEqual(findPythonPrefixCompletions("en"), []);
  assert.deepEqual(findPythonPrefixCompletions("enum"), ["enumerate"]);
  assert.deepEqual(findPythonPrefixCompletions("ret"), ["return"]);
  assert.deepEqual(findPythonPrefixCompletions("rang"), ["range"]);
  assert.deepEqual(findPythonPrefixCompletions("def"), []);
  assert.deepEqual(findPythonPrefixCompletions("enumerate"), []);
});

test("completion matching is case-sensitive and only accepts identifier prefixes", () => {
  assert.deepEqual(findPythonPrefixCompletions("ENUM"), []);
  assert.deepEqual(findPythonPrefixCompletions("enum."), []);
  assert.deepEqual(findPythonPrefixCompletions("enum erate"), []);
  assert.deepEqual(findPythonPrefixCompletions("3enum"), []);
  assert.deepEqual(findPythonPrefixCompletions(undefined), []);
});

test("typos and user variable names are never corrected or renamed", () => {
  const originalVariable = "enemerate_count";

  assert.deepEqual(findPythonPrefixCompletions("enemerate"), []);
  assert.equal(originalVariable, "enemerate_count");
  assert.equal(pythonCompletionCandidates.includes("enemerate"), false);
  assert.equal(pythonCompletionCandidates.includes("enumerate"), true);
});

test("callers receive a fresh result without changing the curated candidates", () => {
  const completions = findPythonPrefixCompletions("enum");
  completions.push("not-a-python-completion");

  assert.deepEqual(findPythonPrefixCompletions("enum"), ["enumerate"]);
  assert.equal(Object.isFrozen(pythonCompletionCandidates), true);
});
