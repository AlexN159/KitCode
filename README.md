# KitCode Practice Studio

Practise Python, Java, and SQL in one focused Windows workspace. KitCode combines a curated exercise bank, local code execution, progress tracking, reviewed answers, and optional live coaching from Codex—without requiring a Git or terminal workflow.

<p align="center">
  <a href="https://github.com/AlexN159/KitCode/releases/latest/download/KitCode-Windows.zip">
    <img src=".github/download-windows.svg" alt="Download KitCode for Windows">
  </a>
</p>

![KitCode workspace preview](.github/kitcode-workspace.png)

## Why learn with KitCode?

- **700 curated coding exercises:** 400 Python, 150 Java, and 150 SQL drills across Easy, Medium, and Hard levels.
- **Live help from Codex:** ask questions naturally, request a targeted hint, or get an explanation based on the exercise and your current code.
- **A complete feedback loop:** run code, inspect output, submit against the exercise test suite, and track completed problems.
- **Reviewed best answers:** after a correct submission, compare your approach with the expected solution, its Big-O target, and the readability-first selection rubric.
- **Python line-by-line tracing:** step through executed lines and inspect changing values when a program is difficult to reason about.
- **100 Python fundamentals questions:** use the optional multiple-choice interview bank to review language concepts without opening the code editor.
- **Local-first practice:** the curated bank, runner, drafts, and progress stay on your computer and continue to work offline after initial setup.

KitCode works well for first-time practice, interview preparation, refreshing fundamentals, learning data structures and algorithms, or building confidence before moving into larger projects.

## A practical learning loop

1. Choose Python, Java, or SQL and select an Easy, Medium, or Hard practice level.
2. Read the task, examples, constraints, hints, and expected complexity.
3. Write your answer in the built-in Monaco editor.
4. Press **F5** to run it. Python exercises can also be traced line by line.
5. Press **F6** to submit it against the full exercise test suite.
6. After passing, open **Best answer** to compare complexity, clarity, and implementation choices.

Your selected level, drafts, solved exercises, fundamentals score, and recent coach conversations are remembered locally.

## Live coaching with Codex

KitCode can connect to an existing authenticated Codex CLI and use it as a live programming coach. The guided setup can detect Codex, install the official CLI when it is missing, and help you begin the external ChatGPT sign-in flow. KitCode never asks for your ChatGPT password and does not copy a Codex API key into the app.

Once connected, you can:

- ask follow-up questions in a streaming conversation while you work;
- request a concise, read-only hint anchored near the relevant editor line;
- keep separate conversations for each exercise and AI provider;
- retry or restart an interrupted response without retyping the question;
- ask for explanations of errors, concepts, trade-offs, or possible next steps.

The coach receives the visible exercise context, your current script, cursor position, question, and a small amount of recent conversation so it can respond usefully. Hidden tests and reviewed reference answers are never included. Codex is optional and requires an internet connection plus an authenticated CLI; OpenAI, Anthropic/Claude, and compatible local LLMs are also supported.

## Learning topics available

| Track | Curated practice | Topics include |
| --- | ---: | --- |
| **Python** | 400 exercises: 176 Easy, 130 Medium, 94 Hard | Types, conditionals, loops, functions, strings, lists, hashing, parsing, files, exceptions, classes and OOP, searching, sorting, two pointers, stacks, heaps, trees, graphs, grids, dynamic programming, intervals, sweep lines, simulation, and advanced algorithms |
| **Java** | 150 exercises: 35 Easy, 86 Medium, 29 Hard | Core syntax, arrays, strings, loops, collections and maps, stacks, linked lists, binary search, sliding windows, trees, graphs, greedy algorithms, dynamic programming, backtracking, design, and advanced graph problems |
| **SQL** | 150 exercises: 46 Easy, 89 Medium, 15 Hard | Filtering, ordering, aggregation, `GROUP BY`, `HAVING`, joins, `NULL`, `CASE`, subqueries, set operations, window functions, ranking, running totals, recursive CTEs, time-series analysis, gaps and islands, relational division, hierarchies, and reachability |
| **Python Fundamentals** | 100 optional multiple-choice questions | The GIL and concurrency, mutable and immutable types, hashing, iteration, generators, functions and scope, exceptions, files, modules, packaging, the standard library, OOP, dunder methods, testing, security, and complexity |

SQL practice includes SQLite, PostgreSQL, MySQL, and SQL Server syntax choices. Queries are parsed and translated when necessary, then executed safely against fresh local SQLite fixtures so the exercises remain zero-install and deterministic.

## More useful features

- Searchable exercise banks and solved counts for each difficulty level.
- Automatic draft saving and recovery if a newer edit would otherwise hide earlier work.
- Public feedback plus private checks that discourage hard-coded answers.
- Direct class-API testing for Python OOP exercises.
- Optional AI-generated practice drills, clearly marked as provisional and kept separate from the curated 700.
- One-click hints from Kit, the movable desktop mascot.
- Keyboard-first Run and Submit shortcuts, responsive drawers, and accessible dialogs.

## Start KitCode

1. Open the downloaded **`KitCode-Windows.zip`** file and select **Extract All**.
2. Open the extracted **`KitCode`** folder.
3. Double-click **`launch.bat`**.

KitCode opens in your browser. Keep the KitCode launcher window open while you practise; closing it stops the app.

> **First launch:** KitCode may need a few minutes and an internet connection while it prepares Python and the required packages. Later launches are much faster and the core exercises work offline.

> **Java exercises:** KitCode also tries to prepare Java automatically. If a managed school or work computer blocks that installation, Python and SQL still work.

## Need help?

See [Troubleshooting](TROUBLESHOOTING.md) if KitCode does not start.
