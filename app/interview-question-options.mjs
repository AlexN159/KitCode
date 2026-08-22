/** Deterministically balances correct-answer positions without changing answer text. */

function seededRandom(seedText) {
  let state = 2166136261;
  for (const character of seedText) {
    state ^= character.codePointAt(0);
    state = Math.imul(state, 16777619);
  }
  return () => {
    state += 0x6d2b79f5;
    let value = state;
    value = Math.imul(value ^ (value >>> 15), value | 1);
    value ^= value + Math.imul(value ^ (value >>> 7), value | 61);
    return ((value ^ (value >>> 14)) >>> 0) / 4294967296;
  };
}

function shuffle(values, random) {
  const shuffled = [...values];
  for (let index = shuffled.length - 1; index > 0; index -= 1) {
    const swapIndex = Math.floor(random() * (index + 1));
    [shuffled[index], shuffled[swapIndex]] = [
      shuffled[swapIndex],
      shuffled[index],
    ];
  }
  return shuffled;
}

function balancedTargetPositions(length, random) {
  const remaining = Array.from(
    { length: 4 },
    (_, position) =>
      Math.floor(length / 4) + (position < length % 4 ? 1 : 0),
  );
  const positions = [];
  let repeated = 0;

  while (positions.length < length) {
    const previous = positions.at(-1);
    const candidates = remaining
      .map((count, position) => ({ count, position }))
      .filter(
        ({ count, position }) =>
          count > 0 && !(repeated >= 2 && position === previous),
      );
    const totalWeight = candidates.reduce(
      (total, candidate) => total + candidate.count,
      0,
    );
    let selectedWeight = random() * totalWeight;
    const selected =
      candidates.find((candidate) => {
        selectedWeight -= candidate.count;
        return selectedWeight < 0;
      }) ?? candidates.at(-1);
    positions.push(selected.position);
    remaining[selected.position] -= 1;
    repeated = selected.position === previous ? repeated + 1 : 1;
  }
  return positions;
}

export function balanceInterviewQuestionOptions(questions, seed) {
  const random = seededRandom(`kitcode:${seed}:answer-layout-v2`);
  const targetPositions = balancedTargetPositions(questions.length, random);

  return Object.freeze(
    questions.map((question, questionIndex) => {
      const correctAnswer = question.options[question.correctIndex];
      const distractors = shuffle(
        question.options.filter((_, index) => index !== question.correctIndex),
        random,
      );
      const correctIndex = targetPositions[questionIndex];
      const options = [...distractors];
      options.splice(correctIndex, 0, correctAnswer);
      return Object.freeze({
        ...question,
        options: Object.freeze(options),
        correctIndex,
      });
    }),
  );
}
