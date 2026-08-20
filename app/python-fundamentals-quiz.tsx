"use client";

import { useEffect, useMemo, useState } from "react";
import {
  pythonFundamentalsQuestions,
} from "./python-fundamentals-questions.mjs";

type PythonFundamentalsQuestion =
  (typeof pythonFundamentalsQuestions)[number];

type QuizAnswers = Record<string, number>;
type QuizFilter = "all" | "unanswered" | "incorrect";

const progressStorageKey = "kitcode:python-fundamentals-progress-v1";
const selectedQuestionStorageKey =
  "kitcode:selected-python-fundamentals-question";

function isAnswerIndex(question: PythonFundamentalsQuestion, value: unknown) {
  return (
    Number.isInteger(value) &&
    Number(value) >= 0 &&
    Number(value) < question.options.length
  );
}

function readSavedAnswers(): QuizAnswers {
  if (typeof window === "undefined") return {};
  try {
    const parsed = JSON.parse(
      window.localStorage.getItem(progressStorageKey) ?? "{}",
    ) as Record<string, unknown>;
    return Object.fromEntries(
      pythonFundamentalsQuestions.flatMap((question) =>
        isAnswerIndex(question, parsed[question.id])
          ? [[question.id, Number(parsed[question.id])]]
          : [],
      ),
    );
  } catch {
    return {};
  }
}

function readSavedQuestionId() {
  if (typeof window === "undefined")
    return pythonFundamentalsQuestions[0]?.id ?? "";
  try {
    const saved = window.localStorage.getItem(selectedQuestionStorageKey);
    return pythonFundamentalsQuestions.some((question) => question.id === saved)
      ? saved!
      : (pythonFundamentalsQuestions[0]?.id ?? "");
  } catch {
    return pythonFundamentalsQuestions[0]?.id ?? "";
  }
}

function optionLetter(index: number) {
  return String.fromCharCode(65 + index);
}

export function PythonFundamentalsQuiz({
  clock,
  onReturnToCoding,
}: {
  clock: string;
  onReturnToCoding: () => void;
}) {
  const [answers, setAnswers] = useState<QuizAnswers>(readSavedAnswers);
  const [questionId, setQuestionId] = useState(readSavedQuestionId);
  const [selectedOption, setSelectedOption] = useState<number | null>(() => {
    const savedAnswers = readSavedAnswers();
    const savedQuestion = readSavedQuestionId();
    return savedAnswers[savedQuestion] ?? null;
  });
  const [topic, setTopic] = useState("All topics");
  const [filter, setFilter] = useState<QuizFilter>("all");
  const [announcement, setAnnouncement] = useState("");

  const currentIndex = Math.max(
    0,
    pythonFundamentalsQuestions.findIndex(
      (question) => question.id === questionId,
    ),
  );
  const current =
    pythonFundamentalsQuestions[currentIndex] ??
    pythonFundamentalsQuestions[0];
  const submittedAnswer = current ? answers[current.id] : undefined;
  const answered = Object.keys(answers).length;
  const correct = pythonFundamentalsQuestions.filter(
    (question) => answers[question.id] === question.correctIndex,
  ).length;
  const topics = useMemo(
    () =>
      Array.from(
        new Set(pythonFundamentalsQuestions.map((question) => question.topic)),
      ).sort((left, right) => left.localeCompare(right)),
    [],
  );
  const visibleQuestions = useMemo(
    () =>
      pythonFundamentalsQuestions.filter((question) => {
        if (topic !== "All topics" && question.topic !== topic) return false;
        if (filter === "unanswered") return answers[question.id] === undefined;
        if (filter === "incorrect")
          return (
            answers[question.id] !== undefined &&
            answers[question.id] !== question.correctIndex
          );
        return true;
      }),
    [answers, filter, topic],
  );

  useEffect(() => {
    try {
      window.localStorage.setItem(progressStorageKey, JSON.stringify(answers));
    } catch {
      /* Progress remains available for the current session. */
    }
  }, [answers]);

  useEffect(() => {
    try {
      window.localStorage.setItem(selectedQuestionStorageKey, questionId);
    } catch {
      /* The current question remains selected for this session. */
    }
  }, [questionId]);

  if (!current) return null;

  function goToQuestion(nextQuestion: PythonFundamentalsQuestion) {
    setQuestionId(nextQuestion.id);
    setSelectedOption(answers[nextQuestion.id] ?? null);
    setAnnouncement(
      `Question ${pythonFundamentalsQuestions.indexOf(nextQuestion) + 1}: ${nextQuestion.title}`,
    );
  }

  function moveBy(offset: number) {
    const nextIndex = Math.min(
      pythonFundamentalsQuestions.length - 1,
      Math.max(0, currentIndex + offset),
    );
    goToQuestion(pythonFundamentalsQuestions[nextIndex]);
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
      ...pythonFundamentalsQuestions.slice(currentIndex + 1),
      ...pythonFundamentalsQuestions.slice(0, currentIndex + 1),
    ];
    const next = afterCurrent.find(
      (question) => answers[question.id] === undefined,
    );
    if (next) goToQuestion(next);
    else setAnnouncement("All 100 questions have an answer.");
  }

  function resetProgress() {
    if (
      !window.confirm(
        "Reset all Python Fundamentals answers? This only clears quiz progress; coding progress and drafts stay intact.",
      )
    )
      return;
    setAnswers({});
    setQuestionId(pythonFundamentalsQuestions[0].id);
    setSelectedOption(null);
    setTopic("All topics");
    setFilter("all");
    setAnnouncement("Python Fundamentals progress reset.");
  }

  return (
    <>
      <header className="topbar fundamentals-topbar">
        <div className="crumbs">
          <span>Practice</span>
          <b>/</b>
          <span>Python</span>
          <b>/</b>
          <strong>Fundamentals</strong>
        </div>
        <div className="session-meta">
          <span className="fundamentals-score">
            {correct} correct · {answered}/100 answered
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
              <p className="eyebrow">OPTIONAL INTERVIEW PRACTICE</p>
              <h1 id="quiz-title">Python Fundamentals</h1>
              <p>
                100 common multiple-choice interview questions. Answers are
                checked locally and kept separate from coding progress.
              </p>
            </div>
            <button type="button" onClick={onReturnToCoding}>
              Return to coding
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
              <strong>{answered ? Math.round((correct / answered) * 100) : 0}%</strong>
              <span>accuracy</span>
            </div>
            <span className="fundamentals-progress-track" aria-hidden="true">
              <i style={{ width: `${answered}%` }} />
            </span>
          </div>

          <article className="fundamentals-card">
            <div className="fundamentals-question-meta">
              <span>
                Question {currentIndex + 1} of {pythonFundamentalsQuestions.length}
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
                disabled={
                  currentIndex === pythonFundamentalsQuestions.length - 1
                }
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
              <strong>Question bank</strong>
              <small>{visibleQuestions.length} shown</small>
            </div>
            <button type="button" onClick={resetProgress}>
              Reset progress
            </button>
          </div>
          <label>
            <span>Topic</span>
            <select value={topic} onChange={(event) => setTopic(event.target.value)}>
              <option>All topics</option>
              {topics.map((item) => (
                <option key={item}>{item}</option>
              ))}
            </select>
          </label>
          <div className="fundamentals-filters" role="group" aria-label="Filter questions">
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
              const questionNumber =
                pythonFundamentalsQuestions.indexOf(question) + 1;
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
