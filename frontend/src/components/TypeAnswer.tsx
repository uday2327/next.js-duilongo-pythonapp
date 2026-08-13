"use client";

export function TypeAnswer({ disabled, answer, setAnswer, onEnter }: { disabled: boolean; answer: string; setAnswer: (value: string) => void; onEnter: () => void }) {
  return (
    <input
      autoFocus
      disabled={disabled}
      value={answer}
      onChange={(event) => setAnswer(event.target.value)}
      onKeyDown={(event) => {
        if (event.key === "Enter" && answer.trim()) onEnter();
      }}
      className="w-full rounded-2xl border-2 border-b-4 border-slate-200 px-5 py-4 text-xl font-bold text-slate-800 outline-none focus:border-[#1cb0f6]"
      placeholder="Type in English"
    />
  );
}
