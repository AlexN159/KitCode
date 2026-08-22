import assert from "node:assert/strict";
import test from "node:test";

import {
  javaInterviewQuestions,
  machineLearningInterviewQuestions,
  sqlInterviewQuestions,
} from "../../app/interview-question-banks.mjs";

const banks = [
  ["sql-interview", sqlInterviewQuestions, 100],
  ["java-interview", javaInterviewQuestions, 100],
  ["ml-interview", machineLearningInterviewQuestions, 100],
];

test("new interview banks export stable, scoreable multiple-choice questions", () => {
  for (const [prefix, bank, expectedLength] of banks) {
    assert.equal(bank.length, expectedLength);
    assert.equal(new Set(bank.map(({ id }) => id)).size, expectedLength);
    assert.deepEqual(
      bank.map(({ id }) => id),
      Array.from(
        { length: expectedLength },
        (_, index) => `${prefix}-${String(index + 1).padStart(3, "0")}`,
      ),
    );

    for (const item of bank) {
      assert.equal(item.title, item.question.slice(0, -1));
      assert.equal(item.question.endsWith("?"), true);
      assert.equal(item.options.length, 4);
      assert.equal(
        new Set(item.options.map((option) => option.toLocaleLowerCase())).size,
        4,
      );
      assert.equal(Number.isInteger(item.correctIndex), true);
      assert.equal(item.correctIndex >= 0 && item.correctIndex < 4, true);
      assert.equal(item.explanation.length >= 40, true);
      assert.equal(
        ["Easy", "Intermediate", "Advanced"].includes(item.difficulty),
        true,
      );
    }
  }
});

test("SQL and Java banks cover common interview areas", () => {
  const sql = sqlInterviewQuestions
    .map(({ question, explanation }) => `${question} ${explanation}`)
    .join(" ")
    .toLocaleLowerCase();
  const java = javaInterviewQuestions
    .map(({ question, explanation }) => `${question} ${explanation}`)
    .join(" ")
    .toLocaleLowerCase();

  for (const concept of ["left join", "window function", "index", "transaction", "sql injection"])
    assert.match(sql, new RegExp(concept));
  for (const concept of ["jvm", "equals", "generics", "hashmap", "virtual threads"])
    assert.match(java, new RegExp(concept));
  for (const concept of ["serializable", "keyset pagination", "cardinality estimation", "relational division"])
    assert.match(sql, new RegExp(concept));
  for (const concept of ["completablefuture", "class loading", "bigdecimal", "thread interruption"])
    assert.match(java, new RegExp(concept));
});

test("machine-learning bank covers requested core concepts and interview breadth", () => {
  const content = machineLearningInterviewQuestions
    .map(({ question, explanation }) => `${question} ${explanation}`)
    .join(" ")
    .toLocaleLowerCase();

  for (const concept of [
    "linear regression",
    "gradient descent",
    "l1 regularization",
    "l2 regularization",
    "queries, keys, and values",
    "random forest",
    "data leakage",
    "precision-recall",
    "cross-entropy",
    "collaborative filtering",
    "cross-attention",
    "convolutional layers",
  ])
    assert.match(content, new RegExp(concept));
});
