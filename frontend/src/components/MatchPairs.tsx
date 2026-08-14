"use client";

import { useMemo, useState } from "react";
import type { Exercise } from "@/types";
import { cx } from "@/lib/utils";

export function MatchPairs({ exercise, disabled, onComplete }: { exercise: Exercise; disabled: boolean; onComplete: (answer: Record<string, string>) => void }) {
  const [left, setLeft] = useState<string | null>(null);
  const [matched, setMatched] = useState<Record<string, string>>({});
  const [wrong, setWrong] = useState(false);
  const [checking, setChecking] = useState(false);
  const rights = useMemo(() => [...exercise.pairs].sort((a, b) => b.right_text.localeCompare(a.right_text)), [exercise.pairs]);

  function chooseRight(right: string) {
    if (!left || disabled) return;
    const pair = exercise.pairs.find((item) => item.left_text === left);
    if (pair?.right_text === right) {
      const next = { ...matched, [left]: right };
      setMatched(next);
      setLeft(null);
      if (Object.keys(next).length === exercise.pairs.length) {
        setChecking(true);
        onComplete(next);
      }
    } else {
      setWrong(true);
      setLeft(null);
      setChecking(true);
      onComplete({ [left]: right });
    }
  }

  return (
    <div className={cx("grid grid-cols-2 gap-4", wrong && "animate-pulse")}>
      <div className="space-y-3">
        {exercise.pairs.map((pair) => (
                    <button key={pair.id} disabled={disabled || checking || !!matched[pair.left_text]} onClick={() => setLeft(pair.left_text)} className={cx("w-full rounded-2xl border-2 border-b-4 px-4 py-3 font-black", left === pair.left_text ? "border-accent bg-accent-10" : "border-slate-200 bg-card", matched[pair.left_text] && "opacity-20")}>
            {pair.left_text}
          </button>
        ))}
      </div>
      <div className="space-y-3">
        {rights.map((pair) => (
          <button key={pair.id} disabled={disabled || checking || Object.values(matched).includes(pair.right_text)} onClick={() => chooseRight(pair.right_text)} className="w-full rounded-2xl border-2 border-b-4 border-slate-200 bg-white px-4 py-3 font-black disabled:opacity-20">
            {pair.right_text}
          </button>
        ))}
      </div>
    </div>
  );
}
