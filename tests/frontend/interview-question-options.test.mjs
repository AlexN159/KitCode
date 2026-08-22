import assert from "node:assert/strict";
import test from "node:test";

import {
  javaInterviewQuestions,
  machineLearningInterviewQuestions,
  sqlInterviewQuestions,
} from "../../app/interview-question-banks.mjs";
import { balanceInterviewQuestionOptions } from "../../app/interview-question-options.mjs";
import { pythonFundamentalsQuestions } from "../../app/python-fundamentals-questions.mjs";

const banks = [
  ["python-fundamentals", pythonFundamentalsQuestions],
  ["sql-interview", sqlInterviewQuestions],
  ["java-interview", javaInterviewQuestions],
  ["machine-learning-interview", machineLearningInterviewQuestions],
];

function longestAnswerPositionRun(questions) {
  let longest = 0;
  let current = 0;
  let previous = -1;
  for (const question of questions) {
    current = question.correctIndex === previous ? current + 1 : 1;
    previous = question.correctIndex;
    longest = Math.max(longest, current);
  }
  return longest;
}

test("every 100-question bank presents exactly 25 correct answers in each A-D position", () => {
  for (const [seed, source] of banks) {
    const balanced = balanceInterviewQuestionOptions(source, seed);
    assert.deepEqual(
      [0, 1, 2, 3].map(
        (position) =>
          balanced.filter((question) => question.correctIndex === position)
            .length,
      ),
      [25, 25, 25, 25],
      seed,
    );
    assert.equal(longestAnswerPositionRun(balanced) <= 2, true, seed);
  }
});

test("balancing preserves the correct answer and deterministically permutes every option set", () => {
  for (const [seed, source] of banks) {
    const balanced = balanceInterviewQuestionOptions(source, seed);
    const repeated = balanceInterviewQuestionOptions(source, seed);
    assert.deepEqual(balanced, repeated);

    for (let index = 0; index < source.length; index += 1) {
      const original = source[index];
      const presented = balanced[index];
      assert.equal(
        presented.options[presented.correctIndex],
        original.options[original.correctIndex],
      );
      assert.deepEqual(
        [...presented.options].sort(),
        [...original.options].sort(),
      );
    }
  }
});
