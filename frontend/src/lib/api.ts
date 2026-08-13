import type { Language, LearnPath, Lesson, Quest, Stats, LeaderboardEntry } from "@/types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...init,
    headers: { "Content-Type": "application/json", ...(init?.headers || {}) },
    cache: "no-store",
  });
  if (!response.ok) {
    const body = await response.json().catch(() => ({}));
    throw new Error(body.detail || "Request failed");
  }
  return response.json();
}

export const api = {
  me: () => request<{ user: { display_name: string; username: string; avatar: string }; stats: Stats }>("/api/me"),
  languages: (search?: string) => request<Language[]>(`/api/languages${search ? `?search=${encodeURIComponent(search)}` : ""}`),
  courseStatus: (base: string, target: string) =>
    request<{ available: boolean; message: string; course_id: number | null }>(`/api/languages/course-status?base=${encodeURIComponent(base)}&target=${encodeURIComponent(target)}`),
  stats: () => request<Stats>("/api/stats"),
  learn: () => request<LearnPath>("/api/learn"),
  lesson: (id: number) => request<Lesson>(`/api/lessons/${id}`),
  answer: (exerciseId: number, answer: unknown) =>
    request<{ correct: boolean; correct_answer: string; hearts: number }>(`/api/exercises/${exerciseId}/answer`, {
      method: "POST",
      body: JSON.stringify({ answer }),
    }),
  completeLesson: (lessonId: number, payload: { score: number; mistakes: number; correct_count: number; total_count: number }) =>
    request<{ earned_xp: number; score: number; stats: Stats; skill_progress: number }>(`/api/lessons/${lessonId}/complete`, {
      method: "POST",
      body: JSON.stringify(payload),
    }),
  setGoal: (daily_goal: number) => request<Stats>("/api/stats/goal", { method: "POST", body: JSON.stringify({ daily_goal }) }),
  buy: (item: string) => request<Stats>("/api/stats/shop", { method: "POST", body: JSON.stringify({ item }) }),
  quests: () => request<{ quests: Quest[] }>("/api/quests"),
  leaderboard: () => request<{ league: string; entries: LeaderboardEntry[] }>("/api/leaderboard"),
  profile: () =>
    request<{
      user: { display_name: string; username: string; avatar: string };
      stats: Stats;
      lessons_completed: number;
      skills_completed: number;
      achievements: { id: number; title: string; description: string; icon: string; unlocked: boolean }[];
    }>("/api/profile"),
  characters: () => request<{ cards: { sound: string; word: string; hint: string; example: string }[] }>("/api/characters"),
};
