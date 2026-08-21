import assert from "node:assert/strict";
import { access, readFile as readRawFile, readdir, stat } from "node:fs/promises";
import test from "node:test";

const projectRoot = new URL("../../", import.meta.url);

async function readFile(url, encoding) {
  const contents = await readRawFile(url, encoding);
  return typeof contents === "string" ? contents.replaceAll("\r\n", "\n") : contents;
}

test("the local production bundle contains the practice workspace", async () => {
  const index = await readFile(new URL("frontend_dist/index.html", projectRoot), "utf8");
  assert.match(index, /KitCode/);
  assert.match(index, /<script[^>]+type="module"/);
  await access(new URL("frontend_dist/assets/", projectRoot));
});

test("examples show exact input lines and explain how Python consumes them", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /function splitExampleInputLines\(value: string\)/);
  assert.match(page, /Input — line by line/);
  assert.match(page, /className="example-input-lines"/);
  assert.match(page, /Each numbered row is a separate input line/);
  assert.match(page, /each <code>input\(\)<\/code> call\s+reads the next line/i);
  assert.match(page, /className="example-value example-output"/);
  assert.match(styles, /\.example-value\{[^}]*white-space:pre-wrap/);
  assert.match(styles, /\.example-input-lines li\{[^}]*white-space:pre-wrap/);
  assert.match(page, /Input for your program/);
  assert.match(page, /Reset to example input/);
  assert.match(page, /<strong>Program output<\/strong>/);
  assert.doesNotMatch(page, /Custom stdin/);
});

test("the client wires every core local API workflow", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  for (const route of [
    "/api/exercises",
    "/api/run",
    "/api/trace",
    "/api/submit",
    "/api/ai/status",
    "/api/ai/coach",
    "/api/ai/editor-hint",
    "/api/ai/configure",
    "/api/ai/detect-codex",
    "/api/ai/install-codex",
    "/api/ai/start-codex-login",
    "/api/ai/detect-local-llm",
  ]) {
    assert.match(page, new RegExp(route.replaceAll("/", "\\/")));
  }
  assert.match(page, /localStorage/);
  assert.match(page, /type="password"/);
  assert.match(page, /setSetupKey\(""\)/);
});

test("AI-created drills stay optional and separate from the curated practice bank", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /\/api\/generated-exercises/);
  assert.match(page, /source: "ai_generated"/);
  assert.match(page, /Create an extra practice drill/);
  assert.match(page, /Configure an AI provider above to unlock optional generated drills/);
  assert.match(page, /AI-generated extras/);
  assert.match(page, /curated completed/);
  assert.match(page, /AI-made · provisional/);
  assert.match(page, /tests, and expected solution may contain AI mistakes/);
  assert.match(page, /Up to 2,000 saved drills are\s+retained at once/);
  assert.match(page, /Each click makes one external provider request/);
  assert.match(page, /may consume billed\s+tokens \(or local compute\)/);
  assert.match(page, /No background generation or\s+automatic retry occurs/);
  assert.match(page, /window\.confirm\(\s*"Remove this AI-made drill/);
  assert.match(
    page,
    /clearPersistedDraft\(\s*window\.localStorage,\s*selectedLanguage,\s*exerciseId/,
  );
  assert.match(page, /selectedRef\.current === exerciseId/);
  assert.match(page, /ai-made-current-badge/);
  assert.match(page, /expected_provider: aiStatus\.provider/);
  assert.match(page, /expected_model: aiStatus\.model/);
  assert.match(page, /expected_base_url: aiStatus\.base_url/);
  assert.match(styles, /\.generated-drill-settings/);
  assert.match(styles, /\.generated-bank-section/);
  assert.match(styles, /\.ai-generated-badge/);
  assert.match(styles, /\.ai-made-current-notice/);
});

test("the language rail switches Python, SQL, and Java as isolated practice contexts", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /type PracticeLanguage = "python" \| "sql" \| "java"/);
  assert.match(page, /kitcode:selected-language/);
  assert.match(page, /kitcode:selected-exercise:\$\{selectedLanguage\}/);
  assert.match(
    page,
    /readPersistedDraft\(\s*localStorage,\s*selectedLanguage,\s*exercise\.id/,
  );
  assert.match(page, /api\/exercises\?language=\$\{selectedLanguage\}/);
  assert.match(page, /language: selectedLanguage/);
  assert.match(page, /aria-pressed=\{selectedLanguage === language\.id\}/);
  assert.match(page, /Switch to \$\{language\.label\}/);
  assert.match(page, /monaco: "sql"/);
  assert.match(page, /monaco: "java"/);
  assert.match(page, /Trace · Python only/);
  assert.match(page, /<span>\{activeLanguage\.label\}<\/span>/);
  assert.match(page, /Write a clear, maintainable \$\{activeLanguage\.label\} solution/);
  assert.match(page, /Exercise dataset · managed/);
  assert.match(page, /Loaded automatically by this SQL exercise/);
  assert.match(page, /disabled=\{selectedLanguage === "sql"\}/);
  assert.match(page, /example\.input \|\| "Exercise dataset"/);
  assert.match(page, /language-dot/);
  assert.match(styles, /\.language-rail/);
  assert.match(styles, /\.language-button\.active/);
  assert.match(styles, /\.language-dot\.sql/);
});

test("the curated bank starts with a remembered practice level instead of one flat list", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /Choose a practice level/);
  assert.match(page, /kitcode:selected-level:\$\{language\}/);
  assert.match(page, /role="radiogroup" aria-label="Practice level"/);
  assert.match(page, /Foundations/);
  assert.match(page, /Practice/);
  assert.match(page, /Advanced/);
  assert.match(page, /levelCounts\[level\.id\]/);
  assert.match(page, /levelSolved\[difficulty\]/);
  assert.match(page, /Filter drills by topic/);
  assert.match(page, /item\.difficulty === difficulty/);
  assert.doesNotMatch(page, /\["All", "Easy", "Medium", "Hard"\]/);
  assert.match(styles, /\.level-picker/);
  assert.match(styles, /\.level-card\.active/);
  assert.match(styles, /\.topic-filter select/);
});

test("SQL practice offers a persistent dialect selector while keeping the local judge explicit", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /type SqlDialect = "sqlite" \| "postgresql" \| "mysql" \| "mssql"/);
  for (const name of ["SQLite", "PostgreSQL", "MySQL", "Microsoft SQL Server"]) {
    assert.match(page, new RegExp(name));
  }
  assert.match(page, /kitcode:selected-sql-dialect/);
  assert.match(page, /aria-label="SQL dialect"/);
  assert.match(page, /sql_dialect: workflow\.dialect/);
  assert.match(page, /workflow\.language !== "sql" \|\| sqlDialect === workflow\.dialect/);
  assert.match(page, /sql_dialect: snapshot\.sqlDialect/);
  assert.match(page, /executed_engine\?: string/);
  assert.match(page, /Writing dialect: \{activeSqlDialect\.shortLabel\} · Judge:/);
  assert.match(page, /syntax is translated for compatibility and executed in local SQLite/);
  assert.match(styles, /\.sql-dialect-select/);
  assert.match(styles, /\.sql-engine-status/);
});

test("the delivered UI contains final product metadata", async () => {
  const index = await readFile(new URL("frontend/index.html", projectRoot), "utf8");
  assert.match(index, /KitCode/);
  assert.match(index, /favicon\.svg/);
  assert.doesNotMatch(index, /codex-preview|Starter Project|Your site is taking shape/);
});

test("the shipped browser bundle contains no source maps", async () => {
  const assets = await readdir(new URL("frontend_dist/assets/", projectRoot));
  assert.deepEqual(assets.filter((name) => name.endsWith(".map")), []);
});

test("responsive drawers and AI data consent stay wired", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /kitcode:coach-data-consent-provider/);
  assert.match(page, /title,\s+description, topics, examples, constraints, complexity and\s+hints/);
  assert.match(page, /Hidden tests and\s+reference solutions are not included/);
  assert.match(page, /Open practice problems/);
  assert.match(page, /Open AI coach/);
  assert.match(styles, /\.problem-bank\.drawer-open/);
  assert.match(styles, /\.coach-panel\.drawer-open/);
});

test("workflow results are scoped to the active drill and dialogs keep keyboard focus", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /workflowGenerationRef/);
  assert.match(page, /workflowIsCurrent/);
  assert.match(page, /selectExercise/);
  assert.match(page, /event\.key === "Escape"/);
  assert.match(page, /data-dialog-initial-focus/);
  assert.match(page, /coach-drawer-backdrop/);
  assert.match(styles, /min-width:871px/);
  assert.match(styles, /\.coach-panel\.drawer-open\{transform:translateX\(0\)/);
});

test("plain F5 runs the script instead of refreshing, Spyder-style", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  assert.match(page, /const plainF5 =\s+event\.key === "F5" &&\s+!event\.ctrlKey &&\s+!event\.metaKey &&\s+!event\.altKey &&\s+!event\.shiftKey/);
  assert.match(page, /if \(plainF5\) \{\s*event\.preventDefault\(\);\s*event\.stopPropagation\(\);/);
  assert.match(page, /workflowBusyRef\.current/);
  assert.match(page, /runCode\(\);\s*return;\s*\}/);
  assert.match(page, /addEventListener\("keydown", onShortcut, true\)/);
  assert.match(page, /settingsOpen\s+\|\|\s+coachConsentOpen\s+\|\|\s+codexInstallConfirmOpen\s+\|\|\s+event\.repeat\s+\|\|\s+event\.isComposing/);
  assert.match(page, /aria-keyshortcuts="F5 Control\+Enter"/);
  assert.match(page, /Run script \(F5 or Ctrl\+Enter\)/);
});

test("plain F6 submits the current solution outside dialogs", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  assert.match(
    page,
    /const plainF6 =\s+event\.key === "F6" &&\s+!event\.ctrlKey &&\s+!event\.metaKey &&\s+!event\.altKey &&\s+!event\.shiftKey/,
  );
  assert.match(
    page,
    /if \(plainF6\) \{\s*event\.preventDefault\(\);[\s\S]*?settingsOpen\s*\|\|\s*coachConsentOpen\s*\|\|\s*codexInstallConfirmOpen[\s\S]*?return;[\s\S]*?submitCode\(\);\s*return;\s*\}/,
  );
  assert.match(page, /aria-keyshortcuts="F6 Control\+Shift\+S"/);
  assert.match(page, /Submit solution \(F6 or Ctrl\+Shift\+S\)/);
  assert.match(page, /Submit <kbd>F6<\/kbd>/);
});

test("README gives learners a direct Windows download and short startup path", async () => {
  const readme = await readFile(new URL("README.md", projectRoot), "utf8");
  assert.match(readme, /releases\/latest\/download\/KitCode-Windows\.zip/);
  assert.match(readme, /!\[KitCode workspace preview\]\(\.github\/kitcode-workspace\.png\)/);
  await access(new URL(".github/kitcode-workspace.png", projectRoot));
  assert.match(readme, /Extract All/);
  assert.match(readme, /double-click \*\*`launch\.bat`\*\*/i);
  assert.doesNotMatch(readme, /## AI coach setup/);
  assert.doesNotMatch(readme, /## Development/);
});

test("AI setup keeps provider choices, privacy terms, and current-model guidance local", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  for (const model of ["gpt-5.6-terra", "gpt-5.6-luna", "gpt-5.4-mini", "gpt-5.6-sol", "claude-sonnet-5", "claude-haiku-4-5", "claude-opus-5"]) {
    assert.match(page, new RegExp(model.replaceAll(".", "\\.")));
  }
  assert.match(page, /Set up AI/);
  assert.match(page, /I am an advanced user with custom LLM instructions/);
  assert.match(page, /Choose a custom provider/);
  assert.match(page, /API providers may charge/);
  assert.match(page, /non-loopback model URLs can send\s+coaching data off this PC/);
  assert.match(page, /rel="noopener noreferrer"/);
  assert.doesNotMatch(page, /Codex quick start/);
});

test("AI switching keeps saved keys private and re-prompts consent per provider", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  assert.match(page, /model\?: string \| null/);
  assert.match(page, /providers\?: Record/);
  assert.match(page, /Leave blank to keep saved key/);
  assert.match(page, /Remove all AI configuration/);
  assert.match(page, /kitcode:coach-data-consent-provider/);
  assert.match(page, /function hasCoachConsent/);
  assert.match(page, /function rememberCoachConsent/);
  assert.match(page, /learn\.chatgpt\.com\/docs\/codex\/cli/);
  assert.match(page, /Your first request asks for consent/);
  assert.match(page, /coachBusy/);
});

test("AI setup starts with one Codex-first path and keeps custom LLM setup collapsed", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /<details\s+className="advanced-llm-options"[\s\S]{0,300}<summary>I am an advanced user with custom LLM instructions<\/summary>/);
  assert.equal((page.match(/Connect Codex/g) ?? []).length, 1);
  assert.match(page, /Download Codex CLI/);
  assert.match(page, /https:\/\/learn\.chatgpt\.com\/docs\/codex\/cli/);
  assert.match(page, /No API key is\s+needed/);
  assert.match(page, /cannot read your open chats/);
  assert.match(page, /\/api\/ai\/detect-codex/);
  assert.match(page, /setSetupProvider\("codex"\);\s+setCodexDetecting/);
  assert.match(page, /app_open\?: boolean/);
  assert.match(page, /cli_detected\?: boolean/);
  assert.match(page, /authenticated\?: boolean/);
  assert.match(page, /\[\s*"openai",\s*"anthropic",\s*"local_llm",\s*\]\s+as SetupProvider\[\]/);
  assert.match(page, /await refreshAiStatus\(\)/);
  assert.match(styles, /\.detect-codex-card/);
  assert.match(styles, /\.codex-detection\.ready/);
  assert.match(styles, /\.advanced-llm-options/);
});

test("Codex guided setup confirms installation and monitors external sign-in", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /Install the official Codex CLI\?/);
  assert.match(page, /https:\/\/chatgpt\.com\/codex\/install\.ps1/);
  assert.match(page, /JSON\.stringify\(\{ confirmed: true \}\)/);
  assert.match(page, /codexInstallDialogRef/);
  assert.match(page, /aria-labelledby="codex-install-title"/);
  assert.match(page, /setCodexLoginPolling\(true\)/);
  assert.match(page, /attempts >= 40/);
  assert.match(page, /window\.clearTimeout\(timer\)/);
  assert.match(page, /KitCode never receives your\s+password or Codex session tokens/);
  assert.match(styles, /\.install-confirm-backdrop/);
});

test("advanced custom-model setup detects any reachable endpoint and re-prompts consent by URL", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /local_llm/);
  assert.match(page, /http:\/\/127\.0\.0\.1:5000\//);
  assert.match(page, /Enter your server's model ID/);
  assert.match(page, /Connect local LLM/);
  assert.match(page, /Probe only:/);
  assert.match(page, /never downloads, installs,\s+starts, supervises, or keeps a local model server running/);
  assert.match(page, /only when you\s+click the button/);
  assert.doesNotMatch(page, /\/v1\/models/);
  assert.match(page, /\/v1\/chat\/completions/);
  assert.match(page, /if \(payload\.reachable\)/);
  assert.doesNotMatch(page, /OpenAI compatibility:/);
  assert.match(page, /local_llm\|\$\{status\.local_llm_url/);
  assert.match(page, /Loopback URLs such as/);
  assert.match(page, /may send prompts and\s+editor code to another device or service/);
  assert.match(page, /base_url:\s+setupProvider === "local_llm"/);
  assert.match(styles, /\.local-llm-setup/);
});

test("coach composer sends on Enter without breaking IME or multiline input", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  assert.match(page, /function handleCoachKeyDown/);
  assert.match(page, /event\.key !== "Enter" \|\|\s+event\.shiftKey \|\|\s+event\.repeat \|\|\s+event\.nativeEvent\.isComposing/);
  assert.match(page, /event\.preventDefault\(\);\s+submitCoachQuestion\(\)/);
  assert.match(page, /onKeyDown=\{handleCoachKeyDown\}/);
  assert.match(page, /Enter to send; Shift\+Enter for a new line/);
  assert.match(page, /coachSubmitRef/);
  assert.match(page, /!coachReady \|\|\s+coachBusy \|\|\s+coachRestarting \|\|\s+!coachInput\.trim\(\)/);
});

test("class exercises explain that Submit checks the class API directly", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /submission_mode\?: "python_class"/);
  assert.match(page, /current\.submission_mode === "python_class"/);
  assert.match(page, /Class API exercise/);
  assert.match(page, /Submit imports your[\s\S]*?tests its methods directly/);
  assert.match(styles, /\.class-submission-note/);
});

test("coach discussions are restored locally for the same exercise and provider", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  assert.match(
    page,
    /import \{[\s\S]*?coachConversationScope,[\s\S]*?readCoachConversation,[\s\S]*?writeCoachConversation,[\s\S]*?\} from "\.\/coach-conversation-storage"/,
  );
  assert.match(page, /const coachConversationScopeRef = useRef\(""\)/);
  assert.match(
    page,
    /readCoachConversation\(\s*window\.localStorage,\s*selectedLanguage,\s*selected,\s*currentCoachRuntimeIdentity/,
  );
  assert.match(
    page,
    /writeCoachConversation\(\s*window\.localStorage,\s*selectedLanguage,\s*selected,\s*currentCoachRuntimeIdentity,\s*coachMessagesForStorage\(\)/,
  );
  assert.match(
    page,
    /const previousScope = coachConversationScopeRef\.current;[\s\S]*?JSON\.parse\(previousScope\)[\s\S]*?writeCoachConversation\(\s*window\.localStorage,\s*previousLanguage,\s*previousExercise,\s*previousRuntime,\s*coachMessagesForStorage\(\)/,
  );
  assert.match(page, /saved locally for this exercise/);
  assert.match(
    page,
    /window\.addEventListener\("pagehide", flushBeforeLeaving\)[\s\S]*?flushBeforeLeaving\(\)[\s\S]*?window\.removeEventListener\("pagehide", flushBeforeLeaving\)/,
  );
  assert.match(
    page,
    /const coachMessagesForStorage = useCallback\(\(\)[\s\S]*?coachStreamingMessageRef\.current[\s\S]*?coachStreamTextRef\.current[\s\S]*?contextual: false/,
  );
  assert.match(
    page,
    /function selectExercise\([\s\S]*?flushCoachConversationToStorage\(\)[\s\S]*?cancelCoachWork\(true, true\)/,
  );
  const restoreStart = page.indexOf("const scope = coachConversationScope(");
  const restoreEnd = page.indexOf("useEffect(", restoreStart + 1);
  assert.ok(restoreStart >= 0 && restoreEnd > restoreStart);
  assert.doesNotMatch(page.slice(restoreStart, restoreEnd), /fetch\(/);
  const deletionStart = page.indexOf("async function deleteGeneratedProblem");
  const deletionEnd = page.indexOf("const generatedDrillSettings", deletionStart);
  const deletion = page.slice(deletionStart, deletionEnd);
  assert.ok(
    deletion.indexOf("selectExercise(problems[0]?.id") <
      deletion.indexOf("clearCoachConversationsForExercise("),
    "the final delete must clear any conversation flushed during replacement selection",
  );
});

test("adaptive coach renders provider-neutral streamed replies progressively", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /\/api\/ai\/coach\/stream/);
  assert.match(page, /import \{ readCoachStream \} from "\.\/coach-stream"/);
  const stream = await readFile(new URL("app/coach-stream.mjs", projectRoot), "utf8");
  assert.match(stream, /eventName === "delta"/);
  assert.match(stream, /MAX_COACH_STREAM_BYTES/);
  assert.match(stream, /MAX_COACH_STREAM_PENDING_CHARS/);
  assert.match(stream, /receivedBytes > MAX_COACH_STREAM_BYTES/);
  assert.match(stream, /pending\.length > MAX_COACH_STREAM_PENDING_CHARS/);
  assert.match(stream, /await reader\.cancel\(\)\.catch/);
  assert.match(page, /\(\) => coachSnapshotIsCurrent\(snapshot, generation\)/);
  assert.match(page, /queueStreamingCoachMessage/);
  assert.match(page, /requestAnimationFrame/);
  assert.match(page, /flushStreamingCoachMessage\(id, true\)/);
  assert.match(page, /stream\.status === 404 \|\| stream\.status === 405/);
  assert.match(page, /Streaming stopped:/);
  assert.match(page, /contextual: false/);
  assert.match(page, /ref=\{coachMessagesRef\}/);
  assert.match(styles, /\.message\.streaming \.coach-reply/);
  assert.match(page, /function stopCoachResponse/);
  assert.match(page, /coachAbortRef\.current\?\.abort\(\)/);
  assert.match(page, /Response stopped\. Choose Try again/);
  assert.match(page, /Stop coach response/);
  assert.match(page, /Codex is responding…/);
  assert.match(page, /Coach is responding…/);
  assert.match(styles, /\.coach-compose \.coach-cancel-button/);
});

test("delayed SSE delta reaches the client before the completed event", async () => {
  const { readCoachStream } = await import(new URL("../../app/coach-stream.mjs", import.meta.url));
  const encoder = new TextEncoder();
  const events = [];
  const response = new Response(
    new ReadableStream({
      async start(controller) {
        controller.enqueue(encoder.encode('event: meta\ndata: {"provider":"openai"}\n\n'));
        await new Promise((resolve) => setTimeout(resolve, 45));
        controller.enqueue(encoder.encode('event: delta\ndata: {"delta":"First visible part"}\n\n'));
        await new Promise((resolve) => setTimeout(resolve, 70));
        controller.enqueue(encoder.encode('event: delta\ndata: {"delta":" then later"}\n\n'));
        await new Promise((resolve) => setTimeout(resolve, 45));
        controller.enqueue(encoder.encode('event: done\ndata: {"provider":"openai"}\n\n'));
        controller.close();
      },
    }),
  );
  await readCoachStream(response, (event) => events.push({ ...event, at: Date.now() }));
  const firstDelta = events.find((event) => event.type === "delta");
  const done = events.find((event) => event.type === "done");
  assert.equal(firstDelta?.delta, "First visible part");
  assert.ok(done && firstDelta && firstDelta.at < done.at, "first delta arrives before done");
  assert.equal(events.filter((event) => event.type === "delta").map((event) => event.delta).join(""), "First visible part then later");
});

test("coach replies render safe structured text with readable code and lists", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /function CoachReply/);
  assert.match(page, /coachInline/);
  assert.match(page, /<h3 key=/);
  assert.match(page, /<ol key=/);
  assert.match(page, /<ul key=/);
  assert.match(page, /coach-code-block/);
  assert.match(page, /navigator\.clipboard\?\.writeText/);
  assert.match(page, /<CoachReply text=\{message\.text\}/);
  assert.match(page, /role="log"\s+aria-live="polite"\s+aria-relevant="additions text"/);
  assert.doesNotMatch(page, /dangerouslySetInnerHTML/);
  assert.doesNotMatch(page, /<a href=\{text/);
  assert.doesNotMatch(page, /<img src=\{text/);
  assert.match(styles, /\.coach-reply/);
  assert.match(styles, /\.coach-code-block/);
  assert.match(styles, /font-size:14px;line-height:1\.6/);
  assert.match(styles, /font:12px\/1\.55/);
  assert.match(styles, /overflow-wrap:anywhere/);
  assert.match(styles, /overflow:auto/);
  assert.match(styles, /\.message\.you/);
});

test("accepted submissions have optional, motion-aware visual celebrations", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  assert.match(page, /function SuccessCelebration/);
  assert.match(page, /celebratedWorkflowRef/);
  assert.match(page, /celebrateSuccess\(workflow\)/);
  assert.match(page, /kitcode:success-celebrations/);
  assert.match(page, /function readCelebrationPreference/);
  assert.match(page, /celebrationsEnabledRef/);
  assert.match(page, /current\?\.id === celebrationId/);
  assert.match(page, /setCelebration\(null\);\s+setRunResult/);
  assert.match(page, /Celebrate accepted solutions/);
  assert.match(page, /All tests passed/);
  assert.match(page, /Accepted · all tests passed/);
  assert.match(page, /key=\{celebration\.id\}/);
  assert.match(styles, /pointer-events:none/);
  assert.match(styles, /z-index:6/);
  assert.match(styles, /--dx/);
  assert.doesNotMatch(styles, /var\(--particle\) %/);
  assert.match(styles, /prefers-reduced-motion:reduce/);
  assert.match(styles, /\.success-celebration\.stars/);
});

test("KitCode offers one removable, motion-aware Kit mascot", async () => {
  const [page, styles, sequenceBuilder] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
    readFile(new URL("scripts/build_mascot_sequence_assets.py", projectRoot), "utf8"),
  ]);
  assert.doesNotMatch(page, /type MascotStyle/);
  assert.doesNotMatch(page, /\bmascotOptions\b/);
  assert.doesNotMatch(page, /kitcode:mascot-style/);
  assert.doesNotMatch(page, /readMascotStylePreference|setMascotStylePreference|mascotStyle/);
  assert.doesNotMatch(page, /Choose Kit's illustration style|name="mascot-style"/);
  assert.doesNotMatch(page, /\bmascotDemo\b|\bsetMascotDemo\b/);
  assert.doesNotMatch(page, /mascot-motion-controls|Preview Kit's animations/);
  for (const preview of [
    "Preview answer hunt",
    "Preview tail-wag",
    "Preview correct answer",
    "Preview nap",
    "Preview surprise",
  ])
    assert.ok(!page.includes(preview), `${preview} is not exposed as a manual control`);
  for (const [name, asset] of [
    ["Storybook", "kit-storybook.webp"],
    ["Paper cut", "kit-paper.webp"],
    ["Playful", "kit-playful.webp"],
    ["Retro print", "kit-retro.webp"],
    ["Minimal", "kit-minimal.webp"],
  ]) {
    assert.ok(!page.includes(name), `${name} is not offered as an alternate Kit style`);
    assert.ok(!page.includes(asset), `${asset} is not referenced by the UI source`);
  }
  assert.match(page, /type MascotMotionRegistration = \{\s*scale: number;\s*translateX\?: number;\s*translateY\?: number;\s*\}/);
  const registrationBlock = page.match(
    /const chibiMotionRegistration = \{([\s\S]*?)\n\} as const satisfies Record<MascotMotion, MascotMotionRegistration>;/,
  )?.[1];
  assert.ok(registrationBlock, "chibi motion registration is declared exhaustively");
  const registrations = [...registrationBlock.matchAll(
    /^ {2}(idle|hunting|complete|happy|sleeping|waking|surprised): \{ scale: ([\d.]+)(?:, translateX: (-?[\d.]+))?(?:, translateY: (-?[\d.]+))? \},$/gm,
  )].map(([, motion, scale, translateX, translateY]) => [
    motion,
    Number(scale),
    Number(translateX ?? 0),
    Number(translateY ?? 0),
  ]);
  assert.deepEqual(registrations, [
    ["idle", 0.968, 0, -3.2227],
    ["hunting", 1.08036, 0, 0],
    ["complete", 0.968, 0, -3.2227],
    ["happy", 1.08036, 0, 0],
    ["sleeping", 1.34444, 0, 0],
    ["waking", 1.08036, 0, 0],
    ["surprised", 1, 0, -1.7578],
  ], "every MascotMotion has its canonical chibi scale and registration offset");
  assert.match(page, /function KitMascot/);
  assert.match(page, /kitcode:mascot-enabled/);
  assert.match(page, /function readMascotPreference/);
  assert.match(page, /function setMascotPreference\(enabled: boolean\)/);
  assert.match(page, /if \(!enabled\) \{[\s\S]*?setMascotMoment\(null\);/);
  assert.match(page, /checked=\{mascotEnabled\}/);
  assert.match(page, /setMascotPreference\(event\.target\.checked\)/);
  assert.match(page, /\{mascotEnabled && !settingsOpen && !fundamentalsActive && \(\s*<div[\s\S]*?className=\{`kit-floating/);
  assert.match(page, /<KitMascot[\s\S]*?size="floating"[\s\S]*?motion=\{coachMascotMotion\}/);
  assert.doesNotMatch(page, /size="rail"/);
  assert.doesNotMatch(page, /size="coach"/);
  assert.match(
    page,
    /\{mascotEnabled && \(\s*<KitMascot\s+size="settings"\s*\/>\s*\)\}/,
    "settings shows the single static Kit only while the mascot is enabled",
  );
  assert.match(page, /className=\{`kit-floating\$\{mascotDragging \? " is-dragging" : ""\}`\}/);
  assert.match(page, /const defaultMascotPosition: MascotPosition = \{\s*x:\s*75,\s*y:\s*50\s*\}/);
  assert.match(page, /kitcode:mascot-position-v1/);
  assert.match(page, /function readMascotPositionPreference\(\): MascotPosition/);
  assert.match(page, /function clampMascotPosition\(position: MascotPosition\): MascotPosition/);
  assert.match(page, /const mascotHalfSize = 105/);
  assert.match(page, /const edgeGap = 8/);
  assert.match(page, /window\.addEventListener\("resize", keepMascotVisible\)/);
  assert.match(page, /function positionMascotFromPointer\(clientX: number, clientY: number\)/);
  assert.match(page, /function persistMascotPosition\(position: MascotPosition\)/);
  assert.match(page, /onPointerDown=\{\(event\) => \{[\s\S]*?setPointerCapture\(event\.pointerId\)[\s\S]*?event\.preventDefault\(\)/);
  assert.match(page, /onPointerMove=\{\(event\) => \{[\s\S]*?positionMascotFromPointer\(event\.clientX, event\.clientY\)/);
  assert.match(page, /onPointerUp=\{\(event\) => \{[\s\S]*?releasePointerCapture\(event\.pointerId\)[\s\S]*?persistMascotPosition\(position\)/);
  assert.match(page, /onPointerCancel=\{\(event\) => \{[\s\S]*?releasePointerCapture\(event\.pointerId\)/);
  assert.match(page, /Ask Kit for a hint or drag Kit to reposition/);
  assert.match(page, /event\.key === "ArrowLeft"[\s\S]*?event\.key === "ArrowRight"[\s\S]*?event\.key === "ArrowUp"[\s\S]*?event\.key === "ArrowDown"/);
  assert.match(page, /Show Kit in the workspace/);
  assert.match(page, /coachBusy\s*\?\s*"hunting"/);
  assert.match(page, /showMascotComplete\(\)/);
  assert.match(page, /function showMascotHappy\(\)/);
  assert.match(page, /motion === "hunting" \|\|\s*motion === "sleeping" \|\|\s*motion === "happy" \|\|\s*motion === "waking"/);
  assert.match(page, /mascotSequenceManifest\[sequenceMotion\]/);
  assert.match(page, /(?:const usesSurpriseFrame = )?motion === "surprised"/);
  assert.match(page, /function showMascotSurprised\(\)/);
  assert.match(page, /const mascotIdleSleepDelay = 15_?000/);
  assert.match(page, /if \(!result\.ok\) showMascotSurprised\(\)/);
  assert.match(page, /celebrateSuccess\(workflow\);\s*showMascotLessonSleep\(\)/);
  const lessonCompleteBody = page.match(
    /function showMascotLessonSleep\(\) \{([\s\S]*?)\n {2}\}\n {2}async function submitCode/,
  )?.[1];
  assert.ok(lessonCompleteBody, "the accepted-lesson mascot reaction is defined");
  assert.match(
    lessonCompleteBody,
    /showMascotHappy\(\);[\s\S]*?resetMascotIdleRef\.current\(\);/,
    "an accepted answer leaves Kit happy and refreshes its real inactivity window",
  );
  assert.doesNotMatch(
    lessonCompleteBody,
    /(?:setTimeout|motion:\s*"sleeping"|setMascotSleeping\(true\))/,
    "accepting an answer must not schedule a short auto-sleep handoff",
  );
  assert.match(page, /type MascotSequenceMotion = Extract</);
  assert.match(page, /type MascotSequenceFrame = \{\s*src: string;\s*duration: number;\s*translateX\?: number;\s*translateY\?: number;\s*scale\?: number;\s*shadowScale\?: number;/);
  assert.match(page, /type MascotSequence = \{\s*frames: readonly MascotSequenceFrame\[\];\s*restIndex: number;/);
  assert.match(page, /mascotSequenceManifest/);
  assert.match(page, /satisfies Record<MascotSequenceMotion, MascotSequence>/);
  assert.match(page, /function MascotSequencePlayer/);
  assert.match(page, /window\.matchMedia\("\(prefers-reduced-motion: reduce\)"\)/);
  assert.match(
    page,
    /function MascotSequencePlayer[\s\S]*?timer = window\.setTimeout[\s\S]*?sequence\.frames\[currentIndex\]\.duration[\s\S]*?return \(\) => \{\s*cancelled = true;\s*if \(timer !== undefined\) window\.clearTimeout\(timer\);/,
  );
  assert.match(page, /const activeIndex = reducedMotion \? sequence\.restIndex : frameIndex/);
  assert.match(page, /const activeFrame = sequence\.frames\[activeIndex\]/);
  assert.match(page, /"--kit-frame-y": `\$\{activeFrame\.translateY \?\? 0\}%`/);
  assert.match(page, /"--kit-frame-scale": activeFrame\.scale \?\? 1/);
  assert.match(page, /className={`kit-sequence-player\$\{activeIndex === sequence\.restIndex \? " is-rest-frame"/);
  assert.match(page, /<span className="kit-sequence-stage">/);
  assert.match(page, /(?:const motionRegistration(?:: MascotMotionRegistration)? =\s*)?chibiMotionRegistration\[motion\]/);
  assert.match(page, /"--kit-motion-x": `\$\{motionRegistration\.translateX \?\? 0\}%`/);
  assert.match(page, /"--kit-motion-y": `\$\{motionRegistration\.translateY \?\? 0\}%`/);
  assert.match(page, /"--kit-motion-scale": motionRegistration\.scale/);
  assert.match(
    page,
    /<span className="kit-motion-stage" style=\{motionStyle\}>[\s\S]*?<MascotSequencePlayer/,
    "the motion registration wraps every animated sequence",
  );
  assert.doesNotMatch(page, /kit-dive-/);
  assert.doesNotMatch(page, /kit-sleep-yawn\.webp/);
  assert.doesNotMatch(page, /kit-(?:hunt|sleep)-09\.webp|kit-happy-08\.webp/);
  assert.match(styles, /\.kit-mascot\.is-hunting/);
  assert.match(styles, /\.kit-mascot\.is-happy/);
  assert.match(styles, /\.kit-mascot\.is-sleeping/);
  assert.match(styles, /\.kit-mascot\.is-surprised/);
  assert.match(styles, /\.kit-mascot\.is-complete/);
  assert.match(
    styles,
    /\.kit-motion-stage\{position:absolute;z-index:1;inset:0;transform-origin:50% 94\.53125%;transform:translate\(var\(--kit-motion-x,0\),var\(--kit-motion-y,0\)\) scale\(var\(--kit-motion-scale,1\)\)\}/,
    "the shared motion registration is ground-anchored",
  );
  assert.match(
    styles,
    /\.kit-sequence-stage\{transform:translate\(var\(--kit-frame-x,0\),var\(--kit-frame-y,0\)\) scale\(var\(--kit-frame-scale,1\)\);transition:transform 90ms linear\}/,
    "frame motion remains a composed inner transform rather than replacing canonical scale",
  );
  assert.match(styles, /\.kit-floating\{position:fixed;z-index:16;width:210px;height:210px;transform:translate\(-50%,-50%\);touch-action:none;user-select:none;cursor:grab/);
  assert.match(styles, /\.kit-floating\.is-dragging\{cursor:grabbing;z-index:17\}/);
  assert.match(styles, /@media\(max-width:560px\)\{[\s\S]*?\.kit-floating\{width:180px;height:180px\}/);
  assert.match(styles, /\.kit-mascot\.is-hunting \.kit-sequence-player\.is-rest-frame/);
  assert.match(styles, /\.kit-mascot\.is-sleeping \.kit-sequence-player\.is-rest-frame/);
  assert.match(
    styles,
    /\.kit-mascot\.is-sleeping \.kit-sequence-player\.is-rest-frame\{animation:kit-sleep-breathe 4\.4s ease-in-out infinite\}/,
    "only the final settled sleep frame may breathe",
  );
  assert.doesNotMatch(
    styles,
    /\.kit-mascot\.is-sleeping \.kit-sequence-(?:stage|frame)\{[^}]*kit-sleep-breathe/,
    "transition frames must remain registered instead of breathing independently",
  );
  assert.match(
    styles,
    /@keyframes kit-sleep-breathe\{0%,100%\{filter:brightness\(1\)\}50%\{filter:brightness\(\.985\)\}\}/,
    "the settled breathing cue must not move or scale Kit",
  );
  const sleepBreathing = styles.match(/@keyframes kit-sleep-breathe\{[^}]+\}50%\{[^}]+\}\}/)?.[0];
  assert.ok(sleepBreathing, "sleep breathing keyframes are declared");
  assert.doesNotMatch(sleepBreathing, /(?:transform|scale|translate)/);
  assert.match(styles, /\.kit-mascot\.is-happy \.kit-jump-shadow\{display:block\}/);
  assert.match(styles, /\.kit-mascot\.is-happy \.kit-jump-shadow\{display:none\}/);
  assert.match(styles, /@keyframes kit-happy-wag/);
  assert.match(styles, /@keyframes kit-surprise/);
  const sequenceAssets = [
    ...Array.from({ length: 8 }, (_, index) =>
      `kit-hunt-${String(index + 1).padStart(2, "0")}.webp`,
    ),
    ...Array.from({ length: 8 }, (_, index) =>
      `kit-sleep-${String(index + 1).padStart(2, "0")}.webp`,
    ),
    ...Array.from({ length: 7 }, (_, index) =>
      `kit-happy-${String(index + 1).padStart(2, "0")}.webp`,
    ),
  ];
  assert.equal(sequenceAssets.filter((asset) => asset.startsWith("kit-hunt-")).length, 8);
  assert.equal(sequenceAssets.filter((asset) => asset.startsWith("kit-sleep-")).length, 8);
  assert.equal(sequenceAssets.filter((asset) => asset.startsWith("kit-happy-")).length, 7);
  const sleepingManifest = page.match(
    /const mascotSequenceManifest = \{[\s\S]*?sleeping:\s*\{[\s\S]*?\n\s*restIndex: 7,/,
  )?.[0];
  assert.ok(sleepingManifest, "sleeping rests only after all eight registered poses");
  const compactSleepingManifest = sleepingManifest.replace(/\s+/g, " ");
  const sleepFrameTaper = [
    ["01", 420, 0, 1],
    ["02", 400, 0, 1],
    ["03", 400, 0.74, 0.93],
    ["04", 400, 2.53, 0.76],
    ["05", 400, 2.32, 0.78],
    ["06", 400, 2.64, 0.75],
    ["07", 450, 2.95, 0.72],
    ["08", 2330, 1.9, 0.82],
  ];
  for (const [index, duration, translateY, scale] of sleepFrameTaper) {
    const expectedFrame =
      scale === 1
        ? `kit-sleep-${index}.webp", duration: ${duration} }`
        : `kit-sleep-${index}.webp", duration: ${duration}, translateY: ${translateY}, scale: ${scale}, }`;
    assert.ok(
      compactSleepingManifest.includes(expectedFrame),
      `sleep frame ${index} retains its grounded natural-size registration`,
    );
  }
  assert.equal(
    sleepFrameTaper[0][3],
    1,
    "the first seated frame keeps the established full body size",
  );
  assert.equal(
    sleepFrameTaper[1][3],
    1,
    "the drowsy seated frame keeps the established full body size",
  );
  assert.ok(
    sleepFrameTaper.slice(2).every(([, , translateY, scale]) => scale < 1 && translateY > 0),
    "only the turning/curl poses shrink around the shared ground anchor",
  );
  assert.equal(
    1.34444 * sleepFrameTaper[6][3],
    0.9679968,
    "the deepest tuck composes with the global sleep registration back to Kit's idle-scale body",
  );
  const sleepSequenceBlock = sequenceBuilder.match(
    /"sleep": \[([\s\S]*?)\n {4}\],/,
  )?.[1];
  assert.ok(sleepSequenceBlock, "the sprite builder declares the eight sleep source poses");
  const sleepSourceStems = [...sleepSequenceBlock.matchAll(/"([^"]+)",/g)].map(([, stem]) => stem);
  assert.equal(sleepSourceStems[3], "kit-sleep-settle-right", "frame four keeps Kit's tail on the viewer-right");
  assert.ok(!sleepSourceStems.includes("kit-sleep-settle"), "the left-tail settle source cannot return to the sleep sequence");
  const targetHeightBlock = sequenceBuilder.match(
    /SLEEP_TARGET_HEIGHTS = \{([\s\S]*?)\n\}/,
  )?.[1];
  assert.ok(targetHeightBlock, "the curl registration has explicit target heights");
  assert.deepEqual(
    [...targetHeightBlock.matchAll(/"([^"]+)": (\d+),/g)].map(([, stem, height]) => [stem, Number(height)]),
    [
      ["kit-chibi", 360],
      ["kit-sleep-drowsy", 360],
      ["kit-sleep-nod", 360],
      ["kit-sleep-settle-right", 360],
      ["kit-sleep-lower", 360],
      ["kit-sleep-nestle", 360],
      ["kit-sleep-tuck", 360],
      ["kit-sleep-curled", 360],
    ],
    "every sleep pose is rendered at the same 360px visible height",
  );
  const offsetBlock = sequenceBuilder.match(
    /SLEEP_OFFSETS = \{([\s\S]*?)\n\}/,
  )?.[1];
  assert.ok(offsetBlock, "the curl registration has intentional positional offsets");
  assert.deepEqual(
    [...offsetBlock.matchAll(/"([^"]+)": \((-?\d+), (-?\d+)\),/g)].map(
      ([, stem, x, y]) => [stem, Number(x), Number(y)],
    ),
    [
      ["kit-chibi", 0, 0],
      ["kit-sleep-drowsy", 0, 0],
      ["kit-sleep-nod", 0, 0],
      ["kit-sleep-settle-right", 5, 0],
      ["kit-sleep-lower", 25, 0],
      ["kit-sleep-nestle", -25, 0],
      ["kit-sleep-tuck", 5, 0],
      ["kit-sleep-curled", -3, 0],
    ],
    "all sleep poses retain their ground anchor; only horizontal registration is allowed",
  );
  assert.match(
    sequenceBuilder,
    /target_height \/ subject\.height[\s\S]*?SLEEP_OFFSETS\.get\(stem, \(0, 0\)\)/,
    "the builder applies registration instead of independently fitting each curl silhouette",
  );
  const happyManifest = page.match(
    /happy:\s*\{[\s\S]*?\n\s*restIndex: 6,/,
  )?.[0];
  assert.ok(happyManifest, "happy sequence is declared with a settled rest frame");
  const happyFrames = [
    ...happyManifest.matchAll(
      /\{\s*src: "\/mascots\/kit-happy-\d+\.webp",[\s\S]*?shadowScale: [\d.]+,\s*\}/g,
    ),
  ].map(([frame]) => ({
    duration: Number(frame.match(/duration: (\d+)/)?.[1]),
    translateY: Number(frame.match(/translateY: (-?\d+)/)?.[1]),
  }));
  assert.equal(happyFrames.length, 7, "the correct-answer jump keeps all seven poses");
  assert.equal(happyFrames[0].translateY, 0, "the jump begins on the ground");
  assert.ok(
    Math.min(...happyFrames.map((frame) => frame.translateY)) <= -25,
    "the happy jump has a visibly high apex rather than a bottom-anchored pose swap",
  );
  assert.equal(happyFrames.at(-1).translateY, 0, "reduced motion settles on ground level");
  assert.equal(
    happyFrames.reduce((total, frame) => total + frame.duration, 0),
    2400,
    "the happy sequence completes before the lesson-sleep handoff",
  );
  for (const asset of sequenceAssets) {
    assert.ok(page.includes(asset), `${asset} is declared in the mascot sequence manifest`);
  }
  for (const asset of [
    "kit-chibi.webp",
    "kit-surprised.webp",
    ...sequenceAssets,
  ]) {
    const assetUrl = new URL(`public/mascots/${asset}`, projectRoot);
    await access(assetUrl);
    assert.ok((await stat(assetUrl)).size > 0, `${asset} is nonempty`);
  }
});

test("Kit activates the same safe hint request as the coach quick action without confusing a drag for a click", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");

  assert.match(
    page,
    /const mascotDragStartRef = useRef<[\s\S]*?pointerId: number;[\s\S]*?x: number;[\s\S]*?y: number;[\s\S]*?moved: boolean;[\s\S]*?\| null>\(null\);/,
    "Kit records where a press began so a repositioning gesture is not activated as a hint",
  );
  assert.match(
    page,
    /const mascotDragThreshold = \d+;/,
    "Kit uses an explicit movement threshold before treating a press as a drag",
  );
  assert.match(
    page,
    /onPointerDown=\{\(event\) => \{[\s\S]*?mascotDragStartRef\.current = \{[\s\S]*?pointerId: event\.pointerId,[\s\S]*?x: event\.clientX,[\s\S]*?y: event\.clientY,[\s\S]*?moved: false,[\s\S]*?setPointerCapture\(event\.pointerId\)/,
    "the pointer origin is captured before Kit begins following the pointer",
  );
  assert.match(
    page,
    /onPointerMove=\{\(event\) => \{[\s\S]*?drag\.pointerId !== event\.pointerId[\s\S]*?Math\.hypot\([\s\S]*?distance < mascotDragThreshold[\s\S]*?drag\.moved = true;[\s\S]*?setMascotDragging\(true\)[\s\S]*?positionMascotFromPointer\(event\.clientX, event\.clientY\)/,
    "only movement beyond the threshold becomes a drag",
  );
  assert.match(
    page,
    /onPointerUp=\{\(event\) => \{[\s\S]*?const wasDragging =[\s\S]*?drag\.moved \|\|[\s\S]*?Math\.hypot\([\s\S]*?mascotDragThreshold[\s\S]*?persistMascotPosition\(position\);[\s\S]*?else \{[\s\S]*?requestHint\(\);/,
    "a short click or tap invokes requestHint, while a completed drag only persists Kit's position",
  );
  const pointerCancelHandler = page.match(
    /onPointerCancel=\{\(event\) => \{([\s\S]*?)\}\}\s*onKeyDown=/,
  )?.[1];
  assert.ok(pointerCancelHandler, "Kit has a dedicated pointer-cancellation handler");
  assert.match(pointerCancelHandler, /mascotDragStartRef\.current = null;/);
  assert.match(pointerCancelHandler, /setMascotDragging\(false\)/);
  assert.match(pointerCancelHandler, /releasePointerCapture\(event\.pointerId\)/);
  assert.doesNotMatch(pointerCancelHandler, /requestHint\(/, "cancelling a gesture must never request a hint");
  assert.match(
    page,
    /onKeyDown=\{\(event\) => \{[\s\S]*?event\.key === "Enter" \|\| event\.key === " "[\s\S]*?event\.preventDefault\(\);[\s\S]*?requestHint\(\);/,
    "keyboard Enter and Space activate Kit accessibly",
  );
  assert.match(
    page,
    /Ask Kit for a hint or drag Kit to reposition/,
  );
  assert.match(
    page,
    /coachReady && !coachBusy[\s\S]*?Ask Kit for a hint or drag Kit to reposition[\s\S]*?Hints are available when AI coaching is ready/,
    "Kit exposes its matching hint availability without disabling repositioning",
  );
  assert.match(
    page,
    /function requestHint\(\) \{\s*if \(coachBusyRef\.current \|\| !coachReady \|\| coachSubmitRef\.current\) return;/,
    "Kit calls the guarded shared hint action, so unavailable and busy states behave like the quick action",
  );
  const requestHintBody = page.match(
    /function requestHint\(\) \{([\s\S]*?)\n {2}\}\n {2}function restartCoachResponse/,
  )?.[1];
  assert.ok(requestHintBody, "Kit's shared hint action is defined directly in the client");
  assert.match(
    requestHintBody,
    /const snapshot = buildCoachSnapshot\([\s\S]*?dispatchCoachAction\(snapshot\);/,
    "a hint request is dispatched in the same synchronous activation path",
  );
  assert.doesNotMatch(
    requestHintBody,
    /(?:await|setTimeout|requestAnimationFrame|mascot(?:Moment|Sleeping|Wake)|waking)/,
    "Kit never waits for a mascot animation or client-side delay before the hint request begins",
  );
  assert.match(
    page,
    /<button[\s\S]*?onClick=\{requestHint\}[\s\S]*?disabled=\{!coachReady \|\| coachBusy \|\| coachRestarting\}/,
    "the quick-action button retains the matching public availability contract",
  );
});

test("Kit sleeps promptly while the workspace is inactive and only wakes after a returning click", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);

  assert.match(
    page,
    /const mascotIdleTimerRef = useRef<number \| null>\(null\);/,
    "Kit owns a clearable inactivity timer",
  );
  assert.match(
    page,
    /const mascotIdleSleepDelay = 15_?000;[\s\S]*?window\.setTimeout\([\s\S]*?putMascotToSleep\(false\)[\s\S]*?mascotIdleSleepDelay/,
    "ordinary in-window inactivity puts Kit to sleep after about fifteen seconds",
  );
  assert.match(
    page,
    /document\.addEventListener\([\s\S]*?"visibilitychange",[\s\S]*?handleMascotVisibilityChange,[\s\S]*?\);/,
    "switching away from the tab is an explicit sleep signal",
  );
  assert.match(
    page,
    /window\.addEventListener\("blur",\s*[^)]+\)/,
    "losing the active window is an explicit sleep signal",
  );
  assert.match(
    page,
    /document\.hidden[\s\S]*?scheduleInactiveWindowSleep\(\)/,
    "a hidden tab continues Kit's fifteen-second inactivity deadline",
  );
  assert.match(
    page,
    /mascot\w*(?:Wake|WakeOn|Window)[\w]*Ref\.current\s*=\s*true/,
    "returning from an inactive window records that Kit must wait for an in-window click",
  );
  assert.match(
    page,
    /window\.addEventListener\("focus", handleMascotWindowFocus\)/,
    "focus itself does not wake Kit",
  );
  assert.match(
    page,
    /handleMascotPointerActivity[\s\S]*?mascotWakeRequiresClickRef\.current = false[\s\S]*?setMascotWindowInactive\(false\)[\s\S]*?scheduleMascotSleep\(\)/,
    "the first pointer press after returning wakes Kit and starts a new inactivity window",
  );
  assert.match(
    page,
    /removeEventListener\("pointerdown",[\s\S]*?removeEventListener\("blur", handleMascotWindowBlur\)[\s\S]*?removeEventListener\("focus", handleMascotWindowFocus\)[\s\S]*?removeEventListener\([\s\S]*?"visibilitychange"/,
    "unmount removes all focus and visibility listeners",
  );
  assert.match(
    styles,
    /\.kit-floating\{position:fixed;z-index:16;/,
    "the floating Kit sits above Monaco editor chrome while remaining beneath the modal layers",
  );
  assert.match(
    styles,
    /\.modal-backdrop\{[^}]*z-index:(?:[2-9]\d|1[7-9])/,
    "modal backdrops stay above Kit's interaction layer",
  );
});

test("Kit wakes through a short registered sequence only after an actual waking click", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");

  const wakingManifest = page.match(
    /waking:\s*\{[\s\S]*?\n\s*restIndex: 2,/,
  )?.[0];
  assert.ok(wakingManifest, "waking uses two new poses before its reduced-motion seated rest pose");
  const wakingFrames = [
    ...wakingManifest.matchAll(
      /\{\s*src: "(\/mascots\/kit-wake-\d+\.webp)",\s*duration: (\d+)[^}]*\}/g,
    ),
  ];
  assert.equal(wakingFrames.length, 2, "Kit has exactly two new wake-up drawings");
  assert.deepEqual(
    wakingFrames.map(([, src]) => src),
    ["/mascots/kit-wake-01.webp", "/mascots/kit-wake-02.webp"],
    "the wake-up sequence is declared in order",
  );
  assert.ok(
    wakingFrames.every(([, , duration]) => Number(duration) >= 120 && Number(duration) <= 1000),
    "wake-up frames have deliberate visible timing",
  );
  assert.match(
    wakingManifest,
    /src: "\/mascots\/kit-chibi\.webp"[\s\S]*?restIndex: 2/,
    "the generated wake drawings settle into Kit's existing registered awake pose",
  );
  assert.match(
    page,
    /type MascotSequenceMotion = Extract<[\s\S]*?"waking"[\s\S]*?>;/,
    "the wake-up sequence is rendered by the same reduced-motion-aware player",
  );
  assert.match(
    page,
    /reducedMotion \? sequence\.restIndex : frameIndex/,
    "reduced motion immediately uses the settled wake pose",
  );

  for (const asset of ["kit-wake-01.webp", "kit-wake-02.webp"]) {
    const assetUrl = new URL(`public/mascots/${asset}`, projectRoot);
    await access(assetUrl);
    assert.ok((await stat(assetUrl)).size > 0, `${asset} is nonempty`);
  }

  const pointerActivity = page.match(
    /const handleMascotPointerActivity = \(\) => \{([\s\S]*?)\n\s*\};\n\s*const handleMascotKeyboardActivity/,
  )?.[1];
  assert.ok(pointerActivity, "the wake transition is decided from pointer activity");
  assert.match(
    pointerActivity,
    /if \(mascotWakeRequiresClickRef\.current\)[\s\S]*?mascotWakeRequiresClickRef\.current = false[\s\S]*?motion: "waking"/,
    "the first returning click clears the click gate and begins waking Kit",
  );
  assert.doesNotMatch(
    pointerActivity,
    /\n\s*setMascotMoment\(\{[\s\S]*?motion: "waking"[\s\S]*?\n\s*\}\);\s*\n\s*scheduleMascotSleep/,
    "ordinary pointer activity while Kit is already awake must not replay the wake sequence",
  );
  assert.match(
    page,
    /const handleMascotKeyboardActivity = \(\) => \{\s*if \(mascotWakeRequiresClickRef\.current\) return;/,
    "keyboard activity after returning focus still cannot wake Kit",
  );
  assert.match(
    page,
    /mascotMoment\?\.motion === "waking"\s*\?\s*\d+/,
    "the wake moment has a bounded timer",
  );
  assert.match(
    page,
    /window\.clearTimeout\(timer\)/,
    "the wake moment timer is cleared when the component or moment changes",
  );
});

test("adaptive coach offers a non-mutating editor hint workflow", async () => {
  const [page, styles] = await Promise.all([readFile(new URL("app/page.tsx", projectRoot), "utf8"), readFile(new URL("app/globals.css", projectRoot), "utf8")]);
  assert.match(page, /\/api\/ai\/editor-hint/);
  assert.match(page, /Give me a hint/);
  assert.doesNotMatch(page, /coachMode/);
  assert.doesNotMatch(page, /mode: "explain"/);
  assert.match(page, /mode:\s+snapshot\.intent === "hint"\s+\? "editor_hint"\s+: snapshot\.intent === "edit"\s+\? "editor_edit"\s+: "adaptive"/);
  assert.match(page, /history: snapshot\.history/);
  assert.match(page, /filter\(\(message\) => message\.contextual\)\s+\.slice\(-8\)/);
  assert.match(page, /dispatchCoachAction\(snapshot\)/);
  assert.match(page, /hasCoachConsent\(snapshot\.providerIdentity\)/);
  assert.match(page, /pendingCoachSnapshotRef/);
  assert.match(page, /coachGenerationRef/);
  assert.match(page, /coachAbortRef/);
  assert.match(page, /coachSnapshotIsCurrent/);
  assert.match(page, /model\?\.getVersionId\(\)/);
  assert.match(page, /coachRuntimeIdentity\(aiStatusRef\.current\)/);
  assert.match(page, /expected_provider: snapshot\.expectedProvider/);
  assert.match(page, /expected_model: snapshot\.expectedModel/);
  assert.match(page, /expected_base_url: snapshot\.expectedBaseUrl/);
  assert.match(page, /const coachReady = Boolean\(\s*!fundamentalsActive &&\s+aiStatus\.configured &&\s+draftReady/);
  assert.match(page, /setDraftReady\(false\);\s+draftExerciseRef\.current = ""/);
  assert.match(page, /hintDecorationRef/);
  assert.match(page, /editor-hint-inline/);
  assert.match(page, /hintViewZoneRef/);
  assert.match(page, /accessor\.addZone\(\{/);
  assert.match(page, /function readInlineHintPreference\(\)[\s\S]*?localStorage\.getItem\("kitcode:inline-hints"\) !== "off"/);
  assert.match(page, /const \[inlineHintsEnabled, setInlineHintsEnabled\] = useState\(\s*readInlineHintPreference/);
  assert.match(page, /localStorage\.setItem\(\s*"kitcode:inline-hints",\s*enabled \? "on" : "off"/);
  assert.match(page, /id="inline-hints"\s+type="checkbox"\s+checked=\{inlineHintsEnabled\}/);
  assert.match(page, /<label htmlFor="inline-hints">[\s\S]*?Show hints in the editor[\s\S]*?only in the card below your\s+code/);
  assert.match(page, /result\.structured !== true/);
  assert.match(page, /safeInlineHint\(result\.text \?\? result\.hint\)/);
  assert.match(page, /setEditorHint\(\{ id: \+\+hintSequenceRef\.current, line, text: hint, inline \}\)/);
  assert.match(page, /onChange=\{bestSolutionActive \? undefined : handleEditorChange\}/);
  assert.match(page, /function cancelCoachWork\(\s*resetConversation = false,\s+discardVisibleHint = false/);
  assert.match(page, /if \(discardVisibleHint\) setEditorHint\(null\)/);
  assert.match(page, /function handleEditorChange\(value\?: string\)[\s\S]*?coachActiveIntentRef\.current !== "hint"\) cancelCoachWork\(false\)[\s\S]*?setCode\(nextCode\)/);
  const editorChangeBody = page.slice(page.indexOf("function handleEditorChange"), page.indexOf("function undoEditorEdit"));
  assert.doesNotMatch(editorChangeBody, /setEditorHint\(null\)/);
  const resetBody = page.slice(page.indexOf("function resetCode"), page.indexOf("function startWorkflow"));
  assert.doesNotMatch(resetBody, /setEditorHint\(null\)/);
  assert.match(page, /function selectExercise\(exerciseId: string\)[\s\S]*?cancelCoachWork\(true, true\)/);
  assert.doesNotMatch(page, /function requestHint\(\).*clearEditorHint\(\)/);
  assert.match(page, /\{!bestSolutionActive && editorHint && \(\s*<div[\s\S]*?className="editor-hint-card"/);
  assert.match(page, /className="editor-hint-card"\s+role="status"/);
  assert.match(page, /clearEditorHint\(\);\s+editorRef\.current\?\.focus\(\)/);
  assert.match(page, />\s*Dismiss\s*<\/button>/);
  assert.match(page, /consentFocusTargetRef/);
  assert.match(page, /recent\s+current-drill conversation messages/);
  assert.doesNotMatch(page, /setEditorHint\(String\(result\.text/);
  assert.match(styles, /\.coach-quick-actions/);
  assert.match(styles, /\.editor-hint-inline/);
  assert.match(styles, /\.editor-hint-card/);
  assert.match(styles, /forced-colors:active/);
});

test("coach keeps completed hints across edits and can retry a failed chat request", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  assert.match(page, /const coachDocumentRevisionRef = useRef\(0\)/);
  assert.match(page, /documentRevision: coachDocumentRevisionRef\.current/);
  assert.match(page, /coachDocumentRevisionRef\.current === snapshot\.documentRevision/);
  assert.match(page, /function coachResponseIsCurrent\([\s\S]*?snapshot\.intent === "hint"[\s\S]*?coachSnapshotMatchesScope/);
  assert.match(page, /function handleEditorChange\(value\?: string\)[\s\S]*?coachDocumentRevisionRef\.current \+= 1[\s\S]*?coachActiveIntentRef\.current !== "hint"/);
  assert.match(page, /Hint · based on an earlier draft/);
  assert.match(page, /if \(snapshot\.intent === "adaptive"\) setRetryCoachSnapshot\(snapshot\)/);
  assert.match(page, /function retryCoachQuestion\(\)[\s\S]*?dispatchCoachAction\(\{ \.\.\.snapshot, retry: true \}\)/);
  assert.match(page, /↻ Try again/);
  assert.match(page, /Retry the same question with the same saved context/);
});

test("coach recovers from submit, stop, and a genuinely stalled response", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);
  const workflowBody = page.slice(
    page.indexOf("function startWorkflow"),
    page.indexOf("function workflowIsCurrent"),
  );
  assert.doesNotMatch(
    workflowBody,
    /cancelCoachWork/,
    "Run and Submit must not silently kill an unrelated coach response",
  );
  assert.match(page, /const coachBrowserTimeoutMs = 70_000/);
  assert.match(page, /const coachActiveSnapshotRef = useRef<CoachRequestSnapshot \| null>\(null\)/);
  assert.match(
    page,
    /function settleStreamingCoachMessage\([\s\S]*?flushStreamingCoachMessage\(id\)[\s\S]*?coachStreamingMessageRef\.current = null/,
  );
  assert.match(
    page,
    /function cancelCoachWork\([\s\S]*?settleStreamingCoachMessage\([\s\S]*?Response stopped because the workspace changed/,
  );
  assert.match(
    page,
    /function stopCoachResponse\(\)[\s\S]*?interruptActiveCoach\([\s\S]*?Try again is ready[\s\S]*?true/,
  );
  assert.match(
    page,
    /function restartCoachResponse\(\)[\s\S]*?interruptActiveCoach\([\s\S]*?window\.setTimeout\([\s\S]*?dispatchCoachAction\(\{ \.\.\.retry, retry: true \}\)/,
  );
  assert.match(
    page,
    /const browserTimeout = window\.setTimeout\([\s\S]*?Coach timed out · Try again is ready[\s\S]*?coachBrowserTimeoutMs/,
  );
  assert.match(page, /aria-label="Stop and retry the same coach question"/);
  assert.match(
    page,
    /message\.id === streamingCoachMessageId[\s\S]*?streaming \? "Thinking…" : "Response stopped\."/,
  );
  assert.match(styles, /\.coach-compose \.coach-restart-button/);
});

test("a ready hint mounts a Monaco view zone only when inline hints are enabled", async () => {
  const page = await readFile(new URL("app/page.tsx", projectRoot), "utf8");
  const hintAnchor = page.indexOf("const line =\n      editorHint");
  assert.ok(hintAnchor >= 0, "the hint-decoration effect is present");
  const effectStart = page.lastIndexOf("useEffect(() => {", hintAnchor);
  const effectEnd = page.indexOf("  useEffect(() => {", hintAnchor);
  const hintEffect = page.slice(effectStart, effectEnd);

  assert.match(hintEffect, /removeHintViewZone\(\)/);
  assert.match(hintEffect, /inlineHintsEnabled && editorHint\?\.inline && model/);
  assert.match(hintEffect, /if \(!inlineHintsEnabled \|\| !editorHint\?\.inline \|\| !model\)/);
  assert.match(hintEffect, /hintNode\.className = "editor-hint-inline"/);
  assert.match(hintEffect, /hintText\.textContent = editorHint\.text/);
  assert.match(hintEffect, /hintNode\.append\(hintLabel, " ", hintText\)/);
  assert.match(hintEffect, /editor\.changeViewZones\(\(accessor\) => \{/);
  assert.match(hintEffect, /afterLineNumber: line/);
  assert.match(hintEffect, /zoneId = accessor\.addZone\(/);
  assert.match(hintEffect, /hintViewZoneRef\.current = \{ editor, id: zoneId \}/);
  assert.match(hintEffect, /editor\.layout\(\)/);
  assert.match(hintEffect, /editor\.render\(true\)/);
  assert.match(hintEffect, /\}, \[editorHint, editorMountVersion, inlineHintsEnabled\]\);/);
  assert.doesNotMatch(hintEffect, /onDidChangeModelContent|model\.getVersionId\(\)/);
  assert.match(page, /const \[editorMountVersion, setEditorMountVersion\] = useState\(0\)/);
  assert.match(page, /const onMount: OnMount = \(editor, monaco\) => \{[\s\S]*?hintDecorationRef\.current = \[\][\s\S]*?setEditorMountVersion\(\(version\) => version \+ 1\)/);
});

test("Python practice includes an optional 100-question fundamentals quiz", async () => {
  const [page, quiz, bank, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/python-fundamentals-quiz.tsx", projectRoot), "utf8"),
    import(new URL("app/python-fundamentals-questions.mjs", projectRoot)),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);

  assert.equal(bank.pythonFundamentalsQuestions.length, 100);
  assert.match(page, /type PythonPracticeSection = "coding" \| "fundamentals"/);
  assert.match(page, /kitcode:selected-python-section/);
  assert.match(page, /100 optional MCQs/);
  assert.match(page, /<PythonFundamentalsQuiz/);
  assert.match(page, /!fundamentalsActive &&\s+aiStatus\.configured/);
  assert.match(quiz, /100 common multiple-choice interview questions/);
  assert.match(quiz, /kitcode:python-fundamentals-progress-v1/);
  assert.match(quiz, /coding progress and drafts stay intact/);
  assert.match(quiz, /role="radiogroup"/);
  assert.match(quiz, /Check answer/);
  assert.match(quiz, /Next unanswered/);
  assert.match(quiz, /Review misses/);
  assert.match(styles, /\.practice-section-picker/);
  assert.match(styles, /\.fundamentals-workspace/);
  assert.match(styles, /\.fundamentals-option\.correct/);
});

test("an accepted submission opens a reviewed answer in a separate read-only editor tab", async () => {
  const [page, styles] = await Promise.all([
    readFile(new URL("app/page.tsx", projectRoot), "utf8"),
    readFile(new URL("app/globals.css", projectRoot), "utf8"),
  ]);

  assert.match(page, /type AcceptedSubmissionSnapshot = \{/);
  assert.match(page, /type EditorDocument = "learner" \| "reference"/);
  assert.match(
    page,
    /if \(accepted\) \{[\s\S]*?setAcceptedSubmission\(\{[\s\S]*?exerciseId: workflow\.exerciseId,[\s\S]*?language: workflow\.language,[\s\S]*?sqlDialect: workflow\.dialect \?\? "sqlite",[\s\S]*?code,/,
  );
  assert.match(
    page,
    /const referenceAnswerUnlocked = Boolean\([\s\S]*?acceptedSubmission\?\.exerciseId === selected[\s\S]*?acceptedSubmission\.code === code[\s\S]*?acceptedSubmission\.sqlDialect === sqlDialect/,
  );
  assert.match(
    page,
    /function handleEditorChange\(value\?: string\)[\s\S]*?acceptedSubmission\.code !== nextCode\)[\s\S]*?clearReferenceSolutionState\(\)/,
  );
  assert.match(
    page,
    /function selectExercise\(exerciseId: string\)[\s\S]*?clearReferenceSolutionState\(\)/,
  );
  assert.match(
    page,
    /function selectSqlDialect\(dialect: SqlDialect\)[\s\S]*?clearReferenceSolutionState\(\)/,
  );
  assert.match(page, /function submitCode\(\)[\s\S]*?startWorkflow\(true\)/);
  assert.match(
    page,
    /\/api\/exercises\/\$\{encodeURIComponent\(snapshot\.exerciseId\)\}\/reference-solution/,
  );
  assert.match(
    page,
    /body: JSON\.stringify\(\{[\s\S]*?code: snapshot\.code,[\s\S]*?language: snapshot\.language,[\s\S]*?sql_dialect: snapshot\.sqlDialect/,
  );
  assert.match(page, /language !== snapshot\.language/);
  assert.match(page, /payload\.exercise_id !== snapshot\.exerciseId/);
  assert.match(
    page,
    /payload\.review_policy_id !== "kitcode-reference-best-v1"/,
  );
  assert.match(page, /aria-labelledby="reference-answer-title"/);
  assert.match(page, /aria-busy=\{referenceSolutionLoading\}/);
  assert.match(
    page,
    /Submit <kbd>F6<\/kbd>[\s\S]*?referenceAnswerUnlocked[\s\S]*?className="best-answer-button"[\s\S]*?★ Best answer/,
  );
  assert.match(page, /function openBestSolution\(\)[\s\S]*?setEditorDocument\("reference"\)/);
  assert.match(
    page,
    /function showLearnerSolution\(\)[\s\S]*?learnerCodeBeforeReferenceRef\.current[\s\S]*?setCode\(preservedCode\)[\s\S]*?setEditorDocument\("learner"\)/,
  );
  assert.match(
    page,
    /function preserveLearnerSolution\(\)[\s\S]*?editorRef\.current\?\.getValue\(\) \?\? code/,
  );
  assert.match(page, /className="editor-file-tabs"[\s\S]*?role="tablist"/);
  assert.match(page, /id="learner-solution-tab"[\s\S]*?aria-selected=\{!bestSolutionActive\}/);
  assert.match(page, /id="best-solution-tab"[\s\S]*?aria-selected=\{bestSolutionActive\}/);
  assert.match(page, /\{bestSolutionFile\}[\s\S]*?<small>Read only<\/small>/);
  assert.match(
    page,
    /value=\{[\s\S]*?bestSolutionActive \? \(referenceSolution\?\.solution \?\? ""\) : code[\s\S]*?onChange=\{bestSolutionActive \? undefined : handleEditorChange\}/,
  );
  assert.match(page, /readOnly: bestSolutionActive/);
  assert.match(page, /domReadOnly: bestSolutionActive/);
  assert.doesNotMatch(page, /Your answer is safe in/);
  assert.match(page, /Best means target Big-O time and space first/);
  assert.match(page, /Time · space · clear lines/);
  assert.match(page, /referenceSolution\.expectedComplexity/);
  assert.match(page, /referenceSolution\.lineCount/);
  assert.match(page, /referenceSolution\.referenceDialect/);
  assert.match(page, /referenceSolution\.complexityNote/);
  assert.match(page, /provisional AI-created drill/);
  assert.match(page, /Open best answer tab/);
  assert.doesNotMatch(page, /<code>\{referenceSolution\.solution\}<\/code>/);
  assert.match(styles, /\.reference-answer/);
  assert.match(styles, /\.editor-file-tabs/);
  assert.match(styles, /\.best-solution-tab/);
  assert.match(styles, /\.best-answer-button/);
  assert.match(styles, /\.best-solution-banner/);
});

test("explicit editor-write requests are isolated, undoable, and visibly marked", async () => {
  const [page, styles] = await Promise.all([readFile(new URL("app/page.tsx", projectRoot), "utf8"), readFile(new URL("app/globals.css", projectRoot), "utf8")]);
  assert.match(page, /function requestsEditorEdit/);
  assert.match(page, /\/api\/ai\/editor-edit/);
  assert.match(page, /requestsEditorEdit\(question\) \? "edit" : "adaptive"/);
  assert.match(page, /setPendingEditorEdit\(\{\s+id: \+\+editSequenceRef\.current/);
  assert.match(page, /function applyPendingEditorEdit\(\)[\s\S]*?editor\.pushUndoStop\(\)[\s\S]*?editor\.executeEdits/);
  assert.match(page, /model\.getValue\(\) !== edit\.before/);
  assert.match(page, /Exact complete \$\{activeLanguage\.label\} script proposed by AI/);
  assert.match(page, /AI output is untrusted: review it before\s+applying/);
  assert.match(page, />\s*Apply AI edit\s*<\/button>/);
  assert.match(page, />\s*Discard\s*<\/button>/);
  assert.match(page, />\s*Undo AI edit\s*<\/button>/);
  assert.match(page, />\s*Clear highlight\s*<\/button>/);
  assert.match(page, /AI-applied code/);
  assert.match(page, /editorEdit\?\.ranges/);
  assert.match(page, /setEditorEdit\(null\)/);
  assert.match(page, /pendingCoachIntent === "edit"/);
  assert.match(page, /the provider may propose\s+replacement \{activeLanguage\.label\} for the complete editor/);
  assert.match(page, /applyingEditorEditRef/);
  assert.match(page, /editDecorationRef/);
  assert.match(styles, /\.ai-edit-highlight/);
  assert.match(styles, /\.editor-edit-card/);
  assert.match(styles, /#c58cff/);
});
