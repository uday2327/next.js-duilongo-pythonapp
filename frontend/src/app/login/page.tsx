"use client";

import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  function submit(e: React.FormEvent) {
    e.preventDefault();
    setError("");
    // simple demo auth: accept abc@gmail.com / 3214
    if (email.trim().toLowerCase() === "abc@gmail.com" && password === "3214") {
      // mark demo login in localStorage so pages can show as logged-in
      localStorage.setItem("lingo-demo-user", JSON.stringify({ email: "abc@gmail.com", display_name: "Demo User" }));
      // navigate to learn
      router.push("/learn");
      return;
    }
    setError("Invalid demo credentials. Use abc@gmail.com / 3214");
  }

  return (
    <main className="min-h-screen bg-slate-900 text-white">
      <div className="mx-auto max-w-3xl px-4 py-20">
        <div className="mx-auto rounded-2xl bg-slate-800/90 p-8 shadow-xl sm:p-12">
          <div className="mx-auto max-w-md text-center">
            <h1 className="mb-6 text-2xl font-black">Log in</h1>
            <form onSubmit={submit} className="space-y-4">
              <input
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="Email or username"
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-slate-100 outline-none"
              />
              <input
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Password"
                type="password"
                className="w-full rounded-xl border border-slate-700 bg-slate-800 px-4 py-3 text-slate-100 outline-none"
              />
              {error && <div className="text-sm text-rose-400">{error}</div>}
              <button type="submit" className="w-full rounded-xl bg-sky-400 px-4 py-3 font-black text-slate-900">LOG IN</button>
            </form>

            <div className="my-4 flex items-center gap-3">
              <span className="flex-1 border-t border-slate-700" />
              <span className="text-sm text-slate-400">OR</span>
              <span className="flex-1 border-t border-slate-700" />
            </div>

            <div className="grid gap-3 sm:grid-cols-2">
              <button type="button" disabled className="rounded-xl border border-slate-700 px-4 py-3 text-left font-bold text-slate-500">GOOGLE (COMING SOON)</button>
              <button type="button" disabled className="rounded-xl border border-slate-700 px-4 py-3 text-left font-bold text-slate-500">FACEBOOK (COMING SOON)</button>
            </div>

            <p className="mt-6 text-xs text-slate-400">
              By signing in, you agree to our Terms and Privacy Policy.
            </p>

            <div className="mt-6">
              <Link href="/" className="text-sm text-slate-300 underline">Back to site</Link>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}
