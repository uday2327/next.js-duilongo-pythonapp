from sqlalchemy.orm import Session
from app import models


def lesson_ids_in_order(db: Session) -> list[int]:
    return [
        row.id
        for row in db.query(models.Lesson)
        .join(models.Skill)
        .join(models.Unit)
        .order_by(models.Unit.order_index, models.Skill.order_index, models.Lesson.order_index)
        .all()
    ]


def unlocked_lesson_ids(db: Session, user_id: int) -> set[int]:
    ordered = lesson_ids_in_order(db)
    completed = {
        p.lesson_id
        for p in db.query(models.UserLessonProgress).filter_by(user_id=user_id, completed=True).all()
    }
    unlocked = set()
    for lesson_id in ordered:
        unlocked.add(lesson_id)
        if lesson_id not in completed:
            break
    return unlocked | completed


def update_skill_progress(db: Session, user_id: int, skill_id: int) -> models.UserSkillProgress:
    total = db.query(models.Lesson).filter_by(skill_id=skill_id).count()
    lessons = db.query(models.Lesson).filter_by(skill_id=skill_id).all()
    completed = db.query(models.UserLessonProgress).filter(
        models.UserLessonProgress.user_id == user_id,
        models.UserLessonProgress.lesson_id.in_([lesson.id for lesson in lessons]),
        models.UserLessonProgress.completed == True,  # noqa: E712
    ).count()
    progress = db.query(models.UserSkillProgress).filter_by(user_id=user_id, skill_id=skill_id).first()
    if not progress:
        progress = models.UserSkillProgress(user_id=user_id, skill_id=skill_id)
        db.add(progress)
    progress.progress = int((completed / total) * 100) if total else 0
    progress.completed = progress.progress == 100
    progress.level = completed
    progress.crown_level = 1 if progress.completed else 0
    return progress


def build_learning_path(db: Session, user_id: int = 1) -> dict:
    course = db.query(models.Course).first()
    unlocked = unlocked_lesson_ids(db, user_id)
    completed_lessons = {
        p.lesson_id: p
        for p in db.query(models.UserLessonProgress).filter_by(user_id=user_id, completed=True).all()
    }
    skill_progress = {
        p.skill_id: p
        for p in db.query(models.UserSkillProgress).filter_by(user_id=user_id).all()
    }
    units = []
    for unit in sorted(course.units, key=lambda item: item.order_index):
        unit_skills = []
        for skill in sorted(unit.skills, key=lambda item: item.order_index):
            lessons = []
            for lesson in sorted(skill.lessons, key=lambda item: item.order_index):
                lessons.append({
                    "id": lesson.id,
                    "title": lesson.title,
                    "xp_reward": lesson.xp_reward,
                    "state": "completed" if lesson.id in completed_lessons else "available" if lesson.id in unlocked else "locked",
                    "score": completed_lessons.get(lesson.id).best_score if lesson.id in completed_lessons else 0,
                })
            progress = skill_progress.get(skill.id)
            unit_skills.append({
                "id": skill.id,
                "title": skill.title,
                "description": skill.description,
                "icon": skill.icon,
                "color": skill.color,
                "progress": progress.progress if progress else 0,
                "completed": progress.completed if progress else False,
                "lessons": lessons,
            })
        units.append({
            "id": unit.id,
            "number": unit.number,
            "title": unit.title,
            "description": unit.description,
            "skills": unit_skills,
        })
    return {
        "course": {
            "id": course.id,
            "name": course.name,
            "source_language": course.source_language,
            "target_language": course.target_language,
            "description": course.description,
            "icon": course.icon,
        },
        "units": units,
    }
