export type CoachStreamEvent =
  | { type: "meta" | "done"; provider?: string; model?: string }
  | { type: "delta"; delta: string }
  | { type: "error"; message: string; status?: number };
export const MAX_COACH_STREAM_BYTES: number;
export const MAX_COACH_STREAM_PENDING_CHARS: number;
export function readCoachStream(
  response: Response,
  onEvent: (event: CoachStreamEvent) => void,
  shouldContinue?: () => boolean,
): Promise<void>;
