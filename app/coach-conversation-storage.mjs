export const COACH_CONVERSATION_STORAGE_KEY =
  "kitcode:coach-conversations-v1";
export const MAX_SAVED_COACH_CONVERSATIONS = 30;
export const MAX_SAVED_COACH_MESSAGES = 30;
export const MAX_SAVED_COACH_MESSAGE_CHARS = 8_000;
export const MAX_SAVED_COACH_ARCHIVE_CHARS = 1_500_000;

export function coachConversationScope(language, exerciseId, runtimeIdentity) {
  return JSON.stringify([language, exerciseId, runtimeIdentity]);
}

function sanitizeMessages(messages) {
  if (!Array.isArray(messages)) return [];
  return messages
    .filter(
      (message) =>
        message &&
        message.id !== "welcome" &&
        (message.role === "coach" || message.role === "you") &&
        typeof message.text === "string" &&
        message.text.trim(),
    )
    .slice(-MAX_SAVED_COACH_MESSAGES)
    .map((message) => ({
      role: message.role,
      text: message.text.slice(0, MAX_SAVED_COACH_MESSAGE_CHARS),
      contextual: message.contextual === true,
    }));
}

function readArchive(storage) {
  try {
    const parsed = JSON.parse(
      storage.getItem(COACH_CONVERSATION_STORAGE_KEY) ?? "null",
    );
    if (parsed?.version !== 1 || !Array.isArray(parsed.conversations)) return [];
    const scopes = new Set();
    return parsed.conversations
      .filter(
        (conversation) =>
          conversation &&
          typeof conversation.scope === "string" &&
          Number.isFinite(conversation.updatedAt) &&
          Array.isArray(conversation.messages),
      )
      .map((conversation) => ({
        scope: conversation.scope,
        updatedAt: conversation.updatedAt,
        messages: sanitizeMessages(conversation.messages),
      }))
      .filter((conversation) => {
        if (!conversation.messages.length || scopes.has(conversation.scope))
          return false;
        scopes.add(conversation.scope);
        return true;
      })
      .sort((left, right) => right.updatedAt - left.updatedAt)
      .slice(0, MAX_SAVED_COACH_CONVERSATIONS);
  } catch {
    return [];
  }
}

function persistArchive(storage, conversations) {
  try {
    storage.setItem(
      COACH_CONVERSATION_STORAGE_KEY,
      JSON.stringify({ version: 1, conversations }),
    );
  } catch {
    // Private browsing and full local storage should never break practice.
  }
}

/** Read a local conversation without contacting its AI provider. */
export function readCoachConversation(
  storage,
  language,
  exerciseId,
  runtimeIdentity,
) {
  const scope = coachConversationScope(language, exerciseId, runtimeIdentity);
  return (
    readArchive(storage).find((conversation) => conversation.scope === scope)
      ?.messages ?? []
  );
}

/**
 * Save recent conversations in one bounded least-recently-used archive. The
 * archive stays small enough for ordinary browser local-storage quotas.
 */
export function writeCoachConversation(
  storage,
  language,
  exerciseId,
  runtimeIdentity,
  messages,
  updatedAt = Date.now(),
) {
  const scope = coachConversationScope(language, exerciseId, runtimeIdentity);
  const savedMessages = sanitizeMessages(messages);
  let conversations = readArchive(storage).filter(
    (conversation) => conversation.scope !== scope,
  );
  if (savedMessages.length)
    conversations.unshift({ scope, updatedAt, messages: savedMessages });
  conversations = conversations.slice(0, MAX_SAVED_COACH_CONVERSATIONS);

  let serialized = JSON.stringify({ version: 1, conversations });
  while (
    serialized.length > MAX_SAVED_COACH_ARCHIVE_CHARS &&
    conversations.length > 1
  ) {
    conversations.pop();
    serialized = JSON.stringify({ version: 1, conversations });
  }
  if (serialized.length > MAX_SAVED_COACH_ARCHIVE_CHARS) {
    conversations[0].messages = conversations[0].messages.slice(-8);
    serialized = JSON.stringify({ version: 1, conversations });
  }
  try {
    storage.setItem(COACH_CONVERSATION_STORAGE_KEY, serialized);
  } catch {
    // Private browsing and full local storage should never break practice.
  }
}

/** Remove every provider-specific conversation for one deleted exercise. */
export function clearCoachConversationsForExercise(
  storage,
  language,
  exerciseId,
) {
  const conversations = readArchive(storage).filter((conversation) => {
    try {
      const [savedLanguage, savedExerciseId] = JSON.parse(conversation.scope);
      return savedLanguage !== language || savedExerciseId !== exerciseId;
    } catch {
      return true;
    }
  });
  persistArchive(storage, conversations);
}
