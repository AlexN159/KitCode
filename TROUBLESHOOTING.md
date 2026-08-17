# KitCode troubleshooting

## The launcher says Python cannot be found

KitCode first checks `python.exe`, then the Windows `py.exe` launcher, then common per-user installation folders. If none contains Python 3.10 or newer, it tries `winget` and then the official Python 3.12 installer.

The fallback installer is accepted only when Windows validates its Python Software Foundation signature.

- Make sure Windows can reach `python.org` or that `winget` is available.
- If installation completed but detection still fails, restart Windows once and reopen `launch.bat`.
- A manually installed Python 3.10+ also works when `python --version` succeeds in PowerShell.

## Package installation fails

The first launch needs internet access to install the exact package versions in `requirements.txt`. Check your connection, proxy, or security software, then reopen `launch.bat`; setup safely resumes. After bootstrap, the exercise bank and coding tools are offline-capable.

If your organization uses a Python package mirror, set `PIP_INDEX_URL` before launching.

## Java drills say the JDK is unavailable

The one-click launcher checks for `javac` and `java`, then uses `winget` to install the user-level Temurin Java 21 JDK when they are missing. Python and SQL remain available if that optional installation cannot complete.

- Reopen `launch.bat` after any pending Windows installer finishes.
- In PowerShell, verify both `java -version` and `javac -version` work.
- If `winget` is unavailable, install a Java 17-or-newer JDK manually and set `JAVA_HOME` to its installation folder.
- Corporate package policies can block `winget`; ask your administrator for an approved JDK in that case.

SQL needs no separate database installation. Choose SQLite, PostgreSQL, MySQL, or Microsoft SQL Server from the editor toolbar. KitCode parses the selected writing dialect and translates compatible syntax into a fresh, isolated SQLite exercise dataset. The interface therefore says **Writing dialect: … · Judge: SQLite (built in)**. This is excellent for common SQL-query syntax, but it is not a native PostgreSQL, MySQL, or SQL Server instance; highly vendor-specific functions or engine behaviours may be unsupported and return a controlled compatibility error.

## Port 8765 is already in use

Close an older KitCode launcher window first. For development, run:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/launch.ps1 -Port 8766
```

## The page opens but has no styling

Confirm that `frontend_dist/index.html` and `frontend_dist/assets/` are present. Rebuild them with `pnpm build:local` if you are developing the project.

## Run or Trace never finishes

KitCode stops ordinary runs after four seconds by default. Check for an infinite loop, recursion without a base case, or an algorithm that is too expensive for the input. Trace captures at most 200 line events from the interface so the browser remains responsive.

## The AI coach is offline

Open Settings in KitCode to see provider diagnostics.

OpenAI, Anthropic, supported local-model replies, and Codex replies stream progressively. Codex starts a fresh isolated app-server turn for each request, so its initial response can still be slower than a direct API call. For that turn KitCode uses a temporary Codex home containing only a short-lived local copy of the CLI authentication file; it does not load your Codex config, rules, skills, hooks, or MCP servers, and removes the temporary home afterward. Use **Cancel** if a request is no longer useful; changing drills, providers, or code also invalidates the pending response.

- Prefer the in-app AI Coach setup wizard: choose OpenAI, Anthropic/Claude, Local LLM, or Codex, then save. The local page sends a pasted key once to the `127.0.0.1` backend, which writes the ignored local `.env`; it is never returned to the UI. `.env` is plaintext and accessible to your Windows user account, so protect it as you would any credential file.
- For manual setup, copy `.env.example` to `.env`. Use `OPENAI_API_KEY` with `KITCODE_OPENAI_MODEL` (`gpt-5.6-terra`, `gpt-5.6-luna`, `gpt-5.6-sol`, or optionally `gpt-5.4-mini` if available), or `ANTHROPIC_API_KEY` with `ANTHROPIC_MODEL` (`claude-sonnet-5`, `claude-haiku-4-5`, or `claude-opus-5`). Restart `launch.bat` after editing `.env` manually.
- For Codex, select **Existing Codex** and click **Detect & use Codex**. A successful scan confirms the desktop process (optional), a launchable CLI, and `codex login status`, then selects Codex automatically. The open desktop chat itself is private to that app and is never read or continued by KitCode.
- If the CLI is missing, AI Settings offers **Install Codex CLI**. KitCode shows a confirmation before it downloads and runs OpenAI's fixed official Windows installer at `https://chatgpt.com/codex/install.ps1`. This is a user-level installation. KitCode does not ask for or capture a ChatGPT password, browser session, API key, or Codex credential.
- Installation does not sign you in. Use the sign-in action and complete the interactive ChatGPT sign-in in the official Codex window outside KitCode. KitCode checks automatically for up to two minutes; **Recheck Codex** is also available. KitCode only checks the CLI's resulting login status.
- If guided installation fails, open an ordinary PowerShell window and run OpenAI's official fallback command: `irm https://chatgpt.com/codex/install.ps1 | iex`. Then run `codex`, choose **Sign in with ChatGPT**, finish the external sign-in, and re-detect in KitCode. See the [official Codex CLI installation and sign-in guide](https://learn.chatgpt.com/docs/codex/cli).
- If Codex is installed but detection still fails, open ordinary PowerShell and run `codex --version`, then `codex login status`. A Microsoft Store/desktop installation can expose a bundled executable that Windows denies to other programs; repair the standalone CLI with the official installer, reopen KitCode if Windows has not refreshed the executable path, and scan again. You can use an API provider meanwhile.
- When `KITCODE_COACH_PROVIDER` is blank, KitCode can select a configured API provider (OpenAI first, then Anthropic), but will not automatically use Codex. To use Codex without detection, select it in the wizard or set `KITCODE_COACH_PROVIDER=codex` after confirming the CLI works and is authenticated.
- For a local model, start its server and select **Local LLM → Detect & use local LLM**. KitCode never downloads, installs, launches, supervises, or keeps a local model process running. The default probe is a single request to `http://127.0.0.1:5000/`; any HTTP response counts as detected. Enter a model ID to save it. Coaching currently calls `/v1/chat/completions` only when you request help, so detection does not guarantee that coaching will work with every server API. If nothing responds, verify the process, URL, and port.
- No API credential is forwarded to a Local LLM endpoint. If a custom remote endpoint requires authentication, use a trusted local proxy or one of the dedicated API-provider options instead. Treat every non-loopback URL as an external destination: prompts and complete editor contents may leave this PC.
- Exercise hints remain available without either provider.

OpenAI/Anthropic API usage is separately billed from ChatGPT or Claude subscriptions unless the provider explicitly says otherwise. For OpenAI, first create a key, add positive balance/budget, inspect Data Controls for the exact offer, and opt in only if you accept traffic sharing. A small deposit can establish positive balance but does not guarantee eligibility or complimentary tokens. See OpenAI's [data-sharing guidance](https://help.openai.com/en/articles/10306912-sharing-feedback-evals-and-api-data-with-openai), [current models](https://developers.openai.com/api/docs/models), and [Claude model docs](https://platform.claude.com/docs/en/about-claude/models/overview).

OpenAI, Anthropic, and Codex are network services, not offline inference. A loopback Local LLM can stay on this PC, while a custom remote Local LLM endpoint is also a network service. A coach request includes the selected exercise’s visible title, description, topics, examples, constraints, expected complexity, and hints, plus your question, cursor location, complete script, and up to eight recent messages from the current drill. Hidden tests and reference solutions are excluded. Do not use an external coach with sensitive or proprietary code.

Normal coach chat adapts to what you ask; there are no separate Hint/Teach/Show modes. Recent discussions are saved in this browser for the current exercise and AI provider/model, then restored when you return. **Give me a hint** makes an explicit coach request and displays a short, read-only **Hint — line N** panel in the editor as well as the card below it. It does not modify the script. Turn off **Show hints in the editor** under **Other KitCode options** if you want only the lower card. The hint remains visible through typing, reset, run, trace, and submit until you select **Dismiss**. Switching drills or AI providers clears the visible hint because the advice belongs to the previous context.

An editor edit requires unmistakable wording such as “please fix my code,” “apply this fix,” or “put this into the editor.” Questions such as “how would you fix this?” and “review my code” remain guidance-only. If KitCode says an edit needs explicit permission, ask with one of those action phrases. Any proposed replacement is validated and its exact complete code in the active language is shown in a review card; the script changes only when you click **Apply AI edit**. Added or replaced lines are purple and undoable, and are never run automatically. Learner typing or normal undo clears that provenance mark. Exact replacements support scripts up to 8,000 characters; use normal coach guidance for larger scripts. Malformed, unchanged, or unsafe provider output is rejected.

## AI-made drill generation is unavailable or full

The optional generator is deliberately located in Settings so it does not distract from the curated bank. Configure and select an AI provider first; each **Create one AI drill** click makes one provider request. It sends only language, difficulty, and topic—not your editor code, chat history, drafts, or completion record. The request can incur API billing or local-model compute and is never made in the background or retried automatically.

Generated drills are marked **AI-made / provisional** and completed separately from the curated 700 (400 Python, 150 Java, and 150 SQL). Python and Java test I/O is model-supplied, so treat it as provisional. SQL instead uses server-owned trusted schemas and fixture data. The drills are local in `data/generated_exercises.json`; KitCode retains at most 2,000 at once. Delete older generated drills, then continue creating new ones indefinitely.

## Reset local progress

Completed status and notes live in `data/progress.json`. Editor drafts live in this browser's local storage under keys beginning with `kitcode:draft:`. After a product-name update, KitCode copies earlier browser drafts into the current namespace before the workspace opens; it keeps the original entries and never overwrites a genuinely newer edit. Delete draft items only if you intentionally want a fresh start.
