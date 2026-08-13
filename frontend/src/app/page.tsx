"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";
import { BookOpen, CheckCircle, Search, Sparkles } from "lucide-react";
import { api } from "@/lib/api";
import type { Language } from "@/types";

const popularCodes = ["en", "es", "fr", "de", "ja", "hi", "zh", "ko", "ar", "pt"];

function flagEmoji(region?: string | null) {
  if (!region || region.length !== 2) return "🌎";
  return region
    .toUpperCase()
    .split("")
    .map((char) => String.fromCodePoint(127397 + char.charCodeAt(0)))
    .join("");
}

export default function LanguageSelectionPage() {
  const router = useRouter();
  const [languages, setLanguages] = useState<Language[]>([]);
  const [baseCode, setBaseCode] = useState("hi");
  const [targetCode, setTargetCode] = useState("en");
  const [search, setSearch] = useState("");
  const [message, setMessage] = useState("");
  const [checking, setChecking] = useState(false);

  useEffect(() => {
    api.languages().then(setLanguages);
  }, []);

  const filtered = useMemo(() => {
    const term = search.trim().toLowerCase();
    if (!term) return languages;
    return languages.filter((language) =>
      [language.name, language.native_name, language.code].some((value) => value.toLowerCase().includes(term))
    );
  }, [languages, search]);

  const popular = popularCodes
    .map((code) => languages.find((language) => language.code === code))
    .filter(Boolean) as Language[];

  const grouped = filtered.reduce<Record<string, Language[]>>((groups, language) => {
    const letter = language.name[0].toUpperCase();
    groups[letter] = [...(groups[letter] || []), language];
    return groups;
  }, {});

  const selectedTarget = languages.find((language) => language.code === targetCode);

  async function startLearning() {
    setChecking(true);
    const status = await api.courseStatus(baseCode, targetCode);
    setChecking(false);
    setMessage(status.message);
    if (status.available) {
      localStorage.setItem("lingo-language-selection", JSON.stringify({ baseCode, targetCode }));
      router.push("/learn");
    }
  }

  return (
    <main className="min-h-screen bg-[#f7fafc] px-4 py-8">
      <section className="mx-auto max-w-5xl">
        <div className="mb-8 flex items-center justify-center gap-3 text-[#58cc02]">
          <BookOpen size={38} />
          <span className="text-4xl font-black">Lingo</span>
        </div>
        <div className="rounded-[2rem] border-2 border-slate-100 bg-white p-5 shadow-sm sm:p-8">
          <div className="mx-auto max-w-2xl text-center">
            <div className="mx-auto mb-4 grid h-16 w-16 place-items-center rounded-full bg-[#ddf4ff] text-[#1cb0f6]">
              <Sparkles />
            </div>
            <h1 className="text-4xl font-black text-slate-800 sm:text-5xl">What do you want to learn?</h1>
            <p className="mt-3 font-bold text-slate-500">Choose the language you know and the language you want to practice.</p>
          </div>

          <div className="mt-8 grid gap-4 sm:grid-cols-2">
            <label className="block rounded-2xl border-2 border-slate-100 bg-slate-50 p-4">
              <span className="text-xs font-black uppercase text-slate-400">I speak</span>
              <select value={baseCode} onChange={(event) => setBaseCode(event.target.value)} className="mt-2 w-full bg-transparent text-xl font-black text-slate-800 outline-none">
                {languages.map((language) => <option key={language.code} value={language.code}>{language.name} - {language.native_name}</option>)}
              </select>
            </label>
            <div className="rounded-2xl border-2 border-[#84d8ff] bg-[#ddf4ff] p-4">
              <span className="text-xs font-black uppercase text-[#1cb0f6]">I want to learn</span>
              <div className="mt-2 text-xl font-black text-slate-800">
                {selectedTarget ? `${flagEmoji(selectedTarget.flag)} ${selectedTarget.name} - ${selectedTarget.native_name}` : "Choose a language"}
              </div>
            </div>
          </div>

          <div className="mt-6 flex items-center gap-3 rounded-2xl border-2 border-slate-200 px-4 py-3">
            <Search className="text-slate-400" />
            <input value={search} onChange={(event) => setSearch(event.target.value)} placeholder="Search languages..." className="w-full text-lg font-bold text-slate-700 outline-none" />
          </div>

          <section className="mt-8">
            <h2 className="mb-3 text-sm font-black uppercase text-slate-400">Popular languages</h2>
            <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
              {popular.map((language) => (
                <button key={language.code} onClick={() => setTargetCode(language.code)} className={`rounded-2xl border-2 border-b-4 p-4 text-left font-black transition hover:bg-slate-50 ${targetCode === language.code ? "border-[#58cc02] bg-green-50 text-[#46a302]" : "border-slate-100 bg-white text-slate-700"}`}>
                  <div className="text-2xl">{flagEmoji(language.flag)}</div>
                  <div>{language.name}</div>
                  <div className="text-sm font-bold text-slate-400">{language.native_name}</div>
                  <div className={`mt-2 text-xs ${language.available ? "text-[#58cc02]" : "text-slate-400"}`}>{language.available ? "Course available" : "Coming soon"}</div>
                </button>
              ))}
            </div>
          </section>

          <section className="mt-8 max-h-[420px] overflow-y-auto rounded-2xl border-2 border-slate-100 p-4">
            <h2 className="mb-3 text-sm font-black uppercase text-slate-400">All languages</h2>
            {Object.entries(grouped).map(([letter, items]) => (
              <div key={letter} className="mb-5">
                <div className="sticky top-0 bg-white py-2 text-lg font-black text-slate-300">{letter}</div>
                <div className="grid gap-2 sm:grid-cols-2">
                  {items.map((language) => (
                    <button key={language.code} onClick={() => setTargetCode(language.code)} className={`flex items-center justify-between rounded-2xl px-4 py-3 text-left transition ${targetCode === language.code ? "bg-green-50 text-[#46a302]" : "hover:bg-slate-50"}`}>
                      <span className="flex items-center gap-3">
                        <span className="text-xl">{flagEmoji(language.flag)}</span>
                        <span><span className="block font-black">{language.name}</span><span className="text-sm font-bold text-slate-400">{language.native_name}</span></span>
                      </span>
                      {targetCode === language.code && <CheckCircle size={20} />}
                    </button>
                  ))}
                </div>
              </div>
            ))}
          </section>

          {message && <div className={`mt-5 rounded-2xl p-4 text-center font-black ${message.includes("available") ? "bg-green-50 text-[#46a302]" : "bg-amber-50 text-amber-700"}`}>{message}</div>}
          <button onClick={startLearning} disabled={checking || !targetCode || !baseCode} className="mt-6 w-full rounded-2xl border-b-4 border-[#46a302] bg-[#58cc02] px-8 py-4 text-lg font-black uppercase text-white disabled:border-slate-300 disabled:bg-slate-200">
            {checking ? "Checking..." : "Start Learning"}
          </button>
        </div>
      </section>
    </main>
  );
}
