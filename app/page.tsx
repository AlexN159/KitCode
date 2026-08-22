"use client";
/* eslint-disable jsx-a11y/no-noninteractive-element-interactions -- the modal backdrop has an explicit keyboard-accessible close button */
import Editor, { loader, type OnMount } from "@monaco-editor/react";
import * as localMonaco from "monaco-editor/esm/vs/editor/editor.api";
import "monaco-editor/esm/vs/editor/contrib/suggest/browser/suggestController";
import "monaco-editor/esm/vs/basic-languages/python/python.contribution";
import "monaco-editor/esm/vs/basic-languages/sql/sql.contribution";
import "monaco-editor/esm/vs/basic-languages/java/java.contribution";
import EditorWorker from "monaco-editor/esm/vs/editor/editor.worker?worker";
import {
  clearCoachConversationsForExercise,
  coachConversationScope,
  readCoachConversation,
  writeCoachConversation,
} from "./coach-conversation-storage";
import { readCoachStream } from "./coach-stream";
import { InterviewQuiz, type InterviewSubject } from "./interview-quiz";
import {
  clearPersistedDraft,
  readPersistedDraft,
} from "./storage-migration.mjs";
import { findPythonPrefixCompletions } from "./python-completions.mjs";
import type {
  CSSProperties,
  FormEvent,
  KeyboardEvent as ReactKeyboardEvent,
  ReactNode,
} from "react";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
type Example = {
  input: string;
  output: string;
  explanation?: string;
};

function splitExampleInputLines(value: string): string[] {
  const normalized = value.replace(/\r\n?/g, "\n");
  if (!normalized) return [];
  const withoutFinalNewline = normalized.endsWith("\n")
    ? normalized.slice(0, -1)
    : normalized;
  return withoutFinalNewline.split("\n");
}

type Problem = {
  id: string;
  title: string;
  difficulty: "Easy" | "Medium" | "Hard";
  topic: string;
  topics?: string[];
  solved?: boolean;
  description?: string;
  constraints?: string[];
  examples?: Example[];
  hints?: string[];
  starter_code?: string;
  expected_complexity?: string;
  submission_mode?: "python_class";
  required_class?: { name: string; methods: string[] };
  language?: PracticeLanguage;
  source?: "curated" | "ai_generated";
};
type PracticeLanguage = "python" | "sql" | "java";
type PracticeArea = PracticeLanguage | "machine-learning";
type PracticeLevel = Problem["difficulty"];
type PracticeSection = "coding" | "interview";
type SqlDialect = "sqlite" | "postgresql" | "mysql" | "mssql";
type EditorDocument = "learner" | "reference";
type JudgeResult = {
  passed?: boolean;
  name?: string;
  visibility?: string;
  input?: string | null;
  expected_output?: string;
  actual_output?: string;
  error?: string;
  duration_ms?: number;
};
type RunnerResult = {
  ok?: boolean;
  stdout?: string;
  stderr?: string;
  duration_ms?: number;
  timed_out?: boolean;
  tests?: JudgeResult[];
  results?: JudgeResult[];
  passed?: boolean | number;
  total?: number;
  accepted?: boolean;
  status?: string;
  message?: string;
  answer?: string;
  error?: string;
  detail?: string;
  visibility?: string;
  sql_dialect?: SqlDialect;
  sql_engine?: string;
  execution_engine?: string;
  executed_engine?: string;
};
type AcceptedSubmissionSnapshot = {
  exerciseId: string;
  language: PracticeLanguage;
  sqlDialect: SqlDialect;
  code: string;
};
type ReferenceSolution = {
  exerciseId: string;
  language: PracticeLanguage;
  solution: string;
  expectedComplexity: string;
  lineCount: number;
  reviewPolicyId: string;
  selectionBasis: string;
  readabilityFocused: boolean;
  readabilityNote: string;
  referenceDialect?: string;
  dialectNote?: string;
  complexityNote?: string;
};
type TraceStep = {
  line: number;
  locals: Record<string, string>;
  source?: string;
  changed?: string[];
  removed?: string[];
  explanation?: string;
};
type AiStatus = {
  configured?: boolean;
  codex_usable?: boolean;
  codex_detected?: boolean;
  codex_detail?: string;
  provider?: string | null;
  model?: string | null;
  base_url?: string | null;
  local_llm_url?: string | null;
  providers?: Record<string, boolean>;
  openai_configured?: boolean;
  anthropic_configured?: boolean;
  local_llm_configured?: boolean;
  codex_available?: boolean;
};
type CodexDetection = {
  app_open?: boolean;
  cli_detected?: boolean;
  cli_usable?: boolean;
  authenticated?: boolean;
  ready?: boolean;
  detail?: string;
  action?: string;
  status?: string;
};
type CodexActionResult = {
  ok?: boolean;
  success?: boolean;
  ready?: boolean;
  detail?: string;
  action?: string;
  cli_detected?: boolean;
  cli_usable?: boolean;
  authenticated?: boolean;
  status?: CodexDetection;
};
type LocalLlmDetection = {
  reachable?: boolean;
  ready?: boolean;
  base_url?: string;
  models?: string[];
  selected_model?: string;
  detail?: string;
  action?: string;
};
type CelebrationVariant = "confetti" | "sparks" | "stars";
type MascotMotion =
  | "idle"
  | "hunting"
  | "complete"
  | "happy"
  | "sleeping"
  | "waking"
  | "surprised";
type MascotMotionRegistration = {
  scale: number;
  translateX?: number;
  translateY?: number;
};
const chibiMotionRegistration = {
  idle: { scale: 0.968, translateY: -3.2227 },
  hunting: { scale: 1.08036 },
  complete: { scale: 0.968, translateY: -3.2227 },
  happy: { scale: 1.08036 },
  sleeping: { scale: 1.34444 },
  waking: { scale: 1.08036 },
  surprised: { scale: 1, translateY: -1.7578 },
} as const satisfies Record<MascotMotion, MascotMotionRegistration>;
type MascotSequenceMotion = Extract<
  MascotMotion,
  "hunting" | "sleeping" | "happy" | "waking"
>;
type MascotSequenceFrame = {
  src: string;
  duration: number;
  translateX?: number;
  translateY?: number;
  scale?: number;
  shadowScale?: number;
};
type MascotSequence = {
  frames: readonly MascotSequenceFrame[];
  restIndex: number;
};
const mascotSequenceManifest = {
  hunting: {
    frames: [
      { src: "/mascots/kit-hunt-01.webp", duration: 160 },
      { src: "/mascots/kit-hunt-02.webp", duration: 140 },
      { src: "/mascots/kit-hunt-03.webp", duration: 140 },
      { src: "/mascots/kit-hunt-04.webp", duration: 140 },
      { src: "/mascots/kit-hunt-05.webp", duration: 140 },
      { src: "/mascots/kit-hunt-06.webp", duration: 140 },
      { src: "/mascots/kit-hunt-07.webp", duration: 160 },
      { src: "/mascots/kit-hunt-08.webp", duration: 1780 },
    ],
    restIndex: 7,
  },
  sleeping: {
    frames: [
      { src: "/mascots/kit-sleep-01.webp", duration: 420 },
      { src: "/mascots/kit-sleep-02.webp", duration: 400 },
      {
        src: "/mascots/kit-sleep-03.webp",
        duration: 400,
        translateY: 0.74,
        scale: 0.93,
      },
      {
        src: "/mascots/kit-sleep-04.webp",
        duration: 400,
        translateY: 2.53,
        scale: 0.76,
      },
      {
        src: "/mascots/kit-sleep-05.webp",
        duration: 400,
        translateY: 2.32,
        scale: 0.78,
      },
      {
        src: "/mascots/kit-sleep-06.webp",
        duration: 400,
        translateY: 2.64,
        scale: 0.75,
      },
      {
        src: "/mascots/kit-sleep-07.webp",
        duration: 450,
        translateY: 2.95,
        scale: 0.72,
      },
      {
        src: "/mascots/kit-sleep-08.webp",
        duration: 2330,
        translateY: 1.9,
        scale: 0.82,
      },
    ],
    restIndex: 7,
  },
  waking: {
    frames: [
      { src: "/mascots/kit-wake-01.webp", duration: 320 },
      {
        src: "/mascots/kit-wake-02.webp",
        duration: 380,
        translateY: -1.42,
        scale: 1.134,
      },
      {
        src: "/mascots/kit-chibi.webp",
        duration: 260,
        translateY: -1.9,
        scale: 0.896,
      },
    ],
    restIndex: 2,
  },
  happy: {
    frames: [
      {
        src: "/mascots/kit-happy-01.webp",
        duration: 180,
        translateX: -4,
        translateY: 0,
        scale: 1,
        shadowScale: 1,
      },
      {
        src: "/mascots/kit-happy-02.webp",
        duration: 120,
        translateX: -4,
        translateY: 4,
        scale: 1.06,
        shadowScale: 1.08,
      },
      {
        src: "/mascots/kit-happy-03.webp",
        duration: 130,
        translateX: -2,
        translateY: -10,
        scale: 0.99,
        shadowScale: 0.78,
      },
      {
        src: "/mascots/kit-happy-04.webp",
        duration: 250,
        translateX: 2,
        translateY: -30,
        scale: 0.96,
        shadowScale: 0.46,
      },
      {
        src: "/mascots/kit-happy-05.webp",
        duration: 130,
        translateX: 5,
        translateY: -18,
        scale: 0.99,
        shadowScale: 0.68,
      },
      {
        src: "/mascots/kit-happy-06.webp",
        duration: 220,
        translateX: 7,
        translateY: 4,
        scale: 1.07,
        shadowScale: 1.08,
      },
      {
        src: "/mascots/kit-happy-07.webp",
        duration: 1370,
        translateX: 0,
        translateY: 0,
        scale: 1,
        shadowScale: 1,
      },
    ],
    restIndex: 6,
  },
} as const satisfies Record<MascotSequenceMotion, MascotSequence>;
type SetupProvider = "openai" | "anthropic" | "local_llm" | "codex";
type CoachIntent = "adaptive" | "hint" | "edit";
type CoachMessage = {
  id: string;
  role: "coach" | "you";
  text: string;
  contextual?: boolean;
};
type EditorHint = { id: number; line: number; text: string; inline: boolean };
type EditorEdit = {
  id: number;
  startLine: number;
  endLine: number;
  ranges: Array<{ startLine: number; endLine: number }>;
  before: string;
  after: string;
  message: string;
  undoAvailable: boolean;
};
type CoachRequestSnapshot = {
  intent: CoachIntent;
  retry?: boolean;
  question: string;
  exerciseId: string;
  providerIdentity: string;
  runtimeIdentity: string;
  expectedProvider: string;
  expectedModel: string | null;
  expectedBaseUrl: string | null;
  code: string;
  modelVersion: number;
  documentRevision: number;
  cursorLine: number;
  cursorColumn: number;
  history: Array<{ role: "user" | "assistant"; content: string }>;
  language: PracticeLanguage;
  sqlDialect?: SqlDialect;
};
const languages: Array<{
  id: PracticeLanguage;
  label: string;
  short: string;
  file: string;
  monaco: "python" | "sql" | "java";
}> = [
  {
    id: "python",
    label: "Python",
    short: "Py",
    file: "solution.py",
    monaco: "python",
  },
  {
    id: "sql",
    label: "SQL",
    short: "SQL",
    file: "solution.sql",
    monaco: "sql",
  },
  {
    id: "java",
    label: "Java",
    short: "Java",
    file: "Main.java",
    monaco: "java",
  },
];
const pythonKeywordCompletions = new Set([
  "break",
  "class",
  "continue",
  "def",
  "elif",
  "else",
  "except",
  "finally",
  "for",
  "from",
  "if",
  "import",
  "in",
  "not",
  "or",
  "pass",
  "return",
  "try",
  "while",
  "with",
]);
const pythonTypeCompletions = new Set([
  "bool",
  "dict",
  "float",
  "int",
  "list",
  "set",
  "str",
  "tuple",
]);
const practiceLevels: Array<{
  id: PracticeLevel;
  label: string;
  description: string;
}> = [
  {
    id: "Easy",
    label: "Foundations",
    description: "Fluency, syntax, and core patterns",
  },
  {
    id: "Medium",
    label: "Practice",
    description: "Build confidence with common coding tasks",
  },
  {
    id: "Hard",
    label: "Advanced",
    description: "Deep algorithms and system thinking",
  },
];
const sqlDialects: Array<{
  id: SqlDialect;
  label: string;
  shortLabel: string;
}> = [
  { id: "sqlite", label: "SQLite", shortLabel: "SQLite" },
  { id: "postgresql", label: "PostgreSQL", shortLabel: "PostgreSQL" },
  { id: "mysql", label: "MySQL", shortLabel: "MySQL" },
  { id: "mssql", label: "Microsoft SQL Server", shortLabel: "SQL Server" },
];
function languageMeta(language: PracticeLanguage) {
  return languages.find((item) => item.id === language) ?? languages[0];
}
function sqlDialectMeta(dialect: SqlDialect) {
  return sqlDialects.find((item) => item.id === dialect) ?? sqlDialects[0];
}
function readSqlDialectPreference(): SqlDialect {
  if (typeof window === "undefined") return "sqlite";
  try {
    const saved = window.localStorage.getItem("kitcode:selected-sql-dialect");
    return sqlDialects.some((item) => item.id === saved)
      ? (saved as SqlDialect)
      : "sqlite";
  } catch {
    return "sqlite";
  }
}
function readLanguagePreference(): PracticeLanguage {
  if (typeof window === "undefined") return "python";
  try {
    const saved = window.localStorage.getItem("kitcode:selected-language");
    return saved === "sql" || saved === "java" || saved === "python"
      ? saved
      : "python";
  } catch {
    return "python";
  }
}
function readPracticeAreaPreference(): PracticeArea {
  if (typeof window === "undefined") return "python";
  try {
    const saved = window.localStorage.getItem("kitcode:selected-practice-area");
    return saved === "machine-learning"
      ? "machine-learning"
      : readLanguagePreference();
  } catch {
    return readLanguagePreference();
  }
}
function readLevelPreference(language: PracticeLanguage): PracticeLevel {
  if (typeof window === "undefined") return "Easy";
  try {
    const saved = window.localStorage.getItem(
      `kitcode:selected-level:${language}`,
    );
    return saved === "Medium" || saved === "Hard" || saved === "Easy"
      ? saved
      : "Easy";
  } catch {
    return "Easy";
  }
}
function localLlmActionText(action?: string) {
  if (action === "connected")
    return "Connected automatically. This endpoint is now the selected coach.";
  if (action === "check_server")
    return "Start the server or check its URL and port, then try again.";
  if (action === "choose_model")
    return "Enter a valid model ID, then run detection again.";
  if (action === "fix_url")
    return "Enter an HTTP or HTTPS server URL without credentials, a query, or a fragment.";
  if (action === "fix_model")
    return "Use the exact model ID exposed by your server.";
  return action || "Check the server URL and model, then try detection again.";
}
const providerModels: Record<
  Exclude<SetupProvider, "codex" | "local_llm">,
  {
    value: string;
    label: string;
  }[]
> = {
  openai: [
    { value: "gpt-5.6-terra", label: "gpt-5.6-terra — Balanced (recommended)" },
    { value: "gpt-5.6-luna", label: "gpt-5.6-luna — Lower cost" },
    { value: "gpt-5.4-mini", label: "gpt-5.4-mini — Lower cost" },
    { value: "gpt-5.6-sol", label: "gpt-5.6-sol — Maximum capability" },
  ],
  anthropic: [
    { value: "claude-sonnet-5", label: "claude-sonnet-5 — Balanced coding" },
    { value: "claude-haiku-4-5", label: "claude-haiku-4-5 — Lower cost" },
    { value: "claude-opus-5", label: "claude-opus-5 — Maximum capability" },
  ],
};
loader.config({ monaco: localMonaco });
if (typeof globalThis !== "undefined") {
  (
    globalThis as typeof globalThis & {
      MonacoEnvironment?: {
        getWorker(): Worker;
      };
    }
  ).MonacoEnvironment = {
    getWorker: () => new EditorWorker(),
  };
}
const fallbackProblems: Problem[] = [
  {
    id: "warmup-parity",
    title: "Parity Label",
    difficulty: "Easy",
    topic: "Conditionals",
    description:
      "Read one integer. Print `even` when it is divisible by 2; otherwise print `odd`.",
    starter_code:
      "def solve() -> None:\n    value = int(input())\n    # Write your solution here.\n\n\nif __name__ == '__main__':\n    solve()",
    examples: [{ input: "8", output: "even" }],
  },
  {
    id: "warmup-words",
    title: "Word Counter",
    difficulty: "Easy",
    topic: "Strings",
    description: "Read a line and print how many words it contains.",
    starter_code:
      "def solve() -> None:\n    line = input()\n    # Write your solution here.\n\n\nif __name__ == '__main__':\n    solve()",
  },
  {
    id: "warmup-unique",
    title: "Unique Values",
    difficulty: "Medium",
    topic: "Sets",
    description: "Read integers and print the number of distinct values.",
    starter_code:
      "def solve() -> None:\n    values = input().split()\n    # Write your solution here.\n\n\nif __name__ == '__main__':\n    solve()",
  },
];
const blankCode = "# Select a drill to begin.\n";
function blankCodeFor(language: PracticeLanguage) {
  if (language === "sql") return "-- Select a SQL drill to begin.\n";
  if (language === "java") return "// Select a Java drill to begin.\n";
  return blankCode;
}
const coachWelcome: CoachMessage = {
  id: "welcome",
  role: "coach",
  text: "Ask me naturally about your approach, an error, complexity, or what to try next. I’ll adapt to what you need.",
};
const coachBrowserTimeoutMs = 70_000;
const coachRestartDelayMs = 900;

function coachConsentIdentity(status: AiStatus) {
  return status.provider === "local_llm"
    ? `local_llm|${status.local_llm_url ?? status.base_url ?? ""}`
    : (status.provider ?? "local");
}

function coachRuntimeIdentity(status: AiStatus) {
  return `${coachConsentIdentity(status)}|${status.model ?? ""}`;
}

function hasCoachConsent(identity: string) {
  try {
    return (
      window.localStorage.getItem("kitcode:coach-data-consent-provider") ===
      identity
    );
  } catch {
    return false;
  }
}

function rememberCoachConsent(identity: string) {
  try {
    window.localStorage.setItem("kitcode:coach-data-consent-provider", identity);
  } catch {
    /* Consent remains valid for this one explicitly approved request. */
  }
}

function safeInlineHint(value: unknown) {
  return String(value ?? "")
    .normalize("NFKC")
    .replace(/[\p{Cc}\p{Cf}]/gu, " ")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 220);
}
function Icon({ children, label }: { children: string; label: string }) {
  return (
    <span className="icon" aria-label={label} title={label}>
      {children}
    </span>
  );
}
function normalizeProblem(
  item: Record<string, unknown>,
  index: number,
): Problem {
  const difficulty =
    item.difficulty === "Easy" || item.difficulty === "Hard"
      ? item.difficulty
      : "Medium";
  const topics = Array.isArray(item.topics)
    ? item.topics.map(String)
    : Array.isArray(item.tags)
      ? item.tags.map(String)
      : undefined;
  const language =
    item.language === "sql" || item.language === "java"
      ? item.language
      : "python";
  const source = item.source === "ai_generated" ? "ai_generated" : "curated";
  return {
    ...item,
    id: String(item.id ?? index + 1),
    title: String(item.title ?? item.name ?? `Exercise ${index + 1}`),
    difficulty,
    topic: topics?.[0] ?? String(item.topic ?? languageMeta(language).label),
    topics,
    language,
    source,
  } as Problem;
}
function acceptedResult(result: RunnerResult) {
  return (
    result.accepted === true ||
    result.status === "passed" ||
    (typeof result.passed === "number" &&
      typeof result.total === "number" &&
      result.total > 0 &&
      result.passed === result.total)
  );
}

function coachInline(text: string): ReactNode[] {
  const tokens = text.split(/(`[^`]+`|\*\*[^*]+\*\*|\*[^*]+\*|_[^_]+_)/g);
  return tokens.filter(Boolean).map((token, index) => {
    if (token.startsWith("`") && token.endsWith("`"))
      return <code key={index}>{token.slice(1, -1)}</code>;
    if (token.startsWith("**") && token.endsWith("**"))
      return <strong key={index}>{token.slice(2, -2)}</strong>;
    if (
      (token.startsWith("*") && token.endsWith("*")) ||
      (token.startsWith("_") && token.endsWith("_"))
    )
      return <em key={index}>{token.slice(1, -1)}</em>;
    return token;
  });
}

function CoachReply({ text }: { text: string }) {
  const lines = text.replace(/\r\n?/g, "\n").split("\n");
  const blocks: ReactNode[] = [];
  let index = 0;
  const copyCode = (code: string) => void navigator.clipboard?.writeText(code);
  while (index < lines.length) {
    const line = lines[index];
    if (!line.trim()) {
      index += 1;
      continue;
    }
    const fence = line.match(/^```\s*([^\s]*)\s*$/);
    if (fence) {
      const language = fence[1];
      const code: string[] = [];
      index += 1;
      while (index < lines.length && !/^```\s*$/.test(lines[index]))
        code.push(lines[index++]);
      if (index < lines.length) index += 1;
      const value = code.join("\n");
      blocks.push(
        <section className="coach-code-block" key={`code-${blocks.length}`}>
          <header>
            {language || "code"}
            <button
              type="button"
              onClick={() => copyCode(value)}
              aria-label="Copy code block"
            >
              Copy
            </button>
          </header>
          <pre>
            <code>{value}</code>
          </pre>
        </section>,
      );
      continue;
    }
    const heading = line.match(/^(#{1,3})\s+(.+)$/);
    if (heading) {
      const level = heading[1].length;
      const content = coachInline(heading[2]);
      index += 1;
      blocks.push(
        level === 1 ? (
          <h3 key={`heading-${blocks.length}`}>{content}</h3>
        ) : level === 2 ? (
          <h4 key={`heading-${blocks.length}`}>{content}</h4>
        ) : (
          <h5 key={`heading-${blocks.length}`}>{content}</h5>
        ),
      );
      continue;
    }
    const unordered = line.match(/^\s*[-*+]\s+(.+)$/);
    const ordered = line.match(/^\s*\d+[.)]\s+(.+)$/);
    if (unordered || ordered) {
      const items: ReactNode[] = [];
      const isOrdered = Boolean(ordered);
      while (index < lines.length) {
        const match = isOrdered
          ? lines[index].match(/^\s*\d+[.)]\s+(.+)$/)
          : lines[index].match(/^\s*[-*+]\s+(.+)$/);
        if (!match) break;
        items.push(<li key={items.length}>{coachInline(match[1])}</li>);
        index += 1;
      }
      blocks.push(
        isOrdered ? (
          <ol key={`list-${blocks.length}`}>{items}</ol>
        ) : (
          <ul key={`list-${blocks.length}`}>{items}</ul>
        ),
      );
      continue;
    }
    const paragraph: string[] = [line];
    index += 1;
    while (
      index < lines.length &&
      lines[index].trim() &&
      !/^```/.test(lines[index]) &&
      !/^(#{1,3})\s+/.test(lines[index]) &&
      !/^\s*(?:[-*+]\s+|\d+[.)]\s+)/.test(lines[index])
    )
      paragraph.push(lines[index++]);
    blocks.push(
      <p key={`paragraph-${blocks.length}`}>
        {paragraph.map((entry, lineIndex) => (
          <span key={lineIndex}>
            {lineIndex > 0 && <br />}
            {coachInline(entry)}
          </span>
        ))}
      </p>,
    );
  }
  return (
    <div className="coach-reply">{blocks.length ? blocks : <p>{text}</p>}</div>
  );
}
function requestsEditorEdit(question: string) {
  const lowered = question.toLowerCase();
  if (
    /\b(?:do\s+not|don't|dont|never|without|no)\b[\s\S]{0,40}\b(?:type|put|insert|add|replace|write|fix|apply|update|change|edit|modify|rewrite)\w*\b/.test(
      lowered,
    )
  )
    return false;
  return /(?:^|[.!?]\s+)(?:(?:please\s+)|(?:(?:can|could|would)\s+you\s+(?:please\s+)?))?(?:(?:type|put|insert|add|apply|change|replace|write)\b[\s\S]{0,80}\b(?:in|into|to)\s+(?:(?:the|my|this)\s+)?(?:editor|code|script|file|box)\b|(?:fix|update|edit|change|replace)\s+(?:my|this|the)\s+(?:code|script|file)\b|apply\s+(?:this|the)\s+(?:fix|change|edit)\b)/.test(
    lowered,
  );
}

function changedLineRange(before: string, after: string) {
  const beforeLines = before.split("\n");
  const afterLines = after.split("\n");
  const totalLines = beforeLines.length + afterLines.length;
  const offset = totalLines;
  let changedIndexes: number[] | null = null;

  // Myers' line diff gives exact modified-line provenance for normal practice
  // scripts. Cap its work and use a clearly labelled affected span for an
  // unusually large/generated file instead of risking a frozen browser.
  if (totalLines <= 4_000) {
    const frontier = new Int32Array(totalLines * 2 + 3);
    const trace: Int32Array[] = [];
    let finishedDepth = -1;
    outer: for (
      let depth = 0;
      depth <= Math.min(totalLines, 1_000);
      depth += 1
    ) {
      trace.push(frontier.slice());
      for (let diagonal = -depth; diagonal <= depth; diagonal += 2) {
        const index = offset + diagonal;
        let x =
          diagonal === -depth ||
          (diagonal !== depth && frontier[index - 1] < frontier[index + 1])
            ? frontier[index + 1]
            : frontier[index - 1] + 1;
        let y = x - diagonal;
        while (
          x < beforeLines.length &&
          y < afterLines.length &&
          beforeLines[x] === afterLines[y]
        ) {
          x += 1;
          y += 1;
        }
        frontier[index] = x;
        if (x >= beforeLines.length && y >= afterLines.length) {
          finishedDepth = depth;
          break outer;
        }
      }
    }
    if (finishedDepth >= 0) {
      const modified = new Set<number>();
      let x = beforeLines.length;
      let y = afterLines.length;
      for (let depth = finishedDepth; depth >= 0; depth -= 1) {
        const previous = trace[depth];
        const diagonal = x - y;
        const index = offset + diagonal;
        const previousDiagonal =
          diagonal === -depth ||
          (diagonal !== depth && previous[index - 1] < previous[index + 1])
            ? diagonal + 1
            : diagonal - 1;
        const previousX = previous[offset + previousDiagonal];
        const previousY = previousX - previousDiagonal;
        while (x > previousX && y > previousY) {
          x -= 1;
          y -= 1;
        }
        if (depth === 0) break;
        if (x === previousX) {
          y -= 1;
          modified.add(y);
        } else x -= 1;
      }
      changedIndexes = [...modified]
        .filter((line) => line >= 0)
        .sort((a, b) => a - b);
    }
  }
  let prefix = 0;
  while (
    prefix < beforeLines.length &&
    prefix < afterLines.length &&
    beforeLines[prefix] === afterLines[prefix]
  )
    prefix += 1;
  let suffix = 0;
  while (
    suffix < beforeLines.length - prefix &&
    suffix < afterLines.length - prefix &&
    beforeLines[beforeLines.length - 1 - suffix] ===
      afterLines[afterLines.length - 1 - suffix]
  )
    suffix += 1;
  const startLine = Math.min(prefix + 1, Math.max(1, afterLines.length));
  const endLine = Math.max(startLine, afterLines.length - suffix);
  const ranges: Array<{ startLine: number; endLine: number }> = [];
  if (changedIndexes) {
    for (const zeroBasedLine of changedIndexes) {
      const line = zeroBasedLine + 1;
      const last = ranges[ranges.length - 1];
      if (last && line === last.endLine + 1) last.endLine = line;
      else ranges.push({ startLine: line, endLine: line });
    }
  } else if (after !== before && afterLines.length > suffix)
    ranges.push({ startLine, endLine });
  return { startLine, endLine, ranges };
}

function editorEditLabel(edit: EditorEdit) {
  if (!edit.ranges.length) return "deletion-only change";
  if (edit.ranges.length > 1) return `${edit.ranges.length} changed regions`;
  const range = edit.ranges[0];
  return range.startLine === range.endLine
    ? `line ${range.startLine}`
    : `lines ${range.startLine}–${range.endLine}`;
}

function readReducedMotionPreference() {
  return (
    typeof window !== "undefined" &&
    typeof window.matchMedia === "function" &&
    window.matchMedia("(prefers-reduced-motion: reduce)").matches
  );
}

function useReducedMotionPreference() {
  const [reducedMotion, setReducedMotion] = useState(
    readReducedMotionPreference,
  );
  useEffect(() => {
    if (typeof window.matchMedia !== "function") return;
    const query = window.matchMedia("(prefers-reduced-motion: reduce)");
    const updatePreference = () => setReducedMotion(query.matches);
    updatePreference();
    query.addEventListener("change", updatePreference);
    return () => query.removeEventListener("change", updatePreference);
  }, []);
  return reducedMotion;
}

function MascotSequencePlayer({ sequence }: { sequence: MascotSequence }) {
  const reducedMotion = useReducedMotionPreference();
  const [frameIndex, setFrameIndex] = useState(0);
  useEffect(() => {
    if (reducedMotion) return;
    let cancelled = false;
    let timer: number | undefined;
    let currentIndex = 0;
    const scheduleNextFrame = () => {
      if (cancelled || currentIndex >= sequence.restIndex) return;
      timer = window.setTimeout(() => {
        if (cancelled) return;
        currentIndex += 1;
        setFrameIndex(currentIndex);
        scheduleNextFrame();
      }, sequence.frames[currentIndex].duration);
    };
    timer = window.setTimeout(() => {
      if (cancelled) return;
      setFrameIndex(0);
      scheduleNextFrame();
    }, 0);
    return () => {
      cancelled = true;
      if (timer !== undefined) window.clearTimeout(timer);
    };
  }, [reducedMotion, sequence]);
  const activeIndex = reducedMotion ? sequence.restIndex : frameIndex;
  const activeFrame = sequence.frames[activeIndex];
  const frameStyle = reducedMotion
    ? undefined
    : ({
        "--kit-frame-x": `${activeFrame.translateX ?? 0}%`,
        "--kit-frame-y": `${activeFrame.translateY ?? 0}%`,
        "--kit-frame-scale": activeFrame.scale ?? 1,
        "--kit-shadow-scale": activeFrame.shadowScale ?? 1,
      } as CSSProperties);
  return (
    <span
      className={`kit-sequence-player${activeIndex === sequence.restIndex ? " is-rest-frame" : ""}`}
      style={frameStyle}
    >
      <span className="kit-jump-shadow" />
      <span className="kit-sequence-stage">
        <img
          className="kit-sequence-frame"
          src={activeFrame.src}
          alt=""
          draggable={false}
        />
      </span>
    </span>
  );
}

function KitMascot({
  motion = "idle",
  size = "coach",
}: {
  motion?: MascotMotion;
  size?: "rail" | "coach" | "settings" | "floating";
}) {
  const motionRegistration: MascotMotionRegistration =
    chibiMotionRegistration[motion];
  const motionStyle = {
    "--kit-motion-x": `${motionRegistration.translateX ?? 0}%`,
    "--kit-motion-y": `${motionRegistration.translateY ?? 0}%`,
    "--kit-motion-scale": motionRegistration.scale,
  } as CSSProperties;
  const sequenceMotion: MascotSequenceMotion | null =
    motion === "hunting" ||
      motion === "sleeping" ||
      motion === "happy" ||
      motion === "waking"
      ? motion
      : null;
  const usesSurpriseFrame = motion === "surprised";
  return (
    <div
      className={`kit-mascot kit-mascot-${size} is-${motion} is-chibi`}
      aria-hidden="true"
    >
      <span className="kit-motion-stage" style={motionStyle}>
        {sequenceMotion ? (
          <MascotSequencePlayer
            key={sequenceMotion}
            sequence={mascotSequenceManifest[sequenceMotion]}
          />
        ) : usesSurpriseFrame ? (
          <img
            className="kit-state-frame kit-surprise-frame"
            src="/mascots/kit-surprised.webp"
            alt=""
            draggable={false}
          />
        ) : (
          <img
            className="kit-base-image"
            src="/mascots/kit-chibi.webp"
            alt=""
            draggable={false}
          />
        )}
      </span>
      <span className="kit-ground" />
      <span className="kit-dirt kit-dirt-one" />
      <span className="kit-dirt kit-dirt-two" />
      <span className="kit-wag-line kit-wag-line-one" />
      <span className="kit-wag-line kit-wag-line-two" />
    </div>
  );
}

function SuccessCelebration({ variant }: { variant: CelebrationVariant }) {
  const particleCount =
    variant === "confetti" ? 20 : variant === "sparks" ? 14 : 12;
  const particles = Array.from({ length: particleCount }, (_, index) => {
    const angle = (Math.PI * 2 * index) / particleCount - Math.PI / 2;
    const distance = 58 + (index % 4) * 11;
    const style = {
      "--dx": `${Math.round(Math.cos(angle) * distance)}px`,
      "--dy": `${Math.round(Math.sin(angle) * distance)}px`,
      "--spin": `${120 + index * 37}deg`,
      "--delay": `${(index % 5) * 18}ms`,
      "--hue": `${(index * 47 + (variant === "stars" ? 34 : 0)) % 360}`,
    } as CSSProperties;
    return <i aria-hidden="true" key={index} style={style} />;
  });
  return (
    <div className={`success-celebration ${variant}`} aria-hidden="true">
      <div className="success-badge">✓ All tests passed</div>
      <div className="success-particles">{particles}</div>
    </div>
  );
}

function readCelebrationPreference() {
  if (typeof window === "undefined") return true;
  try {
    return window.localStorage.getItem("kitcode:success-celebrations") !== "off";
  } catch {
    return true;
  }
}
function readInlineHintPreference() {
  if (typeof window === "undefined") return true;
  try {
    return window.localStorage.getItem("kitcode:inline-hints") !== "off";
  } catch {
    return true;
  }
}
function readPythonAutocompletePreference() {
  if (typeof window === "undefined") return true;
  try {
    return (
      window.localStorage.getItem("kitcode:python-autocomplete") !== "off"
    );
  } catch {
    return true;
  }
}
function readMascotPreference() {
  if (typeof window === "undefined") return true;
  try {
    return window.localStorage.getItem("kitcode:mascot-enabled") !== "off";
  } catch {
    return true;
  }
}
function readPracticeSection(language: PracticeLanguage): PracticeSection {
  if (typeof window === "undefined") return "coding";
  try {
    const saved = window.localStorage.getItem(
      `kitcode:selected-${language}-section`,
    );
    return saved === "interview" || saved === "fundamentals"
      ? "interview"
      : "coding";
  } catch {
    return "coding";
  }
}
type MascotPosition = { x: number; y: number };
const defaultMascotPosition: MascotPosition = { x: 75, y: 50 };
const mascotDragThreshold = 8;
const mascotIdleSleepDelay = 15000;
function clampMascotPosition(position: MascotPosition): MascotPosition {
  const mascotHalfSize = 105;
  const edgeGap = 8;
  const width = Math.max(window.innerWidth, mascotHalfSize * 2 + edgeGap * 2);
  const height = Math.max(window.innerHeight, mascotHalfSize * 2 + edgeGap * 2);
  const minX = ((mascotHalfSize + edgeGap) / width) * 100;
  const maxX = 100 - minX;
  const minY = ((mascotHalfSize + edgeGap) / height) * 100;
  const maxY = 100 - minY;
  return {
    x: Math.min(maxX, Math.max(minX, position.x)),
    y: Math.min(maxY, Math.max(minY, position.y)),
  };
}
function readMascotPositionPreference(): MascotPosition {
  if (typeof window === "undefined") return defaultMascotPosition;
  try {
    const parsed = JSON.parse(
      window.localStorage.getItem("kitcode:mascot-position-v1") ?? "null",
    ) as Partial<MascotPosition> | null;
    return parsed && Number.isFinite(parsed.x) && Number.isFinite(parsed.y)
      ? clampMascotPosition({ x: parsed.x!, y: parsed.y! })
      : clampMascotPosition(defaultMascotPosition);
  } catch {
    return clampMascotPosition(defaultMascotPosition);
  }
}
export default function Home() {
  const [selectedLanguage, setSelectedLanguage] = useState<PracticeLanguage>(
    readLanguagePreference,
  );
  const [selectedPracticeArea, setSelectedPracticeArea] =
    useState<PracticeArea>(readPracticeAreaPreference);
  const [practiceSection, setPracticeSection] = useState<PracticeSection>(() =>
    readPracticeSection(readLanguagePreference()),
  );
  const [sqlDialect, setSqlDialect] = useState<SqlDialect>(
    readSqlDialectPreference,
  );
  const [problems, setProblems] = useState<Problem[]>([]);
  const [generatedProblems, setGeneratedProblems] = useState<Problem[]>([]);
  const [generatedDifficulty, setGeneratedDifficulty] =
    useState<Problem["difficulty"]>("Medium");
  const [generatedTopic, setGeneratedTopic] = useState("");
  const [generatingProblem, setGeneratingProblem] = useState(false);
  const [generatedNotice, setGeneratedNotice] = useState("");
  const [catalogTotal, setCatalogTotal] = useState(0);
  const [selected, setSelected] = useState("");
  const [query, setQuery] = useState("");
  const [difficulty, setDifficulty] = useState<PracticeLevel>(() =>
    readLevelPreference(readLanguagePreference()),
  );
  const [topicFilter, setTopicFilter] = useState("All topics");
  const [code, setCode] = useState(blankCode);
  const [stdin, setStdin] = useState("");
  const [tab, setTab] = useState<"Console" | "Tests" | "Trace">("Console");
  const [status, setStatus] = useState("Choose a drill to begin");
  const [elapsed, setElapsed] = useState(0);
  const [runResult, setRunResult] = useState<RunnerResult | null>(null);
  const [acceptedSubmission, setAcceptedSubmission] =
    useState<AcceptedSubmissionSnapshot | null>(null);
  const [referenceSolution, setReferenceSolution] =
    useState<ReferenceSolution | null>(null);
  const [editorDocument, setEditorDocument] =
    useState<EditorDocument>("learner");
  const [referenceSolutionLoading, setReferenceSolutionLoading] =
    useState(false);
  const [referenceSolutionError, setReferenceSolutionError] = useState("");
  const [traceSteps, setTraceSteps] = useState<TraceStep[]>([]);
  const [traceIndex, setTraceIndex] = useState(0);
  const [workflowBusy, setWorkflowBusy] = useState(false);
  const [draftReady, setDraftReady] = useState(false);
  const [draftExerciseId, setDraftExerciseId] = useState("");
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [setupProvider, setSetupProvider] = useState<SetupProvider>("codex");
  const [setupModel, setSetupModel] = useState("gpt-5.6-terra");
  const [setupCustomModel, setSetupCustomModel] = useState("");
  const [setupKey, setSetupKey] = useState("");
  const [setupLocalUrl, setSetupLocalUrl] = useState("http://127.0.0.1:5000/");
  const [setupNotice, setSetupNotice] = useState("");
  const [setupSaving, setSetupSaving] = useState(false);
  const [codexDetecting, setCodexDetecting] = useState(false);
  const [codexInstalling, setCodexInstalling] = useState(false);
  const [codexLoginStarting, setCodexLoginStarting] = useState(false);
  const [codexLoginPolling, setCodexLoginPolling] = useState(false);
  const [codexInstallConfirmOpen, setCodexInstallConfirmOpen] = useState(false);
  const [codexActionResult, setCodexActionResult] =
    useState<CodexActionResult | null>(null);
  const [codexDetection, setCodexDetection] = useState<CodexDetection | null>(
    null,
  );
  const [localLlmDetecting, setLocalLlmDetecting] = useState(false);
  const [localLlmDetection, setLocalLlmDetection] =
    useState<LocalLlmDetection | null>(null);
  const [problemDrawerOpen, setProblemDrawerOpen] = useState(false);
  const [coachDrawerOpen, setCoachDrawerOpen] = useState(false);
  const [coachConsentOpen, setCoachConsentOpen] = useState(false);
  const [, setPendingCoachQuestion] = useState("");
  const [pendingCoachProvider, setPendingCoachProvider] = useState("");
  const [coachBusy, setCoachBusy] = useState(false);
  const [coachRestarting, setCoachRestarting] = useState(false);
  const [activeCoachIntent, setActiveCoachIntent] =
    useState<CoachIntent | null>(null);
  const [aiStatus, setAiStatus] = useState<AiStatus>({});
  const [coachInput, setCoachInput] = useState("");
  const [retryCoachSnapshot, setRetryCoachSnapshotState] =
    useState<CoachRequestSnapshot | null>(null);
  const [editorHint, setEditorHint] = useState<EditorHint | null>(null);
  const [inlineHintsEnabled, setInlineHintsEnabled] = useState(
    readInlineHintPreference,
  );
  const [pythonAutocompleteEnabled, setPythonAutocompleteEnabled] = useState(
    readPythonAutocompletePreference,
  );
  const [editorMountVersion, setEditorMountVersion] = useState(0);
  const [editorEdit, setEditorEdit] = useState<EditorEdit | null>(null);
  const [pendingEditorEdit, setPendingEditorEdit] = useState<EditorEdit | null>(
    null,
  );
  const [hintNotice, setHintNotice] = useState("");
  const [pendingCoachIntent, setPendingCoachIntent] =
    useState<CoachIntent>("adaptive");
  const [celebrationsEnabled, setCelebrationsEnabled] = useState(
    readCelebrationPreference,
  );
  const [mascotEnabled, setMascotEnabled] = useState(readMascotPreference);
  const [mascotPosition, setMascotPosition] = useState<MascotPosition>(
    readMascotPositionPreference,
  );
  const [mascotDragging, setMascotDragging] = useState(false);
  const [mascotWindowInactive, setMascotWindowInactive] = useState(false);
  const [mascotMoment, setMascotMoment] = useState<{
    id: number;
    motion: "complete" | "happy" | "sleeping" | "waking" | "surprised";
  } | null>(null);
  const [mascotSleeping, setMascotSleeping] = useState(false);
  const [celebration, setCelebration] = useState<{
    variant: CelebrationVariant;
    id: number;
  } | null>(null);
  const [messages, setMessages] = useState<CoachMessage[]>([coachWelcome]);
  const messagesRef = useRef(messages);
  const editorRef = useRef<Parameters<OnMount>[0] | null>(null);
  const monacoRef = useRef<Parameters<OnMount>[1] | null>(null);
  const decorationRef = useRef<string[]>([]);
  const hintDecorationRef = useRef<string[]>([]);
  const hintViewZoneRef = useRef<{
    editor: Parameters<OnMount>[0];
    id: string;
  } | null>(null);
  const editDecorationRef = useRef<string[]>([]);
  const applyingEditorEditRef = useRef(false);
  const editSequenceRef = useRef(0);
  const draftExerciseRef = useRef("");
  const workflowGenerationRef = useRef(0);
  const workflowBusyRef = useRef(false);
  const coachSubmitRef = useRef(false);
  const coachBusyRef = useRef(false);
  const coachGenerationRef = useRef(0);
  // Monaco can deliver an onChange callback before React has committed the
  // matching `code` state. Keep an independent, synchronous revision so an
  // inline edit can never allow a response for the previous document through.
  const coachDocumentRevisionRef = useRef(0);
  const coachActiveIntentRef = useRef<CoachIntent | null>(null);
  const coachAbortRef = useRef<AbortController | null>(null);
  const coachPanelRef = useRef<HTMLElement | null>(null);
  const coachMessagesRef = useRef<HTMLDivElement | null>(null);
  const coachStreamTextRef = useRef("");
  const coachStreamFrameRef = useRef<number | null>(null);
  const coachStreamingMessageRef = useRef<string | null>(null);
  const coachActiveSnapshotRef = useRef<CoachRequestSnapshot | null>(null);
  const retryCoachSnapshotRef = useRef<CoachRequestSnapshot | null>(null);
  const coachRestartTimerRef = useRef<number | null>(null);
  const referenceSolutionGenerationRef = useRef(0);
  const referenceSolutionAbortRef = useRef<AbortController | null>(null);
  const learnerCodeBeforeReferenceRef = useRef<string | null>(null);
  const consentFocusTargetRef = useRef<"editor" | "coach" | null>(null);
  const hintSequenceRef = useRef(0);
  const messageSequenceRef = useRef(0);
  const pendingCoachSnapshotRef = useRef<CoachRequestSnapshot | null>(null);
  const coachIdentityRef = useRef(coachRuntimeIdentity(aiStatus));
  const coachConversationScopeRef = useRef("");
  const aiStatusRef = useRef(aiStatus);
  const celebratedWorkflowRef = useRef<number | null>(null);
  const celebrationSequenceRef = useRef(0);
  const mascotSequenceRef = useRef(0);
  const mascotDragOffsetRef = useRef({ x: 0, y: 0 });
  const mascotDragStartRef = useRef<{
    pointerId: number;
    x: number;
    y: number;
    moved: boolean;
  } | null>(null);
  const mascotIdleTimerRef = useRef<number | null>(null);
  const mascotLessonSleepTimerRef = useRef<number | null>(null);
  const resetMascotIdleRef = useRef<() => void>(() => {});
  const mascotWakeRequiresClickRef = useRef(false);
  const mascotSleepingRef = useRef(false);
  const mascotLastActivityAtRef = useRef(0);
  const celebrationsEnabledRef = useRef(celebrationsEnabled);
  const pythonAutocompleteEnabledRef = useRef(pythonAutocompleteEnabled);
  const mascotEnabledRef = useRef(mascotEnabled);
  const selectedRef = useRef("");
  const dialogRestoreRef = useRef<HTMLElement | null>(null);
  const settingsDialogRef = useRef<HTMLElement | null>(null);
  const consentDialogRef = useRef<HTMLElement | null>(null);
  const codexInstallDialogRef = useRef<HTMLElement | null>(null);
  const codexInstallRestoreRef = useRef<HTMLElement | null>(null);
  const activeCelebrationId = celebration?.id;
  const activeMascotMomentId = mascotMoment?.id;
  const currentCoachRuntimeIdentity = coachRuntimeIdentity(aiStatus);
  const coachMessagesForStorage = useCallback((): CoachMessage[] => {
    const streamingId = coachStreamingMessageRef.current;
    const streamedText = coachStreamTextRef.current;
    if (!streamingId || !streamedText) return messagesRef.current;
    return messagesRef.current.map((message) =>
      message.id === streamingId
        ? { ...message, text: streamedText, contextual: false }
        : message,
    );
  }, []);
  const flushCoachConversationToStorage = useCallback(() => {
    const scope = coachConversationScopeRef.current;
    if (!scope) return;
    try {
      const [language, exerciseId, runtimeIdentity] = JSON.parse(scope) as [
        string,
        string,
        string,
      ];
      writeCoachConversation(
        window.localStorage,
        language,
        exerciseId,
        runtimeIdentity,
        coachMessagesForStorage(),
      );
    } catch {
      /* Leaving or switching remains safe when local storage is unavailable. */
    }
  }, [coachMessagesForStorage]);
  useEffect(() => {
    aiStatusRef.current = aiStatus;
  }, [aiStatus]);
  useEffect(() => {
    const provider = localMonaco.languages.registerCompletionItemProvider(
      "python",
      {
        provideCompletionItems(model, position) {
          const learnerModel = editorRef.current?.getModel();
          if (
            !pythonAutocompleteEnabledRef.current ||
            !learnerModel ||
            model !== learnerModel
          ) {
            return { suggestions: [] };
          }

          const word = model.getWordUntilPosition(position);
          const line = model.getLineContent(position.lineNumber);
          const characterBeforeWord = line.charAt(word.startColumn - 2);
          const characterAfterCursor = line.charAt(position.column - 1);
          const completions = findPythonPrefixCompletions(word.word);
          if (
            characterBeforeWord === "." ||
            /[A-Za-z0-9_]/.test(characterAfterCursor) ||
            completions.length === 0
          ) {
            return { suggestions: [] };
          }

          const range = new localMonaco.Range(
            position.lineNumber,
            word.startColumn,
            position.lineNumber,
            word.endColumn,
          );
          return {
            suggestions: completions.map((label) => {
              const keyword = pythonKeywordCompletions.has(label);
              const builtInType = pythonTypeCompletions.has(label);
              return {
                label,
                kind: keyword
                  ? localMonaco.languages.CompletionItemKind.Keyword
                  : label === "None"
                    ? localMonaco.languages.CompletionItemKind.Constant
                    : builtInType
                      ? localMonaco.languages.CompletionItemKind.Class
                      : localMonaco.languages.CompletionItemKind.Function,
                detail: keyword
                  ? "Python keyword"
                  : builtInType
                    ? "Python built-in type"
                    : label === "None"
                      ? "Python constant"
                      : "Python built-in function",
                insertText: label,
                filterText: label,
                sortText: label,
                range,
              };
            }),
          };
        },
      },
    );
    return () => provider.dispose();
  }, []);
  useEffect(() => {
    const timer = window.setInterval(
      () => setElapsed((value) => value + 1),
      1000,
    );
    return () => window.clearInterval(timer);
  }, []);
  useEffect(() => {
    if (!activeCelebrationId) return;
    const celebrationId = activeCelebrationId;
    const timer = window.setTimeout(
      () =>
        setCelebration((current) =>
          current?.id === celebrationId ? null : current,
        ),
      2600,
    );
    return () => window.clearTimeout(timer);
  }, [activeCelebrationId]);
  useEffect(() => {
    if (!activeMascotMomentId) return;
    const mascotMomentId = activeMascotMomentId;
    const duration =
      mascotMoment?.motion === "complete"
        ? 1800
        : mascotMoment?.motion === "happy"
          ? 2400
        : mascotMoment?.motion === "surprised"
          ? 2200
          : mascotMoment?.motion === "waking"
            ? 960
          : 0;
    if (!duration) return;
    const timer = window.setTimeout(
      () =>
        setMascotMoment((current) =>
          current?.id === mascotMomentId ? null : current,
        ),
      duration,
    );
    return () => window.clearTimeout(timer);
  }, [activeMascotMomentId, mascotMoment?.motion]);
  useEffect(() => {
    const keepMascotVisible = () =>
      setMascotPosition((current) => clampMascotPosition(current));
    window.addEventListener("resize", keepMascotVisible);
    return () => window.removeEventListener("resize", keepMascotVisible);
  }, []);
  useEffect(() => {
    mascotLastActivityAtRef.current = Date.now();
    const clearMascotSleepTimers = () => {
      if (mascotIdleTimerRef.current !== null)
        window.clearTimeout(mascotIdleTimerRef.current);
      if (mascotLessonSleepTimerRef.current !== null)
        window.clearTimeout(mascotLessonSleepTimerRef.current);
      mascotIdleTimerRef.current = null;
      mascotLessonSleepTimerRef.current = null;
    };
    const putMascotToSleep = (fromInactiveWindow: boolean) => {
      mascotIdleTimerRef.current = null;
      if (!mascotEnabledRef.current) return;
      setMascotMoment(null);
      mascotSleepingRef.current = true;
      setMascotSleeping(true);
      setMascotWindowInactive(fromInactiveWindow);
    };
    const scheduleMascotSleep = () => {
      clearMascotSleepTimers();
      if (mascotWakeRequiresClickRef.current) return;
      mascotLastActivityAtRef.current = Date.now();
      setMascotWindowInactive(false);
      setMascotMoment((current) =>
        current?.motion === "sleeping" ? null : current,
      );
      mascotSleepingRef.current = false;
      setMascotSleeping(false);
      mascotIdleTimerRef.current = window.setTimeout(() => {
        mascotIdleTimerRef.current = null;
        if (
          mascotEnabledRef.current &&
          !coachBusyRef.current &&
          !workflowBusyRef.current
        ) {
          putMascotToSleep(false);
        } else if (mascotEnabledRef.current) {
          scheduleMascotSleep();
        }
      }, mascotIdleSleepDelay);
    };
    resetMascotIdleRef.current = scheduleMascotSleep;
    const scheduleInactiveWindowSleep = () => {
      clearMascotSleepTimers();
      if (!mascotWakeRequiresClickRef.current) {
        mascotWakeRequiresClickRef.current = true;
      }
      const remaining = Math.max(
        0,
        mascotIdleSleepDelay - (Date.now() - mascotLastActivityAtRef.current),
      );
      mascotIdleTimerRef.current = window.setTimeout(
        () => {
          if (mascotWakeRequiresClickRef.current) putMascotToSleep(true);
        },
        remaining,
      );
    };
    const finishInactiveSleepWhenDue = () => {
      if (
        mascotWakeRequiresClickRef.current &&
        Date.now() - mascotLastActivityAtRef.current >= mascotIdleSleepDelay
      )
        putMascotToSleep(true);
    };
    const handleMascotPointerActivity = () => {
      const wasSleeping =
        mascotSleepingRef.current || mascotWakeRequiresClickRef.current;
      if (mascotWakeRequiresClickRef.current) {
        mascotWakeRequiresClickRef.current = false;
        setMascotWindowInactive(false);
      }
      if (wasSleeping && mascotEnabledRef.current) {
        mascotSleepingRef.current = false;
        setMascotSleeping(false);
        setMascotMoment({
          id: ++mascotSequenceRef.current,
          motion: "waking",
        });
      }
      scheduleMascotSleep();
    };
    const handleMascotKeyboardActivity = () => {
      if (mascotWakeRequiresClickRef.current) return;
      scheduleMascotSleep();
    };
    const handleMascotWindowBlur = () => scheduleInactiveWindowSleep();
    const handleMascotWindowFocus = () => finishInactiveSleepWhenDue();
    const handleMascotVisibilityChange = () => {
      if (document.hidden) scheduleInactiveWindowSleep();
      else finishInactiveSleepWhenDue();
    };
    window.addEventListener("pointerdown", handleMascotPointerActivity, {
      passive: true,
    });
    window.addEventListener("keydown", handleMascotKeyboardActivity);
    window.addEventListener("blur", handleMascotWindowBlur);
    window.addEventListener("focus", handleMascotWindowFocus);
    document.addEventListener(
      "visibilitychange",
      handleMascotVisibilityChange,
    );
    if (document.hidden || !document.hasFocus()) scheduleInactiveWindowSleep();
    else scheduleMascotSleep();
    return () => {
      window.removeEventListener("pointerdown", handleMascotPointerActivity);
      window.removeEventListener("keydown", handleMascotKeyboardActivity);
      window.removeEventListener("blur", handleMascotWindowBlur);
      window.removeEventListener("focus", handleMascotWindowFocus);
      document.removeEventListener(
        "visibilitychange",
        handleMascotVisibilityChange,
      );
      clearMascotSleepTimers();
      resetMascotIdleRef.current = () => {};
    };
  }, []);
  async function refreshAiStatus() {
    try {
      const response = await fetch("/api/ai/status");
      if (response.ok) setAiStatus(await response.json());
    } catch {
      /* Settings remains usable when the local service is restarting. */
    }
  }
  useEffect(() => {
    fetch("/api/ai/status")
      .then((response) => (response.ok ? response.json() : null))
      .then((data) => data && setAiStatus(data))
      .catch(() => undefined);
  }, []);
  useEffect(() => {
    const identity = currentCoachRuntimeIdentity;
    if (coachIdentityRef.current === identity) return;
    coachIdentityRef.current = identity;
    if (coachRestartTimerRef.current !== null) {
      window.clearTimeout(coachRestartTimerRef.current);
      coachRestartTimerRef.current = null;
    }
    coachGenerationRef.current += 1;
    coachAbortRef.current?.abort();
    coachAbortRef.current = null;
    coachBusyRef.current = false;
    coachActiveIntentRef.current = null;
    coachActiveSnapshotRef.current = null;
    coachSubmitRef.current = false;
    pendingCoachSnapshotRef.current = null;
    setCoachBusy(false);
    setCoachRestarting(false);
    setActiveCoachIntent(null);
    setCoachConsentOpen(false);
    setPendingCoachQuestion("");
    setPendingCoachProvider("");
    setPendingCoachIntent("adaptive");
    retryCoachSnapshotRef.current = null;
    setRetryCoachSnapshotState(null);
    setEditorHint(null);
    setEditorEdit(null);
    setPendingEditorEdit(null);
    setHintNotice("");
  }, [currentCoachRuntimeIdentity]);
  useEffect(() => {
    if (!selected) return;
    const scope = coachConversationScope(
      selectedLanguage,
      selected,
      currentCoachRuntimeIdentity,
    );
    if (coachConversationScopeRef.current !== scope) {
      const previousScope = coachConversationScopeRef.current;
      if (previousScope) {
        try {
          const [previousLanguage, previousExercise, previousRuntime] =
            JSON.parse(previousScope) as [string, string, string];
          writeCoachConversation(
            window.localStorage,
            previousLanguage,
            previousExercise,
            previousRuntime,
            coachMessagesForStorage(),
          );
        } catch {
          /* A provider change must still work when storage is unavailable. */
        }
      }
      coachConversationScopeRef.current = scope;
      let restored: ReturnType<typeof readCoachConversation> = [];
      try {
        restored = readCoachConversation(
          window.localStorage,
          selectedLanguage,
          selected,
          currentCoachRuntimeIdentity,
        );
      } catch {
        /* A fresh conversation remains available when storage is blocked. */
      }
      const restoredMessages: CoachMessage[] = [
        coachWelcome,
        ...restored.map((message) => ({
          ...message,
          id: `message-${++messageSequenceRef.current}`,
        })),
      ];
      messagesRef.current = restoredMessages;
      setMessages(restoredMessages);
      return;
    }
    const saveTimer = window.setTimeout(() => {
      try {
        writeCoachConversation(
          window.localStorage,
          selectedLanguage,
          selected,
          currentCoachRuntimeIdentity,
          coachMessagesForStorage(),
        );
      } catch {
        /* The visible conversation remains available for this session. */
      }
    }, 150);
    return () => window.clearTimeout(saveTimer);
  }, [
    coachMessagesForStorage,
    currentCoachRuntimeIdentity,
    messages,
    selected,
    selectedLanguage,
  ]);
  useEffect(() => {
    const flushBeforeLeaving = () => flushCoachConversationToStorage();
    window.addEventListener("pagehide", flushBeforeLeaving);
    return () => {
      flushBeforeLeaving();
      window.removeEventListener("pagehide", flushBeforeLeaving);
    };
  }, [flushCoachConversationToStorage]);
  useEffect(
    () => () => {
      if (coachRestartTimerRef.current !== null)
        window.clearTimeout(coachRestartTimerRef.current);
      coachGenerationRef.current += 1;
      coachAbortRef.current?.abort();
      referenceSolutionGenerationRef.current += 1;
      referenceSolutionAbortRef.current?.abort();
    },
    [],
  );
  useEffect(() => {
    try {
      window.localStorage.setItem(
        "kitcode:selected-practice-area",
        selectedPracticeArea,
      );
    } catch {
      /* The session selection remains available. */
    }
  }, [selectedPracticeArea]);
  useEffect(() => {
    try {
      window.localStorage.setItem("kitcode:selected-language", selectedLanguage);
    } catch {
      /* The session selection remains available. */
    }
    Promise.all([
      fetch(`/api/exercises?language=${selectedLanguage}`).then((r) =>
        r.ok ? r.json() : null,
      ),
      fetch(`/api/progress?language=${selectedLanguage}`).then((r) =>
        r.ok ? r.json() : null,
      ),
      fetch(`/api/generated-exercises?language=${selectedLanguage}`).then(
        (r) => (r.ok ? r.json() : null),
      ),
    ])
      .then(([catalog, progress, generated]) => {
        const rows = Array.isArray(catalog) ? catalog : catalog?.exercises;
        setCatalogTotal(
          Number(catalog?.overall_total ?? catalog?.catalog_total ?? 0) || 0,
        );
        const progressMap = progress?.progress ?? {};
        const list =
          Array.isArray(rows) && rows.length
            ? rows
                .map(normalizeProblem)
                .filter(
                  (item: Problem) =>
                    item.language === selectedLanguage &&
                    item.source !== "ai_generated",
                )
                .map((item: Problem) => ({
                  ...item,
                  solved: progressMap[item.id]?.status === "completed",
                }))
            : fallbackProblems.filter(
                (item) => (item.language ?? "python") === selectedLanguage,
              );
        const generatedRows = Array.isArray(generated)
          ? generated
          : generated?.exercises;
        setGeneratedProblems(
          Array.isArray(generatedRows)
            ? generatedRows
                .map(normalizeProblem)
                .filter((item: Problem) => item.language === selectedLanguage)
                .map((item: Problem) => ({
                  ...item,
                  source: "ai_generated",
                  solved:
                    item.solved ?? progressMap[item.id]?.status === "completed",
                }))
            : [],
        );
        setProblems(list);
        let remembered = "";
        try {
          remembered =
            window.localStorage.getItem(
              `kitcode:selected-exercise:${selectedLanguage}`,
            ) ?? "";
        } catch {
          /* Default selection remains usable. */
        }
        const preferredLevel = readLevelPreference(selectedLanguage);
        const candidate =
          list.find(
            (item: Problem) =>
              item.id === remembered && item.difficulty === preferredLevel,
          ) ??
          list.find(
            (item: Problem) =>
              item.difficulty === preferredLevel && !item.solved,
          ) ??
          list.find((item: Problem) => item.difficulty === preferredLevel) ??
          list[0];
        setSelected((old) =>
          list.some((item: Problem) => item.id === old)
            ? old
            : (candidate?.id ?? ""),
        );
      })
      .catch(() => {
        const list = fallbackProblems.filter(
          (item) => (item.language ?? "python") === selectedLanguage,
        );
        setCatalogTotal(0);
        setProblems(list);
        setGeneratedProblems([]);
        setSelected(list[0]?.id ?? "");
      });
  }, [selectedLanguage]);
  useEffect(() => {
    try {
      window.localStorage.setItem("kitcode:selected-sql-dialect", sqlDialect);
    } catch {
      /* The selection remains available for this session. */
    }
  }, [sqlDialect]);
  useEffect(() => {
    if (!selected) return;
    let cancelled = false;
    if (coachRestartTimerRef.current !== null) {
      window.clearTimeout(coachRestartTimerRef.current);
      coachRestartTimerRef.current = null;
    }
    coachGenerationRef.current += 1;
    coachAbortRef.current?.abort();
    coachAbortRef.current = null;
    coachBusyRef.current = false;
    coachActiveIntentRef.current = null;
    coachActiveSnapshotRef.current = null;
    coachSubmitRef.current = false;
    pendingCoachSnapshotRef.current = null;
    workflowGenerationRef.current += 1;
    selectedRef.current = selected;
    draftExerciseRef.current = "";
    fetch(
      `/api/exercises/${encodeURIComponent(selected)}?language=${selectedLanguage}`,
    )
      .then((r) => (r.ok ? r.json() : null))
      .then((data) => {
        if (cancelled || !data) return;
        const exercise = normalizeProblem(data, 0);
        coachGenerationRef.current += 1;
        coachAbortRef.current?.abort();
        coachAbortRef.current = null;
        coachBusyRef.current = false;
        coachSubmitRef.current = false;
        pendingCoachSnapshotRef.current = null;
        setCoachBusy(false);
        setCoachRestarting(false);
        setActiveCoachIntent(null);
        setCoachConsentOpen(false);
        setPendingCoachQuestion("");
        setPendingCoachProvider("");
        setPendingCoachIntent("adaptive");
        setEditorHint(null);
        setEditorEdit(null);
        setPendingEditorEdit(null);
        setHintNotice("");
        if (exercise.source === "ai_generated")
          setGeneratedProblems((all) =>
            all.map((item) =>
              item.id === exercise.id
                ? { ...item, ...exercise, source: "ai_generated" }
                : item,
            ),
          );
        else
          setProblems((all) =>
            all.map((item) =>
              item.id === exercise.id ? { ...item, ...exercise } : item,
            ),
          );
        let savedDraft: string | null = null;
        try {
          savedDraft = readPersistedDraft(
            localStorage,
            selectedLanguage,
            exercise.id,
            exercise.starter_code,
          );
        } catch {
          /* Starter code remains available. */
        }
        setCode(
          savedDraft ?? exercise.starter_code ?? blankCodeFor(selectedLanguage),
        );
        setStdin(exercise.examples?.[0]?.input ?? "");
        setRunResult(null);
        setTraceSteps([]);
        setTraceIndex(0);
        draftExerciseRef.current = exercise.id;
        setDraftExerciseId(exercise.id);
        setDraftReady(true);
        setStatus("Ready to run");
      })
      .catch(() => {
        if (cancelled) return;
        coachGenerationRef.current += 1;
        coachAbortRef.current?.abort();
        coachAbortRef.current = null;
        coachBusyRef.current = false;
        coachSubmitRef.current = false;
        pendingCoachSnapshotRef.current = null;
        setCoachBusy(false);
        setCoachRestarting(false);
        setActiveCoachIntent(null);
        setCoachConsentOpen(false);
        setPendingCoachQuestion("");
        setPendingCoachProvider("");
        setPendingCoachIntent("adaptive");
        setEditorHint(null);
        setEditorEdit(null);
        setPendingEditorEdit(null);
        setHintNotice("");
        const local = problems.find((item) => item.id === selected);
        let savedDraft: string | null = null;
        try {
          savedDraft = readPersistedDraft(
            localStorage,
            selectedLanguage,
            selected,
            local?.starter_code,
          );
        } catch {
          /* Starter code remains available. */
        }
        setCode(
          savedDraft ?? local?.starter_code ?? blankCodeFor(selectedLanguage),
        );
        draftExerciseRef.current = selected;
        setDraftExerciseId(selected);
        setDraftReady(true);
      });
    return () => {
      cancelled = true;
    };
    // problems intentionally excluded: catalog arrival must not reset code while the user types.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [selected, selectedLanguage]);
  useEffect(() => {
    if (draftReady && selected && draftExerciseRef.current === selected)
      try {
        localStorage.setItem(
          `kitcode:draft:${selectedLanguage}:${selected}`,
          code,
        );
      } catch {
        /* Session draft remains available. */
      }
  }, [code, draftReady, selected, selectedLanguage]);
  useEffect(() => {
    if (!settingsOpen && !coachConsentOpen && !codexInstallConfirmOpen) return;
    const dialog = codexInstallConfirmOpen
      ? codexInstallDialogRef.current
      : settingsOpen
        ? settingsDialogRef.current
        : consentDialogRef.current;
    const focusInitial = () =>
      dialog
        ?.querySelector<HTMLElement>("[data-dialog-initial-focus]")
        ?.focus();
    const focusTimer = window.setTimeout(focusInitial, 0);
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.preventDefault();
        if (codexInstallConfirmOpen) setCodexInstallConfirmOpen(false);
        else if (settingsOpen) setSettingsOpen(false);
        else {
          const pending = pendingCoachSnapshotRef.current;
          if (pending?.intent === "adaptive")
            setCoachInput((currentValue) => currentValue || pending.question);
          pendingCoachSnapshotRef.current = null;
          coachSubmitRef.current = false;
          setCoachConsentOpen(false);
          setPendingCoachQuestion("");
          setPendingCoachProvider("");
          setPendingCoachIntent("adaptive");
        }
        return;
      }
      if (event.key !== "Tab" || !dialog) return;
      const focusable = Array.from(
        dialog.querySelectorAll<HTMLElement>(
          "button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex='-1'])",
        ),
      ).filter((item) => !item.hasAttribute("hidden"));
      if (!focusable.length) {
        event.preventDefault();
        return;
      }
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };
    document.addEventListener("keydown", onKeyDown);
    return () => {
      window.clearTimeout(focusTimer);
      document.removeEventListener("keydown", onKeyDown);
    };
  }, [settingsOpen, coachConsentOpen, codexInstallConfirmOpen]);
  useEffect(() => {
    if (!settingsOpen) return;
    const restoreTarget = dialogRestoreRef.current;
    return () => {
      window.setTimeout(() => restoreTarget?.focus(), 0);
    };
  }, [settingsOpen]);
  useEffect(() => {
    if (!coachConsentOpen) return;
    const restoreTarget = dialogRestoreRef.current;
    const restoreCoachPanel = coachPanelRef.current;
    return () => {
      window.setTimeout(() => {
        const target = consentFocusTargetRef.current;
        consentFocusTargetRef.current = null;
        if (target === "editor") editorRef.current?.focus();
        else if (target === "coach") restoreCoachPanel?.focus();
        else restoreTarget?.focus();
      }, 0);
    };
  }, [coachConsentOpen]);
  useEffect(() => {
    if (!codexInstallConfirmOpen) return;
    const restoreTarget = codexInstallRestoreRef.current;
    return () => {
      window.setTimeout(() => restoreTarget?.focus(), 25);
    };
  }, [codexInstallConfirmOpen]);
  useEffect(() => {
    if (!codexLoginPolling || !settingsOpen) return;
    let cancelled = false;
    let attempts = 0;
    let timer = 0;
    const poll = async () => {
      if (cancelled) return;
      attempts += 1;
      try {
        const response = await fetch("/api/ai/detect-codex", {
          method: "POST",
        });
        const payload: CodexDetection = await response.json().catch(() => ({}));
        if (!response.ok) throw new Error();
        if (cancelled) return;
        setCodexDetection(payload);
        if (payload.ready) {
          setSetupNotice(
            "ChatGPT sign-in confirmed. Codex is connected and selected as your coach.",
          );
          const statusResponse = await fetch("/api/ai/status");
          if (statusResponse.ok && !cancelled)
            setAiStatus(await statusResponse.json());
          if (!cancelled) setCodexLoginPolling(false);
          return;
        }
      } catch {
        // Sign-in can briefly interrupt the local status check; retry below.
      }
      if (attempts >= 40) {
        setCodexLoginPolling(false);
        setSetupNotice(
          "Sign-in was not confirmed yet. Finish the ChatGPT browser flow, then click Recheck Codex.",
        );
        return;
      }
      timer = window.setTimeout(() => void poll(), 3000);
    };
    timer = window.setTimeout(() => void poll(), 1500);
    return () => {
      cancelled = true;
      window.clearTimeout(timer);
    };
  }, [codexLoginPolling, settingsOpen]);
  useEffect(() => {
    const line = traceSteps[traceIndex]?.line;
    const editor = editorRef.current;
    const monaco = monacoRef.current;
    if (!line || !editor || !monaco) return;
    editor.revealLineInCenter(line);
    decorationRef.current = editor.deltaDecorations(decorationRef.current, [
      {
        range: new monaco.Range(line, 1, line, 1),
        options: {
          isWholeLine: true,
          className: "trace-line-highlight",
          glyphMarginClassName: "trace-line-glyph",
        },
      },
    ]);
  }, [traceIndex, traceSteps]);
  useEffect(() => {
    const editor = editorRef.current;
    const monaco = monacoRef.current;
    const removeHintViewZone = () => {
      const existing = hintViewZoneRef.current;
      if (!existing) return;
      hintViewZoneRef.current = null;
      const existingModel = existing.editor.getModel();
      if (!existingModel || existingModel.isDisposed()) return;
      existing.editor.changeViewZones((accessor) => {
        accessor.removeZone(existing.id);
      });
    };

    removeHintViewZone();
    if (!editor || !monaco) return;
    const model = editor.getModel();
    const line =
      editorHint && model
        ? Math.min(Math.max(1, editorHint.line), model.getLineCount())
        : 1;
    hintDecorationRef.current = editor.deltaDecorations(
      hintDecorationRef.current,
      inlineHintsEnabled && editorHint?.inline && model
        ? [
            {
              range: new monaco.Range(line, 1, line, 1),
              options: {
                isWholeLine: true,
                className: "editor-hint-line",
              },
            },
          ]
        : [],
    );

    if (!inlineHintsEnabled || !editorHint?.inline || !model) {
      editor.render(true);
      return;
    }

    const hintNode = document.createElement("div");
    hintNode.className = "editor-hint-inline";
    hintNode.setAttribute("aria-hidden", "true");
    const hintLabel = document.createElement("strong");
    hintLabel.textContent = `Hint - Line ${line}:`;
    const hintText = document.createElement("span");
    hintText.textContent = editorHint.text;
    hintNode.append(hintLabel, " ", hintText);

    let zoneId = "";
    editor.changeViewZones((accessor) => {
      zoneId = accessor.addZone({
        afterLineNumber: line,
        heightInPx: 58,
        domNode: hintNode,
        suppressMouseDown: true,
      });
    });
    if (zoneId) hintViewZoneRef.current = { editor, id: zoneId };
    editor.revealLineInCenterIfOutsideViewport(line);
    editor.layout();
    editor.render(true);
    return () => {
      if (hintViewZoneRef.current?.editor === editor) removeHintViewZone();
    };
  }, [editorHint, editorMountVersion, inlineHintsEnabled]);
  useEffect(() => {
    const editor = editorRef.current;
    const monaco = monacoRef.current;
    const model = editor?.getModel();
    if (!editor || !monaco || !model) return;
    const editDecorations = (editorEdit?.ranges ?? []).map((changedRange) => {
      const startLine = Math.min(
        Math.max(1, changedRange.startLine),
        model.getLineCount(),
      );
      const endLine = Math.min(
        Math.max(startLine, changedRange.endLine),
        model.getLineCount(),
      );
      return {
        range: new monaco.Range(
          startLine,
          1,
          endLine,
          model.getLineMaxColumn(endLine),
        ),
        options: {
          isWholeLine: true,
          className: "ai-edit-highlight",
          glyphMarginClassName: "ai-edit-glyph",
          hoverMessage: { value: "AI-applied code — review before running" },
        },
      };
    });
    editDecorationRef.current = editor.deltaDecorations(
      editDecorationRef.current,
      editDecorations,
    );
  }, [editorEdit]);
  const levelCounts = useMemo(
    () =>
      Object.fromEntries(
        practiceLevels.map((level) => [
          level.id,
          problems.filter(
            (item) =>
              item.language === selectedLanguage &&
              item.difficulty === level.id,
          ).length,
        ]),
      ) as Record<PracticeLevel, number>,
    [problems, selectedLanguage],
  );
  const levelSolved = useMemo(
    () =>
      Object.fromEntries(
        practiceLevels.map((level) => [
          level.id,
          problems.filter(
            (item) =>
              item.language === selectedLanguage &&
              item.difficulty === level.id &&
              item.solved,
          ).length,
        ]),
      ) as Record<PracticeLevel, number>,
    [problems, selectedLanguage],
  );
  const availableTopics = useMemo(
    () =>
      Array.from(
        new Set(
          problems
            .filter(
              (item) =>
                item.language === selectedLanguage &&
                item.difficulty === difficulty,
            )
            .flatMap((item) =>
              item.topics?.length ? item.topics : [item.topic],
            )
            .filter(Boolean),
        ),
      ).sort((left, right) => left.localeCompare(right)),
    [problems, selectedLanguage, difficulty],
  );
  const visible = useMemo(
    () =>
      problems.filter(
        (item) =>
          item.language === selectedLanguage &&
          item.difficulty === difficulty &&
          (topicFilter === "All topics" ||
            (item.topics?.length ? item.topics : [item.topic]).includes(
              topicFilter,
            )) &&
          `${item.title} ${item.topic} ${(item.topics ?? []).join(" ")}`
            .toLowerCase()
            .includes(query.toLowerCase()),
      ),
    [problems, difficulty, topicFilter, query, selectedLanguage],
  );
  const visibleGenerated = useMemo(
    () =>
      generatedProblems.filter(
        (item) =>
          item.language === selectedLanguage &&
          item.difficulty === difficulty &&
          (topicFilter === "All topics" ||
            (item.topics?.length ? item.topics : [item.topic]).includes(
              topicFilter,
            )) &&
          `${item.title} ${item.topic} ${(item.topics ?? []).join(" ")}`
            .toLowerCase()
            .includes(query.toLowerCase()),
      ),
    [generatedProblems, difficulty, topicFilter, query, selectedLanguage],
  );
  const current =
    problems.find((item) => item.id === selected) ??
    generatedProblems.find((item) => item.id === selected) ??
    problems[0] ??
    fallbackProblems[0];
  const results = runResult?.results ?? runResult?.tests ?? [];
  const solved = problems.filter((item) => item.solved).length;
  const visibleGeneratedSolved = visibleGenerated.filter(
    (item) => item.solved,
  ).length;
  const clock = `${String(Math.floor(elapsed / 60)).padStart(2, "0")}:${String(elapsed % 60).padStart(2, "0")}`;
  const selectedProvider =
    aiStatus.provider === "codex"
      ? "Codex"
      : aiStatus.provider === "anthropic"
        ? "Anthropic API"
        : aiStatus.provider === "openai"
          ? "OpenAI API"
          : aiStatus.provider === "local_llm"
            ? "Local LLM"
            : "No AI provider";
  const availableProviders =
    [
      aiStatus.openai_configured && "OpenAI API",
      aiStatus.anthropic_configured && "Anthropic API",
      aiStatus.local_llm_configured && "Local LLM",
      aiStatus.codex_usable && "Codex",
    ]
      .filter(Boolean)
      .join(" and ") || "none";
  const interviewSubject: InterviewSubject | null =
    selectedPracticeArea === "machine-learning"
      ? "machine-learning"
      : selectedPracticeArea === selectedLanguage &&
          practiceSection === "interview"
        ? selectedLanguage
        : null;
  const interviewActive = interviewSubject !== null;
  const machineLearningActive =
    selectedPracticeArea === "machine-learning";
  const coachReady = Boolean(
    !interviewActive &&
      aiStatus.configured &&
      draftReady &&
      selected &&
      draftExerciseId === selected,
  );
  const referenceAnswerUnlocked = Boolean(
    acceptedSubmission?.exerciseId === selected &&
      acceptedSubmission.language === selectedLanguage &&
      acceptedSubmission.code === code &&
      (selectedLanguage !== "sql" ||
        acceptedSubmission.sqlDialect === sqlDialect),
  );
  const bestSolutionActive = Boolean(
    editorDocument === "reference" &&
      referenceSolution?.exerciseId === selected &&
      referenceSolution.language === selectedLanguage,
  );
  const streamingCoachMessageId = coachBusy
    ? messages.reduce<string | null>(
        (latest, message) =>
          message.role === "coach" &&
          !message.contextual &&
          !message.text
            ? message.id
            : latest,
        null,
      )
    : null;
  const setupProviderConfigured =
    setupProvider === "openai"
      ? Boolean(aiStatus.openai_configured)
        : setupProvider === "anthropic"
          ? Boolean(aiStatus.anthropic_configured)
          : true;
  const activeLanguage = languageMeta(selectedLanguage);
  const pythonAutocompleteActive =
    selectedLanguage === "python" &&
    pythonAutocompleteEnabled &&
    !bestSolutionActive;
  const bestSolutionFile = `best-${activeLanguage.file}`;
  const activeSqlDialect = sqlDialectMeta(sqlDialect);
  const sqlExecutionEngineValue =
    runResult?.executed_engine ??
    runResult?.sql_engine ??
    runResult?.execution_engine ??
    "sqlite";
  const sqlExecutionEngine =
    sqlExecutionEngineValue.toLowerCase() === "sqlite"
      ? "SQLite (built in)"
      : sqlExecutionEngineValue;
  const onMount: OnMount = (editor, monaco) => {
    editorRef.current = editor;
    monacoRef.current = monaco;
    hintDecorationRef.current = [];
    monaco.editor.defineTheme("kitcode-night", {
      base: "vs-dark",
      inherit: true,
      rules: [
        { token: "comment", foreground: "71809c" },
        { token: "keyword", foreground: "9bb5ff" },
        { token: "string", foreground: "9ee2b7" },
        { token: "number", foreground: "e9bd76" },
      ],
      colors: {
        "editor.background": "#0b1423",
        "editor.lineHighlightBackground": "#15213a",
        "editorCursor.foreground": "#9eb4ff",
        "editor.selectionBackground": "#314a7d",
      },
    });
    monaco.editor.setTheme("kitcode-night");
    // Replay any hint that became ready while Monaco was still mounting.
    setEditorMountVersion((version) => version + 1);
  };
  function scrollCoachToLatestIfNearBottom() {
    const panel = coachMessagesRef.current;
    if (!panel) return;
    const distance = panel.scrollHeight - panel.scrollTop - panel.clientHeight;
    if (distance < 96) panel.scrollTop = panel.scrollHeight;
  }
  function flushStreamingCoachMessage(id: string, contextual = false) {
    if (coachStreamFrameRef.current !== null) {
      window.cancelAnimationFrame(coachStreamFrameRef.current);
      coachStreamFrameRef.current = null;
    }
    const text = coachStreamTextRef.current;
    messagesRef.current = messagesRef.current.map((message) =>
      message.id === id ? { ...message, text, contextual } : message,
    );
    setMessages((all) =>
      all.map((message) =>
        message.id === id ? { ...message, text, contextual } : message,
      ),
    );
    window.requestAnimationFrame(scrollCoachToLatestIfNearBottom);
  }
  // Keep a synchronous copy so pagehide and a rapid exercise change cannot
  // miss a message React has not rendered yet.
  function replaceCoachMessages(nextMessages: CoachMessage[]) {
    messagesRef.current = nextMessages;
    setMessages(nextMessages);
  }
  function appendCoachMessage(message: CoachMessage) {
    replaceCoachMessages([...messagesRef.current, message]);
  }
  function setRetryCoachSnapshot(snapshot: CoachRequestSnapshot | null) {
    retryCoachSnapshotRef.current = snapshot;
    setRetryCoachSnapshotState(snapshot);
  }
  function queueStreamingCoachMessage(id: string) {
    if (coachStreamFrameRef.current !== null) return;
    // A frame-level cadence keeps React responsive for token-by-token providers.
    coachStreamFrameRef.current = window.requestAnimationFrame(() => {
      coachStreamFrameRef.current = null;
      flushStreamingCoachMessage(id);
    });
  }
  function clearScheduledCoachRestart() {
    if (coachRestartTimerRef.current !== null) {
      window.clearTimeout(coachRestartTimerRef.current);
      coachRestartTimerRef.current = null;
    }
    setCoachRestarting(false);
  }
  function settleStreamingCoachMessage(note: string) {
    const id = coachStreamingMessageRef.current;
    if (!id) return false;
    const partial = coachStreamTextRef.current.trim();
    coachStreamTextRef.current = partial
      ? `${partial}\n\n*${note}*`
      : `*${note}*`;
    flushStreamingCoachMessage(id);
    coachStreamingMessageRef.current = null;
    return true;
  }
  function coachSnapshotMatchesScope(
    snapshot: CoachRequestSnapshot,
    generation?: number,
  ) {
    return (
      (generation === undefined || generation === coachGenerationRef.current) &&
      selectedRef.current === snapshot.exerciseId &&
      selectedLanguage === snapshot.language &&
      (snapshot.language !== "sql" || snapshot.sqlDialect === sqlDialect) &&
      coachRuntimeIdentity(aiStatusRef.current) === snapshot.runtimeIdentity
    );
  }
  function coachSnapshotIsCurrent(
    snapshot: CoachRequestSnapshot,
    generation?: number,
  ) {
    const model = editorRef.current?.getModel();
    return (
      coachSnapshotMatchesScope(snapshot, generation) &&
      coachDocumentRevisionRef.current === snapshot.documentRevision &&
      (model?.getVersionId() ?? 0) === snapshot.modelVersion &&
      (model?.getValue() ?? snapshot.code) === snapshot.code
    );
  }
  function coachResponseIsCurrent(
    snapshot: CoachRequestSnapshot,
    generation?: number,
  ) {
    return snapshot.intent === "hint"
      ? coachSnapshotMatchesScope(snapshot, generation)
      : coachSnapshotIsCurrent(snapshot, generation);
  }
  function coachIntentSupportsRetry(intent?: CoachIntent) {
    return intent === "adaptive" || intent === "edit";
  }
  function interruptActiveCoach(
    note: string,
    notice: string,
    retryable: boolean,
  ) {
    if (!coachBusyRef.current) return null;
    const snapshot = coachActiveSnapshotRef.current;
    coachGenerationRef.current += 1;
    coachAbortRef.current?.abort();
    coachAbortRef.current = null;
    coachBusyRef.current = false;
    coachSubmitRef.current = false;
    coachActiveIntentRef.current = null;
    coachActiveSnapshotRef.current = null;
    setCoachBusy(false);
    setActiveCoachIntent(null);
    const settled = settleStreamingCoachMessage(note);
    if (coachStreamFrameRef.current !== null) {
      window.cancelAnimationFrame(coachStreamFrameRef.current);
      coachStreamFrameRef.current = null;
    }
    if (
      !settled &&
      snapshot &&
      (snapshot.intent === "adaptive" || snapshot.intent === "edit")
    ) {
      appendCoachMessage({
        id: `message-${++messageSequenceRef.current}`,
        role: "coach",
        text: note,
        contextual: false,
      });
    }
    const savedRetry =
      retryable &&
      coachIntentSupportsRetry(snapshot?.intent) &&
      snapshot &&
      coachSnapshotIsCurrent(snapshot)
        ? snapshot
        : null;
    setRetryCoachSnapshot(savedRetry);
    setHintNotice(notice);
    return savedRetry;
  }
  function stopCoachResponse() {
    interruptActiveCoach(
      "Response stopped. Choose Try again to restart it.",
      "Coach response stopped · Try again is ready.",
      true,
    );
  }
  function cancelCoachWork(
    resetConversation = false,
    discardVisibleHint = false,
    preserveSideCoachRetry = false,
  ) {
    const activeSnapshot = coachActiveSnapshotRef.current;
    const previousRetry = retryCoachSnapshotRef.current;
    const activeRetry =
      coachIntentSupportsRetry(activeSnapshot?.intent) &&
      activeSnapshot &&
      coachSnapshotMatchesScope(activeSnapshot)
        ? activeSnapshot
        : null;
    const savedRetry = preserveSideCoachRetry
      ? activeRetry ??
        (coachIntentSupportsRetry(previousRetry?.intent) &&
        previousRetry &&
        coachSnapshotMatchesScope(previousRetry)
          ? previousRetry
          : null)
      : null;
    const interruptedSideRequest =
      preserveSideCoachRetry && activeRetry !== null;
    const interruptionNote = interruptedSideRequest
      ? "Response stopped because your code changed. Choose Try again to ask the same question about your latest code."
      : "Response stopped because the workspace changed.";
    clearScheduledCoachRestart();
    coachGenerationRef.current += 1;
    coachAbortRef.current?.abort();
    coachAbortRef.current = null;
    const settled = !resetConversation
      ? settleStreamingCoachMessage(interruptionNote)
      : false;
    if (!settled && interruptedSideRequest) {
      appendCoachMessage({
        id: `message-${++messageSequenceRef.current}`,
        role: "coach",
        text: interruptionNote,
        contextual: false,
      });
    }
    coachStreamingMessageRef.current = null;
    coachActiveSnapshotRef.current = null;
    coachActiveIntentRef.current = null;
    if (coachStreamFrameRef.current !== null) {
      window.cancelAnimationFrame(coachStreamFrameRef.current);
      coachStreamFrameRef.current = null;
    }
    coachBusyRef.current = false;
    coachSubmitRef.current = false;
    pendingCoachSnapshotRef.current = null;
    setRetryCoachSnapshot(savedRetry);
    setCoachBusy(false);
    setActiveCoachIntent(null);
    setCoachConsentOpen(false);
    setPendingCoachQuestion("");
    setPendingCoachProvider("");
    setPendingCoachIntent("adaptive");
    if (discardVisibleHint) setEditorHint(null);
    setHintNotice(
      savedRetry
        ? "Code changed · Try again will use your latest code."
        : "",
    );
    if (resetConversation) replaceCoachMessages([coachWelcome]);
  }
  function clearEditorHint() {
    setEditorHint(null);
    setHintNotice("");
  }
  function clearEditorEdit() {
    setEditorEdit(null);
    setPendingEditorEdit(null);
  }
  function handleEditorChange(value?: string) {
    const nextCode = value ?? "";
    const isAiEdit = applyingEditorEditRef.current;
    applyingEditorEditRef.current = false;
    if (!isAiEdit) {
      coachDocumentRevisionRef.current += 1;
      if (coachActiveIntentRef.current !== "hint")
        cancelCoachWork(false, false, true);
      setPendingEditorEdit(null);
      setEditorEdit(null);
    }
    if (acceptedSubmission && acceptedSubmission.code !== nextCode)
      clearReferenceSolutionState();
    setCode(nextCode);
  }
  function undoEditorEdit() {
    const edit = editorEdit;
    const editor = editorRef.current;
    const model = editor?.getModel();
    if (!edit || !editor || !model) return;
    if (!edit.undoAvailable || model.getValue() !== edit.after) {
      setStatus(
        "The script changed after the AI edit · use Ctrl+Z for edit history",
      );
      editor.focus();
      return;
    }
    coachDocumentRevisionRef.current += 1;
    if (coachActiveIntentRef.current !== "hint")
      cancelCoachWork(false, false, true);
    applyingEditorEditRef.current = true;
    editor.trigger("kitcode-ai", "undo", null);
    applyingEditorEditRef.current = false;
    setEditorEdit(null);
    setStatus("AI edit undone");
    editor.focus();
  }
  function applyPendingEditorEdit() {
    const edit = pendingEditorEdit;
    const editor = editorRef.current;
    const model = editor?.getModel();
    if (!edit || !editor || !model || model.getValue() !== edit.before) {
      setPendingEditorEdit(null);
      setStatus("The script changed · ask the coach for a fresh edit");
      editor?.focus();
      return;
    }
    coachDocumentRevisionRef.current += 1;
    if (coachActiveIntentRef.current !== "hint")
      cancelCoachWork(false, false, true);
    applyingEditorEditRef.current = true;
    editor.pushUndoStop();
    editor.executeEdits("kitcode-ai", [
      {
        range: model.getFullModelRange(),
        text: edit.after,
        forceMoveMarkers: true,
      },
    ]);
    editor.pushUndoStop();
    applyingEditorEditRef.current = false;
    setCode(edit.after);
    setPendingEditorEdit(null);
    setEditorEdit(edit);
    appendCoachMessage({
      id: `message-${++messageSequenceRef.current}`,
      role: "coach",
      text: `${edit.message}\n\nI applied this as a highlighted, undoable editor edit. Review it before running.`,
      contextual: true,
    });
    setStatus(
      `AI edited ${edit.startLine === edit.endLine ? `line ${edit.startLine}` : `lines ${edit.startLine}–${edit.endLine}`} · review before running`,
    );
    editor.revealLinesInCenterIfOutsideViewport(edit.startLine, edit.endLine);
    editor.focus();
  }
  function clearReferenceSolutionState() {
    referenceSolutionGenerationRef.current += 1;
    referenceSolutionAbortRef.current?.abort();
    referenceSolutionAbortRef.current = null;
    setAcceptedSubmission(null);
    setReferenceSolution(null);
    setEditorDocument("learner");
    learnerCodeBeforeReferenceRef.current = null;
    setReferenceSolutionLoading(false);
    setReferenceSolutionError("");
  }
  function choosePracticeSection(section: PracticeSection) {
    if (
      selectedPracticeArea === selectedLanguage &&
      section === practiceSection
    ) {
      setProblemDrawerOpen(false);
      return;
    }
    flushCoachConversationToStorage();
    cancelCoachWork(false, true);
    clearEditorEdit();
    workflowGenerationRef.current += 1;
    workflowBusyRef.current = false;
    setWorkflowBusy(false);
    setCelebration(null);
    setRunResult(null);
    clearReferenceSolutionState();
    setTraceSteps([]);
    setTraceIndex(0);
    setStatus(
      section === "interview"
        ? `${languageMeta(selectedLanguage).label} Interview FAQs · choose an answer`
        : "Ready to run",
    );
    setSelectedPracticeArea(selectedLanguage);
    setPracticeSection(section);
    setProblemDrawerOpen(false);
    try {
      window.localStorage.setItem(
        `kitcode:selected-${selectedLanguage}-section`,
        section,
      );
    } catch {
      /* The section remains selected for this session. */
    }
  }
  function selectMachineLearning() {
    if (selectedPracticeArea === "machine-learning") return;
    flushCoachConversationToStorage();
    cancelCoachWork(false, true);
    clearEditorEdit();
    workflowGenerationRef.current += 1;
    workflowBusyRef.current = false;
    setWorkflowBusy(false);
    setCelebration(null);
    setRunResult(null);
    clearReferenceSolutionState();
    setTraceSteps([]);
    setTraceIndex(0);
    setStatus("Machine Learning Concepts · choose an answer");
    setSelectedPracticeArea("machine-learning");
    setProblemDrawerOpen(false);
  }
  function selectExercise(exerciseId: string) {
    if (exerciseId === selected) {
      setProblemDrawerOpen(false);
      return;
    }
    flushCoachConversationToStorage();
    try {
      window.localStorage.setItem(
        `kitcode:selected-exercise:${selectedLanguage}`,
        exerciseId,
      );
    } catch {
      /* Current session selection still works. */
    }
    coachConversationScopeRef.current = "";
    cancelCoachWork(true, true);
    clearEditorEdit();
    setDraftReady(false);
    draftExerciseRef.current = "";
    setDraftExerciseId("");
    workflowGenerationRef.current += 1;
    selectedRef.current = exerciseId;
    workflowBusyRef.current = false;
    setWorkflowBusy(false);
    setCelebration(null);
    setRunResult(null);
    clearReferenceSolutionState();
    setTraceSteps([]);
    setTraceIndex(0);
    setStatus("Loading drill…");
    setSelected(exerciseId);
  }
  function selectLanguage(language: PracticeLanguage) {
    if (language === selectedLanguage) {
      if (selectedPracticeArea === selectedLanguage) return;
      const nextSection = readPracticeSection(language);
      setSelectedPracticeArea(language);
      setPracticeSection(nextSection);
      setStatus(
        nextSection === "interview"
          ? `${languageMeta(language).label} Interview FAQs · choose an answer`
          : "Ready to run",
      );
      setProblemDrawerOpen(false);
      return;
    }
    flushCoachConversationToStorage();
    coachConversationScopeRef.current = "";
    cancelCoachWork(true, true);
    clearEditorEdit();
    setDraftReady(false);
    draftExerciseRef.current = "";
    setDraftExerciseId("");
    workflowGenerationRef.current += 1;
    selectedRef.current = "";
    workflowBusyRef.current = false;
    setWorkflowBusy(false);
    setCelebration(null);
    setRunResult(null);
    clearReferenceSolutionState();
    setTraceSteps([]);
    setTraceIndex(0);
    setQuery("");
    setTopicFilter("All topics");
    setDifficulty(readLevelPreference(language));
    const nextSection = readPracticeSection(language);
    setStatus(
      nextSection === "interview"
        ? `${languageMeta(language).label} Interview FAQs · choose an answer`
        : `Loading ${languageMeta(language).label} drills…`,
    );
    setSelected("");
    setSelectedLanguage(language);
    setSelectedPracticeArea(language);
    setPracticeSection(nextSection);
  }
  function selectSqlDialect(dialect: SqlDialect) {
    if (dialect === sqlDialect) return;
    clearReferenceSolutionState();
    setRunResult(null);
    setTraceSteps([]);
    setTraceIndex(0);
    setSqlDialect(dialect);
    setStatus(`SQL dialect changed to ${sqlDialectMeta(dialect).label}`);
  }
  function choosePracticeLevel(level: PracticeLevel) {
    setDifficulty(level);
    setTopicFilter("All topics");
    setQuery("");
    try {
      window.localStorage.setItem(
        `kitcode:selected-level:${selectedLanguage}`,
        level,
      );
    } catch {
      /* The in-memory level remains active. */
    }
    const currentProblem = problems.find((item) => item.id === selectedRef.current);
    if (currentProblem?.difficulty !== level) {
      const next =
        problems.find(
          (item) => item.difficulty === level && !item.solved,
        ) ?? problems.find((item) => item.difficulty === level);
      if (next) selectExercise(next.id);
    }
  }
  function resetCode() {
    if (coachActiveIntentRef.current !== "hint")
      cancelCoachWork(false, false, true);
    coachDocumentRevisionRef.current += 1;
    clearEditorEdit();
    clearReferenceSolutionState();
    const fresh = current.starter_code ?? blankCodeFor(selectedLanguage);
    try {
      clearPersistedDraft(localStorage, selectedLanguage, selected);
    } catch {
      /* Starter code remains usable. */
    }
    setCode(fresh);
    setStatus("Starter code restored");
  }
  function startWorkflow(clearAcceptedSubmission = false) {
    if (!selected || workflowBusyRef.current) return null;
    resetMascotIdleRef.current();
    if (clearAcceptedSubmission) clearReferenceSolutionState();
    else {
      setEditorDocument("learner");
      if (referenceSolutionAbortRef.current) {
        referenceSolutionGenerationRef.current += 1;
        referenceSolutionAbortRef.current.abort();
        referenceSolutionAbortRef.current = null;
        setReferenceSolutionLoading(false);
      }
    }
    workflowBusyRef.current = true;
    const generation = workflowGenerationRef.current + 1;
    workflowGenerationRef.current = generation;
    const exerciseId = selected;
    const language = selectedLanguage;
    const dialect = language === "sql" ? sqlDialect : undefined;
    selectedRef.current = exerciseId;
    setCelebration(null);
    setWorkflowBusy(true);
    return { generation, exerciseId, language, dialect };
  }
  function workflowIsCurrent(workflow: {
    generation: number;
    exerciseId: string;
    language: PracticeLanguage;
    dialect?: SqlDialect;
  }) {
    return (
      workflowGenerationRef.current === workflow.generation &&
      selectedRef.current === workflow.exerciseId &&
      selectedLanguage === workflow.language &&
      (workflow.language !== "sql" || sqlDialect === workflow.dialect)
    );
  }
  async function runCode() {
    const workflow = startWorkflow();
    if (!workflow) return;
    setStatus("Running…");
    setTab("Console");
    try {
      const response = await fetch("/api/run", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code,
          input: stdin,
          language: workflow.language,
          sql_dialect: workflow.dialect,
          exercise_id: workflow.exerciseId,
        }),
      });
      const result = await response.json();
      if (!workflowIsCurrent(workflow)) return;
      setRunResult(result);
      if (!result.ok) showMascotSurprised();
      setStatus(
        result.ok
          ? `Completed · ${result.duration_ms ?? 0}ms`
          : result.timed_out
            ? "Execution timed out"
            : "Run finished with errors",
      );
    } catch {
      if (!workflowIsCurrent(workflow)) return;
      setRunResult({
        error:
          "The local runner is unavailable. Start KitCode with launch.bat.",
      });
      setStatus("Runner unavailable");
    } finally {
      if (workflowIsCurrent(workflow)) {
        workflowBusyRef.current = false;
        setWorkflowBusy(false);
      }
    }
  }
  async function runTrace() {
    if (selectedLanguage !== "python") {
      setStatus(
        `Line trace is currently available for Python; ${activeLanguage.label} can still run and submit.`,
      );
      return;
    }
    const workflow = startWorkflow();
    if (!workflow) return;
    setStatus("Building trace…");
    setTab("Trace");
    try {
      const response = await fetch("/api/trace", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code,
          input: stdin,
          max_steps: 200,
          language: selectedLanguage,
          exercise_id: workflow.exerciseId,
        }),
      });
      const result = await response.json();
      if (!workflowIsCurrent(workflow)) return;
      setRunResult(result);
      setTraceSteps(result.steps ?? []);
      setTraceIndex(0);
      if (!result.ok) showMascotSurprised();
      setStatus(
        result.ok
          ? `${(result.steps ?? []).length} execution steps captured`
          : "Trace could not run",
      );
    } catch {
      if (!workflowIsCurrent(workflow)) return;
      setRunResult({ error: "The trace service is unavailable." });
      setStatus("Trace unavailable");
    } finally {
      if (workflowIsCurrent(workflow)) {
        workflowBusyRef.current = false;
        setWorkflowBusy(false);
      }
    }
  }
  function celebrateSuccess(workflow: { generation: number }) {
    if (
      !celebrationsEnabledRef.current ||
      celebratedWorkflowRef.current === workflow.generation
    )
      return;
    celebratedWorkflowRef.current = workflow.generation;
    const variants: CelebrationVariant[] = ["confetti", "sparks", "stars"];
    const id = ++celebrationSequenceRef.current;
    setCelebration({ variant: variants[(id - 1) % variants.length], id });
  }
  function setCelebrationPreference(enabled: boolean) {
    celebrationsEnabledRef.current = enabled;
    setCelebrationsEnabled(enabled);
    if (!enabled) setCelebration(null);
    try {
      window.localStorage.setItem(
        "kitcode:success-celebrations",
        enabled ? "on" : "off",
      );
    } catch {
      // The in-memory preference still works when browser storage is unavailable.
    }
  }
  function setInlineHintPreference(enabled: boolean) {
    setInlineHintsEnabled(enabled);
    try {
      window.localStorage.setItem(
        "kitcode:inline-hints",
        enabled ? "on" : "off",
      );
    } catch {
      // The in-memory preference still works when browser storage is unavailable.
    }
  }
  function setPythonAutocompletePreference(enabled: boolean) {
    pythonAutocompleteEnabledRef.current = enabled;
    setPythonAutocompleteEnabled(enabled);
    try {
      window.localStorage.setItem(
        "kitcode:python-autocomplete",
        enabled ? "on" : "off",
      );
    } catch {
      // The in-memory preference still works when browser storage is unavailable.
    }
  }
  function previewCelebration() {
    if (!celebrationsEnabledRef.current) return;
    const id = ++celebrationSequenceRef.current;
    const variants: CelebrationVariant[] = ["confetti", "sparks", "stars"];
    closeSettings();
    setCelebration({ variant: variants[(id - 1) % variants.length], id });
  }
  function setMascotPreference(enabled: boolean) {
    mascotEnabledRef.current = enabled;
    setMascotEnabled(enabled);
    if (!enabled) {
      mascotWakeRequiresClickRef.current = false;
      mascotLastActivityAtRef.current = Date.now();
      setMascotWindowInactive(false);
      if (mascotIdleTimerRef.current !== null)
        window.clearTimeout(mascotIdleTimerRef.current);
      if (mascotLessonSleepTimerRef.current !== null)
        window.clearTimeout(mascotLessonSleepTimerRef.current);
      mascotIdleTimerRef.current = null;
      mascotLessonSleepTimerRef.current = null;
      setMascotMoment(null);
      mascotSleepingRef.current = false;
      setMascotSleeping(false);
    }
    try {
      window.localStorage.setItem(
        "kitcode:mascot-enabled",
        enabled ? "on" : "off",
      );
    } catch {
      // The in-memory preference still works when browser storage is unavailable.
    }
  }
  function positionMascotFromPointer(clientX: number, clientY: number) {
    setMascotPosition(
      clampMascotPosition({
        x:
          ((clientX - mascotDragOffsetRef.current.x) / window.innerWidth) *
          100,
        y:
          ((clientY - mascotDragOffsetRef.current.y) / window.innerHeight) *
          100,
      }),
    );
  }
  function persistMascotPosition(position: MascotPosition) {
    try {
      window.localStorage.setItem(
        "kitcode:mascot-position-v1",
        JSON.stringify(position),
      );
    } catch {
      // Dragging remains available for this session when storage is unavailable.
    }
  }
  function showMascotComplete() {
    if (!mascotEnabledRef.current) return;
    resetMascotIdleRef.current();
    mascotSleepingRef.current = false;
    setMascotSleeping(false);
    setMascotMoment({
      id: ++mascotSequenceRef.current,
      motion: "complete",
    });
  }
  function showMascotHappy() {
    if (!mascotEnabledRef.current) return;
    resetMascotIdleRef.current();
    mascotSleepingRef.current = false;
    setMascotSleeping(false);
    setMascotMoment({
      id: ++mascotSequenceRef.current,
      motion: "happy",
    });
  }
  function showMascotSurprised() {
    if (!mascotEnabledRef.current) return;
    if (mascotLessonSleepTimerRef.current !== null)
      window.clearTimeout(mascotLessonSleepTimerRef.current);
    resetMascotIdleRef.current();
    mascotSleepingRef.current = false;
    setMascotSleeping(false);
    setMascotMoment({
      id: ++mascotSequenceRef.current,
      motion: "surprised",
    });
  }
  function showMascotLessonSleep() {
    if (!mascotEnabledRef.current) return;
    // Finishing a lesson is a fresh interaction, not an invitation to sleep.
    showMascotHappy();
    resetMascotIdleRef.current();
  }
  async function submitCode() {
    const workflow = startWorkflow(true);
    if (!workflow) return;
    setStatus("Submitting…");
    try {
      const response = await fetch("/api/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          code,
          exercise_id: workflow.exerciseId,
          language: workflow.language,
          sql_dialect: workflow.dialect,
        }),
      });
      const result: RunnerResult = await response.json();
      if (!workflowIsCurrent(workflow)) return;
      setRunResult(result);
      setTab("Tests");
      const accepted = acceptedResult(result);
      if (accepted) {
        setAcceptedSubmission({
          exerciseId: workflow.exerciseId,
          language: workflow.language,
          sqlDialect: workflow.dialect ?? "sqlite",
          code,
        });
        setProblems((all) =>
          all.map((item) =>
            item.id === workflow.exerciseId ? { ...item, solved: true } : item,
          ),
        );
        setGeneratedProblems((all) =>
          all.map((item) =>
            item.id === workflow.exerciseId ? { ...item, solved: true } : item,
          ),
        );
        celebrateSuccess(workflow);
        showMascotLessonSleep();
      } else {
        setCelebration(null);
        showMascotSurprised();
      }
      setStatus(
        accepted
          ? "Accepted · all tests passed"
          : (result.error ??
              result.message ??
              "Not accepted yet — review test feedback"),
      );
    } catch {
      if (!workflowIsCurrent(workflow)) return;
      setCelebration(null);
      setStatus("Submission service unavailable");
    } finally {
      if (workflowIsCurrent(workflow)) {
        workflowBusyRef.current = false;
        setWorkflowBusy(false);
      }
    }
  }
  function showLearnerSolution() {
    const preservedCode = learnerCodeBeforeReferenceRef.current;
    if (preservedCode !== null && preservedCode !== code)
      setCode(preservedCode);
    setEditorDocument("learner");
    setStatus("Your answer is active · the reviewed answer stays read-only");
  }
  function preserveLearnerSolution() {
    learnerCodeBeforeReferenceRef.current =
      editorRef.current?.getValue() ?? code;
  }
  function openBestSolution() {
    if (
      !referenceAnswerUnlocked ||
      current.source === "ai_generated" ||
      referenceSolutionLoading
    )
      return;
    if (referenceSolution?.exerciseId === selected) {
      preserveLearnerSolution();
      setEditorDocument("reference");
      setStatus("Best answer opened · your solution is unchanged");
      return;
    }
    void revealReferenceSolution();
  }
  async function revealReferenceSolution() {
    const snapshot = acceptedSubmission;
    if (
      !snapshot ||
      referenceSolutionLoading ||
      snapshot.exerciseId !== selectedRef.current
    )
      return;
    const generation = referenceSolutionGenerationRef.current + 1;
    referenceSolutionGenerationRef.current = generation;
    const controller = new AbortController();
    referenceSolutionAbortRef.current?.abort();
    referenceSolutionAbortRef.current = controller;
    setReferenceSolutionLoading(true);
    setReferenceSolutionError("");
    try {
      const response = await fetch(
        `/api/exercises/${encodeURIComponent(snapshot.exerciseId)}/reference-solution`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          signal: controller.signal,
          body: JSON.stringify({
            code: snapshot.code,
            language: snapshot.language,
            sql_dialect: snapshot.sqlDialect,
          }),
        },
      );
      const payload = (await response.json().catch(() => ({}))) as Record<
        string,
        unknown
      >;
      if (
        controller.signal.aborted ||
        generation !== referenceSolutionGenerationRef.current ||
        snapshot.exerciseId !== selectedRef.current
      )
        return;
      if (!response.ok)
        throw new Error(
          typeof payload.detail === "string"
            ? payload.detail
            : "The reference answer is unavailable right now.",
        );
      const language = payload.language;
      if (
        typeof payload.solution !== "string" ||
        !payload.solution.trim() ||
        payload.review_policy_id !== "kitcode-reference-best-v1" ||
        (language !== "python" && language !== "java" && language !== "sql") ||
        language !== snapshot.language ||
        payload.exercise_id !== snapshot.exerciseId
      )
        throw new Error("The reference answer could not be displayed safely.");
      setReferenceSolution({
        exerciseId: snapshot.exerciseId,
        language,
        solution: payload.solution,
        expectedComplexity: String(
          payload.expected_complexity ?? "Not specified",
        ),
        lineCount:
          typeof payload.line_count === "number" ? payload.line_count : 0,
        reviewPolicyId: payload.review_policy_id,
        selectionBasis: String(payload.selection_basis ?? ""),
        readabilityFocused: payload.readability_focused === true,
        readabilityNote: String(payload.readability_note ?? ""),
        referenceDialect:
          typeof payload.reference_dialect === "string"
            ? payload.reference_dialect
            : undefined,
        dialectNote:
          typeof payload.dialect_note === "string"
            ? payload.dialect_note
            : undefined,
        complexityNote:
          typeof payload.complexity_note === "string"
            ? payload.complexity_note
            : undefined,
      });
      preserveLearnerSolution();
      setEditorDocument("reference");
      setStatus("Best answer opened · your solution is unchanged");
    } catch (error) {
      if (
        controller.signal.aborted ||
        generation !== referenceSolutionGenerationRef.current
      )
        return;
      setReferenceSolutionError(
        error instanceof Error
          ? error.message
          : "The reference answer is unavailable right now.",
      );
      setStatus("Best answer unavailable · try again");
    } finally {
      if (generation === referenceSolutionGenerationRef.current) {
        if (referenceSolutionAbortRef.current === controller)
          referenceSolutionAbortRef.current = null;
        setReferenceSolutionLoading(false);
      }
    }
  }
  function buildCoachSnapshot(
    intent: CoachIntent,
    question: string,
  ): CoachRequestSnapshot {
    const editor = editorRef.current;
    const model = editor?.getModel();
    const position = editor?.getPosition();
    const history = messages
      .filter((message) => message.contextual)
      .slice(-8)
      .map((message) => ({
        role:
          message.role === "you" ? ("user" as const) : ("assistant" as const),
        content: message.text.slice(0, 1000),
      }));
    return {
      intent,
      question: question.slice(0, 4000),
      exerciseId: selectedRef.current || selected,
      providerIdentity: coachConsentIdentity(aiStatus),
      runtimeIdentity: coachRuntimeIdentity(aiStatus),
      expectedProvider: aiStatus.provider ?? "",
      expectedModel: aiStatus.model ?? null,
      expectedBaseUrl:
        aiStatus.provider === "local_llm"
          ? (aiStatus.local_llm_url ?? aiStatus.base_url ?? null)
          : null,
      code: model?.getValue() ?? code,
      modelVersion: model?.getVersionId() ?? 0,
      documentRevision: coachDocumentRevisionRef.current,
      cursorLine: position?.lineNumber ?? 1,
      cursorColumn: position?.column ?? 1,
      history,
      language: selectedLanguage,
      sqlDialect: selectedLanguage === "sql" ? sqlDialect : undefined,
    };
  }
  async function generateProblem() {
    if (generatingProblem || !aiStatus.configured) return;
    setGeneratingProblem(true);
    setGeneratedNotice("");
    try {
      const response = await fetch("/api/generated-exercises", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          language: selectedLanguage,
          difficulty: generatedDifficulty,
          topic: generatedTopic.trim() || undefined,
          expected_provider: aiStatus.provider,
          expected_model: aiStatus.model,
          expected_base_url: aiStatus.base_url ?? aiStatus.local_llm_url,
        }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok)
        throw new Error(payload.detail ?? "Could not create a practice drill.");
      const generated = normalizeProblem(
        payload.exercise ?? payload,
        generatedProblems.length,
      );
      const saved = { ...generated, source: "ai_generated" as const };
      setGeneratedProblems((all) => [
        saved,
        ...all.filter((item) => item.id !== saved.id),
      ]);
      setGeneratedNotice("New AI drill is ready below the curated bank.");
      selectExercise(saved.id);
      showMascotComplete();
    } catch (error) {
      setGeneratedNotice(
        error instanceof Error
          ? error.message
          : "Could not create a practice drill.",
      );
    } finally {
      setGeneratingProblem(false);
    }
  }
  async function deleteGeneratedProblem(exerciseId: string) {
    if (
      !window.confirm(
        "Remove this AI-made drill? Its saved draft, coach conversation, and generated completion progress will also be removed.",
      )
    )
      return;
    try {
      const response = await fetch(
        `/api/generated-exercises/${encodeURIComponent(exerciseId)}`,
        { method: "DELETE" },
      );
      if (!response.ok) throw new Error("Could not remove that AI drill.");
      setGeneratedProblems((all) =>
        all.filter((item) => item.id !== exerciseId),
      );
      try {
        clearPersistedDraft(
          window.localStorage,
          selectedLanguage,
          exerciseId,
        );
      } catch {
        /* The server removal remains complete when storage is unavailable. */
      }
      if (selectedRef.current === exerciseId)
        selectExercise(problems[0]?.id ?? "");
      try {
        // Selecting a replacement flushes the visible discussion first; clear
        // the deleted drill after that flush so it cannot be recreated.
        clearCoachConversationsForExercise(
          window.localStorage,
          selectedLanguage,
          exerciseId,
        );
      } catch {
        /* The server removal remains complete when storage is unavailable. */
      }
      setGeneratedNotice("AI drill removed.");
    } catch (error) {
      setGeneratedNotice(
        error instanceof Error
          ? error.message
          : "Could not remove that AI drill.",
      );
    }
  }
  const generatedDrillSettings = (
    <section
      className="generated-drill-settings"
      aria-labelledby="generated-drills-title"
    >
      <div>
        <p className="eyebrow">OPTIONAL · AI EXTENSION</p>
        <h3 id="generated-drills-title">Create an extra practice drill</h3>
        <p>
          AI-made and provisional: generated drills stay separate from the
          curated bank and completion total. Up to 2,000 saved drills are
          retained at once; delete any to keep creating without limit over time.
        </p>
      </div>
      {aiStatus.configured ? (
        <>
          <div className="generated-drill-fields">
            <label>
              Difficulty
              <select
                value={generatedDifficulty}
                onChange={(event) =>
                  setGeneratedDifficulty(
                    event.target.value as Problem["difficulty"],
                  )
                }
              >
                <option>Easy</option>
                <option>Medium</option>
                <option>Hard</option>
              </select>
            </label>
            <label>
              Topic{" "}
              <input
                value={generatedTopic}
                onChange={(event) => setGeneratedTopic(event.target.value)}
                maxLength={80}
                placeholder="Optional, e.g. sliding window"
              />
            </label>
          </div>
          <button
            type="button"
            className="generate-drill-button"
            onClick={() => void generateProblem()}
            disabled={generatingProblem}
          >
            {generatingProblem ? "Creating drill…" : "Create one AI drill"}
          </button>
          <p className="generated-provider-notice">
            Each click makes one external provider request to {selectedProvider}
            {aiStatus.model ? ` · ${aiStatus.model}` : ""}, may consume billed
            tokens (or local compute), and uses only your chosen language,
            difficulty, and topic—not editor code. No background generation or
            automatic retry occurs. AI-made content and tests can contain
            mistakes; review them critically.
          </p>
        </>
      ) : (
        <p className="generated-locked-notice">
          Configure an AI provider above to unlock optional generated drills.
          The curated bank is always available.
        </p>
      )}
      {generatedNotice && (
        <p className="generated-notice" role="status">
          {generatedNotice}
        </p>
      )}
    </section>
  );
  useEffect(() => {
    const onShortcut = (event: KeyboardEvent) => {
      const target = event.target instanceof Element ? event.target : null;
      const inMonaco = Boolean(target?.closest(".monaco-editor"));
      const inFormControl = Boolean(
        target?.closest(
          "input, textarea, select, button, [contenteditable='true']",
        ),
      );
      const plainF5 =
        event.key === "F5" &&
        !event.ctrlKey &&
        !event.metaKey &&
        !event.altKey &&
        !event.shiftKey;
      const plainF6 =
        event.key === "F6" &&
        !event.ctrlKey &&
        !event.metaKey &&
        !event.altKey &&
        !event.shiftKey;
      if (plainF5) {
        event.preventDefault();
        event.stopPropagation();
        if (
          settingsOpen ||
          coachConsentOpen ||
          codexInstallConfirmOpen ||
          event.repeat ||
          event.isComposing ||
          workflowBusyRef.current
        )
          return;
        runCode();
        return;
      }
      if (plainF6) {
        event.preventDefault();
        event.stopPropagation();
        if (
          settingsOpen ||
          coachConsentOpen ||
          codexInstallConfirmOpen ||
          event.repeat ||
          event.isComposing ||
          workflowBusyRef.current
        )
          return;
        submitCode();
        return;
      }
      if (
        settingsOpen ||
        coachConsentOpen ||
        codexInstallConfirmOpen ||
        event.repeat ||
        event.isComposing
      )
        return;
      if (inFormControl && !inMonaco) return;
      if ((event.ctrlKey || event.metaKey) && event.key === "Enter") {
        event.preventDefault();
        runCode();
      }
      if (
        (event.ctrlKey || event.metaKey) &&
        event.shiftKey &&
        event.key.toLowerCase() === "s"
      ) {
        event.preventDefault();
        submitCode();
      }
    };
    window.addEventListener("keydown", onShortcut, true);
    return () => window.removeEventListener("keydown", onShortcut, true);
  });
  function dispatchCoachAction(snapshot: CoachRequestSnapshot) {
    if (!hasCoachConsent(snapshot.providerIdentity)) {
      pendingCoachSnapshotRef.current = snapshot;
      setPendingCoachQuestion(snapshot.question);
      setPendingCoachProvider(snapshot.providerIdentity);
      setPendingCoachIntent(snapshot.intent);
      dialogRestoreRef.current = document.activeElement as HTMLElement | null;
      setCoachConsentOpen(true);
      return;
    }
    coachSubmitRef.current = false;
    void executeCoachAction(snapshot);
  }
  async function executeCoachAction(snapshot: CoachRequestSnapshot) {
    if (coachBusyRef.current || !coachResponseIsCurrent(snapshot)) {
      coachSubmitRef.current = false;
      return;
    }
    resetMascotIdleRef.current();
    coachBusyRef.current = true;
    coachActiveIntentRef.current = snapshot.intent;
    coachActiveSnapshotRef.current = snapshot;
    setActiveCoachIntent(snapshot.intent);
    coachSubmitRef.current = true;
    if (coachIntentSupportsRetry(snapshot.intent)) setRetryCoachSnapshot(null);
    setCoachBusy(true);
    const generation = coachGenerationRef.current + 1;
    coachGenerationRef.current = generation;
    const controller = new AbortController();
    coachAbortRef.current?.abort();
    coachAbortRef.current = controller;
    let streamedMessageId: string | null = null;
    const browserTimeout = window.setTimeout(() => {
      if (
        generation !== coachGenerationRef.current ||
        controller.signal.aborted
      )
        return;
      interruptActiveCoach(
        "The coach took too long to finish. Choose Try again to restart the same question.",
        "Coach timed out · Try again is ready.",
        true,
      );
    }, coachBrowserTimeoutMs);
    if (
      (snapshot.intent === "adaptive" || snapshot.intent === "edit") &&
      !snapshot.retry
    ) {
      const id = `message-${++messageSequenceRef.current}`;
      appendCoachMessage({
        id,
        role: "you",
        text: snapshot.question,
        contextual: true,
      });
    } else setHintNotice("Finding one useful next step…");
    try {
      const endpoint =
        snapshot.intent === "hint"
          ? "/api/ai/editor-hint"
          : snapshot.intent === "edit"
            ? "/api/ai/editor-edit"
            : "/api/ai/coach";
      const payload = {
        schema_version: 1,
        intent:
          snapshot.intent === "hint"
            ? "inline_hint"
            : snapshot.intent === "edit"
              ? "editor_edit"
              : "chat",
        question: snapshot.question,
        code: snapshot.code,
        mode:
          snapshot.intent === "hint"
            ? "editor_hint"
            : snapshot.intent === "edit"
              ? "editor_edit"
              : "adaptive",
        exercise_id: snapshot.exerciseId,
        language: snapshot.language,
        sql_dialect: snapshot.sqlDialect,
        expected_provider: snapshot.expectedProvider,
        expected_model: snapshot.expectedModel,
        expected_base_url: snapshot.expectedBaseUrl,
        cursor: { line: snapshot.cursorLine, column: snapshot.cursorColumn },
        history: snapshot.history,
      };
      const requestOptions: RequestInit = {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        signal: controller.signal,
        body: JSON.stringify(payload),
      };
      let result: Record<string, unknown> = {};
      if (snapshot.intent === "adaptive") {
        const stream = await fetch("/api/ai/coach/stream", requestOptions);
        // Continue to support already-packaged local backends during upgrades.
        if (stream.status === 404 || stream.status === 405 || !stream.body) {
          const response = await fetch(endpoint, requestOptions);
          result = (await response.json().catch(() => ({}))) as Record<string, unknown>;
          if (!response.ok)
            throw new Error(typeof result.detail === "string" ? result.detail : "The coach is unavailable right now.");
        } else {
          if (!stream.ok) {
            const error = (await stream.json().catch(() => ({}))) as Record<string, unknown>;
            throw new Error(typeof error.detail === "string" ? error.detail : "The coach is unavailable right now.");
          }
          const id = `message-${++messageSequenceRef.current}`;
          streamedMessageId = id;
          coachStreamingMessageRef.current = id;
          coachStreamTextRef.current = "";
          appendCoachMessage({ id, role: "coach", text: "", contextual: false });
          window.requestAnimationFrame(scrollCoachToLatestIfNearBottom);
          let completed = false;
          let provider = "";
          await readCoachStream(stream, (event) => {
            if (!coachSnapshotIsCurrent(snapshot, generation)) return;
            if (event.type === "meta" || event.type === "done") {
              provider = event.provider ?? provider;
              if (provider && provider !== snapshot.expectedProvider)
                throw new Error("The AI provider changed before this response completed. Please ask again.");
              if (event.type === "done") completed = true;
            } else if (event.type === "delta") {
              coachStreamTextRef.current += event.delta;
              queueStreamingCoachMessage(id);
            } else if (event.type === "error") throw new Error(event.message);
          }, () => coachSnapshotIsCurrent(snapshot, generation));
          if (!coachSnapshotIsCurrent(snapshot, generation)) return;
          if (!completed) throw new Error("The coach stream ended before the reply completed.");
          const reply = coachStreamTextRef.current.trim();
          if (!reply) throw new Error("The coach returned an empty reply. Please try again.");
          coachStreamTextRef.current = reply;
          flushStreamingCoachMessage(id, true);
          coachStreamingMessageRef.current = null;
          showMascotComplete();
          return;
        }
      } else {
        const response = await fetch(endpoint, requestOptions);
        result = (await response.json().catch(() => ({}))) as Record<string, unknown>;
        if (!response.ok)
          throw new Error(typeof result.detail === "string" ? result.detail : "The coach is unavailable right now.");
      }
      if (!coachResponseIsCurrent(snapshot, generation)) return;
      if (
        typeof result.provider === "string" &&
        result.provider !== snapshot.expectedProvider
      )
        throw new Error(
          "The AI provider changed before this response completed. Please ask again.",
        );
      if (snapshot.intent === "adaptive") {
        const reply = String(result.message ?? result.answer ?? "").trim();
        if (!reply)
          throw new Error(
            "The coach returned an empty reply. Please try again.",
          );
        const id = `message-${++messageSequenceRef.current}`;
        appendCoachMessage({ id, role: "coach", text: reply, contextual: true });
        showMascotComplete();
        return;
      }
      if (snapshot.intent === "edit") {
        const nextCode = typeof result.code === "string" ? result.code : "";
        const editMessage =
          typeof result.message === "string" ? result.message.trim() : "";
        const editor = editorRef.current;
        const model = editor?.getModel();
        if (
          result.structured !== true ||
          !nextCode ||
          !editMessage ||
          !editor ||
          !model
        )
          throw new Error("The coach could not provide a safe editor change.");
        const before = model.getValue();
        const { startLine, endLine, ranges } = changedLineRange(
          before,
          nextCode,
        );
        setPendingEditorEdit({
          id: ++editSequenceRef.current,
          startLine,
          endLine,
          ranges,
          before,
          after: nextCode,
          message: editMessage,
          undoAvailable: true,
        });
        appendCoachMessage({
          id: `message-${++messageSequenceRef.current}`,
          role: "coach",
          text: `${editMessage}\n\nI prepared a code change. Review the summary beside the editor, then choose Apply AI edit if you want it written into your script.`,
          contextual: true,
        });
        setStatus("AI edit ready · review and apply");
        showMascotComplete();
        return;
      }
      if (result.structured !== true) {
        setHintNotice(
          "The coach could not format a safe inline hint. Try again.",
        );
        return;
      }
      const hint = safeInlineHint(result.text ?? result.hint);
      const line = Number.isInteger(result.line)
        ? Number(result.line)
        : snapshot.cursorLine;
      if (!hint) {
        setHintNotice(
          "The coach could not provide a safe hint. Try again.",
        );
        return;
      }
      const model = editorRef.current?.getModel();
      const basedOnPriorDraft =
        coachDocumentRevisionRef.current !== snapshot.documentRevision;
      const inline = Boolean(
        !basedOnPriorDraft && model && line >= 1 && line <= model.getLineCount(),
      );
      setEditorHint({ id: ++hintSequenceRef.current, line, text: hint, inline });
      setHintNotice(
        basedOnPriorDraft ? "Hint shown below · based on your earlier draft." : "",
      );
      if (inline) editorRef.current?.revealLineInCenterIfOutsideViewport(line);
      showMascotComplete();
    } catch (error) {
      if (
        controller.signal.aborted ||
        !coachResponseIsCurrent(snapshot, generation)
      )
        return;
      const detail =
        error instanceof Error && error.message
          ? error.message
          : "The coach is unavailable right now.";
      if (snapshot.intent === "adaptive" || snapshot.intent === "edit") {
        if (streamedMessageId) {
          const partial = coachStreamTextRef.current.trim();
          coachStreamTextRef.current = partial
            ? `${partial}\n\n*Streaming stopped: ${detail}*`
            : detail;
          flushStreamingCoachMessage(streamedMessageId);
          coachStreamingMessageRef.current = null;
        } else {
          const id = `message-${++messageSequenceRef.current}`;
          appendCoachMessage({ id, role: "coach", text: detail, contextual: false });
        }
        if (snapshot.intent === "edit")
          setStatus("AI editor request failed · your code was not changed");
        if (coachIntentSupportsRetry(snapshot.intent)) {
          setRetryCoachSnapshot(snapshot);
          setHintNotice(
            snapshot.intent === "edit"
              ? "AI editor request failed · Try again is ready."
              : "Coach request failed · Try again is ready.",
          );
        }
      } else
        setHintNotice(
          "The hint service is unavailable. Your code was not changed.",
        );
    } finally {
      window.clearTimeout(browserTimeout);
      if (generation === coachGenerationRef.current) {
        if (coachAbortRef.current === controller) coachAbortRef.current = null;
        coachBusyRef.current = false;
        coachActiveIntentRef.current = null;
        coachActiveSnapshotRef.current = null;
        coachSubmitRef.current = false;
        setCoachBusy(false);
        setActiveCoachIntent(null);
      }
    }
  }
  function openSettings(trigger: HTMLElement) {
    const reportedProvider = aiStatus.provider;
    const provider: SetupProvider =
      reportedProvider === "anthropic" ||
      reportedProvider === "codex" ||
      reportedProvider === "openai" ||
      reportedProvider === "local_llm"
        ? reportedProvider
        : "codex";
    const reportedModel = aiStatus.model ?? "";
    const knownModels =
      provider === "openai" || provider === "anthropic"
        ? providerModels[provider].map((item) => item.value)
        : [];
    setSetupProvider(provider);
    setSetupModel(
      knownModels.includes(reportedModel)
        ? reportedModel
        : provider === "anthropic"
          ? "claude-sonnet-5"
          : provider === "openai"
            ? "gpt-5.6-terra"
            : reportedModel,
    );
    setSetupCustomModel(
      reportedModel && !knownModels.includes(reportedModel)
        ? reportedModel
        : "",
    );
    setSetupLocalUrl(
      aiStatus.local_llm_url ?? aiStatus.base_url ?? "http://127.0.0.1:5000/",
    );
    setSetupKey("");
    setSetupNotice("");
    setCodexDetection(null);
    setCodexActionResult(null);
    setCodexInstallConfirmOpen(false);
    setCodexLoginPolling(false);
    setLocalLlmDetection(null);
    dialogRestoreRef.current = trigger;
    setSettingsOpen(true);
  }
  function closeSettings() {
    setCodexInstallConfirmOpen(false);
    setCodexLoginPolling(false);
    setSettingsOpen(false);
  }
  function chooseSetupProvider(provider: SetupProvider) {
    setSetupProvider(provider);
    if (provider !== "codex") setCodexLoginPolling(false);
    setSetupNotice("");
    setSetupKey("");
    setSetupCustomModel("");
    setSetupModel(
      provider === "anthropic"
        ? "claude-sonnet-5"
        : provider === "openai"
          ? "gpt-5.6-terra"
          : "",
    );
  }
  async function saveAiSetup(event: FormEvent) {
    event.preventDefault();
    const model = setupCustomModel.trim() || setupModel.trim() || undefined;
    const providerConfigured =
      setupProvider === "openai"
        ? aiStatus.openai_configured
        : setupProvider === "anthropic"
          ? aiStatus.anthropic_configured
          : true;
    if (
      (setupProvider === "openai" || setupProvider === "anthropic") &&
      !setupKey.trim() &&
      !providerConfigured
    ) {
      setSetupNotice("Enter an API key before saving this provider.");
      return;
    }
    setSetupSaving(true);
    setSetupNotice("");
    try {
      const response = await fetch("/api/ai/configure", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          provider: setupProvider,
          model: setupProvider === "codex" ? undefined : model,
          api_key:
            setupProvider === "openai" || setupProvider === "anthropic"
              ? setupKey.trim() || undefined
              : undefined,
          base_url:
            setupProvider === "local_llm" ? setupLocalUrl.trim() : undefined,
        }),
      });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok)
        throw new Error(
          payload.detail ??
            "The local setup service could not save this provider.",
        );
      setSetupKey("");
      setSetupNotice(
        setupProvider === "codex"
          ? "Codex preference saved. The local CLI will be checked before coaching."
          : setupProvider === "local_llm"
            ? "Local LLM saved. KitCode will send coach requests to this endpoint."
            : "Provider saved locally. Your key is cleared from this browser and is never displayed again.",
      );
      await refreshAiStatus();
    } catch (error) {
      setSetupNotice(
        error instanceof Error
          ? error.message
          : "The local setup service is unavailable.",
      );
    } finally {
      setSetupSaving(false);
    }
  }
  async function clearAiSetup() {
    setSetupSaving(true);
    setSetupNotice("");
    try {
      const response = await fetch("/api/ai/configure", { method: "DELETE" });
      const payload = await response.json().catch(() => ({}));
      if (!response.ok)
        throw new Error(
          payload.detail ??
            "Removing saved AI configuration is not available in this version.",
        );
      setSetupKey("");
      setSetupNotice(
        "All saved AI provider configuration was removed from this app.",
      );
      await refreshAiStatus();
    } catch (error) {
      setSetupNotice(
        error instanceof Error
          ? error.message
          : "The local setup service is unavailable.",
      );
    } finally {
      setSetupSaving(false);
    }
  }
  async function detectCodex(force = false) {
    if (codexDetecting || (codexLoginPolling && !force)) return;
    setSetupProvider("codex");
    setCodexDetecting(true);
    setCodexDetection(null);
    setSetupNotice("");
    try {
      const response = await fetch("/api/ai/detect-codex", { method: "POST" });
      const payload: CodexDetection = await response.json().catch(() => ({}));
      if (!response.ok)
        throw new Error(
          payload.detail ?? "Codex detection could not complete.",
        );
      setCodexDetection(payload);
      if (payload.ready) {
        setSetupNotice(
          "Codex connected and was selected automatically. No API key was copied into KitCode.",
        );
        await refreshAiStatus();
      }
    } catch (error) {
      setCodexDetection({
        detail:
          error instanceof Error
            ? error.message
            : "The local detection service is unavailable.",
        action: "Start KitCode with launch.bat, then try Detect Codex again.",
      });
    } finally {
      setCodexDetecting(false);
    }
  }
  async function installCodex() {
    if (codexInstalling) return;
    setCodexInstallConfirmOpen(false);
    setCodexInstalling(true);
    setCodexActionResult(null);
    setSetupNotice(
      "Downloading and starting the official Codex CLI installer…",
    );
    try {
      const response = await fetch("/api/ai/install-codex", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ confirmed: true }),
      });
      const payload: CodexActionResult = await response
        .json()
        .catch(() => ({}));
      if (!response.ok || payload.ok !== true)
        throw new Error(
          payload.detail ?? "The Codex CLI installer could not start.",
        );
      setCodexActionResult(payload);
      if (payload.status) setCodexDetection(payload.status);
      setSetupNotice(
        payload.detail ??
          "Codex CLI was installed. Continue with ChatGPT sign-in.",
      );
      await detectCodex();
    } catch (error) {
      setCodexActionResult({
        detail:
          error instanceof Error
            ? error.message
            : "The local installer service is unavailable.",
      });
      setSetupNotice("Codex CLI installation could not start.");
    } finally {
      setCodexInstalling(false);
    }
  }
  async function startCodexLogin() {
    if (codexLoginStarting || codexLoginPolling) return;
    setCodexLoginStarting(true);
    setCodexActionResult(null);
    setSetupNotice(
      "Opening the official ChatGPT sign-in outside KitCode…",
    );
    try {
      const response = await fetch("/api/ai/start-codex-login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ confirmed: true }),
      });
      const payload: CodexActionResult = await response
        .json()
        .catch(() => ({}));
      if (!response.ok || payload.action !== "login_started")
        throw new Error(payload.detail ?? "The Codex sign-in could not start.");
      setCodexActionResult(payload);
      setSetupNotice(
        "Finish the official ChatGPT sign-in in the window that opened. KitCode is checking automatically…",
      );
      setCodexLoginPolling(true);
    } catch (error) {
      setCodexActionResult({
        detail:
          error instanceof Error
            ? error.message
            : "The local sign-in service is unavailable.",
      });
      setSetupNotice("Codex sign-in could not start.");
    } finally {
      setCodexLoginStarting(false);
    }
  }
  async function detectLocalLlm() {
    if (localLlmDetecting) return;
    setSetupProvider("local_llm");
    setLocalLlmDetecting(true);
    setLocalLlmDetection(null);
    setSetupNotice("");
    try {
      const response = await fetch("/api/ai/detect-local-llm", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          base_url: setupLocalUrl.trim(),
          model: setupCustomModel.trim() || setupModel.trim() || undefined,
        }),
      });
      const payload: LocalLlmDetection = await response
        .json()
        .catch(() => ({}));
      if (!response.ok)
        throw new Error(
          payload.detail ?? "Local LLM detection could not complete.",
        );
      setLocalLlmDetection(payload);
      if (payload.reachable) {
        if (payload.base_url) setSetupLocalUrl(payload.base_url);
        if (payload.selected_model) {
          setSetupModel(payload.selected_model);
          setSetupCustomModel("");
        }
        setSetupNotice(
          payload.selected_model
            ? "Local server detected and selected. KitCode will try the model when you ask for coaching."
            : "Local server detected. Enter its model ID, then save the settings.",
        );
        if (payload.selected_model) await refreshAiStatus();
      }
    } catch (error) {
      setLocalLlmDetection({
        detail:
          error instanceof Error
            ? error.message
            : "The local detection service is unavailable.",
      });
    } finally {
      setLocalLlmDetecting(false);
    }
  }
  function closeCoachConsent() {
    const pending = pendingCoachSnapshotRef.current;
    if (pending?.intent === "adaptive")
      setCoachInput((currentValue) => currentValue || pending.question);
    pendingCoachSnapshotRef.current = null;
    coachSubmitRef.current = false;
    setCoachConsentOpen(false);
    setPendingCoachQuestion("");
    setPendingCoachProvider("");
    setPendingCoachIntent("adaptive");
  }
  function submitCoachQuestion() {
    const question = coachInput.trim();
    if (
      !question ||
      coachBusyRef.current ||
      !coachReady ||
      coachSubmitRef.current
    )
      return;
    coachSubmitRef.current = true;
    const snapshot = buildCoachSnapshot(
      requestsEditorEdit(question) ? "edit" : "adaptive",
      question,
    );
    setCoachInput("");
    dispatchCoachAction(snapshot);
  }
  function requestHint() {
    if (coachBusyRef.current || !coachReady || coachSubmitRef.current) return;
    coachSubmitRef.current = true;
    const snapshot = buildCoachSnapshot(
      "hint",
      "Give one concise next-step hint for the current code at the cursor. Do not provide the full solution.",
    );
    dispatchCoachAction(snapshot);
  }
  function restartCoachResponse() {
    const snapshot = coachActiveSnapshotRef.current;
    if (
      !snapshot ||
      snapshot.intent !== "adaptive" ||
      !coachReady ||
      !coachSnapshotIsCurrent(snapshot)
    ) {
      stopCoachResponse();
      return;
    }
    const retry = interruptActiveCoach(
      "Response interrupted so it could be restarted.",
      "Restarting the same question…",
      true,
    );
    if (!retry) return;
    setCoachRestarting(true);
    coachSubmitRef.current = true;
    coachRestartTimerRef.current = window.setTimeout(() => {
      coachRestartTimerRef.current = null;
      setCoachRestarting(false);
      coachSubmitRef.current = false;
      if (
        !aiStatusRef.current.configured ||
        !coachSnapshotIsCurrent(retry)
      ) {
        setRetryCoachSnapshot(null);
        setHintNotice(
          "The drill, code, or AI provider changed. Please ask again.",
        );
        return;
      }
      coachSubmitRef.current = true;
      dispatchCoachAction({ ...retry, retry: true });
    }, coachRestartDelayMs);
  }
  function cancelCoachRestart() {
    if (coachRestartTimerRef.current === null) return;
    window.clearTimeout(coachRestartTimerRef.current);
    coachRestartTimerRef.current = null;
    coachSubmitRef.current = false;
    setCoachRestarting(false);
    setHintNotice("Coach restart cancelled · Try again when you are ready.");
  }
  function rebaseCoachRetry(
    snapshot: CoachRequestSnapshot,
  ): CoachRequestSnapshot {
    const editor = editorRef.current;
    const model = editor?.getModel();
    const position = editor?.getPosition();
    return {
      ...snapshot,
      retry: true,
      code: model?.getValue() ?? code,
      modelVersion: model?.getVersionId() ?? 0,
      documentRevision: coachDocumentRevisionRef.current,
      cursorLine: position?.lineNumber ?? snapshot.cursorLine,
      cursorColumn: position?.column ?? snapshot.cursorColumn,
    };
  }
  function retryCoachQuestion() {
    const snapshot = retryCoachSnapshot;
    if (
      !snapshot ||
      coachBusyRef.current ||
      coachRestarting ||
      !coachReady ||
      !coachSnapshotMatchesScope(snapshot)
    ) {
      setRetryCoachSnapshot(null);
      setHintNotice(
        "The drill or AI provider changed. Please ask the coach again.",
      );
      return;
    }
    coachSubmitRef.current = true;
    dispatchCoachAction(rebaseCoachRetry(snapshot));
  }
  function askCoach(event: FormEvent) {
    event.preventDefault();
    submitCoachQuestion();
  }
  function handleCoachKeyDown(event: ReactKeyboardEvent<HTMLTextAreaElement>) {
    if (
      event.key !== "Enter" ||
      event.shiftKey ||
      event.repeat ||
      event.nativeEvent.isComposing
    )
      return;
    event.preventDefault();
    submitCoachQuestion();
  }
  function acceptCoachConsent() {
    const snapshot = pendingCoachSnapshotRef.current;
    if (!snapshot || !coachReady || !coachSnapshotIsCurrent(snapshot)) {
      closeCoachConsent();
      setHintNotice(
        "The drill, code, or AI provider changed. Please ask again.",
      );
      return;
    }
    rememberCoachConsent(snapshot.providerIdentity);
    consentFocusTargetRef.current =
      snapshot.intent === "hint" ? "editor" : "coach";
    pendingCoachSnapshotRef.current = null;
    setCoachConsentOpen(false);
    setPendingCoachQuestion("");
    setPendingCoachProvider("");
    setPendingCoachIntent("adaptive");
    coachSubmitRef.current = false;
    void executeCoachAction(snapshot);
  }
  const codexGuidedActions =
    setupProvider === "codex" && codexDetection && !codexDetection.ready ? (
      <div
        className="codex-guided-actions"
        role="region"
        aria-label="Codex CLI setup actions"
      >
        {codexDetection.cli_detected === false ||
        codexDetection.cli_usable === false ? (
          <>
            <strong>
              {codexDetection.cli_detected
                ? "Repair the Codex CLI"
                : "Install the Codex CLI"}
            </strong>
            <p>
              {codexDetection.detail ??
                (codexDetection.cli_detected
                  ? "Install the standalone CLI to repair this connection."
                  : "Install the Codex CLI, then sign in with ChatGPT.")}
            </p>
            <button
              type="button"
              className="detect-codex-button"
              onClick={(event) => {
                codexInstallRestoreRef.current = event.currentTarget;
                setCodexInstallConfirmOpen(true);
              }}
              disabled={
                codexInstalling || codexLoginStarting || codexLoginPolling
              }
            >
              {codexInstalling
                ? "Installing Codex CLI…"
                : codexDetection.cli_detected
                  ? "Install / repair Codex CLI"
                  : "Install Codex CLI"}
            </button>
          </>
        ) : codexDetection.cli_usable === true &&
          codexDetection.authenticated === false ? (
          <>
            <strong>Sign in to Codex CLI</strong>
            <p>
              {codexDetection.detail ??
                "This opens official ChatGPT sign-in outside KitCode. KitCode never sees your password or tokens."}
            </p>
            <button
              type="button"
              className="detect-codex-button"
              onClick={() => void startCodexLogin()}
              disabled={
                codexInstalling || codexLoginStarting || codexLoginPolling
              }
            >
              {codexLoginStarting
                ? "Opening sign-in…"
                : codexLoginPolling
                  ? "Waiting for ChatGPT sign-in…"
                  : "Open ChatGPT sign-in"}
            </button>
          </>
        ) : (
          <>
            <strong>Recheck Codex</strong>
            <p>
              {codexDetection.detail ??
                "Finish the indicated CLI step, then recheck readiness."}
            </p>
            <button
              type="button"
              className="text-button codex-recheck"
              onClick={() => {
                setCodexLoginPolling(false);
                void detectCodex(true);
              }}
              disabled={
                codexDetecting || codexInstalling || codexLoginStarting
              }
            >
              {codexDetecting ? "Rechecking…" : "Recheck Codex"}
            </button>
          </>
        )}
        {codexActionResult && (
          <p className="codex-action-result" role="status">
            {codexActionResult.detail ??
              codexActionResult.action ??
              "Codex setup action completed."}
          </p>
        )}
      </div>
    ) : null;
  const coachMascotMotion: MascotMotion = mascotWindowInactive
    ? "sleeping"
    : mascotMoment?.motion === "waking"
      ? "waking"
      : coachBusy
        ? "hunting"
        : mascotMoment?.motion ?? (mascotSleeping ? "sleeping" : "idle");
  return (
    <main className={`shell${interviewActive ? " fundamentals-mode" : ""}`}>
      {celebration && (
        <SuccessCelebration
          key={celebration.id}
          variant={celebration.variant}
        />
      )}
      {mascotEnabled && !settingsOpen && !interviewActive && (
        <div
          className={`kit-floating${mascotDragging ? " is-dragging" : ""}`}
          style={{
            left: `${mascotPosition.x}%`,
            top: `${mascotPosition.y}%`,
          }}
          role="button"
          tabIndex={0}
          aria-label={
            coachReady && !coachBusy
              ? "Ask Kit for a hint or drag Kit to reposition"
              : "Drag Kit to reposition. Hints are available when AI coaching is ready"
          }
          title={
            coachReady && !coachBusy
              ? "Click Kit for a hint, or drag him anywhere"
              : "Drag Kit anywhere · connect AI coaching to ask for hints"
          }
          onPointerDown={(event) => {
            if (event.button !== 0 || !event.isPrimary) return;
            const bounds = event.currentTarget.getBoundingClientRect();
            mascotDragOffsetRef.current = {
              x: event.clientX - (bounds.left + bounds.width / 2),
              y: event.clientY - (bounds.top + bounds.height / 2),
            };
            mascotDragStartRef.current = {
              pointerId: event.pointerId,
              x: event.clientX,
              y: event.clientY,
              moved: false,
            };
            event.currentTarget.setPointerCapture(event.pointerId);
            event.currentTarget.focus({ preventScroll: true });
            event.preventDefault();
          }}
          onPointerMove={(event) => {
            const drag = mascotDragStartRef.current;
            if (!drag || drag.pointerId !== event.pointerId) return;
            if (!drag.moved) {
              const distance = Math.hypot(
                event.clientX - drag.x,
                event.clientY - drag.y,
              );
              if (distance < mascotDragThreshold) return;
              drag.moved = true;
              setMascotDragging(true);
            }
            positionMascotFromPointer(event.clientX, event.clientY);
          }}
          onPointerUp={(event) => {
            const drag = mascotDragStartRef.current;
            if (!drag || drag.pointerId !== event.pointerId) return;
            const wasDragging =
              drag.moved ||
              Math.hypot(event.clientX - drag.x, event.clientY - drag.y) >=
                mascotDragThreshold;
            mascotDragStartRef.current = null;
            setMascotDragging(false);
            if (event.currentTarget.hasPointerCapture(event.pointerId))
              event.currentTarget.releasePointerCapture(event.pointerId);
            if (wasDragging) {
              positionMascotFromPointer(event.clientX, event.clientY);
              const position = clampMascotPosition({
                x:
                  ((event.clientX - mascotDragOffsetRef.current.x) /
                    window.innerWidth) *
                  100,
                y:
                  ((event.clientY - mascotDragOffsetRef.current.y) /
                    window.innerHeight) *
                  100,
              });
              persistMascotPosition(position);
            } else {
              requestHint();
            }
          }}
          onPointerCancel={(event) => {
            const drag = mascotDragStartRef.current;
            if (!drag || drag.pointerId !== event.pointerId) return;
            mascotDragStartRef.current = null;
            setMascotDragging(false);
            if (event.currentTarget.hasPointerCapture(event.pointerId))
              event.currentTarget.releasePointerCapture(event.pointerId);
          }}
          onKeyDown={(event) => {
            if (event.key === "Enter" || event.key === " ") {
              event.preventDefault();
              requestHint();
              return;
            }
            const movement = event.shiftKey ? 5 : 2;
            const delta =
              event.key === "ArrowLeft"
                ? { x: -movement, y: 0 }
                : event.key === "ArrowRight"
                  ? { x: movement, y: 0 }
                  : event.key === "ArrowUp"
                    ? { x: 0, y: -movement }
                    : event.key === "ArrowDown"
                      ? { x: 0, y: movement }
                      : null;
            if (!delta) return;
            event.preventDefault();
            const next = clampMascotPosition({
              x: mascotPosition.x + delta.x,
              y: mascotPosition.y + delta.y,
            });
            setMascotPosition(next);
            persistMascotPosition(next);
          }}
        >
          <KitMascot
            key={
              coachBusy
                ? "kit-hunting"
                : mascotMoment
                  ? `kit-${mascotMoment.motion}-${mascotMoment.id}`
                  : `kit-${coachMascotMotion}`
            }
            size="floating"
            motion={coachMascotMotion}
          />
        </div>
      )}
      <aside className="activity-rail" aria-label="Workspace navigation">
        <div className="brand" aria-label="KitCode">
          <span className="brand-wordmark">
            <b>Kit</b>
            <span>Code</span>
          </span>
        </div>
        <div
          className="language-rail"
          role="group"
          aria-label="Practice area"
        >
          {languages.map((language) => (
            <button
              key={language.id}
              type="button"
              className={
                selectedPracticeArea === language.id
                  ? "rail-button language-button active"
                  : "rail-button language-button"
              }
              onClick={() => selectLanguage(language.id)}
              aria-label={`Switch to ${language.label} practice`}
              aria-pressed={selectedPracticeArea === language.id}
              title={`Switch to ${language.label}`}
            >
              <span aria-hidden="true">{language.short}</span>
              <span className="sr-only">{language.label}</span>
            </button>
          ))}
          <button
            type="button"
            className={
              machineLearningActive
                ? "rail-button language-button active"
                : "rail-button language-button"
            }
            onClick={selectMachineLearning}
            aria-label="Switch to Machine Learning interview FAQs"
            aria-pressed={machineLearningActive}
            title="Machine Learning interview FAQs"
          >
            <span aria-hidden="true">ML</span>
            <span className="sr-only">Machine Learning</span>
          </button>
        </div>
        <div className="rail-divider" aria-hidden="true" />
        <button
          className="rail-button"
          onClick={() => setProblemDrawerOpen(true)}
          aria-label="Open practice problems"
          aria-expanded={problemDrawerOpen}
          title="Open practice problems"
        >
          <Icon label="Practice problems">⌘</Icon>
        </button>
        <button
          className="rail-button coach-rail-button"
          onClick={() => setCoachDrawerOpen(true)}
          aria-label="Open AI coach"
          aria-expanded={coachDrawerOpen}
          title="Open AI coach"
        >
          <Icon label="AI coach">✦</Icon>
        </button>
        <div className="rail-bottom">
          <button
            className="rail-button"
            onClick={(event) => openSettings(event.currentTarget)}
            aria-label="Settings"
            title="Settings"
          >
            <Icon label="Settings">⚙</Icon>
          </button>
          <div className="avatar" aria-label="Local learner profile">
            AJ
          </div>
        </div>
      </aside>
      {(problemDrawerOpen || coachDrawerOpen) && (
        <button
          className={`drawer-backdrop ${coachDrawerOpen ? "coach-drawer-backdrop" : ""}`}
          aria-label="Close open panel"
          onClick={() => {
            setProblemDrawerOpen(false);
            setCoachDrawerOpen(false);
          }}
        />
      )}
      <aside
        className={`problem-bank ${problemDrawerOpen ? "drawer-open" : ""}`}
        aria-label="Practice navigator"
      >
        <div className="bank-heading">
          <div>
            <p className="eyebrow">
              KITCODE · {machineLearningActive
                ? "MACHINE LEARNING"
                : activeLanguage.label.toUpperCase()}
            </p>
            <h1>
              {machineLearningActive
                ? "Machine Learning Practice"
                : `${activeLanguage.label} Practice`}
            </h1>
          </div>
          <button
            className="drawer-close"
            onClick={() => setProblemDrawerOpen(false)}
            aria-label="Close practice problems"
          >
            ×
          </button>
        </div>
        {!machineLearningActive && (
          <div
            className="practice-section-picker"
            role="group"
            aria-label={`${activeLanguage.label} practice section`}
          >
            <button
              type="button"
              className={!interviewActive ? "active" : ""}
              aria-pressed={!interviewActive}
              onClick={() => choosePracticeSection("coding")}
            >
              Coding drills
              <small>Write and run {activeLanguage.label}</small>
            </button>
            <button
              type="button"
              className={interviewActive ? "active" : ""}
              aria-pressed={interviewActive}
              onClick={() => choosePracticeSection("interview")}
            >
              Interview FAQs
              <small>Core multiple choice</small>
            </button>
          </div>
        )}
        {interviewActive ? (
          <div className="fundamentals-bank-summary">
            <div>
              <p className="eyebrow">INTERVIEW PREP</p>
              <h2>
                {machineLearningActive
                  ? "Machine Learning concept FAQs"
                  : `${activeLanguage.label} interview question bank`}
              </h2>
            </div>
            <div className="fundamentals-bank-stat">
              <b>FAQ</b>
              <span>
                {machineLearningActive
                  ? "Core questions covering linear models, optimization, regularization, trees, evaluation, neural networks, and transformers."
                  : `Common ${activeLanguage.label} questions with answer explanations and topic filters.`}
              </span>
            </div>
            <p>
              <strong>Optional and separate:</strong> quiz answers are saved
              locally and never change your coding-drill completion.
            </p>
            <button
              type="button"
              onClick={() => choosePracticeSection("coding")}
            >
              Return to {activeLanguage.label} coding
            </button>
          </div>
        ) : (
          <>
        <section className="level-picker" aria-labelledby="level-picker-title">
          <div className="level-picker-heading">
            <strong id="level-picker-title">Choose a practice level</strong>
            <small>Your choice is remembered</small>
          </div>
          <div className="level-cards" role="radiogroup" aria-label="Practice level">
            {practiceLevels.map((level) => (
              <button
                key={level.id}
                type="button"
                role="radio"
                aria-checked={difficulty === level.id}
                onClick={() => choosePracticeLevel(level.id)}
                className={`level-card ${level.id.toLowerCase()} ${difficulty === level.id ? "active" : ""}`}
              >
                <span><strong>{level.label}</strong><small>{level.id}</small></span>
                <b>{levelCounts[level.id]}</b>
                <em>{levelSolved[level.id]} solved</em>
                <p>{level.description}</p>
              </button>
            ))}
          </div>
        </section>
        <div className="bank-tools">
          <label className="search">
            <span>⌕</span>
            <input
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder={`Search ${difficulty.toLowerCase()} drills`}
              aria-label={`Search ${difficulty} ${activeLanguage.label} drills`}
            />
          </label>
          <label className="topic-filter">
            <span className="sr-only">Filter by topic</span>
            <select
              value={availableTopics.includes(topicFilter) ? topicFilter : "All topics"}
              onChange={(event) => setTopicFilter(event.target.value)}
              aria-label="Filter drills by topic"
            >
              <option>All topics</option>
              {availableTopics.map((topic) => <option key={topic}>{topic}</option>)}
            </select>
          </label>
        </div>
        <div className="problem-count">
          <span>
            {visible.length} {difficulty.toLowerCase()} {activeLanguage.label} drills
          </span>
          <span>{levelSolved[difficulty]}/{levelCounts[difficulty]} solved</span>
        </div>
        <nav
          className="problem-list"
          aria-label={`${difficulty} ${activeLanguage.label} curated drills`}
        >
          {visible.map((item) => (
            <button
              key={item.id}
              className={item.id === selected ? "problem selected" : "problem"}
              onClick={() => {
                selectExercise(item.id);
                setProblemDrawerOpen(false);
              }}
            >
              <span className={item.solved ? "check solved" : "check"}>
                {item.solved ? "✓" : ""}
              </span>
              <span className="problem-copy">
                <strong>{item.title}</strong>
                <small>{item.topic}</small>
              </span>
              <span className={`difficulty ${item.difficulty.toLowerCase()}`}>
                {item.difficulty}
              </span>
            </button>
          ))}
          {visibleGenerated.length > 0 && (
            <section
              className="generated-bank-section"
              aria-label={`${activeLanguage.label} AI-generated drills`}
            >
              <div className="generated-bank-heading">
                <span>AI-generated extras</span>
                <small>
                  {visibleGeneratedSolved}/{visibleGenerated.length} completed in this level
                </small>
              </div>
              {visibleGenerated.map((item) => (
                <div className="generated-problem-row" key={item.id}>
                  <button
                    className={
                      item.id === selected ? "problem selected" : "problem"
                    }
                    onClick={() => {
                      selectExercise(item.id);
                      setProblemDrawerOpen(false);
                    }}
                  >
                    <span className={item.solved ? "check solved" : "check"}>
                      {item.solved ? "✓" : ""}
                    </span>
                    <span className="problem-copy">
                      <strong>{item.title}</strong>
                      <small>{item.topic}</small>
                    </span>
                    <span className="ai-generated-badge">AI</span>
                    <span
                      className={`difficulty ${item.difficulty.toLowerCase()}`}
                    >
                      {item.difficulty}
                    </span>
                  </button>
                  <button
                    type="button"
                    className="delete-generated-button"
                    onClick={() => void deleteGeneratedProblem(item.id)}
                    aria-label={`Remove AI-generated drill ${item.title}`}
                    title="Remove AI drill"
                  >
                    ×
                  </button>
                </div>
              ))}
            </section>
          )}
        </nav>
        <div className="bank-footer">
          <span>{solved} curated completed</span>
          <span>
            {problems.length} {activeLanguage.label}
            {catalogTotal ? ` · ${catalogTotal} overall` : ""}
          </span>
        </div>
          </>
        )}
      </aside>
      <section className="workspace">
        {interviewActive && interviewSubject ? (
          <InterviewQuiz
            key={interviewSubject}
            subject={interviewSubject}
            clock={clock}
            onReturnToCoding={() => choosePracticeSection("coding")}
            returnLabel={
              machineLearningActive
                ? `Return to ${activeLanguage.label} coding`
                : "Return to coding"
            }
          />
        ) : (
          <>
        <header className="topbar">
          <div className="crumbs">
            <span>Practice</span>
            <b>/</b>
            <span>{activeLanguage.label}</span>
            {selectedLanguage === "sql" && (
              <>
                <b>/</b>
                <span>{activeSqlDialect.shortLabel}</span>
              </>
            )}
            <b>/</b>
            <span>{difficulty}</span>
            <b>/</b>
            <strong>{current.title}</strong>
          </div>
          <div className="session-meta">
            <span className="timer" title="Elapsed practice time">
              ◷ {clock}
            </span>
          </div>
        </header>
        <div className="work-grid">
          <article className="problem-panel">
            <div className="problem-title">
              <div>
                <div className="title-row">
                  <h2>{current.title}</h2>
                  <span
                    className={`difficulty ${current.difficulty.toLowerCase()}`}
                  >
                    {current.difficulty}
                  </span>
                  {current.source === "ai_generated" && (
                    <span className="ai-made-current-badge">
                      AI-made · provisional
                    </span>
                  )}
                </div>
                <div className="tag-row">
                  {(current.topics?.length
                    ? current.topics
                    : [current.topic]
                  ).map((topic) => (
                    <span key={topic}>{topic}</span>
                  ))}
                </div>
              </div>
            </div>
            {current.source === "ai_generated" && (
              <aside className="ai-made-current-notice" role="note">
                <strong>AI-made practice drill</strong>
                <p>
                  This drill is separate from curated progress. Its wording,
                  tests, and expected solution may contain AI mistakes—validate
                  assumptions as part of your practice.
                </p>
              </aside>
            )}
            {selectedLanguage === "sql" && (
              <aside className="sql-dialect-note" role="note">
                <strong>{activeSqlDialect.label} syntax mode</strong>
                <p>
                  {sqlDialect === "sqlite"
                    ? "This drill runs with SQLite locally."
                    : `${activeSqlDialect.label} syntax is translated for compatibility and executed in local SQLite unless the runner reports another engine.`}
                </p>
              </aside>
            )}
            {current.submission_mode === "python_class" && (
              <aside className="class-submission-note" role="note">
                <strong>Class API exercise</strong>
                <p>
                  Run uses the included command-line demo. Submit imports your
                  {current.required_class?.name
                    ? ` ${current.required_class.name} class`
                    : " class"} and tests its methods directly.
                </p>
              </aside>
            )}
            <div className="statement">
              <p>{current.description ?? "Loading drill…"}</p>
              {(current.examples ?? []).map((example, index) => {
                const inputLines = splitExampleInputLines(example.input);
                return (
                  <div key={index}>
                    <h3>Example {index + 1}</h3>
                    <div className="example">
                      <section className="example-field">
                        <strong className="example-label">
                          {selectedLanguage === "sql"
                            ? "Dataset"
                            : "Input — line by line"}
                        </strong>
                        {selectedLanguage === "sql" ? (
                          <pre className="example-value">
                            <code>{example.input || "Exercise dataset"}</code>
                          </pre>
                        ) : inputLines.length ? (
                          <ol
                            className="example-input-lines"
                            aria-label={`${inputLines.length} input ${inputLines.length === 1 ? "line" : "lines"}`}
                          >
                            {inputLines.map((line, lineIndex) => (
                              <li key={lineIndex}>
                                <code>
                                  {line || (
                                    <span className="example-blank-line">
                                      (blank line)
                                    </span>
                                  )}
                                </code>
                              </li>
                            ))}
                          </ol>
                        ) : (
                          <pre className="example-value example-empty-value">
                            <code>(no input)</code>
                          </pre>
                        )}
                        {selectedLanguage !== "sql" && (
                          <p className="example-input-guidance">
                            Each numbered row is a separate input line.
                            {selectedLanguage === "python" && (
                              <>
                                {" "}In Python, each <code>input()</code> call
                                reads the next line.
                              </>
                            )}
                          </p>
                        )}
                      </section>
                      <section className="example-field">
                        <strong className="example-label">
                          Expected output
                        </strong>
                        <pre className="example-value example-output">
                          <code>{example.output || "(no output)"}</code>
                        </pre>
                      </section>
                      {example.explanation && (
                        <p className="example-explanation">
                          <b>Explanation:</b> {example.explanation}
                        </p>
                      )}
                    </div>
                  </div>
                );
              })}
              <h3>Constraints</h3>
              <ul>
                {(current.constraints?.length
                  ? current.constraints
                  : [
                      `Write a clear, maintainable ${activeLanguage.label} solution.`,
                    ]
                ).map((constraint, index) => (
                  <li key={index}>{constraint}</li>
                ))}
              </ul>
            </div>
            <div className="coach-note">
              <span>✦</span>
              <div>
                <strong>Coach prompt</strong>
                <p>
                  {current.hints?.[0] ??
                    current.expected_complexity ??
                    "Explain your approach before you start coding."}
                </p>
              </div>
            </div>
          </article>
          <section className="editor-area">
            <div className="editor-toolbar">
              <div
                className="editor-file-tabs"
                role="tablist"
                aria-label="Open editor documents"
              >
                <button
                  type="button"
                  id="learner-solution-tab"
                  role="tab"
                  aria-selected={!bestSolutionActive}
                  aria-controls="solution-editor-panel"
                  className={`file-tab ${!bestSolutionActive ? "active" : ""}`}
                  onClick={showLearnerSolution}
                >
                  <span className={`language-dot ${selectedLanguage}`}>●</span>
                  {activeLanguage.file}
                  {selectedLanguage === "sql" && (
                    <span className="sql-editor-dialect">
                      {activeSqlDialect.shortLabel} mode
                    </span>
                  )}
                </button>
                {referenceSolution?.exerciseId === selected && (
                  <button
                    type="button"
                    id="best-solution-tab"
                    role="tab"
                    aria-selected={bestSolutionActive}
                    aria-controls="solution-editor-panel"
                    className={`file-tab best-solution-tab ${bestSolutionActive ? "active" : ""}`}
                    onClick={openBestSolution}
                  >
                    <span aria-hidden="true">★</span>
                    {bestSolutionFile}
                    <small>Read only</small>
                  </button>
                )}
              </div>
              <div className="editor-actions">
                {selectedLanguage === "sql" && (
                  <label className="sql-dialect-select">
                    <span>SQL dialect</span>
                    <select
                      value={sqlDialect}
                      onChange={(event) =>
                        selectSqlDialect(event.target.value as SqlDialect)
                      }
                      disabled={bestSolutionActive}
                      aria-label="SQL dialect"
                    >
                      {sqlDialects.map((dialect) => (
                        <option key={dialect.id} value={dialect.id}>
                          {dialect.label}
                        </option>
                      ))}
                    </select>
                  </label>
                )}
                <button
                  onClick={resetCode}
                  className="text-button"
                  disabled={bestSolutionActive}
                  title={
                    bestSolutionActive
                      ? "Switch to your solution before resetting it"
                      : "Restore the starter code"
                  }
                >
                  Reset
                </button>
              </div>
            </div>
            {bestSolutionActive && referenceSolution && (
              <div className="best-solution-banner" role="status">
                <strong>Reviewed best answer</strong>
                <span>{referenceSolution.expectedComplexity}</span>
                {referenceSolution.lineCount > 0 && (
                  <span>{referenceSolution.lineCount} non-blank lines</span>
                )}
              </div>
            )}
            <div
              className={`editor-shell monaco-shell ${bestSolutionActive ? "showing-best-solution" : ""}`}
              id="solution-editor-panel"
              role="tabpanel"
              aria-labelledby={
                bestSolutionActive
                  ? "best-solution-tab"
                  : "learner-solution-tab"
              }
            >
              <Editor
                key={`${bestSolutionActive ? "reference" : "learner"}-${selected}-${selectedLanguage}`}
                path={`inmemory://kitcode/${encodeURIComponent(selected)}/${bestSolutionActive ? bestSolutionFile : activeLanguage.file}`}
                height="100%"
                language={activeLanguage.monaco}
                theme="kitcode-night"
                value={
                  bestSolutionActive ? (referenceSolution?.solution ?? "") : code
                }
                onChange={bestSolutionActive ? undefined : handleEditorChange}
                onMount={
                  bestSolutionActive
                    ? () => {
                        editorRef.current = null;
                      }
                    : onMount
                }
                loading={
                  <div className="editor-loading" role="status">
                    Loading {bestSolutionActive ? "reviewed answer" : `accessible ${activeLanguage.label} editor`}…
                  </div>
                }
                options={{
                  fontSize: 13,
                  fontFamily: "var(--font-geist-mono), Consolas, monospace",
                  minimap: { enabled: false },
                  automaticLayout: true,
                  wordWrap: "off",
                  tabSize: 4,
                  insertSpaces: true,
                  renderWhitespace: "selection",
                  bracketPairColorization: { enabled: true },
                  smoothScrolling: true,
                  cursorSmoothCaretAnimation: "on",
                  glyphMargin: true,
                  padding: { top: 14 },
                  accessibilitySupport: "on",
                  quickSuggestions:
                    selectedLanguage === "python"
                      ? pythonAutocompleteActive
                        ? {
                            other: "on",
                            comments: "off",
                            strings: "off",
                          }
                        : false
                      : undefined,
                  quickSuggestionsDelay: pythonAutocompleteActive
                    ? 100
                    : undefined,
                  wordBasedSuggestions:
                    selectedLanguage === "python" ? "off" : undefined,
                  suggestOnTriggerCharacters: pythonAutocompleteActive
                    ? false
                    : undefined,
                  acceptSuggestionOnEnter: pythonAutocompleteActive
                    ? "on"
                    : undefined,
                  suggestSelection: pythonAutocompleteActive
                    ? "first"
                    : undefined,
                  suggest: pythonAutocompleteActive
                    ? {
                        showWords: false,
                        selectionMode: "whenQuickSuggestion",
                        matchOnWordStartOnly: true,
                      }
                    : undefined,
                  readOnly: bestSolutionActive,
                  domReadOnly: bestSolutionActive,
                  readOnlyMessage: {
                    value:
                      "The reviewed best answer is read-only. Switch to your solution tab to keep coding.",
                  },
                }}
              />
              {!bestSolutionActive && editorHint && (
                <div
                  key={editorHint.id}
                  className="editor-hint-card"
                  role="status"
                  aria-live="polite"
                  aria-atomic="true"
                >
                  <span>
                    <strong>
                      {editorHint.inline
                        ? `Hint · line ${editorHint.line}`
                        : "Hint · based on an earlier draft"}
                    </strong>
                    {editorHint.text}
                  </span>
                  <button
                    type="button"
                    onClick={() => {
                      clearEditorHint();
                      editorRef.current?.focus();
                    }}
                  >
                    Dismiss
                  </button>
                </div>
              )}
            </div>
            {!bestSolutionActive && pendingEditorEdit && (
              <div
                className="editor-edit-card pending"
                role="region"
                aria-label="AI editor change review"
              >
                <span>
                  <strong>
                    AI change ready · {editorEditLabel(pendingEditorEdit)}
                  </strong>
                  {pendingEditorEdit.message}
                  <small>
                    Your script has not changed. The exact complete proposed
                    script is below. AI output is untrusted: review it before
                    applying. Applying replaces the editor but never runs the
                    code.
                  </small>
                  <label className="editor-edit-preview-label">
                    Exact proposed {activeLanguage.label} script
                    <textarea
                      value={pendingEditorEdit.after}
                      readOnly
                      spellCheck={false}
                      aria-label={`Exact complete ${activeLanguage.label} script proposed by AI`}
                    />
                  </label>
                </span>
                <button type="button" onClick={applyPendingEditorEdit}>
                  Apply AI edit
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setPendingEditorEdit(null);
                    setStatus("AI edit discarded · code unchanged");
                    editorRef.current?.focus();
                  }}
                >
                  Discard
                </button>
              </div>
            )}
            {!bestSolutionActive && editorEdit && (
              <div
                className="editor-edit-card applied"
                role="region"
                aria-label="Applied AI editor change"
              >
                <span>
                  <strong>
                    AI-applied code · {editorEditLabel(editorEdit)}
                  </strong>
                  {editorEdit.message}
                  <small>
                    Purple marks the exact added or replaced lines. Any learner
                    edit or normal undo clears this provenance; the script is
                    never run automatically.
                  </small>
                </span>
                <button type="button" onClick={undoEditorEdit}>
                  Undo AI edit
                </button>
                <button
                  type="button"
                  onClick={() => {
                    clearEditorEdit();
                    editorRef.current?.focus();
                  }}
                >
                  Clear highlight
                </button>
              </div>
            )}
            <div className="control-bar">
              <button
                onClick={runCode}
                disabled={workflowBusy}
                className="run-button"
                aria-keyshortcuts="F5 Control+Enter"
                title="Run script (F5 or Ctrl+Enter)"
              >
                ▶ Run <kbd>F5</kbd>
              </button>
              <button
                onClick={runTrace}
                disabled={workflowBusy || selectedLanguage !== "python"}
                className="trace-button"
                title={
                  selectedLanguage === "python"
                    ? "Trace Python line by line"
                    : "Line trace is currently available for Python"
                }
              >
                {selectedLanguage === "python"
                  ? "≡ Trace"
                  : "Trace · Python only"}
              </button>
              <button
                onClick={submitCode}
                disabled={workflowBusy}
                className="submit-button"
                aria-keyshortcuts="F6 Control+Shift+S"
                title="Submit solution (F6 or Ctrl+Shift+S)"
              >
                Submit <kbd>F6</kbd>
              </button>
              {referenceAnswerUnlocked &&
                current.source !== "ai_generated" && (
                  <button
                    type="button"
                    onClick={
                      bestSolutionActive
                        ? showLearnerSolution
                        : openBestSolution
                    }
                    disabled={referenceSolutionLoading}
                    className="best-answer-button"
                    aria-pressed={bestSolutionActive}
                    aria-controls="solution-editor-panel"
                    title={
                      bestSolutionActive
                        ? "Return to your unchanged solution"
                        : "Open the reviewed answer in a read-only editor tab"
                    }
                  >
                    {referenceSolutionLoading
                      ? "Opening best answer…"
                      : bestSolutionActive
                        ? `← ${activeLanguage.file}`
                        : referenceSolutionError
                          ? "↻ Retry best answer"
                          : "★ Best answer"}
                  </button>
                )}
              <span
                className="run-status"
                role="status"
                aria-live="polite"
                aria-atomic="true"
              >
                ● {status}
              </span>
            </div>
            <div className="output-panel">
              <div className="output-tabs">
                {(["Console", "Tests", "Trace"] as const).map((item) => (
                  <button
                    key={item}
                    onClick={() => setTab(item)}
                    className={
                      tab === item ? "output-tab active" : "output-tab"
                    }
                  >
                    {item}
                    {item === "Tests" && (
                      <span className="test-count">{results.length}</span>
                    )}
                  </button>
                ))}
              </div>
              {tab === "Console" && (
                <div className="console-wrap">
                  <div className="console-input">
                    <div className="console-heading">
                      <label htmlFor="program-input">
                        {selectedLanguage === "sql"
                          ? "Exercise dataset · managed"
                          : "Input for your program"}
                      </label>
                      {selectedLanguage !== "sql" && (
                        <button
                          type="button"
                          onClick={() =>
                            setStdin(current.examples?.[0]?.input ?? "")
                          }
                          disabled={!current.examples?.length}
                        >
                          Reset to example input
                        </button>
                      )}
                    </div>
                    <textarea
                      id="program-input"
                      value={selectedLanguage === "sql" ? "" : stdin}
                      onChange={(event) => setStdin(event.target.value)}
                      placeholder={
                        selectedLanguage === "sql"
                          ? "Loaded automatically by this SQL exercise"
                          : `Input passed to your ${activeLanguage.label} program`
                      }
                      aria-label={
                        selectedLanguage === "sql"
                          ? "SQL exercise dataset is managed by this drill"
                          : `Input lines for your ${activeLanguage.label} program`
                      }
                      disabled={selectedLanguage === "sql"}
                    />
                    {selectedLanguage !== "sql" && (
                      <p className="console-input-help">
                        Enter separate lines exactly as shown in the example.
                        {selectedLanguage === "python" && (
                          <>
                            {" "}Each <code>input()</code> call reads the next
                            line.
                          </>
                        )}
                      </p>
                    )}
                  </div>
                  <div className="console-output">
                    <strong>Program output</strong>
                    <pre className="console">
                      {runResult
                        ? `${runResult.stdout ?? ""}${runResult.stderr ? `\n${runResult.stderr}` : ""}${runResult.error ? `\n${runResult.error}` : ""}`
                        : `Run your ${activeLanguage.label} code to see output here.`}
                    </pre>
                  </div>
                  {selectedLanguage === "sql" && (
                    <p className="sql-engine-status" role="status">
                      Writing dialect: {activeSqlDialect.shortLabel} · Judge: {sqlExecutionEngine}
                      {sqlDialect !== "sqlite" &&
                      sqlExecutionEngine.toLowerCase().includes("sqlite")
                        ? " · compatibility syntax is translated where supported"
                        : ""}
                    </p>
                  )}
                </div>
              )}
              {tab === "Tests" && (
                <div className="test-content">
                  {results.length ? (
                    results.map((test, index) => (
                      <div className="test-result" key={index}>
                        <div className="pass-line">
                          <span>{test.passed === true ? "✓" : "×"}</span>
                          <strong>
                            {String(test.name ?? `Test ${index + 1}`)}
                          </strong>
                          <small>
                            {String(
                              test.visibility ??
                                runResult?.visibility ??
                                (test.passed === true ? "Passed" : "Failed"),
                            )}
                          </small>
                        </div>
                        {(test.input ||
                          test.expected_output ||
                          test.actual_output ||
                          test.error) && (
                          <div className="test-grid">
                            <span>
                              {selectedLanguage === "sql" ? "Dataset" : "Input"}
                            </span>
                            <code>
                              {selectedLanguage === "sql"
                                ? String(test.input || "Exercise dataset")
                                : String(test.input ?? "—")}
                            </code>
                            <span>Expected</span>
                            <code>{String(test.expected_output ?? "—")}</code>
                            <span>Actual</span>
                            <code>
                              {String(test.actual_output ?? test.error ?? "—")}
                            </code>
                          </div>
                        )}
                      </div>
                    ))
                  ) : (
                    <div className="empty-result">
                      <strong>
                        {acceptedResult(runResult ?? {})
                          ? "✓ Accepted"
                          : "No test results yet"}
                      </strong>
                      <p>
                        {runResult?.error ??
                          runResult?.message ??
                          "Submit your solution to run the exercise test suite."}
                      </p>
                    </div>
                  )}
                  {referenceAnswerUnlocked && (
                    <section
                      className="reference-answer"
                      aria-labelledby="reference-answer-title"
                      aria-busy={referenceSolutionLoading}
                    >
                      <div className="reference-answer-heading">
                        <div>
                          <h3 id="reference-answer-title">
                            Compare with the expected approach
                          </h3>
                          <p>
                            Best means target Big-O time and space first, then
                            the fewest clear lines. Readability wins when the
                            task emphasizes human-facing code.
                          </p>
                        </div>
                        {current.source !== "ai_generated" && (
                          <button
                            type="button"
                            aria-controls="solution-editor-panel"
                            aria-expanded={bestSolutionActive}
                            onClick={
                              bestSolutionActive
                                ? showLearnerSolution
                                : openBestSolution
                            }
                            disabled={referenceSolutionLoading}
                          >
                            {referenceSolutionLoading
                              ? "Checking your accepted answer…"
                              : referenceSolution
                                ? bestSolutionActive
                                  ? "Return to my answer"
                                  : "Open best answer tab"
                                : referenceSolutionError
                                  ? "Try again"
                                  : "Open best answer tab"}
                          </button>
                        )}
                      </div>
                      {current.source === "ai_generated" ? (
                        <p className="reference-answer-unavailable">
                          This is a provisional AI-created drill, so it does
                          not have a vetted reference answer.
                        </p>
                      ) : referenceSolution?.exerciseId === selected ? (
                        <div
                          className="reference-answer-details"
                          id="reference-answer-details"
                        >
                          <h4>Expected best answer</h4>
                          <div className="reference-answer-metrics">
                            <span>
                              Reviewed rubric
                              <strong title={referenceSolution.reviewPolicyId}>
                                Time · space · clear lines
                              </strong>
                            </span>
                            <span>
                              Target
                              <strong>
                                {referenceSolution.expectedComplexity}
                              </strong>
                            </span>
                            {referenceSolution.lineCount > 0 && (
                              <span>
                                Full reference
                                <strong>
                                  {referenceSolution.lineCount} non-blank lines
                                </strong>
                              </span>
                            )}
                            {referenceSolution.referenceDialect && (
                              <span>
                                Reference dialect
                                <strong>
                                  {referenceSolution.referenceDialect}
                                </strong>
                              </span>
                            )}
                            {referenceSolution.readabilityFocused && (
                              <span>
                                Priority
                                <strong>Readable API and structure</strong>
                              </span>
                            )}
                          </div>
                          <p className="reference-answer-editor-note">
                            The complete answer is available in the read-only
                            {` ${bestSolutionFile}`} editor tab. Your code stays
                            unchanged in {activeLanguage.file}.
                          </p>
                          <p>{referenceSolution.selectionBasis}</p>
                          <p>{referenceSolution.readabilityNote}</p>
                          {referenceSolution.complexityNote && (
                            <p>{referenceSolution.complexityNote}</p>
                          )}
                          {referenceSolution.dialectNote && (
                            <p>{referenceSolution.dialectNote}</p>
                          )}
                        </div>
                      ) : null}
                      {referenceSolutionError &&
                        current.source !== "ai_generated" && (
                          <p className="reference-answer-error" role="alert">
                            {referenceSolutionError}
                          </p>
                        )}
                    </section>
                  )}
                </div>
              )}
              {tab === "Trace" && (
                <div className="trace">
                  {traceSteps.length ? (
                    <>
                      <div className="trace-controls">
                        <button
                          onClick={() =>
                            setTraceIndex((value) => Math.max(0, value - 1))
                          }
                          disabled={traceIndex === 0}
                        >
                          ← Previous
                        </button>
                        <span>
                          Step {traceIndex + 1} / {traceSteps.length} · line{" "}
                          {traceSteps[traceIndex]?.line}
                        </span>
                        <button
                          onClick={() =>
                            setTraceIndex((value) =>
                              Math.min(traceSteps.length - 1, value + 1),
                            )
                          }
                          disabled={traceIndex >= traceSteps.length - 1}
                        >
                          Next →
                        </button>
                      </div>
                      {traceSteps[traceIndex]?.source && (
                        <code className="trace-source">
                          {traceSteps[traceIndex].source}
                        </code>
                      )}
                      {traceSteps[traceIndex]?.explanation && (
                        <p className="trace-explanation">
                          {traceSteps[traceIndex].explanation}
                        </p>
                      )}
                      <div className="locals">
                        {Object.entries(
                          traceSteps[traceIndex]?.locals ?? {},
                        ).map(([name, value]) => (
                          <code
                            className={
                              traceSteps[traceIndex]?.changed?.includes(name)
                                ? "changed"
                                : ""
                            }
                            key={name}
                          >
                            {name} = {value}
                          </code>
                        ))}
                        {traceSteps[traceIndex]?.removed?.map((name) => (
                          <code className="removed" key={name}>
                            {name} removed
                          </code>
                        ))}
                      </div>
                    </>
                  ) : (
                    <p>
                      Use <strong>Trace</strong> to step through executed lines
                      and inspect local values.
                    </p>
                  )}
                </div>
              )}
            </div>
          </section>
        </div>
          </>
        )}
      </section>
      <aside
        ref={coachPanelRef}
        tabIndex={-1}
        className={`coach-panel ${coachDrawerOpen ? "drawer-open" : ""}`}
        aria-label="AI coach"
      >
        <header>
          <div className="coach-heading">
            <div>
              <p className="eyebrow">
                {mascotEnabled ? "PAIR PROGRAMMING WITH KIT" : "PAIR PROGRAMMING"}
              </p>
              <h2>
                AI Coach{" "}
                <span className={aiStatus.configured ? "online" : "offline"}>
                  ● {aiStatus.configured ? "ready" : "unavailable"}
                </span>
              </h2>
            </div>
          </div>
          <button
            onClick={() => setCoachDrawerOpen(false)}
            className="drawer-close"
            aria-label="Close AI coach"
          >
            ×
          </button>
          <button
            onClick={(event) => openSettings(event.currentTarget)}
            className="icon-button"
            aria-label="Coach settings"
          >
            ⚙
          </button>
        </header>
        <div className="coach-quick-actions">
          <button
            type="button"
            onClick={requestHint}
            disabled={!coachReady || coachBusy || coachRestarting}
          >
            {hintNotice.startsWith("Finding")
              ? "Finding a hint…"
              : "Give me a hint"}
          </button>
          <span role="status" aria-live="polite" aria-atomic="true">
            {hintNotice || "Adaptive coaching—ask naturally."}
          </span>
          {retryCoachSnapshot && (
            <button
              type="button"
              onClick={retryCoachQuestion}
              disabled={
                coachBusy ||
                coachRestarting ||
                !coachReady
              }
              aria-label="Try the last coach question again"
              title="Retry the same question using your latest code"
            >
              ↻ Try again
            </button>
          )}
        </div>
        <div className="coach-context">
          <span>⌁</span>
          <p>
            {aiStatus.configured
              ? `Selected: ${selectedProvider}${aiStatus.model ? ` · ${aiStatus.model}` : ""}${aiStatus.provider === "local_llm" && (aiStatus.local_llm_url ?? aiStatus.base_url) ? ` · ${aiStatus.local_llm_url ?? aiStatus.base_url}` : ""}. Available: ${availableProviders}. ${aiStatus.provider === "local_llm" ? "Loopback stays on this PC; a custom endpoint may leave it." : "Coach requests are sent only when you ask for help."}`
              : (aiStatus.codex_detail ??
                "No AI provider is configured. Set up OpenAI, Anthropic/Claude, a local LLM, or an authenticated Codex CLI.")}
          </p>
        </div>
        {!aiStatus.configured && (
          <button
            className="setup-ai-button"
            onClick={(event) => openSettings(event.currentTarget)}
          >
            Set up AI
          </button>
        )}
        <div
          ref={coachMessagesRef}
          className="messages"
          role="log"
          aria-live="polite"
          aria-relevant="additions text"
          aria-label="Coach conversation"
        >
          {messages.map((message) => {
            const streaming = Boolean(
              coachBusy &&
                message.role === "coach" &&
                !message.contextual &&
                !message.text &&
                message.id === streamingCoachMessageId,
            );
            return (
              <div
                key={message.id}
                className={`message ${message.role}${streaming ? " streaming" : ""}`}
              >
                <span>{message.role === "coach" ? "✦" : "You"}</span>
                {message.role === "coach" ? (
                  message.text ? (
                    <CoachReply text={message.text} />
                  ) : (
                    <p>{streaming ? "Thinking…" : "Response stopped."}</p>
                  )
                ) : (
                  <p>{message.text}</p>
                )}
              </div>
            );
          })}
        </div>
        <form onSubmit={askCoach} className="coach-compose">
          <label className="sr-only" htmlFor="coach-question">
            Ask the AI coach. Press Enter to send; Shift+Enter for a new line.
          </label>
          <textarea
            id="coach-question"
            value={coachInput}
            onChange={(event) => setCoachInput(event.target.value)}
            onKeyDown={handleCoachKeyDown}
            placeholder="Ask about your approach…"
            rows={2}
            maxLength={4000}
            disabled={coachBusy || coachRestarting}
            aria-keyshortcuts="Enter"
          />
          <div>
            <span>
              {coachRestarting
                ? "Restarting the same question…"
                : coachBusy
                ? aiStatus.provider === "codex"
                  ? "Codex is responding…"
                  : "Coach is responding…"
                : aiStatus.configured
                  ? `Using ${selectedProvider} · Enter to send · saved locally for this exercise and AI setup`
                  : "AI unavailable"}
            </span>
            <button
              aria-label="Send question"
              type="submit"
              disabled={
                !coachReady ||
                coachBusy ||
                coachRestarting ||
                !coachInput.trim()
              }
            >
              ↑
            </button>
            {coachBusy && activeCoachIntent === "adaptive" && (
              <button
                className="coach-restart-button"
                type="button"
                onClick={restartCoachResponse}
                aria-label="Stop and retry the same coach question"
                title="Stop this response and retry the same saved question"
              >
                Try again
              </button>
            )}
            {coachBusy && (
              <button
                className="coach-cancel-button"
                type="button"
                onClick={stopCoachResponse}
                aria-label="Stop coach response"
              >
                Stop
              </button>
            )}
            {coachRestarting && (
              <button
                className="coach-cancel-button"
                type="button"
                onClick={cancelCoachRestart}
                aria-label="Cancel coach restart"
              >
                Cancel
              </button>
            )}
          </div>
        </form>
      </aside>
      {settingsOpen && (
        <div
          className="modal-backdrop"
          role="presentation"
          onMouseDown={closeSettings}
        >
          <section
            ref={settingsDialogRef}
            className="settings-modal ai-settings-modal"
            role="dialog"
            aria-modal="true"
            aria-hidden={codexInstallConfirmOpen || undefined}
            aria-labelledby="settings-title"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <button
              data-dialog-initial-focus
              onClick={closeSettings}
              className="modal-close"
              aria-label="Close settings"
            >
              ×
            </button>
            <p className="eyebrow">KITCODE</p>
            <h2 id="settings-title">AI Coach (optional)</h2>
            <p className="modal-copy">
              Get explanations and hints while you practise.
            </p>
            {aiStatus.configured && (
              <div className="connection-status">
                <span className="good">●</span>
                <div>
                  <strong>
                    {selectedProvider} is connected
                    {aiStatus.model ? ` · ${aiStatus.model}` : ""}
                  </strong>
                  <p>Ready for coaching.</p>
                </div>
              </div>
            )}
            <div className="detect-codex-card">
              <div>
                <strong>Start with Codex</strong>
                <p>
                  <a
                    href="https://learn.chatgpt.com/docs/codex/cli"
                    target="_blank"
                    rel="noopener noreferrer"
                  >
                    Download Codex CLI
                  </a>
                  , sign in with ChatGPT, then connect it here. No API key is
                  needed, and KitCode cannot read your open chats.
                </p>
              </div>
              <button
                type="button"
                className="detect-codex-button"
                onClick={() => void detectCodex()}
                disabled={codexDetecting}
              >
                {codexDetecting ? "Checking…" : "Connect Codex"}
              </button>
            </div>
            {codexDetection?.ready && (
              <div
                className="codex-detection ready"
                role="status"
              >
                <strong>Codex is ready for coaching</strong>
                <p>
                  {codexDetection.detail ??
                    codexDetection.status ??
                    "Connected with your ChatGPT sign-in."}
                </p>
              </div>
            )}
            {codexGuidedActions}
            <p className="setup-privacy">
              Your first AI request asks for permission before KitCode sends
              your exercise text or code.
            </p>
            <details className="other-kitcode-options">
              <summary>Other KitCode options</summary>
              <div className="settings-disclosure-body">
                <div className="celebration-setting">
                  <input
                    id="inline-hints"
                    type="checkbox"
                    checked={inlineHintsEnabled}
                    onChange={(event) =>
                      setInlineHintPreference(event.target.checked)
                    }
                  />
                  <label htmlFor="inline-hints">
                    <strong>Show hints in the editor</strong>
                    <small>
                      Turn this off to show AI hints only in the card below your
                      code.
                    </small>
                  </label>
                </div>
                <div className="celebration-setting">
                  <input
                    id="python-autocomplete"
                    type="checkbox"
                    checked={pythonAutocompleteEnabled}
                    onChange={(event) =>
                      setPythonAutocompletePreference(event.target.checked)
                    }
                  />
                  <label htmlFor="python-autocomplete">
                    <strong>Python autocomplete</strong>
                    <small>
                      Suggest common Python keywords and built-ins after three
                      letters. Press Enter to accept; KitCode never autocorrects
                      or renames your code.
                    </small>
                  </label>
                </div>
                <div className="celebration-setting">
              <input
                id="success-celebrations"
                type="checkbox"
                checked={celebrationsEnabled}
                onChange={(event) =>
                  setCelebrationPreference(event.target.checked)
                }
              />
              <label htmlFor="success-celebrations">
                <strong>Celebrate accepted solutions</strong>
                <small>
                  Show a short visual “All tests passed” badge after a
                  successful submission. No sound.
                </small>
              </label>
              <button
                type="button"
                className="celebration-preview"
                onClick={previewCelebration}
                disabled={!celebrationsEnabled}
              >
                Preview
              </button>
                </div>
                <fieldset className="mascot-settings">
              <legend>Kit the fox</legend>
              <div className="mascot-setting-head">
                <label
                  className="mascot-toggle"
                  htmlFor="mascot-enabled"
                  aria-label="Show Kit in the workspace"
                >
                  <input
                    id="mascot-enabled"
                    type="checkbox"
                    checked={mascotEnabled}
                    onChange={(event) =>
                      setMascotPreference(event.target.checked)
                    }
                  />
                  <span>
                    <strong>Show Kit in the workspace</strong>
                    <small>
                      Kit hunts for answers while AI is working, celebrates
                      wins, naps when things are quiet, and jumps at script
                      errors. No sound.
                    </small>
                  </span>
                </label>
                {mascotEnabled && (
                  <KitMascot size="settings" />
                )}
              </div>
                </fieldset>
                {generatedDrillSettings}
              </div>
            </details>
            <details
              className="advanced-llm-options"
              onToggle={(event) => {
                if (event.currentTarget.open && setupProvider === "codex") {
                  chooseSetupProvider("openai");
                }
              }}
            >
              <summary>I am an advanced user with custom LLM instructions</summary>
              <form className="ai-setup-form" onSubmit={saveAiSetup}>
              <p className="advanced-llm-intro">
                Use this only if you already have an API key or model server.
                API providers may charge, and non-loopback model URLs can send
                coaching data off this PC.
              </p>
              <fieldset>
                <legend>Choose a custom provider</legend>
                <div
                  className="provider-choices"
                  role="radiogroup"
                  aria-label="AI provider"
                >
                  {(
                    [
                      "openai",
                      "anthropic",
                      "local_llm",
                    ] as SetupProvider[]
                  ).map((provider) => (
                    <button
                      key={provider}
                      type="button"
                      role="radio"
                      aria-checked={setupProvider === provider}
                      className={
                        setupProvider === provider
                          ? "provider-choice active"
                          : "provider-choice"
                      }
                      onClick={() => chooseSetupProvider(provider)}
                    >
                      <strong>
                        {provider === "openai"
                          ? "OpenAI API"
                          : provider === "anthropic"
                            ? "Anthropic / Claude"
                            : provider === "local_llm"
                              ? "Local LLM"
                              : "ChatGPT / Codex"}
                      </strong>
                      <small>
                        {provider === "openai"
                          ? "API key and billing"
                          : provider === "anthropic"
                            ? "Claude API key and billing"
                            : provider === "local_llm"
                              ? "Local model server"
                              : "Easiest · no API key"}
                      </small>
                    </button>
                  ))}
                </div>
              </fieldset>
              {setupProvider === "openai" || setupProvider === "anthropic" ? (
                <>
                  <label>
                    Model preset
                    <select
                      value={setupModel}
                      onChange={(event) => {
                        setSetupModel(event.target.value);
                        setSetupCustomModel("");
                      }}
                    >
                      {providerModels[setupProvider].map((model) => (
                        <option value={model.value} key={model.value}>
                          {model.label}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    Custom model (optional)
                    <input
                      value={setupCustomModel}
                      onChange={(event) =>
                        setSetupCustomModel(event.target.value)
                      }
                      maxLength={160}
                      placeholder="Use a supported model ID"
                      autoComplete="off"
                    />
                  </label>
                  <label>
                    API key{" "}
                    <small>
                      {setupProviderConfigured
                        ? "Leave blank to keep saved key."
                        : "Required for a new provider."}
                    </small>
                    <input
                      type="password"
                      value={setupKey}
                      onChange={(event) => setSetupKey(event.target.value)}
                      maxLength={600}
                      placeholder={
                        setupProvider === "openai" ? "sk-…" : "sk-ant-…"
                      }
                      autoComplete="new-password"
                    />
                  </label>
                </>
              ) : setupProvider === "local_llm" ? (
                <div className="local-llm-setup">
                  <strong>Connect a local model server</strong>
                  <p>
                    Detection checks whether anything responds at this URL.
                    KitCode contacts <code>/v1/chat/completions</code> only when
                    you ask for coaching; your browser never directly contacts
                    the model server.
                  </p>
                  <label>
                    Server URL
                    <input
                      value={setupLocalUrl}
                      onChange={(event) => setSetupLocalUrl(event.target.value)}
                      maxLength={500}
                      placeholder="http://127.0.0.1:5000/"
                      inputMode="url"
                      autoComplete="url"
                    />
                  </label>
                  <label>
                    Model ID
                    <input
                      value={setupCustomModel || setupModel}
                      onChange={(event) => {
                        setSetupCustomModel(event.target.value);
                        setSetupModel("");
                      }}
                      maxLength={160}
                      placeholder="Enter your server's model ID"
                      autoComplete="off"
                      required
                    />
                  </label>
                  <button
                    className="detect-codex-button"
                    type="button"
                    onClick={() => void detectLocalLlm()}
                    disabled={localLlmDetecting}
                  >
                    {localLlmDetecting
                      ? "Detecting…"
                      : "Connect local LLM"}
                  </button>
                  <p className="detect-codex-explainer">
                    Loopback URLs such as <code>127.0.0.1</code> keep prompts on
                    this PC. A custom or non-loopback URL may send prompts and
                    editor code to another device or service.
                  </p>
                  {localLlmDetection && (
                    <div
                      className={`codex-detection ${localLlmDetection.reachable ? "ready" : ""}`}
                      role="status"
                    >
                      <strong>
                        {localLlmDetection.reachable
                          ? "Local server detected"
                          : "No local server response"}
                      </strong>
                      <ul>
                        <li>
                          Server response:{" "}
                          {localLlmDetection.reachable
                            ? "received"
                            : "not received"}
                        </li>
                        <li>
                          Models:{" "}
                          {localLlmDetection.models?.length
                            ? localLlmDetection.models.join(", ")
                            : "none reported"}
                        </li>
                      </ul>
                      <p>
                        {localLlmDetection.detail ??
                          "No additional detail was returned."}
                      </p>
                      {localLlmDetection.action && (
                        <p>
                          <strong>Next:</strong>{" "}
                          {localLlmActionText(localLlmDetection.action)}
                        </p>
                      )}
                    </div>
                  )}
                </div>
              ) : null}
              {setupProvider === "local_llm" && (
                <p className="setup-notice">
                  <strong>Probe only:</strong> KitCode never downloads, installs,
                  starts, supervises, or keeps a local model server running.
                  Detection checks a server you already started, only when you
                  click the button.
                </p>
              )}
              <p className="setup-privacy">
                Your first request asks for consent. Never send secrets,
                personal data, or proprietary code.
              </p>
              {setupNotice && (
                <p className="setup-notice" role="status">
                  {setupNotice}
                </p>
              )}
              <div className="modal-actions">
                <button
                  type="button"
                  className="text-button"
                  onClick={() => void clearAiSetup()}
                  disabled={setupSaving}
                >
                  Remove all AI configuration
                </button>
                {setupProvider !== "codex" && (
                  <button
                    type="submit"
                    className="submit-button"
                    disabled={setupSaving}
                  >
                    {setupSaving
                      ? "Saving…"
                      : setupProvider === "local_llm"
                        ? "Use local LLM"
                        : "Save locally"}
                  </button>
                )}
              </div>
              </form>
            </details>
          </section>
        </div>
      )}
      {codexInstallConfirmOpen && (
        <div
          className="modal-backdrop install-confirm-backdrop"
          role="presentation"
          onMouseDown={() => setCodexInstallConfirmOpen(false)}
        >
          <section
            ref={codexInstallDialogRef}
            className="settings-modal install-confirm-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="codex-install-title"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <button
              data-dialog-initial-focus
              onClick={() => setCodexInstallConfirmOpen(false)}
              className="modal-close"
              aria-label="Cancel Codex CLI installation"
            >
              ×
            </button>
            <p className="eyebrow">SOFTWARE INSTALLATION</p>
            <h2 id="codex-install-title">Install the official Codex CLI?</h2>
            <p className="modal-copy">
              KitCode will run OpenAI&apos;s fixed Windows installer from{" "}
              <code>https://chatgpt.com/codex/install.ps1</code>. It installs
              Codex for your Windows user and may update your user PATH. It does
              not ask KitCode for an administrator password.
            </p>
            <p className="modal-copy">
              The installer downloads software from OpenAI. After installation,
              ChatGPT sign-in opens separately; KitCode never receives your
              password or Codex session tokens.
            </p>
            <div className="modal-actions">
              <button
                type="button"
                className="text-button"
                onClick={() => setCodexInstallConfirmOpen(false)}
              >
                Cancel
              </button>
              <button
                type="button"
                className="submit-button"
                onClick={() => void installCodex()}
              >
                Install Codex CLI
              </button>
            </div>
          </section>
        </div>
      )}
      {coachConsentOpen && (
        <div
          className="modal-backdrop"
          role="presentation"
          onMouseDown={closeCoachConsent}
        >
          <section
            ref={consentDialogRef}
            className="settings-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="coach-consent-title"
            onMouseDown={(event) => event.stopPropagation()}
          >
            <button
              data-dialog-initial-focus
              onClick={closeCoachConsent}
              className="modal-close"
              aria-label="Close AI data notice"
            >
              ×
            </button>
            <p className="eyebrow">
              AI DATA NOTICE · {activeLanguage.label.toUpperCase()}
            </p>
            <h2 id="coach-consent-title">
              Before you{" "}
              {pendingCoachIntent === "hint"
                ? "request a hint from "
                : pendingCoachIntent === "edit"
                  ? "request an editor change from "
                  : "ask "}
              {pendingCoachProvider.startsWith("local_llm|")
                ? "your local LLM"
                : pendingCoachProvider === "anthropic"
                  ? "Anthropic"
                  : pendingCoachProvider === "codex"
                    ? "Codex"
                    : "OpenAI"}
            </h2>
            <p className="modal-copy">
              Learner-visible {activeLanguage.label} exercise title,
              description, topics, examples, constraints, complexity and hints,
              plus your question, current cursor location, up to eight recent
              current-drill conversation messages, and complete editor contents
              will be sent to the selected {selectedProvider} service to
              generate a reply.{" "}
              {pendingCoachProvider.startsWith("local_llm|") ? (
                <>
                  Endpoint:{" "}
                  <code>{pendingCoachProvider.slice("local_llm|".length)}</code>
                  . Loopback endpoints stay on this PC; a non-loopback endpoint
                  may send this data to another device or service.
                </>
              ) : null}{" "}
              Hidden tests and reference solutions are not included. Do not
              include secrets, personal data, proprietary code, or other
              sensitive information.
            </p>
            {pendingCoachIntent === "edit" && (
              <p className="modal-copy edit-consent-copy">
                <strong>Editor change:</strong> the provider may propose
                replacement {activeLanguage.label} for the complete editor.
                KitCode will show a summary first; your script changes only
                if
                you then choose <strong>Apply AI edit</strong>. Applied lines
                are highlighted, remain undoable, and are never run
                automatically.
              </p>
            )}
            <div className="modal-actions">
              <button className="text-button" onClick={closeCoachConsent}>
                Cancel
              </button>
              <button className="submit-button" onClick={acceptCoachConsent}>
                I understand — continue
              </button>
            </div>
          </section>
        </div>
      )}
    </main>
  );
}
