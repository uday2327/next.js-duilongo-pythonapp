import { AppShell } from "@/components/AppShell";

export default function SettingsPage() {
  const rows = ["Sound effects", "Animations", "Daily reminders", "Public profile", "Dark mode"];
  return (
    <AppShell>
      <main className="mx-auto max-w-3xl px-4 py-8">
        <h1 className="text-4xl font-black text-slate-800">Settings</h1>
        <div className="mt-8 space-y-4">{rows.map((row, index) => <label key={row} className="flex items-center justify-between rounded-2xl border-2 border-slate-100 bg-white p-5 font-black text-slate-700"><span>{row}</span><input type="checkbox" defaultChecked={index < 3} className="h-6 w-6 accent-[#58cc02]" /></label>)}</div>
      </main>
    </AppShell>
  );
}
