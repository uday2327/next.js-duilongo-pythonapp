"use client";

import { useEffect, useState } from "react";
import { Sidebar } from "./Sidebar";
import { HeaderStats } from "./HeaderStats";
import { api } from "@/lib/api";
import type { Stats } from "@/types";

export function AppShell({ children }: { children: React.ReactNode }) {
  const [stats, setStats] = useState<Stats | null>(null);
  useEffect(() => {
    api.stats().then(setStats).catch(() => undefined);
  }, []);
  return (
    <div className="min-h-screen bg-white lg:pl-60">
      <Sidebar />
      {stats && <HeaderStats stats={stats} />}
      <div className="pb-20 lg:pb-0">{children}</div>
    </div>
  );
}
