import Link from "next/link";
import type { Stats } from "@/types";

export function HeaderStats({ stats }: { stats: Stats }) {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b-2 border-slate-100 bg-surface/90 px-4 py-3 backdrop-blur">
      <span className="rounded-xl border-2 border-slate-100 px-3 py-2 text-sm font-black text-muted">US English</span>
      <div className="flex items-center gap-3 text-sm font-black sm:gap-5 sm:text-base">
        <Link href="/profile" className="text-orange-400">Flame {stats.streak}</Link>
        <Link href="/leaderboard" className="text-accent">XP {stats.total_xp}</Link>
        <Link href="/shop" className="text-purple-400">Gem {stats.gems}</Link>
        <Link href="/shop" className="text-rose-400">Heart {stats.hearts}</Link>
      </div>
    </header>
  );
}
