"use client";

import Link from "next/link";
import { Check, Lock, Play, Star } from "lucide-react";
import type { Skill } from "@/types";
import { ProgressRing } from "./ProgressRing";
import { cx } from "@/lib/utils";

export function SkillNode({ skill, offset }: { skill: Skill; offset: "left" | "right" | "center" }) {
  const availableLesson = skill.lessons.find((lesson) => lesson.state === "available");
  const completed = skill.completed;
  const locked = !availableLesson && !completed;
  const content = (
    <div className={cx("group relative flex w-56 flex-col items-center gap-2", offset === "left" && "mr-28", offset === "right" && "ml-28")}>
      <ProgressRing progress={skill.progress}>
        <div className={cx("grid h-16 w-16 place-items-center rounded-full border-b-8 text-white shadow-lg transition group-hover:translate-y-1", locked ? "border-slate-400 bg-slate-300" : completed ? "border-amber-500 bg-amber-400" : "border-[#46a302] bg-[#58cc02]")}>
          {locked ? <Lock /> : completed ? <Check /> : <Star />}
        </div>
      </ProgressRing>
      <div className="text-center">
        <div className="font-black text-slate-800">{skill.title}</div>
        <div className="text-xs font-bold text-slate-400">{skill.lessons.filter((l) => l.state === "completed").length}/{skill.lessons.length} lessons</div>
      </div>
      {!locked && (
        <div className="absolute -right-10 top-8 rounded-full bg-white p-2 text-[#58cc02] shadow">
          <Play size={18} fill="currentColor" />
        </div>
      )}
    </div>
  );
  if (locked) return <div className="flex justify-center py-6 opacity-80">{content}</div>;
  return <Link href={`/lesson/${availableLesson?.id || skill.lessons[0].id}`} className="flex justify-center py-6">{content}</Link>;
}
