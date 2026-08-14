"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { LessonPlayer } from "@/components/LessonPlayer";
import { api } from "@/lib/api";
import type { Lesson } from "@/types";

export default function LessonPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [lesson, setLesson] = useState<Lesson | null>(null);
  const [error, setError] = useState("");
  useEffect(() => {
    api.lesson(Number(id)).then(setLesson).catch((exc) => setError(exc.message));
  }, [id]);
  if (error) return <div className="grid min-h-screen place-items-center text-center"><div><h1 className="text-3xl font-black">Lesson unavailable</h1><p className="mt-2 font-bold text-slate-500">{error}</p><Link href="/learn" className="mt-6 inline-block rounded-2xl bg-accent px-6 py-3 font-black text-white">Back to path</Link></div></div>;
  if (!lesson) return <div className="grid min-h-screen place-items-center font-black text-slate-400">Loading lesson...</div>;
  return <LessonPlayer lesson={lesson} />;
}
