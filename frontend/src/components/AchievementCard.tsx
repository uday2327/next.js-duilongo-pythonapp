import { Medal } from "lucide-react";

export function AchievementCard({ title, description, unlocked }: { title: string; description: string; unlocked: boolean }) {
  return (
    <div className={`rounded-2xl border-2 p-4 ${unlocked ? "border-amber-200 bg-amber-50 text-amber-800" : "border-slate-100 bg-slate-50 text-slate-400"}`}>
      <Medal className="mb-3" />
      <h3 className="font-black">{title}</h3>
      <p className="text-sm font-semibold">{description}</p>
    </div>
  );
}
