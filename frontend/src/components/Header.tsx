"use client";

import { useEffect, useMemo, useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { api } from "@/lib/api";
import type { Language } from "@/types";

function flagEmoji(region?: string | null) {
  if (!region || region.length !== 2) return "🌎";
  return region
    .toUpperCase()
    .split("")
    .map((char) => String.fromCodePoint(127397 + char.charCodeAt(0)))
    .join("");
}

export function Header() {
  const pathname = usePathname();
  const router = useRouter();
  const [languages, setLanguages] = useState<Language[]>([]);
  const [open, setOpen] = useState(false);
  const [siteLanguageMessage, setSiteLanguageMessage] = useState("");
  const [demoUser, setDemoUser] = useState<{ display_name: string; email?: string } | null>(null);

  useEffect(() => {
    // Hydrate demoUser from localStorage after client hydration
    try {
      const raw = localStorage.getItem("lingo-demo-user");
      setDemoUser(raw ? JSON.parse(raw) : null);
    } catch {
      setDemoUser(null);
    }
    
    api.languages().then(setLanguages).catch(() => setLanguages([]));
  }, []);

  const popular = useMemo(() => {
    const popularCodes = ["en", "es", "fr", "de", "ja", "hi", "zh", "pt"];
    return popularCodes.map((c) => languages.find((l) => l.code === c)).filter(Boolean) as Language[];
  }, [languages]);

  if (pathname !== "/" && pathname !== "/login") return null;

  return (
    <header className="sticky top-0 z-40 bg-white">
      <div className="mx-auto flex max-w-7xl items-center justify-between gap-4 px-4 py-3">
        <div className="flex items-center gap-3 text-2xl font-black text-accent">
          <div className="h-8 w-8 rounded-full bg-surface flex items-center justify-center text-accent">L</div>
          <span>Lingo</span>
        </div>

        <div className="flex items-center gap-3">
          {demoUser ? (
            <div className="flex items-center gap-2">
              <div className="rounded-full bg-slate-100 px-3 py-2 text-sm font-black text-slate-800">{demoUser.display_name}</div>
              <button
                onClick={() => {
                  localStorage.removeItem("lingo-demo-user");
                  setDemoUser(null);
                  router.push("/");
                }}
                className="rounded-xl border px-3 py-2 text-sm font-bold uppercase text-slate-600"
              >
                Sign out
              </button>
            </div>
          ) : (
            <Link href="/login" className="rounded-xl border px-3 py-2 text-sm font-bold uppercase text-slate-600">Sign in</Link>
          )}

          <div className="relative">
            <button
              onClick={() => setOpen((value) => !value)}
              className="rounded-xl border px-3 py-2 text-sm font-bold uppercase text-slate-600"
            >
              Site language: English ▾
            </button>

            {open && (
              <div
                onMouseEnter={() => setOpen(true)}
                onMouseLeave={() => setOpen(false)}
                className="absolute right-0 z-50 mt-2 w-[540px] rounded-xl border bg-white p-4 shadow-lg"
              >
                <div className="mb-3 flex items-center justify-between">
                  <strong className="text-sm">Choose site language</strong>
                </div>

                <div className="mb-2 grid grid-cols-2 gap-2">
                  {popular.map((l) => (
                    <button key={l.code} onClick={() => { setSiteLanguageMessage(`${l.name} interface translations are coming soon.`); setOpen(false); }} className="flex items-center gap-3 rounded px-3 py-2 text-left hover:bg-slate-50">
                      <span className="text-xl">{flagEmoji(l.flag)}</span>
                      <span className="font-black">{l.name}</span>
                      <span className="ml-auto text-sm text-slate-400">{l.native_name}</span>
                    </button>
                  ))}
                </div>

                <div className="max-h-64 overflow-y-auto">
                  <div className="grid grid-cols-2 gap-1">
                    {languages.map((l) => (
                      <button key={l.code} onClick={() => { setSiteLanguageMessage(`${l.name} interface translations are coming soon.`); setOpen(false); }} className="flex items-center gap-3 rounded px-3 py-2 text-left hover:bg-slate-50">
                        <span className="text-xl">{flagEmoji(l.flag)}</span>
                        <span className="block font-black">{l.name}</span>
                        <span className="ml-auto text-sm text-slate-400">{l.native_name}</span>
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
      {siteLanguageMessage && <p role="status" className="mx-auto max-w-7xl px-4 pb-3 text-right text-xs font-bold text-muted">{siteLanguageMessage}</p>}
    </header>
  );
}
