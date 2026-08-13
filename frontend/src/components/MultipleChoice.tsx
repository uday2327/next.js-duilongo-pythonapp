"use client";

import type { Exercise } from "@/types";
import { cx } from "@/lib/utils";

export function MultipleChoice({ exercise, disabled, selected, setSelected, correctAnswer }: { exercise: Exercise; disabled: boolean; selected: string; setSelected: (value: string) => void; correctAnswer?: string }) {
  return (
    <div className="grid gap-3">
      {exercise.options.map((option, index) => {
        const isSelected = selected === option.text;
        const revealCorrect = disabled && option.text === correctAnswer;
        return (
          <button
            key={option.id}
            disabled={disabled}
            onClick={() => setSelected(option.text)}
            className={cx(
              "rounded-2xl border-2 border-b-4 px-5 py-4 text-left text-lg font-black transition hover:bg-slate-50",
              isSelected && "border-[#1cb0f6] bg-[#ddf4ff] text-[#1cb0f6]",
              disabled && isSelected && option.text !== correctAnswer && "border-red-300 bg-red-50 text-red-600",
              revealCorrect && "border-green-400 bg-green-50 text-green-700"
            )}
          >
            <span className="mr-4 text-slate-400">{index + 1}</span>{option.text}
          </button>
        );
      })}
    </div>
  );
}
