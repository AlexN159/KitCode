import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
import {
  clearPersistedDraft,
  migrateLegacyBrowserStorage,
  readPersistedDraft,
} from "../../app/storage-migration.mjs";

const oldPrefix = ["py", "pair:"].join("");

class MemoryStorage {
  constructor(entries = []) {
    this.values = new Map(entries);
    this.removals = [];
  }

  get length() {
    return this.values.size;
  }

  key(index) {
    return [...this.values.keys()][index] ?? null;
  }

  getItem(key) {
    return this.values.has(key) ? this.values.get(key) : null;
  }

  setItem(key, value) {
    this.values.set(String(key), String(value));
  }

  removeItem(key) {
    this.removals.push(key);
    this.values.delete(key);
  }
}

test("the KitCode rename preserves every earlier browser value byte for byte", () => {
  const solutions = [
    "print('one')\n",
    "def two():\n    return '✓'\n",
    "SELECT 'three';\n",
    "class Four { /* my solution */ }\n",
  ];
  const exerciseIds = ["number-001", "number-002", "number-003", "number-004"];
  const entries = solutions.map((solution, index) => [
    `${oldPrefix}draft:python:${exerciseIds[index]}`,
    solution,
  ]);
  entries.push(
    [`${oldPrefix}selected-language`, "python"],
    [`${oldPrefix}solution:custom`, "keep this text too"],
    ["unrelated:text", "never touch me"],
  );
  const storage = new MemoryStorage(entries);

  migrateLegacyBrowserStorage(storage);

  solutions.forEach((solution, index) => {
    assert.equal(
      storage.getItem(`kitcode:draft:python:${exerciseIds[index]}`),
      solution,
    );
    assert.equal(
      storage.getItem(`${oldPrefix}draft:python:${exerciseIds[index]}`),
      solution,
    );
  });
  assert.equal(storage.getItem("kitcode:selected-language"), "python");
  assert.equal(storage.getItem("kitcode:solution:custom"), "keep this text too");
  assert.equal(storage.getItem("unrelated:text"), "never touch me");
  assert.deepEqual(storage.removals, []);
});

test("migration never overwrites newer KitCode data and is idempotent", () => {
  const storage = new MemoryStorage([
    [`${oldPrefix}selected-language`, "python"],
    ["kitcode:selected-language", "java"],
    [`${oldPrefix}selected-level:python`, "Hard"],
    ["kitcode:selected-level:python", ""],
  ]);

  migrateLegacyBrowserStorage(storage);
  const once = [...storage.values.entries()];
  migrateLegacyBrowserStorage(storage);

  assert.equal(storage.getItem("kitcode:selected-language"), "java");
  assert.equal(storage.getItem("kitcode:selected-level:python"), "");
  assert.deepEqual([...storage.values.entries()], once);
  assert.deepEqual(storage.removals, []);
});

test("an auto-saved starter cannot hide a recovered solution", () => {
  const exerciseKey = "python:exercise-1";
  const starter = "# starter\n";
  const solution = "print('my old answer')\n";
  const storage = new MemoryStorage([
    [`${oldPrefix}draft:${exerciseKey}`, solution],
    [`kitcode:draft:${exerciseKey}`, starter],
  ]);

  migrateLegacyBrowserStorage(storage);
  assert.equal(
    readPersistedDraft(storage, "python", "exercise-1", starter),
    solution,
  );
  assert.equal(storage.getItem(`kitcode:draft:${exerciseKey}`), solution);
  assert.equal(storage.getItem(`${oldPrefix}draft:${exerciseKey}`), solution);
});

test("line endings and an empty auto-save cannot hide a recovered solution", () => {
  const oldSolution = "def solve():\n    return 4\n";
  const crlfStorage = new MemoryStorage([
    [`${oldPrefix}draft:python:number-004`, oldSolution],
    ["kitcode:draft:python:number-004", "# starter\r\n"],
  ]);
  migrateLegacyBrowserStorage(crlfStorage);
  assert.equal(
    readPersistedDraft(
      crlfStorage,
      "python",
      "number-004",
      "# starter\n",
    ),
    oldSolution,
  );

  const emptyStorage = new MemoryStorage([
    [`${oldPrefix}draft:python:number-003`, oldSolution],
    ["kitcode:draft:python:number-003", ""],
  ]);
  migrateLegacyBrowserStorage(emptyStorage);
  assert.equal(
    readPersistedDraft(
      emptyStorage,
      "python",
      "number-003",
      "# starter\n",
    ),
    oldSolution,
  );
});

test("a genuine newer edit wins while the earlier solution remains recoverable", () => {
  const exerciseKey = "python:exercise-2";
  const storage = new MemoryStorage([
    [`${oldPrefix}draft:${exerciseKey}`, "old answer"],
    [`kitcode:draft:${exerciseKey}`, "new answer"],
  ]);

  migrateLegacyBrowserStorage(storage);
  assert.equal(
    readPersistedDraft(storage, "python", "exercise-2", "starter"),
    "new answer",
  );
  assert.equal(
    storage.getItem(`kitcode:recovered-draft:${exerciseKey}`),
    "old answer",
  );
  assert.equal(storage.getItem(`${oldPrefix}draft:${exerciseKey}`), "old answer");
});

test("only an explicit reset clears active and recovery drafts", () => {
  const storage = new MemoryStorage([
    ["kitcode:draft:python:exercise-3", "current"],
    ["kitcode:recovered-draft:python:exercise-3", "recovered"],
  ]);

  clearPersistedDraft(storage, "python", "exercise-3");

  assert.equal(storage.getItem("kitcode:draft:python:exercise-3"), null);
  assert.equal(
    storage.getItem("kitcode:recovered-draft:python:exercise-3"),
    null,
  );
});

test("storage migration runs before React mounts", async () => {
  const entry = await readFile(
    new URL("../../frontend/entry.tsx", import.meta.url),
    "utf8",
  );
  const migrationIndex = entry.indexOf(
    "migrateLegacyBrowserStorage(window.localStorage)",
  );
  const mountIndex = entry.indexOf("createRoot(root).render");

  assert.ok(migrationIndex >= 0);
  assert.ok(mountIndex >= 0);
  assert.ok(migrationIndex < mountIndex);
});
