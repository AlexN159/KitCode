import assert from "node:assert/strict";
import test from "node:test";
import {
  clearCoachConversationsForExercise,
  COACH_CONVERSATION_STORAGE_KEY,
  MAX_SAVED_COACH_CONVERSATIONS,
  MAX_SAVED_COACH_MESSAGES,
  readCoachConversation,
  writeCoachConversation,
} from "../../app/coach-conversation-storage.mjs";

class MemoryStorage {
  constructor() {
    this.values = new Map();
  }

  getItem(key) {
    return this.values.get(key) ?? null;
  }

  setItem(key, value) {
    this.values.set(String(key), String(value));
  }
}

class UnavailableStorage extends MemoryStorage {
  setItem() {
    throw new Error("QuotaExceededError");
  }
}

const discussion = [
  { id: "welcome", role: "coach", text: "Welcome", contextual: false },
  { id: "one", role: "you", text: "Why does this loop stop?", contextual: true },
  { id: "two", role: "coach", text: "Because the range excludes its end.", contextual: true },
];

test("coach discussions restore only for the same exercise, language, and provider", () => {
  const storage = new MemoryStorage();
  writeCoachConversation(storage, "python", "array-003", "codex|gpt", discussion, 1);

  assert.deepEqual(
    readCoachConversation(storage, "python", "array-003", "codex|gpt"),
    [
      { role: "you", text: "Why does this loop stop?", contextual: true },
      {
        role: "coach",
        text: "Because the range excludes its end.",
        contextual: true,
      },
    ],
  );
  assert.deepEqual(
    readCoachConversation(storage, "python", "array-004", "codex|gpt"),
    [],
  );
  assert.deepEqual(
    readCoachConversation(storage, "java", "array-003", "codex|gpt"),
    [],
  );
  assert.deepEqual(
    readCoachConversation(storage, "python", "array-003", "openai|gpt"),
    [],
  );
});

test("saved conversations are bounded and omit welcome, empty, and malformed messages", () => {
  const storage = new MemoryStorage();
  const messages = Array.from({ length: MAX_SAVED_COACH_MESSAGES + 5 }, (_, index) => ({
    id: `message-${index}`,
    role: index % 2 ? "coach" : "you",
    text: `message ${index}`,
    contextual: true,
  }));
  messages.unshift(
    { id: "welcome", role: "coach", text: "not saved", contextual: false },
    { id: "empty", role: "coach", text: "", contextual: false },
  );
  writeCoachConversation(storage, "python", "one", "codex|gpt", messages, 1);

  const restored = readCoachConversation(
    storage,
    "python",
    "one",
    "codex|gpt",
  );
  assert.equal(restored.length, MAX_SAVED_COACH_MESSAGES);
  assert.equal(restored[0].text, "message 5");
  assert.equal(restored.at(-1).text, `message ${MAX_SAVED_COACH_MESSAGES + 4}`);
});

test("the archive evicts the least recently used exercise and tolerates corrupt data", () => {
  const storage = new MemoryStorage();
  for (let index = 0; index <= MAX_SAVED_COACH_CONVERSATIONS; index += 1)
    writeCoachConversation(
      storage,
      "python",
      `exercise-${index}`,
      "codex|gpt",
      discussion,
      index,
    );

  assert.deepEqual(
    readCoachConversation(storage, "python", "exercise-0", "codex|gpt"),
    [],
  );
  assert.equal(
    readCoachConversation(
      storage,
      "python",
      `exercise-${MAX_SAVED_COACH_CONVERSATIONS}`,
      "codex|gpt",
    ).length,
    2,
  );

  storage.setItem(COACH_CONVERSATION_STORAGE_KEY, "not json");
  assert.deepEqual(
    readCoachConversation(storage, "python", "exercise-1", "codex|gpt"),
    [],
  );
});

test("deleting a generated exercise clears its history for every provider", () => {
  const storage = new MemoryStorage();
  writeCoachConversation(storage, "python", "generated-1", "codex|gpt", discussion, 1);
  writeCoachConversation(storage, "python", "generated-1", "openai|gpt", discussion, 2);
  writeCoachConversation(storage, "python", "keep-me", "codex|gpt", discussion, 3);

  clearCoachConversationsForExercise(storage, "python", "generated-1");

  assert.deepEqual(
    readCoachConversation(storage, "python", "generated-1", "codex|gpt"),
    [],
  );
  assert.deepEqual(
    readCoachConversation(storage, "python", "generated-1", "openai|gpt"),
    [],
  );
  assert.equal(
    readCoachConversation(storage, "python", "keep-me", "codex|gpt").length,
    2,
  );
});

test("a full or unavailable local storage never interrupts practice", () => {
  const storage = new UnavailableStorage();

  assert.doesNotThrow(() =>
    writeCoachConversation(storage, "python", "one", "codex|gpt", discussion),
  );
  assert.doesNotThrow(() =>
    clearCoachConversationsForExercise(storage, "python", "one"),
  );
});
