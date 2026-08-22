import type { InterviewQuestion } from "./interview-question-banks.mjs";

type SupplementalInterviewQuestion = Omit<InterviewQuestion, "id" | "title">;

export const sqlInterviewQuestionSupplement: readonly SupplementalInterviewQuestion[];
export const javaInterviewQuestionSupplement: readonly SupplementalInterviewQuestion[];
export const machineLearningInterviewQuestionSupplement: readonly SupplementalInterviewQuestion[];
