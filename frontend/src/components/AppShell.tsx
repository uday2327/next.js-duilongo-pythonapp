"use client";

import { useEffect, useState } from "react";
import { AnimatePresence, motion } from "framer-motion";
import { usePathname } from "next/navigation";
import { Sidebar } from "./Sidebar";
import { HeaderStats } from "./HeaderStats";
import { api } from "@/lib/api";
import type { Stats } from "@/types";

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const [stats, setStats] = useState<Stats | null>(null);
  useEffect(() => {
    api.stats().then(setStats).catch(() => undefined);
  }, []);
  return (
    <div className="min-h-screen bg-[var(--background)] lg:pl-60 text-[var(--foreground)]">
      <Sidebar />
      {stats && <HeaderStats stats={stats} />}
      <AnimatePresence mode="wait" initial={false}>
        <motion.div
          key={pathname}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -8 }}
          transition={{ duration: 0.18, ease: "easeOut" }}
          className="pb-20 lg:pb-0"
        >
          {children}
        </motion.div>
      </AnimatePresence>
    </div>
  );
}
