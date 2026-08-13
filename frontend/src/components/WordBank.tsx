"use client";

import type { Exercise } from "@/types";

type Chip = { id: string; text: string };

function chipsFor(exercise: Exercise): Chip[] {
  const source = exercise.options.length ? exercise.options.map((o) => o.text) : exercise.correct_answer.split(" ");
  return source.map((text, index) => ({ id: `${text}-${index}`, text }));
}

export function WordBank({ exercise, disabled, answer, setAnswer }: { exercise: Exercise; disabled: boolean; answer: string[]; setAnswer: (value: string[]) => void }) {
  const chips = chipsFor(exercise);
  const selectedIds = answer.map((_, index) => index);
  const selectedText = answer.join(" ");
  return (
    <div className="space-y-8">
      <div className="min-h-24 rounded-2xl border-2 border-dashed border-slate-200 p-4 text-lg font-bold text-slate-700">
        {selectedText || <span className="text-slate-300">Tap words to build your answer</span>}
      </div>
      <div className="flex flex-wrap justify-center gap-3">
        {chips.map((chip, index) => {
          const used = selectedIds.includes(index) && answer.includes(chip.text);
          return (
            <button
              key={chip.id}
              disabled={disabled || used}
              onClick={() => setAnswer([...answer, chip.text])}
              className="rounded-2xl border-2 border-b-4 border-slate-200 bg-white px-5 py-3 font-black text-slate-700 disabled:opacity-30"
            >
              {chip.text}
            </button>
          );
        })}
      </div>
      <button disabled={disabled || answer.length === 0} onClick={() => setAnswer(answer.slice(0, -1))} className="mx-auto block text-sm font-black uppercase text-[#1cb0f6] disabled:text-slate-300">Undo word</button>
    </div>
  );
}
