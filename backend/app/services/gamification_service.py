from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session
from app import models


DEFAULT_USER_ID = 1
MAX_HEARTS = 5
HEART_REGEN_MINUTES = 30


def get_user(db: Session) -> models.User:
    return db.get(models.User, DEFAULT_USER_ID)


def regenerate_hearts(stats: models.UserStats) -> None:
    if stats.hearts >= MAX_HEARTS:
        stats.last_heart_regeneration_at = datetime.utcnow()
        return
    elapsed = datetime.utcnow() - stats.last_heart_regeneration_at
    gained = int(elapsed.total_seconds() // (HEART_REGEN_MINUTES * 60))
    if gained > 0:
        stats.hearts = min(MAX_HEARTS, stats.hearts + gained)
        stats.last_heart_regeneration_at += timedelta(minutes=gained * HEART_REGEN_MINUTES)


def stats_for_user(db: Session, user_id: int = DEFAULT_USER_ID) -> models.UserStats:
    stats = db.query(models.UserStats).filter_by(user_id=user_id).one()
    regenerate_hearts(stats)
    db.commit()
    db.refresh(stats)
    return stats


def apply_streak(stats: models.UserStats, today: date | None = None) -> None:
    today = today or date.today()
    if stats.last_activity_date == today:
        return
    if stats.last_activity_date == today - timedelta(days=1):
        stats.streak += 1
    else:
        stats.streak = 1
    stats.longest_streak = max(stats.longest_streak, stats.streak)
    stats.last_activity_date = today


def lose_hearts(db: Session, mistakes: int, user_id: int = DEFAULT_USER_ID) -> models.UserStats:
    stats = stats_for_user(db, user_id)
    stats.hearts = max(0, stats.hearts - mistakes)
    db.commit()
    db.refresh(stats)
    return stats


def award_lesson_rewards(db: Session, lesson: models.Lesson, score: int, mistakes: int, user_id: int = DEFAULT_USER_ID) -> dict:
    stats = stats_for_user(db, user_id)
    earned_xp = lesson.xp_reward + (5 if score == 100 else 0)
    stats.total_xp += earned_xp
    stats.daily_xp += earned_xp
    stats.today_goal_progress = min(stats.daily_goal, stats.today_goal_progress + earned_xp)
    stats.hearts = max(0, stats.hearts - mistakes)
    apply_streak(stats)
    update_quests(db, user_id, earned_xp, score)
    unlock_achievements(db, user_id, score)
    entry = db.query(models.LeaderboardEntry).filter_by(user_id=user_id).one()
    entry.weekly_xp += earned_xp
    db.flush()
    rerank_leaderboard(db)
    return {"earned_xp": earned_xp, "stats": stats}


def update_quests(db: Session, user_id: int, earned_xp: int, score: int) -> None:
    quests = db.query(models.Quest).filter_by(active=True).all()
    for quest in quests:
        progress = db.query(models.UserQuestProgress).filter_by(user_id=user_id, quest_id=quest.id).one()
        if progress.completed:
            continue
        if quest.type == "lessons":
            progress.progress += 1
        elif quest.type == "xp":
            progress.progress += earned_xp
        elif quest.type == "perfect" and score == 100:
            progress.progress += 1
        if progress.progress >= quest.target:
            progress.progress = quest.target
            progress.completed = True
            progress.completed_at = datetime.utcnow()
            stats = db.query(models.UserStats).filter_by(user_id=user_id).one()
            stats.total_xp += quest.reward_xp
            stats.gems += quest.reward_gems
            progress.claimed = True


def unlock_achievements(db: Session, user_id: int, score: int) -> None:
    stats = db.query(models.UserStats).filter_by(user_id=user_id).one()
    lessons_done = db.query(models.UserLessonProgress).filter_by(user_id=user_id, completed=True).count()
    owned = {a.achievement_id for a in db.query(models.UserAchievement).filter_by(user_id=user_id).all()}
    for achievement in db.query(models.Achievement).all():
        if achievement.id in owned:
            continue
        ok = (
            achievement.requirement_type == "lessons" and lessons_done >= achievement.requirement_value
            or achievement.requirement_type == "xp" and stats.total_xp >= achievement.requirement_value
            or achievement.requirement_type == "streak" and stats.streak >= achievement.requirement_value
            or achievement.requirement_type == "perfect" and score == 100
        )
        if ok:
            db.add(models.UserAchievement(user_id=user_id, achievement_id=achievement.id))


def rerank_leaderboard(db: Session) -> None:
    entries = db.query(models.LeaderboardEntry).order_by(models.LeaderboardEntry.weekly_xp.desc()).all()
    for index, entry in enumerate(entries, 1):
        entry.rank = index


def set_daily_goal(db: Session, goal: int, user_id: int = DEFAULT_USER_ID) -> models.UserStats:
    stats = stats_for_user(db, user_id)
    stats.daily_goal = goal
    db.commit()
    db.refresh(stats)
    return stats


def buy_shop_item(db: Session, item: str, user_id: int = DEFAULT_USER_ID) -> models.UserStats:
    stats = stats_for_user(db, user_id)
    if item == "heart_refill" and stats.gems >= 50:
        stats.gems -= 50
        stats.hearts = MAX_HEARTS
        stats.last_heart_regeneration_at = datetime.utcnow()
    db.commit()
    db.refresh(stats)
    return stats
