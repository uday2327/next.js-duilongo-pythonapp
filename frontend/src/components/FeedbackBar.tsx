"use client";

import { CheckCircle, XCircle } from "lucide-react";

export function FeedbackBar({ correct, answer, onContinue }: { correct: boolean; answer: string; onContinue: () => void }) {
  return (
    <div className={`fixed inset-x-0 bottom-0 z-30 border-t-2 px-4 py-5 ${correct ? "border-green-200 bg-green-100" : "border-red-200 bg-red-100"}`}>
      <div className="mx-auto flex max-w-4xl flex-col items-start justify-between gap-4 sm:flex-row sm:items-center">
        <div className={`flex items-center gap-3 font-black ${correct ? "text-green-700" : "text-red-700"}`}>
          {correct ? <CheckCircle size={32} /> : <XCircle size={32} />}
          <div>
            <div className="text-xl">{correct ? "Great job!" : "Correct solution:"}</div>
            {!correct && <div className="text-base">{answer}</div>}
          </div>
        </div>
        <button onClick={onContinue} className={`w-full rounded-2xl border-b-4 px-8 py-3 font-black uppercase text-white sm:w-auto ${correct ? "border-green-700 bg-[#58cc02]" : "border-red-700 bg-red-500"}`}>
          Continue
        </button>
      </div>
    </div>
  );
}
