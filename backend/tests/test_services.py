import os
from datetime import date, timedelta

os.environ["DATABASE_URL"] = "sqlite:///./test_duolingo_clone.db"

from app import models  # noqa: E402
from app.database import Base, SessionLocal, engine  # noqa: E402
from app.seed import seed  # noqa: E402
from app.services.gamification_service import apply_streak  # noqa: E402
from app.services.lesson_service import complete_lesson, validate_answer  # noqa: E402
from app.services.progression_service import build_learning_path  # noqa: E402


def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    seed()


def test_streak_rules():
    stats = models.UserStats(user_id=99, streak=0, longest_streak=0)
    today = date(2026, 8, 13)
    apply_streak(stats, today)
    assert stats.streak == 1
    apply_streak(stats, today)
    assert stats.streak == 1
    apply_streak(stats, today + timedelta(days=1))
    assert stats.streak == 2
    apply_streak(stats, today + timedelta(days=4))
    assert stats.streak == 1


def test_lesson_completion_awards_xp_once():
    reset_db()
    db = SessionLocal()
    before = db.query(models.UserStats).filter_by(user_id=1).one().total_xp
    first = complete_lesson(db, 3, 100, 0, 8, 8)
    after_first = db.query(models.UserStats).filter_by(user_id=1).one().total_xp
    second = complete_lesson(db, 3, 100, 0, 8, 8)
    after = db.query(models.UserStats).filter_by(user_id=1).one().total_xp
    assert first["earned_xp"] == 25
    assert second["earned_xp"] == 0
    assert after_first > before
    assert after == after_first
    db.close()


def test_wrong_answer_removes_one_heart():
    reset_db()
    db = SessionLocal()
    exercise = db.query(models.Exercise).filter_by(lesson_id=3).first()
    before = db.query(models.UserStats).filter_by(user_id=1).one().hearts
    result = validate_answer(db, exercise.id, "definitely wrong")
    assert result["correct"] is False
    assert result["hearts"] == before - 1
    db.close()


def test_quest_progress_updates_on_lesson_complete():
    reset_db()
    db = SessionLocal()
    quest = db.query(models.Quest).filter_by(type="lessons").one()
    before = db.query(models.UserQuestProgress).filter_by(user_id=1, quest_id=quest.id).one().progress
    complete_lesson(db, 3, 80, 1, 6, 8)
    after = db.query(models.UserQuestProgress).filter_by(user_id=1, quest_id=quest.id).one().progress
    assert after == before + 1
    db.close()


def test_next_lesson_unlocks_after_completion():
    reset_db()
    db = SessionLocal()
    before = build_learning_path(db)
    lesson_four_before = before["units"][0]["skills"][1]["lessons"][0]
    assert lesson_four_before["state"] == "locked"
    complete_lesson(db, 3, 90, 0, 7, 8)
    after = build_learning_path(db)
    lesson_four_after = after["units"][0]["skills"][1]["lessons"][0]
    assert lesson_four_after["state"] == "available"
    db.close()
