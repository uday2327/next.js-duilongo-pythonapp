from datetime import date, datetime
from sqlalchemy import Boolean, Date, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(64), unique=True)
    display_name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(160), unique=True)
    avatar: Mapped[str] = mapped_column(String(16), default="U")
    age: Mapped[int | None]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    stats: Mapped["UserStats"] = relationship(back_populates="user", uselist=False)


class Language(Base):
    __tablename__ = "languages"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    native_name: Mapped[str] = mapped_column(String(120))
    code: Mapped[str] = mapped_column(String(10), unique=True, index=True)
    flag: Mapped[str | None] = mapped_column(String(8), nullable=True)
    available: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Course(Base):
    __tablename__ = "courses"
    id: Mapped[int] = mapped_column(primary_key=True)
    source_language_id: Mapped[int | None] = mapped_column(ForeignKey("languages.id"), nullable=True)
    target_language_id: Mapped[int | None] = mapped_column(ForeignKey("languages.id"), nullable=True)
    name: Mapped[str] = mapped_column(String(120))
    source_language: Mapped[str] = mapped_column(String(60))
    target_language: Mapped[str] = mapped_column(String(60))
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(16), default="US")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    units: Mapped[list["Unit"]] = relationship(back_populates="course", cascade="all, delete-orphan")


class Unit(Base):
    __tablename__ = "units"
    id: Mapped[int] = mapped_column(primary_key=True)
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    number: Mapped[int]
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    order_index: Mapped[int]
    course: Mapped[Course] = relationship(back_populates="units")
    skills: Mapped[list["Skill"]] = relationship(back_populates="unit", cascade="all, delete-orphan")


class Skill(Base):
    __tablename__ = "skills"
    id: Mapped[int] = mapped_column(primary_key=True)
    unit_id: Mapped[int] = mapped_column(ForeignKey("units.id"))
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(20), default="Star")
    color: Mapped[str] = mapped_column(String(20), default="#58cc02")
    order_index: Mapped[int]
    required_skill_id: Mapped[int | None] = mapped_column(ForeignKey("skills.id"), nullable=True)
    unit: Mapped[Unit] = relationship(back_populates="skills")
    lessons: Mapped[list["Lesson"]] = relationship(back_populates="skill", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"
    id: Mapped[int] = mapped_column(primary_key=True)
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    title: Mapped[str] = mapped_column(String(120))
    order_index: Mapped[int]
    xp_reward: Mapped[int] = mapped_column(default=20)
    heart_cost: Mapped[int] = mapped_column(default=0)
    estimated_minutes: Mapped[int] = mapped_column(default=4)
    skill: Mapped[Skill] = relationship(back_populates="lessons")
    exercises: Mapped[list["Exercise"]] = relationship(back_populates="lesson", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"
    id: Mapped[int] = mapped_column(primary_key=True)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    type: Mapped[str] = mapped_column(String(40))
    prompt: Mapped[str] = mapped_column(Text)
    instruction: Mapped[str] = mapped_column(Text)
    correct_answer: Mapped[str] = mapped_column(Text)
    explanation: Mapped[str] = mapped_column(Text, default="")
    audio_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    order_index: Mapped[int]
    lesson: Mapped[Lesson] = relationship(back_populates="exercises")
    options: Mapped[list["ExerciseOption"]] = relationship(back_populates="exercise", cascade="all, delete-orphan")
    pairs: Mapped[list["MatchPair"]] = relationship(back_populates="exercise", cascade="all, delete-orphan")


class ExerciseOption(Base):
    __tablename__ = "exercise_options"
    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    text: Mapped[str] = mapped_column(String(160))
    is_correct: Mapped[bool] = mapped_column(Boolean, default=False)
    order_index: Mapped[int]
    exercise: Mapped[Exercise] = relationship(back_populates="options")


class MatchPair(Base):
    __tablename__ = "match_pairs"
    id: Mapped[int] = mapped_column(primary_key=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    left_text: Mapped[str] = mapped_column(String(160))
    right_text: Mapped[str] = mapped_column(String(160))
    exercise: Mapped[Exercise] = relationship(back_populates="pairs")


class UserCourseProgress(Base):
    __tablename__ = "user_course_progress"
    __table_args__ = (UniqueConstraint("user_id", "course_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    course_id: Mapped[int] = mapped_column(ForeignKey("courses.id"))
    current_unit_id: Mapped[int | None]
    current_skill_id: Mapped[int | None]
    completed_lessons: Mapped[int] = mapped_column(default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserSkillProgress(Base):
    __tablename__ = "user_skill_progress"
    __table_args__ = (UniqueConstraint("user_id", "skill_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    skill_id: Mapped[int] = mapped_column(ForeignKey("skills.id"))
    xp: Mapped[int] = mapped_column(default=0)
    level: Mapped[int] = mapped_column(default=0)
    progress: Mapped[int] = mapped_column(default=0)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    crown_level: Mapped[int] = mapped_column(default=0)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class UserLessonProgress(Base):
    __tablename__ = "user_lesson_progress"
    __table_args__ = (UniqueConstraint("user_id", "lesson_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lessons.id"))
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    score: Mapped[int] = mapped_column(default=0)
    attempts: Mapped[int] = mapped_column(default=0)
    best_score: Mapped[int] = mapped_column(default=0)
    completed_at: Mapped[datetime | None]


class UserExerciseProgress(Base):
    __tablename__ = "user_exercise_progress"
    __table_args__ = (UniqueConstraint("user_id", "exercise_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"))
    attempts: Mapped[int] = mapped_column(default=0)
    correct_attempts: Mapped[int] = mapped_column(default=0)
    incorrect_attempts: Mapped[int] = mapped_column(default=0)
    last_attempt_at: Mapped[datetime | None]


class UserStats(Base):
    __tablename__ = "user_stats"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    total_xp: Mapped[int] = mapped_column(default=0)
    daily_xp: Mapped[int] = mapped_column(default=0)
    streak: Mapped[int] = mapped_column(default=0)
    longest_streak: Mapped[int] = mapped_column(default=0)
    hearts: Mapped[int] = mapped_column(default=5)
    gems: Mapped[int] = mapped_column(default=100)
    last_activity_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    daily_goal: Mapped[int] = mapped_column(default=10)
    today_goal_progress: Mapped[int] = mapped_column(default=0)
    last_heart_regeneration_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    user: Mapped[User] = relationship(back_populates="stats")


class Quest(Base):
    __tablename__ = "quests"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    type: Mapped[str] = mapped_column(String(40))
    target: Mapped[int]
    reward_xp: Mapped[int] = mapped_column(default=0)
    reward_gems: Mapped[int] = mapped_column(default=0)
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class UserQuestProgress(Base):
    __tablename__ = "user_quest_progress"
    __table_args__ = (UniqueConstraint("user_id", "quest_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    quest_id: Mapped[int] = mapped_column(ForeignKey("quests.id"))
    progress: Mapped[int] = mapped_column(default=0)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
    claimed: Mapped[bool] = mapped_column(Boolean, default=False)
    completed_at: Mapped[datetime | None]


class Achievement(Base):
    __tablename__ = "achievements"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120))
    description: Mapped[str] = mapped_column(Text)
    icon: Mapped[str] = mapped_column(String(20))
    requirement_type: Mapped[str] = mapped_column(String(40))
    requirement_value: Mapped[int]


class UserAchievement(Base):
    __tablename__ = "user_achievements"
    __table_args__ = (UniqueConstraint("user_id", "achievement_id"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    achievement_id: Mapped[int] = mapped_column(ForeignKey("achievements.id"))
    unlocked_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class LeaderboardEntry(Base):
    __tablename__ = "leaderboard_entries"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    display_name: Mapped[str] = mapped_column(String(120))
    league: Mapped[str] = mapped_column(String(60), default="Silver League")
    weekly_xp: Mapped[int] = mapped_column(default=0)
    rank: Mapped[int] = mapped_column(default=1)
    week_start: Mapped[date] = mapped_column(Date, default=func.current_date())
