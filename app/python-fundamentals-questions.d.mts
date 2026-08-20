export type PythonFundamentalsDifficulty =
  | "Easy"
  | "Intermediate"
  | "Advanced";

export interface PythonFundamentalsQuestion {
  id: string;
  title: string;
  topic: string;
  difficulty: PythonFundamentalsDifficulty;
  question: string;
  options: readonly [string, string, string, string];
  correctIndex: 0 | 1 | 2 | 3;
  explanation: string;
}

export const pythonFundamentalsQuestions: readonly PythonFundamentalsQuestion[];
