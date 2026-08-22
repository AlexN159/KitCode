"use client";

import { InterviewQuiz } from "./interview-quiz";

export function PythonFundamentalsQuiz({
  clock,
  onReturnToCoding,
}: {
  clock: string;
  onReturnToCoding: () => void;
}) {
  return (
    <InterviewQuiz
      subject="python"
      clock={clock}
      onReturnToCoding={onReturnToCoding}
    />
  );
}
