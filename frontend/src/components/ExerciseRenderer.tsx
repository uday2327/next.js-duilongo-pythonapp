"use client";

import type { Exercise } from "@/types";
import { MultipleChoice } from "./MultipleChoice";
import { WordBank } from "./WordBank";
import { MatchPairs } from "./MatchPairs";
import { TypeAnswer } from "./TypeAnswer";

export function ExerciseRenderer({
  exercise,
  disabled,
  answer,
  setAnswer,
  correctAnswer,
  submit,
}: {
  exercise: Exercise;
  disabled: boolean;
  answer: string | string[] | Record<string, string>;
  setAnswer: (answer: string | string[] | Record<string, string>) => void;
  correctAnswer?: string;
  submit: (override?: unknown) => void;
}) {
  if (exercise.type === "multiple_choice" || exercise.type === "fill_blank") {
    return <MultipleChoice exercise={exercise} disabled={disabled} selected={String(answer || "")} setSelected={setAnswer as (value: string) => void} correctAnswer={correctAnswer} />;
  }
  if (exercise.type === "translate" || exercise.type === "word_bank") {
    return <WordBank exercise={exercise} disabled={disabled} answer={Array.isArray(answer) ? answer : []} setAnswer={setAnswer as (value: string[]) => void} />;
  }
  if (exercise.type === "match_pairs") {
    return <MatchPairs exercise={exercise} disabled={disabled} onComplete={(value) => { setAnswer(value); submit(value); }} />;
  }
  return <TypeAnswer disabled={disabled} answer={String(answer || "")} setAnswer={setAnswer as (value: string) => void} onEnter={() => submit()} />;
}
