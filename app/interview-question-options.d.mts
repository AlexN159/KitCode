import type { InterviewQuestion } from "./interview-question-banks.mjs";

export function balanceInterviewQuestionOptions(
  questions: readonly InterviewQuestion[],
  seed: string,
): readonly InterviewQuestion[];
