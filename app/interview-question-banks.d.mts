export type InterviewQuestionDifficulty = "Easy" | "Intermediate" | "Advanced";

export interface InterviewQuestion {
  id: string;
  title: string;
  topic: string;
  difficulty: InterviewQuestionDifficulty;
  question: string;
  options: readonly [string, string, string, string];
  correctIndex: 0 | 1 | 2 | 3;
  explanation: string;
}

export const sqlInterviewQuestions: readonly InterviewQuestion[];
export const javaInterviewQuestions: readonly InterviewQuestion[];
export const machineLearningInterviewQuestions: readonly InterviewQuestion[];
