from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.gamification_service import DEFAULT_USER_ID
from app.services.lesson_service import stats_payload
from app.schemas import SelectCourseRequest

router = APIRouter(prefix="/api", tags=["users"])


@router.get("/me")
def me(db: Session = Depends(get_db)):
    user = db.get(models.User, DEFAULT_USER_ID)
    progress = db.query(models.UserCourseProgress).filter_by(user_id=user.id).first()
    selected_course = None
    if progress and progress.course_id:
        course = db.get(models.Course, progress.course_id)
        if course:
            selected_course = {"id": course.id, "name": course.name, "source_language": course.source_language, "target_language": course.target_language}
    return {"user": {"id": user.id, "username": user.username, "display_name": user.display_name, "avatar": user.avatar}, "stats": stats_payload(user.stats), "selected_course": selected_course}


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



@router.post("/select-course")
def select_course(payload: SelectCourseRequest, db: Session = Depends(get_db)):
    """Set the user's selected course (demo endpoint)."""
    user = db.get(models.User, DEFAULT_USER_ID)
    course = db.get(models.Course, payload.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    progress = db.query(models.UserCourseProgress).filter_by(user_id=user.id).first()
    if not progress:
        progress = models.UserCourseProgress(
            user_id=user.id,
            course_id=course.id,
            current_unit_id=None,
            current_skill_id=None,
            completed_lessons=0,
        )
        db.add(progress)
    else:
        progress.course_id = course.id
    db.commit()
    return {"ok": True, "course_id": course.id}
