"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { QuestCard } from "@/components/QuestCard";
import { api } from "@/lib/api";
import type { Quest } from "@/types";

export default function QuestsPage() {
  const [quests, setQuests] = useState<Quest[]>([]);
  useEffect(() => { api.quests().then((data) => setQuests(data.quests)); }, []);
  return (
    <AppShell>
      <main className="mx-auto max-w-3xl px-4 py-8">
        <h1 className="text-4xl font-black text-slate-800">Quests</h1>
        <p className="mt-2 font-bold text-slate-400">Daily quests update automatically when lessons are completed.</p>
        <div className="mt-8 grid gap-4">{quests.map((quest) => <QuestCard key={quest.id} quest={quest} />)}</div>
        <div className="mt-6 rounded-2xl border-2 border-purple-100 bg-purple-50 p-5 font-black text-purple-700">Monthly Challenge: finish 20 lessons. Coming soon.</div>
      </main>
    </AppShell>
  );
}
