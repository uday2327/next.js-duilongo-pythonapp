"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { BookOpen, Flame, Home, Menu, Settings, ShoppingBag, Trophy, User, Volume2 } from "lucide-react";
import { cx } from "@/lib/utils";

const items = [
  { href: "/learn", label: "Learn", icon: Home },
  { href: "/characters", label: "Characters", icon: Volume2 },
  { href: "/leaderboard", label: "Leaderboard", icon: Trophy },
  { href: "/quests", label: "Quests", icon: Flame },
  { href: "/shop", label: "Shop", icon: ShoppingBag },
  { href: "/profile", label: "Profile", icon: User },
  { href: "/settings", label: "Settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();
  return (
    <>
      <aside className="fixed left-0 top-0 hidden h-screen w-60 border-r-2 border-slate-100 bg-white px-4 py-6 lg:block">
        <Link href="/learn" className="mb-8 flex items-center gap-2 px-3 text-3xl font-black text-[#58cc02]">
          <BookOpen size={34} /> Lingo
        </Link>
        <nav className="space-y-2">
          {items.map(({ href, label, icon: Icon }) => (
            <Link
              key={href}
              href={href}
              className={cx(
                "flex items-center gap-3 rounded-2xl px-4 py-3 text-sm font-black uppercase text-slate-500 hover:bg-slate-50",
                pathname === href && "border-2 border-[#84d8ff] bg-[#ddf4ff] text-[#1cb0f6]"
              )}
            >
              <Icon size={24} /> {label}
            </Link>
          ))}
        </nav>
        <button className="mt-3 flex w-full items-center gap-3 rounded-2xl px-4 py-3 text-sm font-black uppercase text-slate-500 hover:bg-slate-50">
          <Menu size={24} /> More
        </button>
      </aside>
      <nav className="fixed bottom-0 left-0 z-30 grid w-full grid-cols-5 border-t-2 border-slate-100 bg-white lg:hidden">
        {items.slice(0, 5).map(({ href, label, icon: Icon }) => (
          <Link key={href} href={href} className={cx("flex flex-col items-center gap-1 py-2 text-[11px] font-bold text-slate-500", pathname === href && "text-[#1cb0f6]")}>
            <Icon size={22} /> {label}
          </Link>
        ))}
      </nav>
    </>
  );
}
