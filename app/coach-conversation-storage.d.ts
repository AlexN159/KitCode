export type SavedCoachMessage = {
  role: "coach" | "you";
  text: string;
  contextual: boolean;
};

export const COACH_CONVERSATION_STORAGE_KEY: string;
export const MAX_SAVED_COACH_CONVERSATIONS: number;
export const MAX_SAVED_COACH_MESSAGES: number;
export const MAX_SAVED_COACH_MESSAGE_CHARS: number;
export const MAX_SAVED_COACH_ARCHIVE_CHARS: number;

export function coachConversationScope(
  language: string,
  exerciseId: string,
  runtimeIdentity: string,
): string;

export function readCoachConversation(
  storage: Storage,
  language: string,
  exerciseId: string,
  runtimeIdentity: string,
): SavedCoachMessage[];

export function writeCoachConversation(
  storage: Storage,
  language: string,
  exerciseId: string,
  runtimeIdentity: string,
  messages: Array<{
    id?: string;
    role: "coach" | "you";
    text: string;
    contextual?: boolean;
  }>,
  updatedAt?: number,
): void;

export function clearCoachConversationsForExercise(
  storage: Storage,
  language: string,
  exerciseId: string,
): void;
