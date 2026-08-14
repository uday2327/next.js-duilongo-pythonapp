"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { AchievementCard } from "@/components/AchievementCard";
import { api } from "@/lib/api";

export default function ProfilePage() {
  const [profile, setProfile] = useState<Awaited<ReturnType<typeof api.profile>> | null>(null);
  useEffect(() => { api.profile().then(setProfile); }, []);
  return (
    <AppShell>
      <main className="mx-auto max-w-4xl px-4 py-8">
        {profile && <>
          <div className="flex items-center gap-5"><div className="grid h-24 w-24 place-items-center rounded-full bg-accent text-3xl font-black text-white">{profile.user.avatar}</div><div><h1 className="text-4xl font-black text-[var(--foreground)]">{profile.user.display_name}</h1><p className="font-bold text-muted">@{profile.user.username}</p></div></div>
          <div className="mt-8 grid gap-4 sm:grid-cols-4">{[["Current Streak", `${profile.stats.streak} day`], ["Total XP", profile.stats.total_xp], ["Lessons", profile.lessons_completed], ["Skills", profile.skills_completed]].map(([label, value]) => <div key={String(label)} className="rounded-2xl border-2 border-slate-100 bg-white p-4"><div className="text-xs font-black uppercase text-slate-400">{label}</div><div className="mt-2 text-2xl font-black text-slate-800">{value}</div></div>)}</div>
          <h2 className="mt-10 text-2xl font-black text-slate-800">Achievements</h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-3">{profile.achievements.map((item) => <AchievementCard key={item.id} title={item.title} description={item.description} unlocked={item.unlocked} />)}</div>
        </>}
      </main>
    </AppShell>
  );
}
