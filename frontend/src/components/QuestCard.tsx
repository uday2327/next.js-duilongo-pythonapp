import type { Quest } from "@/types";

export function QuestCard({ quest }: { quest: Quest }) {
  const percent = Math.min(100, (quest.progress / quest.target) * 100);
  return (
    <div className="rounded-2xl border-2 border-slate-100 bg-card p-4">
      <div className="flex items-start justify-between gap-4">
        <div>
          <h3 className="font-black text-slate-800">{quest.title}</h3>
          <p className="text-sm font-semibold text-slate-400">{quest.description}</p>
        </div>
        <span className="rounded-full bg-amber-100 px-2 py-1 text-xs font-black text-amber-700">+{quest.reward_xp} XP</span>
      </div>
      <div className="mt-4 h-4 rounded-full bg-slate-100">
        <div className="h-full rounded-full bg-accent" style={{ width: `${percent}%` }} />
      </div>
      <div className="mt-2 text-sm font-black text-slate-500">{quest.progress}/{quest.target}{quest.completed ? " complete" : ""}</div>
    </div>
  );
}
