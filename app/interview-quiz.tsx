"use client";

import { useEffect, useMemo, useState } from "react";
import {
  javaInterviewQuestions,
  machineLearningInterviewQuestions,
  sqlInterviewQuestions,
  type InterviewQuestion,
} from "./interview-question-banks.mjs";
import { balanceInterviewQuestionOptions } from "./interview-question-options.mjs";
import { pythonFundamentalsQuestions } from "./python-fundamentals-questions.mjs";

export type InterviewSubject =
  | "python"
  | "sql"
  | "java"
  | "machine-learning";

type QuizAnswers = Record<string, number>;
type QuizFilter = "all" | "unanswered" | "incorrect";

const subjectConfig: Record<
  InterviewSubject,
  {
    label: string;
    crumb: string;
    eyebrow: string;
    description: string;
    storageNamespace: string;
    legacyQuestions: readonly InterviewQuestion[];
    questions: readonly InterviewQuestion[];
  }
> = {
  python: {
    label: "Python Fundamentals",
    crumb: "Python",
    eyebrow: "OPTIONAL INTERVIEW PRACTICE",
    description:
      "common multiple-choice interview questions covering Python syntax, behavior, and design.",
    storageNamespace: "python-fundamentals",
    legacyQuestions: pythonFundamentalsQuestions,
    questions: balanceInterviewQuestionOptions(
      pythonFundamentalsQuestions,
      "python-fundamentals",
    ),
  },
  sql: {
    label: "SQL Interview FAQs",
    crumb: "SQL",
    eyebrow: "QUERY & DATABASE INTERVIEW PRACTICE",
    description:
      "interview questions on querying, joins, modeling, indexes, transactions, and performance.",
    storageNamespace: "sql-interview",
    legacyQuestions: sqlInterviewQuestions,
    questions: balanceInterviewQuestionOptions(sqlInterviewQuestions, "sql-interview"),
  },
  java: {
    label: "Java Interview FAQs",
    crumb: "Java",
    eyebrow: "JAVA INTERVIEW PRACTICE",
    description:
      "interview questions on Java semantics, OOP, collections, the JVM, and concurrency.",
    storageNamespace: "java-interview",
    legacyQuestions: javaInterviewQuestions,
    questions: balanceInterviewQuestionOptions(
      javaInterviewQuestions,
      "java-interview",
    ),
  },
  "machine-learning": {
    label: "Machine Learning Concepts",
    crumb: "Machine Learning",
    eyebrow: "CORE CONCEPT INTERVIEW FAQS",
    description:
      "interview questions spanning classical ML, evaluation, regularization, neural networks, and transformers.",
    storageNamespace: "machine-learning-interview",
    legacyQuestions: machineLearningInterviewQuestions,
    questions: balanceInterviewQuestionOptions(
      machineLearningInterviewQuestions,
      "machine-learning-interview",
    ),
  },
};

function isAnswerIndex(question: InterviewQuestion, value: unknown) {
  return (
    Number.isInteger(value) &&
    Number(value) >= 0 &&
    Number(value) < question.options.length
  );
}

function readSavedAnswers(
  storageKey: string,
  questions: readonly InterviewQuestion[],
  legacyStorageKey: string,
  legacyQuestions: readonly InterviewQuestion[],
): QuizAnswers {
  if (typeof window === "undefined") return {};
  try {
    const currentSaved = window.localStorage.getItem(storageKey);
    if (currentSaved !== null) {
      const parsed = JSON.parse(currentSaved) as Record<string, unknown>;
      return Object.fromEntries(
        questions.flatMap((question) =>
          isAnswerIndex(question, parsed[question.id])
            ? [[question.id, Number(parsed[question.id])]]
            : [],
        ),
      );
    }

    const legacySaved = window.localStorage.getItem(legacyStorageKey);
    if (legacySaved === null) return {};
    const parsed = JSON.parse(legacySaved) as Record<string, unknown>;
    const legacyById = new Map(
      legacyQuestions.map((question) => [question.id, question]),
    );
    return Object.fromEntries(
      questions.flatMap((question) => {
        const legacyQuestion = legacyById.get(question.id);
        const legacyAnswer = parsed[question.id];
        if (!legacyQuestion || !isAnswerIndex(legacyQuestion, legacyAnswer))
          return [];
        const selectedAnswer = legacyQuestion.options[Number(legacyAnswer)];
        const migratedIndex = question.options.indexOf(selectedAnswer);
        return migratedIndex >= 0 ? [[question.id, migratedIndex]] : [];
      }),
    );
  } catch {
    return {};
  }
}

function readSavedQuestionId(
  storageKey: string,
  questions: readonly InterviewQuestion[],
) {
  if (typeof window === "undefined") return questions[0]?.id ?? "";
  try {
    const saved = window.localStorage.getItem(storageKey);
    return questions.some((question) => question.id === saved)
      ? saved!
      : (questions[0]?.id ?? "");
  } catch {
    return questions[0]?.id ?? "";
  }
}

function optionLetter(index: number) {
  return String.fromCharCode(65 + index);
}

export function InterviewQuiz({
  subject,
  clock,
  onReturnToCoding,
  returnLabel = "Return to coding",
}: {
  subject: InterviewSubject;
  clock: string;
  onReturnToCoding: () => void;
  returnLabel?: string;
}) {
  const config = subjectConfig[subject];
  const questions = config.questions;
  const progressStorageKey = `kitcode:${config.storageNamespace}-progress-v2`;
  const legacyProgressStorageKey = `kitcode:${config.storageNamespace}-progress-v1`;
  const selectedQuestionStorageKey = `kitcode:selected-${config.storageNamespace}-question`;
  const [answers, setAnswers] = useState<QuizAnswers>(() =>
    readSavedAnswers(
      progressStorageKey,
      questions,
      legacyProgressStorageKey,
      config.legacyQuestions,
    ),
  );
  const [questionId, setQuestionId] = useState(() =>
    readSavedQuestionId(selectedQuestionStorageKey, questions),
  );
  const [selectedOption, setSelectedOption] = useState<number | null>(() => {
    const savedAnswers = readSavedAnswers(
      progressStorageKey,
      questions,
      legacyProgressStorageKey,
      config.legacyQuestions,
    );
    const savedQuestion = readSavedQuestionId(
      selectedQuestionStorageKey,
      questions,
    );
    return savedAnswers[savedQuestion] ?? null;
  });
  const [topic, setTopic] = useState("All topics");
  const [filter, setFilter] = useState<QuizFilter>("all");
  const [announcement, setAnnouncement] = useState("");

  const currentIndex = Math.max(
    0,
    questions.findIndex((question) => question.id === questionId),
  );
  const current = questions[currentIndex] ?? questions[0];
  const submittedAnswer = current ? answers[current.id] : undefined;
  const answered = Object.keys(answers).length;
  const correct = questions.filter(
    (question) => answers[question.id] === question.correctIndex,
  ).length;
  const topics = useMemo(
    () =>
      Array.from(new Set(questions.map((question) => question.topic))).sort(
        (left, right) => left.localeCompare(right),
      ),
    [questions],
  );
  const visibleQuestions = useMemo(
    () =>
      questions.filter((question) => {
        if (topic !== "All topics" && question.topic !== topic) return false;
        if (filter === "unanswered") return answers[question.id] === undefined;
        if (filter === "incorrect")
          return (
            answers[question.id] !== undefined &&
            answers[question.id] !== question.correctIndex
          );
        return true;
      }),
    [answers, filter, questions, topic],
  );

  useEffect(() => {
    try {
      window.localStorage.setItem(progressStorageKey, JSON.stringify(answers));
    } catch {
      /* Progress remains available for the current session. */
    }
  }, [answers, progressStorageKey]);

  useEffect(() => {
    try {
      window.localStorage.setItem(selectedQuestionStorageKey, questionId);
    } catch {
      /* The current question remains selected for this session. */
    }
  }, [questionId, selectedQuestionStorageKey]);

  if (!current) return null;

  function goToQuestion(nextQuestion: InterviewQuestion) {
    setQuestionId(nextQuestion.id);
    setSelectedOption(answers[nextQuestion.id] ?? null);
    setAnnouncement(
      `Question ${questions.indexOf(nextQuestion) + 1}: ${nextQuestion.title}`,
    );
  }

  function moveBy(offset: number) {
    const nextIndex = Math.min(
      questions.length - 1,
      Math.max(0, currentIndex + offset),
    );
    goToQuestion(questions[nextIndex]);
  }

  function checkAnswer() {
    if (selectedOption === null) return;
    setAnswers((all) => ({ ...all, [current.id]: selectedOption }));
    setAnnouncement(
      selectedOption === current.correctIndex
        ? "Correct answer."
        : `Not quite. The correct answer is ${optionLetter(current.correctIndex)}.`,
    );
  }

  function tryAgain() {
    setAnswers((all) => {
      const next = { ...all };
      delete next[current.id];
      return next;
    });
    setSelectedOption(null);
    setAnnouncement("Answer cleared. Choose another option.");
  }

  function goToNextUnanswered() {
    const afterCurrent = [
      ...questions.slice(currentIndex + 1),
      ...questions.slice(0, currentIndex + 1),
    ];
    const next = afterCurrent.find(
      (question) => answers[question.id] === undefined,
    );
    if (next) goToQuestion(next);
    else setAnnouncement(`All ${questions.length} questions have an answer.`);
  }

  function resetAll() {
    if (
      !window.confirm(
        `Reset all ${config.label} answers? Coding progress and drafts will stay intact.`,
      )
    )
      return;
    setAnswers({});
    setQuestionId(questions[0].id);
    setSelectedOption(null);
    setTopic("All topics");
    setFilter("all");
    setAnnouncement(`${config.label} progress reset.`);
  }

  const answeredPercent = questions.length
    ? (answered / questions.length) * 100
    : 0;

  return (
    <>
      <header className="topbar fundamentals-topbar">
        <div className="crumbs">
          <span>Practice</span>
          <b>/</b>
          <span>{config.crumb}</span>
          <b>/</b>
          <strong>Interview FAQs</strong>
        </div>
        <div className="session-meta">
          <span className="fundamentals-score">
            {correct} correct · {answered}/{questions.length} answered
          </span>
          <span className="timer" title="Elapsed practice time">
            ◷ {clock}
          </span>
        </div>
      </header>
      <div className="fundamentals-workspace">
        <section className="fundamentals-main" aria-labelledby="quiz-title">
          <div className="fundamentals-intro">
            <div>
              <p className="eyebrow">{config.eyebrow}</p>
              <h1 id="quiz-title">{config.label}</h1>
              <p>
                {questions.length} {config.description} Answers are checked
                locally and saved separately from coding progress.
              </p>
            </div>
            <button type="button" onClick={onReturnToCoding}>
              {returnLabel}
            </button>
          </div>

          <div className="fundamentals-progress" aria-label="Quiz progress">
            <div>
              <strong>{answered}</strong>
              <span>answered</span>
            </div>
            <div>
              <strong>{correct}</strong>
              <span>correct</span>
            </div>
            <div>
              <strong>
                {answered ? Math.round((correct / answered) * 100) : 0}%
              </strong>
              <span>accuracy</span>
            </div>
            <span className="fundamentals-progress-track" aria-hidden="true">
              <i style={{ width: `${answeredPercent}%` }} />
            </span>
          </div>

          <article className="fundamentals-card">
            <div className="fundamentals-question-meta">
              <span>
                Question {currentIndex + 1} of {questions.length}
              </span>
              <span>{current.topic}</span>
              <span className={`difficulty ${current.difficulty.toLowerCase()}`}>
                {current.difficulty}
              </span>
            </div>
            <h2>{current.question}</h2>
            <div
              className="fundamentals-options"
              role="radiogroup"
              aria-label={`Answers for question ${currentIndex + 1}`}
            >
              {current.options.map((option, index) => {
                const checked = selectedOption === index;
                const revealed = submittedAnswer !== undefined;
                const answerClass = revealed
                  ? index === current.correctIndex
                    ? " correct"
                    : submittedAnswer === index
                      ? " incorrect"
                      : ""
                  : "";
                return (
                  <button
                    key={option}
                    type="button"
                    role="radio"
                    aria-checked={checked}
                    className={`fundamentals-option${checked ? " selected" : ""}${answerClass}`}
                    onClick={() => setSelectedOption(index)}
                    disabled={revealed}
                  >
                    <b>{optionLetter(index)}</b>
                    <span>{option}</span>
                    {revealed && index === current.correctIndex && (
                      <em>Correct answer</em>
                    )}
                  </button>
                );
              })}
            </div>

            {submittedAnswer !== undefined && (
              <div
                className={`fundamentals-feedback ${submittedAnswer === current.correctIndex ? "correct" : "incorrect"}`}
                role="status"
              >
                <strong>
                  {submittedAnswer === current.correctIndex
                    ? "✓ Correct"
                    : `Not quite — ${optionLetter(current.correctIndex)} is correct`}
                </strong>
                <p>{current.explanation}</p>
              </div>
            )}

            <div className="fundamentals-actions">
              <button
                type="button"
                onClick={() => moveBy(-1)}
                disabled={currentIndex === 0}
              >
                ← Previous
              </button>
              {submittedAnswer === undefined ? (
                <button
                  type="button"
                  className="check-answer-button"
                  onClick={checkAnswer}
                  disabled={selectedOption === null}
                >
                  Check answer
                </button>
              ) : (
                <button type="button" onClick={tryAgain}>
                  Try again
                </button>
              )}
              <button
                type="button"
                onClick={() => moveBy(1)}
                disabled={currentIndex === questions.length - 1}
              >
                Next →
              </button>
              <button type="button" onClick={goToNextUnanswered}>
                Next unanswered
              </button>
            </div>
          </article>
          <p className="sr-only" aria-live="polite" aria-atomic="true">
            {announcement}
          </p>
        </section>

        <aside className="fundamentals-navigator" aria-label="Question navigator">
          <div className="fundamentals-navigator-heading">
            <div>
              <strong>FAQ bank</strong>
              <small>{visibleQuestions.length} shown</small>
            </div>
            <button type="button" className="reset-all-button" onClick={resetAll}>
              Reset all
            </button>
          </div>
          <label>
            <span>Topic</span>
            <select
              value={topic}
              onChange={(event) => setTopic(event.target.value)}
            >
              <option>All topics</option>
              {topics.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </label>
          <div
            className="fundamentals-filters"
            role="group"
            aria-label="Filter questions"
          >
            {(
              [
                ["all", "All"],
                ["unanswered", "Unanswered"],
                ["incorrect", "Review misses"],
              ] as const
            ).map(([value, label]) => (
              <button
                key={value}
                type="button"
                className={filter === value ? "active" : ""}
                aria-pressed={filter === value}
                onClick={() => setFilter(value)}
              >
                {label}
              </button>
            ))}
          </div>
          <div className="fundamentals-question-grid">
            {visibleQuestions.map((question) => {
              const questionNumber = questions.indexOf(question) + 1;
              const answer = answers[question.id];
              const state =
                answer === undefined
                  ? "unanswered"
                  : answer === question.correctIndex
                    ? "correct"
                    : "incorrect";
              return (
                <button
                  key={question.id}
                  type="button"
                  className={`${question.id === current.id ? "current " : ""}${state}`}
                  onClick={() => goToQuestion(question)}
                  aria-label={`Question ${questionNumber}: ${question.title}, ${state}`}
                  aria-current={question.id === current.id ? "true" : undefined}
                >
                  {questionNumber}
                </button>
              );
            })}
          </div>
          {!visibleQuestions.length && (
            <p className="fundamentals-empty-filter">
              No questions match this filter. Choose another view.
            </p>
          )}
        </aside>
      </div>
    </>
  );
}
