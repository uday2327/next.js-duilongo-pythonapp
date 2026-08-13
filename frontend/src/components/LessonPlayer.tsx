"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";
import { X } from "lucide-react";
import type { Lesson } from "@/types";
import { api } from "@/lib/api";
import { ExerciseRenderer } from "./ExerciseRenderer";
import { FeedbackBar } from "./FeedbackBar";
import { Hearts } from "./Hearts";

type Answer = string | string[] | Record<string, string>;

export function LessonPlayer({ lesson }: { lesson: Lesson }) {
  const router = useRouter();
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState<Answer>("");
  const [submitted, setSubmitted] = useState(false);
  const [correct, setCorrect] = useState(false);
  const [correctAnswer, setCorrectAnswer] = useState("");
  const [hearts, setHearts] = useState(lesson.hearts);
  const [correctCount, setCorrectCount] = useState(0);
  const [complete, setComplete] = useState<{ earned_xp: number; score: number } | null>(null);
  const exercise = lesson.exercises[index];
  const progress = useMemo(() => ((index + (submitted && correct ? 1 : 0)) / lesson.exercises.length) * 100, [index, submitted, correct, lesson.exercises.length]);

  async function submit(override?: unknown) {
    if (submitted) return;
    const payload = override ?? answer;
    if (exercise.type !== "match_pairs" && (!payload || (Array.isArray(payload) && payload.length === 0))) return;
    const result = await api.answer(exercise.id, payload);
    setSubmitted(true);
    setCorrect(result.correct);
    setCorrectAnswer(result.correct_answer);
    setHearts(result.hearts);
    if (result.correct) setCorrectCount((value) => value + 1);
  }

  async function continueLesson() {
    if (index < lesson.exercises.length - 1) {
      setIndex(index + 1);
      setAnswer("");
      setSubmitted(false);
      setCorrect(false);
      setCorrectAnswer("");
      return;
    }
    const finalCorrect = correctCount;
    const score = Math.round((finalCorrect / lesson.exercises.length) * 100);
    const result = await api.completeLesson(lesson.id, { score, mistakes: lesson.exercises.length - finalCorrect, correct_count: finalCorrect, total_count: lesson.exercises.length });
    setComplete({ earned_xp: result.earned_xp, score: result.score });
  }

  if (hearts <= 0 && !complete) {
    return (
      <div className="grid min-h-screen place-items-center bg-white p-6 text-center">
        <div className="max-w-md rounded-3xl border-2 border-slate-100 p-8 shadow-xl">
          <div className="text-6xl">Heart</div>
          <h1 className="mt-4 text-3xl font-black text-slate-800">Out of hearts!</h1>
          <p className="mt-2 font-semibold text-slate-500">Practice to earn hearts back or refill them in the shop.</p>
          <div className="mt-6 flex gap-3">
            <Link href="/learn" className="flex-1 rounded-2xl border-b-4 border-slate-300 bg-slate-100 px-5 py-3 font-black text-slate-600">Close</Link>
            <Link href="/shop" className="flex-1 rounded-2xl border-b-4 border-[#46a302] bg-[#58cc02] px-5 py-3 font-black text-white">Refill</Link>
          </div>
        </div>
      </div>
    );
  }

  if (complete) {
    return (
      <div className="grid min-h-screen place-items-center bg-[#f7ffef] p-6 text-center">
        <div className="max-w-xl">
          <div className="mx-auto grid h-32 w-32 place-items-center rounded-full bg-[#58cc02] text-5xl font-black text-white shadow-xl">Duo</div>
          <h1 className="mt-6 text-5xl font-black text-slate-800">Lesson complete!</h1>
          <p className="mt-3 text-xl font-bold text-slate-500">Score {complete.score}%</p>
          <div className="mt-8 grid grid-cols-2 gap-4">
            <div className="rounded-2xl border-2 border-amber-200 bg-white p-5 font-black text-amber-600">+{complete.earned_xp} XP</div>
            <div className="rounded-2xl border-2 border-rose-200 bg-white p-5 font-black text-rose-500">{hearts} hearts left</div>
          </div>
          <button onClick={() => router.push("/learn")} className="mt-8 w-full rounded-2xl border-b-4 border-[#46a302] bg-[#58cc02] px-8 py-4 font-black uppercase text-white">Back to path</button>
        </div>
      </div>
    );
  }

  return (
    <main className="mx-auto flex min-h-screen max-w-4xl flex-col px-4 pb-32 pt-6">
      <div className="flex items-center gap-4">
        <button onClick={() => confirm("Leave lesson? Your progress in this lesson will not be saved.") && router.push("/learn")} aria-label="Leave lesson" className="text-slate-400"><X size={32} /></button>
        <div className="h-5 flex-1 rounded-full bg-slate-100"><div className="h-full rounded-full bg-[#58cc02] transition-all" style={{ width: `${progress}%` }} /></div>
        <Hearts count={hearts} />
      </div>
      <section className="flex flex-1 flex-col justify-center py-14">
        <p className="mb-2 font-black uppercase text-[#1cb0f6]">{exercise.instruction}</p>
        <h1 className="mb-12 text-3xl font-black text-slate-800 sm:text-4xl">{exercise.prompt}</h1>
        <ExerciseRenderer exercise={exercise} disabled={submitted} answer={answer} setAnswer={setAnswer} correctAnswer={correctAnswer} submit={submit} />
      </section>
      {!submitted && exercise.type !== "match_pairs" && (
        <button onClick={() => submit()} className="ml-auto rounded-2xl border-b-4 border-[#46a302] bg-[#58cc02] px-10 py-4 font-black uppercase text-white disabled:border-slate-300 disabled:bg-slate-200" disabled={!answer || (Array.isArray(answer) && answer.length === 0)}>
          Check
        </button>
      )}
      {submitted && <FeedbackBar correct={correct} answer={correctAnswer} onContinue={continueLesson} />}
    </main>
  );
}
