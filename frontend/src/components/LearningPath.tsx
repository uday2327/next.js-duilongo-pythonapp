import type { LearnPath } from "@/types";
import { SkillNode } from "./SkillNode";

export function LearningPath({ path }: { path: LearnPath }) {
  const offsets = ["center", "left", "right"] as const;
  return (
    <div className="relative mx-auto max-w-2xl pb-20">
      <div className="absolute left-1/2 top-32 h-[calc(100%-10rem)] w-2 -translate-x-1/2 rounded-full bg-slate-100" />
      {path.units.map((unit) => (
        <section key={unit.id} className="relative mb-10">
          <div className="sticky top-16 z-10 mx-auto mb-8 rounded-2xl border-b-4 border-accent bg-accent px-6 py-4 text-white shadow-sm">
            <div className="text-xs font-black uppercase">Unit {unit.number}</div>
            <h2 className="text-2xl font-black">{unit.title}</h2>
            <p className="text-sm font-bold text-white/80">{unit.description}</p>
          </div>
          {unit.skills.map((skill, index) => (
            <SkillNode key={skill.id} skill={skill} offset={offsets[index % offsets.length]} />
          ))}
        </section>
      ))}
    </div>
  );
}
