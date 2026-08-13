export type Stats = {
  total_xp: number;
  daily_xp: number;
  streak: number;
  longest_streak: number;
  hearts: number;
  gems: number;
  daily_goal: number;
  today_goal_progress: number;
};

export type LessonSummary = {
  id: number;
  title: string;
  xp_reward: number;
  state: "locked" | "available" | "completed";
  score: number;
};

export type Skill = {
  id: number;
  title: string;
  description: string;
  icon: string;
  color: string;
  progress: number;
  completed: boolean;
  lessons: LessonSummary[];
};

export type Unit = {
  id: number;
  number: number;
  title: string;
  description: string;
  skills: Skill[];
};

export type LearnPath = {
  course: { id: number; name: string; source_language: string; target_language: string; description: string; icon: string };
  units: Unit[];
};

export type Exercise = {
  id: number;
  type: "multiple_choice" | "translate" | "word_bank" | "match_pairs" | "fill_blank" | "type_answer";
  prompt: string;
  instruction: string;
  correct_answer: string;
  explanation: string;
  options: { id: number; text: string; is_correct: boolean }[];
  pairs: { id: number; left_text: string; right_text: string }[];
};

export type Lesson = {
  id: number;
  title: string;
  xp_reward: number;
  estimated_minutes: number;
  hearts: number;
  exercises: Exercise[];
};

export type Quest = {
  id: number;
  title: string;
  description: string;
  target: number;
  progress: number;
  completed: boolean;
  reward_xp: number;
  reward_gems: number;
};

export type LeaderboardEntry = {
  id: number;
  display_name: string;
  weekly_xp: number;
  rank: number;
  is_current_user: boolean;
};

export type Language = {
  id: number;
  name: string;
  native_name: string;
  code: string;
  flag?: string | null;
  available: boolean;
};
