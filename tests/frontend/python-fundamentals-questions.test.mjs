import assert from "node:assert/strict";
import test from "node:test";

import { pythonFundamentalsQuestions } from "../../app/python-fundamentals-questions.mjs";

const requiredFields = ["id", "title", "topic", "difficulty", "question", "options", "correctIndex", "explanation"];

test("Python fundamentals bank exports exactly 100 stable, scoreable questions", () => {
  assert.equal(pythonFundamentalsQuestions.length, 100);
  assert.deepEqual(
    pythonFundamentalsQuestions.map(({ id }) => id),
    Array.from({ length: 100 }, (_, index) => `python-fundamentals-${String(index + 1).padStart(3, "0")}`),
  );

  for (const item of pythonFundamentalsQuestions) {
    assert.deepEqual(Object.keys(item).sort(), [...requiredFields].sort());
    assert.equal(item.title, item.question.slice(0, -1));
    assert.equal(item.question.endsWith("?"), true);
    assert.equal(item.options.length, 4);
    assert.equal(new Set(item.options.map((option) => option.toLocaleLowerCase())).size, 4);
    assert.equal(Number.isInteger(item.correctIndex), true);
    assert.equal(item.correctIndex >= 0 && item.correctIndex < item.options.length, true);
    assert.equal(item.explanation.length >= 25, true);
    assert.equal(["Easy", "Intermediate", "Advanced"].includes(item.difficulty), true);
  }
});

test("Python fundamentals bank includes essential interview coverage", () => {
  const questions = pythonFundamentalsQuestions.map(({ question }) => question.toLocaleLowerCase()).join(" ");
  const topics = new Set(pythonFundamentalsQuestions.map(({ topic }) => topic));
  assert.match(questions, /global interpreter lock/);
  assert.match(questions, /immutable/);
  for (const topic of ["types", "functions", "collections", "oop", "exceptions", "concurrency"]) assert.equal(topics.has(topic), true);
});

test("Python fundamentals bank keeps version-sensitive and protocol answers precise", () => {
  const byId = new Map(pythonFundamentalsQuestions.map((item) => [item.id, item]));

  assert.match(byId.get("python-fundamentals-001").options[0], /GIL-enabled build/);
  assert.match(byId.get("python-fundamentals-001").explanation, /free-threaded CPython builds/);
  assert.equal(byId.get("python-fundamentals-014").options[3], "tuple containing only hashable values");
  assert.equal(byId.get("python-fundamentals-026").options[1], "Only if the loop completed normally without break");
  assert.equal(byId.get("python-fundamentals-068").options[1], "Instances become unhashable by default");
});
