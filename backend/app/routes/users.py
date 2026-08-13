from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.gamification_service import DEFAULT_USER_ID
from app.services.lesson_service import stats_payload

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/me")
def me(db: Session = Depends(get_db)):
    user = db.get(models.User, DEFAULT_USER_ID)
    return {"user": {"id": user.id, "username": user.username, "display_name": user.display_name, "avatar": user.avatar}, "stats": stats_payload(user.stats)}


@router.get("/profile")
def profile(db: Session = Depends(get_db)):
    user = db.get(models.User, DEFAULT_USER_ID)
    lessons = db.query(models.UserLessonProgress).filter_by(user_id=user.id, completed=True).count()
    skills = db.query(models.UserSkillProgress).filter_by(user_id=user.id, completed=True).count()
    achievements = []
    unlocked = {ua.achievement_id: ua for ua in db.query(models.UserAchievement).filter_by(user_id=user.id).all()}
    for achievement in db.query(models.Achievement).all():
        achievements.append({
            "id": achievement.id,
            "title": achievement.title,
            "description": achievement.description,
            "icon": achievement.icon,
            "unlocked": achievement.id in unlocked,
        })
    return {
        "user": {"username": user.username, "display_name": user.display_name, "avatar": user.avatar},
        "stats": stats_payload(user.stats),
        "lessons_completed": lessons,
        "skills_completed": skills,
        "achievements": achievements,
    }
