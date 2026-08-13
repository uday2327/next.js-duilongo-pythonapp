"use client";

import { useEffect, useState } from "react";
import { Volume2 } from "lucide-react";
import { AppShell } from "@/components/AppShell";
import { api } from "@/lib/api";

export default function CharactersPage() {
  const [cards, setCards] = useState<{ sound: string; word: string; hint: string; example: string }[]>([]);
  useEffect(() => { api.characters().then((data) => setCards(data.cards)); }, []);
  return (
    <AppShell>
      <main className="mx-auto max-w-4xl px-4 py-8">
        <h1 className="text-4xl font-black text-slate-800">Characters</h1>
        <p className="mt-2 font-bold text-slate-400">Practice English sounds and pronunciation patterns.</p>
        <div className="mt-8 grid gap-4 sm:grid-cols-2">
          {cards.map((card) => <button key={card.sound} onClick={() => speechSynthesis?.speak(new SpeechSynthesisUtterance(card.word))} className="rounded-2xl border-2 border-b-4 border-slate-100 bg-white p-6 text-left hover:bg-slate-50"><Volume2 className="text-[#1cb0f6]" /><div className="mt-4 text-4xl font-black text-slate-800">{card.sound}</div><div className="mt-1 text-xl font-black text-[#58cc02]">{card.word}</div><p className="mt-2 font-bold text-slate-400">{card.hint}</p></button>)}
        </div>
      </main>
    </AppShell>
  );
}
