import Link from "next/link";
import type { Stats } from "@/types";

export function HeaderStats({ stats }: { stats: Stats }) {
  return (
    <header className="sticky top-0 z-20 flex items-center justify-between border-b-2 border-slate-100 bg-white/95 px-4 py-3 backdrop-blur">
      <button className="rounded-xl border-2 border-slate-100 px-3 py-2 text-sm font-black text-slate-700">US English</button>
      <div className="flex items-center gap-3 text-sm font-black sm:gap-5 sm:text-base">
        <Link href="/profile" className="text-orange-500">Flame {stats.streak}</Link>
        <Link href="/leaderboard" className="text-[#1cb0f6]">XP {stats.total_xp}</Link>
        <Link href="/shop" className="text-[#ce82ff]">Gem {stats.gems}</Link>
        <Link href="/shop" className="text-rose-500">Heart {stats.hearts}</Link>
      </div>
    </header>
  );
}
