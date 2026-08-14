"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";
import type { LeaderboardEntry } from "@/types";

export default function LeaderboardPage() {
  const [league, setLeague] = useState("Silver League");
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  useEffect(() => { api.leaderboard().then((data) => { setLeague(data.league); setEntries(data.entries); }); }, []);
  return (
    <AppShell>
      <main className="mx-auto max-w-3xl px-4 py-8">
        <h1 className="text-4xl font-black text-slate-800">Leaderboards</h1>
        <p className="mt-2 font-bold text-slate-400">{league}. Top learners this week.</p>
        <div className="mt-8 space-y-3">
          {entries.map((entry) => <div key={entry.id} className={`flex items-center justify-between rounded-2xl border-2 p-5 font-black ${entry.is_current_user ? "border-accent bg-accent-10 text-accent" : "border-slate-100 bg-card text-muted"}`}><span className="text-lg">{entry.rank <= 3 ? ["Gold", "Silver", "Bronze"][entry.rank - 1] : entry.rank}. {entry.display_name}</span><span>{entry.weekly_xp} XP</span></div>)}
        </div>
      </main>
    </AppShell>
  );
}
