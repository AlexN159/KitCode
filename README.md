# KitCode Interview Studio

KitCode is a local-first Python, Java, and SQL interview-practice workstation. It combines a VS Code-style editor, a carefully checked 500-exercise core bank, real language runtimes, hidden-test judging, saved progress, and an optional AI pair-programming coach in one focused screen.

## Start practising — no developer setup

Double-click **`launch.bat`**. That is the only required setup step.

On its first run, the launcher finds Python 3.10+ or installs Python 3.12, creates this project's private `.venv`, installs the pinned Python dependencies, and makes a best-effort user-level installation of the Temurin Java 21 JDK when Java is missing. SQL uses Python's built-in SQLite judge plus a pinned dialect parser. It then starts the local server and opens KitCode in your browser at `http://127.0.0.1:8765`. **Node.js, pnpm, and VS Code are not required to practise.**

The first run needs internet access only if Python or those packages are missing. Later launches reuse the prepared environment; the exercise bank, editor, runner, trace, and judge work offline. Keep the launcher window open while using KitCode; closing it stops the local server.

## What is included

- **500 curated core exercises**: 200 Python, 150 Java, and 150 SQL, spanning fundamentals through advanced interview work in arrays, strings, collections, trees, graphs, dynamic programming, joins, windows, recursive queries, reporting, and more
- **One-click language switching** from the left rail, with a separately remembered drill and draft for Python, SQL, and Java
- **Level-first practice selection**: choose Foundations, Interview, or Advanced before browsing a focused topic/search list; KitCode remembers the level separately for every language
- **Full-script practice** using normal `stdin`/`stdout` for Python and Java, plus isolated SQL datasets and a writing-dialect selector for SQLite, PostgreSQL, MySQL, and Microsoft SQL Server
- **Truthful local SQL judging**: PostgreSQL, MySQL, and SQL Server syntax is parsed and translated into the built-in SQLite engine; the interface always shows both the writing dialect and the actual judge instead of claiming that three database servers are installed
- **Monaco editor** with Python, Java, and SQL highlighting, bracket matching, completion basics, keyboard shortcuts, and per-problem draft recovery
- **Run and submit workflows** with syntax errors, stderr, timing, public cases, privacy-safe hidden checks, and accurate acceptance state
- **Python execution trace** with each executed source line, the resulting local variables, changed values, explanations, and step navigation; Java and SQL retain normal Run and Submit workflows
- **Interview workflow** with an elapsed session clock, progressive hints, complexity prompts, and a level- and topic-filtered problem bank
- **Local progress** stored under `data/` and drafts stored in the browser on this computer
- **Optional adaptive AI coach** through OpenAI, Anthropic/Claude, a local model server, or an authenticated local Codex CLI, with one-click non-editing hints placed beside the relevant code
- **Responsive coaching output**: OpenAI, Anthropic, compatible local models, and Codex stream text into the conversation as it is generated.
- **Optional AI-made extra drills**, deliberately tucked into Settings so the curated 500-drill curriculum stays front and centre

## AI coach setup

AI help is optional; all exercises, execution, tracing, and judging work without it.

### Recommended: the in-app setup wizard

Open the AI Coach settings (the gear icon), choose **OpenAI**, **Anthropic/Claude**, **Local LLM**, or **Codex**, then follow the prompts. For an API provider, paste a key and choose a model. The local page sends that key once to the loopback (`127.0.0.1`) backend, which saves it in the local, git-ignored `.env` file; it is never returned to the UI. On later coach requests, the backend sends it only as authentication to the selected provider. `.env` is plaintext and therefore accessible to your Windows user account—protect this computer and do not share the file.

The conversation has no artificial Hint/Teach/Show modes: ask naturally about an error, your approach, complexity, or the next step and the coach adapts its response. **Give me a hint** is a separate one-click action. It adds a short, read-only `# Hint:` suggestion at the relevant line in Monaco and an accessible dismissible hint card; it never changes the script. The hint stays visible while you type, reset, run, trace, or submit and is removed only with **Dismiss**. Switching drills or AI providers invalidates it so advice is never carried into unrelated code.

Normal coach replies use a live streaming connection. OpenAI, Anthropic, supported local servers, and Codex expose incremental text, so the first words appear before the model finishes. You can cancel an in-progress response without losing your code.

**Editor edits are separate and always explicit.** Asking “how would you fix this?” or requesting a review can only produce guidance. KitCode will request a proposed full-script replacement only when you clearly ask it to apply a change—for example, “please fix my code,” “apply this fix,” or “replace the code in the editor.” Your script is still untouched while the review card shows the exact complete proposed code in the active language. Only **Apply AI edit** changes it. Added or replaced AI lines are marked in purple, the change is one undoable Monaco edit, and it is never run automatically. Use **Undo AI edit** or **Clear highlight**; typing or normal undo clears the provenance mark rather than labelling later learner code as AI-written. Exact AI replacements are limited to 8,000-character scripts so every supported provider can return the complete reviewable result; larger scripts can still use normal coaching. Provider output must match a strict `{message, code}` shape, and invalid, unchanged, or unsafe output is rejected.

- OpenAI: `gpt-5.6-terra` (balanced), `gpt-5.6-luna` (lower cost), or `gpt-5.6-sol` (maximum capability). You can also enter `gpt-5.4-mini` manually when it is available to your account.
- Anthropic/Claude: `claude-sonnet-5` (balanced), `claude-haiku-4-5` (lower cost), or `claude-opus-5` (maximum capability).
- Local LLM: defaults to `http://127.0.0.1:5000/`. Start your model server, then choose **Detect & use local LLM**. Detection only checks whether the base URL returns any HTTP response; it does not require a particular discovery API. Enter the server's model ID to use it. **KitCode never downloads, installs, starts, supervises, or keeps a local model server running.** Coaching currently sends requests to `/v1/chat/completions` only when you ask for AI help, so the server still needs to accept that request shape for coaching to work. No OpenAI or Anthropic key is sent to that endpoint.
- Codex: choose **Detect & use Codex**. KitCode checks whether the desktop app is open, whether a standalone Codex CLI is launchable, and whether `codex login status` confirms a sign-in. When all checks pass, Codex is selected automatically without copying a key or session credential. If the CLI is missing on Windows, AI Settings can run OpenAI's fixed official installer after you explicitly confirm the download and user-level installation.

For `127.0.0.1` or `localhost`, Local LLM prompts stay on this computer. A custom hostname or LAN/Internet address sends the visible exercise context, question, and editor contents to that destination, so use only an endpoint you control and trust. Detection and coaching are performed by KitCode's backend rather than the browser, and redirects are not followed. Changing the configured endpoint causes the consent notice to appear again.

The desktop process and the automation interface are separate. Detecting an open ChatGPT/Codex window does not grant another local app access to the conversation on screen. KitCode therefore starts a separate, private coaching run through the authenticated CLI; it cannot silently read, attach to, or continue the currently visible desktop chat. KitCode checks authentication with `codex login status`, uses the CLI's stdio app-server for live deltas, and retains `codex exec` only as a compatibility fallback before any app-server turn has started.

### Guided Codex CLI setup on Windows

The **Install Codex CLI** action in AI Settings is separate from KitCode's normal launcher. `launch.bat` installs KitCode's own Python runtime and application packages; it does not silently install Codex or authorize an external AI account. After your confirmation, the guided action runs only OpenAI's fixed official Windows installer at `https://chatgpt.com/codex/install.ps1`. The installation is for your Windows user and does not require KitCode to receive a ChatGPT password, browser session, API key, or Codex credential.

When installation finishes, start the sign-in action and complete the interactive ChatGPT sign-in in the official Codex window outside KitCode. KitCode checks automatically for up to two minutes; **Recheck Codex** is also available. KitCode only asks the CLI whether it is signed in; it does not capture the sign-in interaction or read the resulting credential.

If the guided installer cannot run, open an ordinary PowerShell window and use OpenAI's official fallback command:

```powershell
irm https://chatgpt.com/codex/install.ps1 | iex
```

Then run `codex`, choose **Sign in with ChatGPT**, complete the external sign-in, and return to KitCode to re-detect. See OpenAI's current [Codex CLI installation and sign-in guide](https://learn.chatgpt.com/docs/codex/cli) before installing.

Model availability, limits, and pricing are set by each provider and may change. See the current [OpenAI model catalog](https://developers.openai.com/api/docs/models) and [Claude model documentation](https://platform.claude.com/docs/en/about-claude/models/overview). API usage is billed through the relevant API account; it is separate from a ChatGPT or Claude subscription unless that provider explicitly says otherwise.

### Manual `.env` setup

Copy `.env.example` to `.env`, add one provider's credential, then restart `launch.bat`:

```dotenv
# OpenAI
OPENAI_API_KEY=your_key_here
KITCODE_OPENAI_MODEL=gpt-5.6-terra

# Or Anthropic/Claude
ANTHROPIC_API_KEY=your_key_here
ANTHROPIC_MODEL=claude-sonnet-5

# Or an installed, authenticated Codex CLI
KITCODE_COACH_PROVIDER=codex

# Or a local model server with a supported chat endpoint
KITCODE_COACH_PROVIDER=local_llm
KITCODE_LOCAL_LLM_URL=http://127.0.0.1:5000/
KITCODE_LOCAL_LLM_MODEL=your-model-id
```

Set `KITCODE_COACH_PROVIDER` to `openai`, `anthropic`, `local_llm`, or `codex` to choose deliberately when more than one option is present. When it is blank, KitCode selects a configured API provider (OpenAI first, then Anthropic); it does **not** automatically contact a local LLM or use Codex. Select those options explicitly through their detector or settings. Codex must be installed, authenticated, and launchable by Windows; KitCode checks both `PATH` and standard per-user install locations. For live text, KitCode starts `codex app-server` over private stdio for one ephemeral, read-only, no-network turn. Because app-server has no `--ignore-user-config` switch, KitCode gives it a temporary Codex home containing only a short-lived local copy of the CLI authentication file; user config, rules, skills, hooks, and MCP servers are not loaded. The temporary copy and workspace are removed when the turn ends and the credential is never returned to the browser.

### OpenAI data-sharing incentive

For the OpenAI API, use this sequence: create an API key; add a positive balance and a spend budget; inspect your organization’s Data Controls for the exact eligibility offer; opt in only if you are comfortable sharing the relevant traffic; choose a currently eligible model; then monitor Usage and Costs. Depositing a few dollars can establish a positive balance, but does **not** itself guarantee eligibility or complimentary tokens. Some eligible organizations may receive complimentary daily tokens for eligible traffic they opt in to share; for an eligible account, that allowance may cover ordinary KitCode practice. Opting in shares selected API inputs and outputs with OpenAI, and only shared eligible traffic qualifies. Models, limits, eligibility, and the offer can change. Read OpenAI's current [data-sharing and complimentary-token guidance](https://help.openai.com/en/articles/10306912-sharing-feedback-evals-and-api-data-with-openai) and [model catalog](https://developers.openai.com/api/docs/models) before enabling it.

**AI privacy:** coaching is a network feature, not offline inference. A request sends the selected exercise’s visible title, description, topics, examples, constraints, expected complexity, and hints, plus your question, cursor location, complete editor contents, and up to eight recent messages from the current drill, to the selected provider. Hidden tests and reference solutions are excluded. Do not submit secrets, employer code, personal data, or other sensitive material.

### Optional AI-made drills

Once an AI provider is configured, Settings includes an intentionally low-profile **Create one AI drill** tool. Each click makes exactly one request using only the chosen language, difficulty, and topic—never editor code, chat history, drafts, or progress. It can use billed provider tokens (or local-model compute); KitCode does not generate in the background or retry automatically.

AI-made drills are labelled **AI-made / provisional** and have their own completion counter, separate from the curated 500, so progress remains comparable. Python and Java use model-supplied test I/O and are therefore provisional. SQL uses KitCode-owned, trusted SQLite schema families and fixture data, while the model supplies only a read-only reference query. Generated drills are stored locally in `data/generated_exercises.json`. Up to 2,000 are retained at once; delete old extras to keep creating drills indefinitely.

## Keyboard shortcuts

| Action | Shortcut |
| --- | --- |
| Run the current script (Spyder-style) | `F5` or `Ctrl+Enter` |
| Submit the current solution | `F6` or `Ctrl+Shift+S` |
| Submit against all tests | `Ctrl+Shift+S` |
| Indent in the editor | `Tab` |
| Find in the editor | `Ctrl+F` |
| Command palette | `F1` |

## Privacy and execution model

KitCode binds only to `127.0.0.1`. Learner scripts run in fresh temporary folders with isolated Python mode, a minimal environment, bounded captured output, a wall-clock timeout, and process-tree cleanup/resource limits where the operating system supports them.

This remains a practice runner for **trusted, self-authored code**, not a security sandbox. A script can access files available to your Windows account and attempt network or disk operations while it runs. Never paste or execute untrusted code, and do not expose KitCode to a network.

Hidden test inputs and expected values are never returned by the catalog or judge. The browser receives only pass/fail metadata for hidden checks.

## Development

The shipped app does not need Node.js. Node is needed only to change or rebuild the interface.

```powershell
# Backend
python -m pip install -r requirements.txt
python -m uvicorn backend.main:app --host 127.0.0.1 --port 8765

# Frontend development (in another terminal)
pnpm install
pnpm dev:local

# Production browser bundle
pnpm build:local

# Automated checks
python -m pytest tests -q
pnpm test
pnpm lint
pnpm typecheck
```

The local Vite development server proxies `/api` to port `8765`. `launch.bat` serves the prebuilt `frontend_dist/` bundle through FastAPI.

## Project map

```text
app/                    React practice workspace
backend/main.py         API, runner, tracer, progress, AI providers
backend/exercise_bank.py Python catalogue and privacy-safe validator
backend/multilang_bank.py SQL and Java catalogue integration
frontend/               Local Vite entry point
frontend_dist/          Prebuilt interface used by launch.bat
scripts/launch.ps1      First-run setup and one-click launcher
tests/                  Bank, backend, bundle, and integration checks
```

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if the launcher cannot prepare Python, a port is already occupied, or AI coaching is unavailable.
