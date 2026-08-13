"use client";

import { useEffect, useState } from "react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";
import type { Stats } from "@/types";

export default function ShopPage() {
  const [stats, setStats] = useState<Stats | null>(null);
  useEffect(() => { api.stats().then(setStats); }, []);
  return (
    <AppShell>
      <main className="mx-auto max-w-3xl px-4 py-8">
        <h1 className="text-4xl font-black text-slate-800">Shop</h1>
        <p className="mt-2 font-bold text-purple-500">You have {stats?.gems ?? 0} gems.</p>
        <div className="mt-8 grid gap-4">
          <div className="rounded-2xl border-2 border-slate-100 bg-white p-5">
            <h2 className="text-xl font-black text-slate-800">Heart Refill</h2>
            <p className="mt-1 font-bold text-slate-400">Restore all five hearts.</p>
            <button onClick={() => api.buy("heart_refill").then(setStats)} className="mt-4 rounded-2xl border-b-4 border-purple-700 bg-purple-500 px-6 py-3 font-black text-white">Buy for 50 gems</button>
          </div>
          {["Streak Freeze", "Double XP Boost"].map((item) => <div key={item} className="rounded-2xl border-2 border-slate-100 bg-slate-50 p-5 opacity-70"><h2 className="text-xl font-black text-slate-600">{item}</h2><p className="font-bold text-slate-400">Coming soon</p></div>)}
        </div>
      </main>
    </AppShell>
  );
}
