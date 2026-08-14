"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { LearningPath } from "@/components/LearningPath";
import { QuestCard } from "@/components/QuestCard";
import { api } from "@/lib/api";
import type { LearnPath, LeaderboardEntry, Quest, Stats } from "@/types";

export default function LearnPage() {
  const [path, setPath] = useState<LearnPath | null>(null);
  const [stats, setStats] = useState<Stats | null>(null);
  const [quests, setQuests] = useState<Quest[]>([]);
  const [leaders, setLeaders] = useState<LeaderboardEntry[]>([]);

  useEffect(() => {
    Promise.all([api.learn(), api.stats(), api.quests(), api.leaderboard()]).then(([pathData, statsData, questData, leaderboard]) => {
      setPath(pathData);
      setStats(statsData);
      setQuests(questData.quests);
      setLeaders(leaderboard.entries.slice(0, 3));
    });
  }, []);

  return (
    <AppShell>
      <main className="mx-auto grid max-w-7xl gap-6 px-4 py-6 lg:grid-cols-[minmax(500px,1fr)_310px]">
        <section>{path ? <LearningPath path={path} /> : <div className="py-20 text-center font-black text-slate-400">Loading path...</div>}</section>
        <aside className="space-y-4">
          <div className="rounded-2xl border-2 border-slate-100 bg-card p-4">
            <h2 className="font-black uppercase text-slate-500">Daily Goal</h2>
            <div className="mt-2 text-2xl font-black text-slate-800">{stats?.today_goal_progress || 0} / {stats?.daily_goal || 10} XP</div>
            <div className="mt-3 h-4 rounded-full bg-slate-100">
              <div className="h-full rounded-full bg-accent" style={{ width: `${stats ? Math.min(100, (stats.today_goal_progress / stats.daily_goal) * 100) : 0}%` }} />
            </div>
            <div className="mt-4 grid grid-cols-4 gap-2">
              {[10, 20, 30, 50].map((goal) => <button key={goal} onClick={() => api.setGoal(goal).then(setStats)} className="rounded-xl bg-slate-100 py-2 text-sm font-black text-slate-600">{goal}</button>)}
            </div>
          </div>
          {quests[0] && <QuestCard quest={quests[0]} />}
          <div className="rounded-2xl border-2 border-slate-100 bg-card p-4">
            <h2 className="mb-3 font-black uppercase text-slate-500">Leaderboard</h2>
            {leaders.map((entry) => (
              <div key={entry.id} className={`flex justify-between rounded-xl px-3 py-2 font-bold ${entry.is_current_user ? "bg-slate-100 text-accent" : "text-muted"}`}>
                <span>{entry.rank}. {entry.display_name}</span><span>{entry.weekly_xp} XP</span>
              </div>
            ))}
          </div>
        </aside>
      </main>
    </AppShell>
  );
}
