import re
from datetime import datetime
from sqlalchemy.orm import Session
from app import models
from app.services import gamification_service, progression_service


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value.strip().lower()).rstrip(".,!?।")


def accessible_lesson(db: Session, lesson_id: int, user_id: int) -> models.Lesson:
    lesson = db.get(models.Lesson, lesson_id)
    if not lesson:
        raise ValueError("NOT_FOUND")
    if lesson_id not in progression_service.unlocked_lesson_ids(db, user_id):
        raise ValueError("LOCKED")
    return lesson


def get_lesson(db: Session, lesson_id: int, user_id: int = 1) -> dict:
    lesson = accessible_lesson(db, lesson_id, user_id)
    stats = gamification_service.stats_for_user(db, user_id)
    if stats.hearts <= 0:
        raise ValueError("OUT_OF_HEARTS")
    return {
        "id": lesson.id,
        "title": lesson.title,
        "xp_reward": lesson.xp_reward,
        "estimated_minutes": lesson.estimated_minutes,
        "hearts": stats.hearts,
        "exercises": [
            {
                "id": exercise.id,
                "type": exercise.type,
                "prompt": exercise.prompt,
                "instruction": exercise.instruction,
                "correct_answer": exercise.correct_answer,
                "explanation": exercise.explanation,
                "options": [
                    {"id": option.id, "text": option.text, "is_correct": option.is_correct}
                    for option in sorted(exercise.options, key=lambda item: item.order_index)
                ],
                "pairs": [
                    {"id": pair.id, "left_text": pair.left_text, "right_text": pair.right_text}
                    for pair in exercise.pairs
                ],
            }
            for exercise in sorted(lesson.exercises, key=lambda item: item.order_index)
        ],
    }


def validate_answer(db: Session, exercise_id: int, answer, user_id: int = 1) -> dict:
    exercise = db.get(models.Exercise, exercise_id)
    if not exercise:
        raise ValueError("NOT_FOUND")
    accessible_lesson(db, exercise.lesson_id, user_id)
    stats = gamification_service.stats_for_user(db, user_id)
    if stats.hearts <= 0:
        raise ValueError("OUT_OF_HEARTS")
    expected = normalize(exercise.correct_answer)
    if exercise.type == "match_pairs":
        correct = isinstance(answer, dict) and all(answer.get(pair.left_text) == pair.right_text for pair in exercise.pairs)
    elif isinstance(answer, list):
        correct = normalize(" ".join(answer)) == expected
    else:
        correct = normalize(str(answer)) == expected
    progress = db.query(models.UserExerciseProgress).filter_by(user_id=user_id, exercise_id=exercise_id).first()
    if not progress:
        progress = models.UserExerciseProgress(user_id=user_id, exercise_id=exercise_id, attempts=0, correct_attempts=0, incorrect_attempts=0)
        db.add(progress)
    progress.attempts += 1
    progress.correct_attempts += 1 if correct else 0
    progress.incorrect_attempts += 0 if correct else 1
    progress.last_attempt_at = datetime.utcnow()
    if not correct:
        stats.hearts = max(0, stats.hearts - 1)
    db.commit()
    return {"correct": correct, "correct_answer": exercise.correct_answer, "hearts": stats.hearts}


def complete_lesson(db: Session, lesson_id: int, score: int, mistakes: int, correct_count: int, total_count: int, user_id: int = 1) -> dict:
    lesson = accessible_lesson(db, lesson_id, user_id)
    stats = gamification_service.stats_for_user(db, user_id)
    if stats.hearts <= 0:
        raise ValueError("OUT_OF_HEARTS")
    if correct_count > total_count:
        raise ValueError("INVALID_COMPLETION")

    progress = db.query(models.UserLessonProgress).filter_by(user_id=user_id, lesson_id=lesson_id).first()
    already_completed = bool(progress and progress.completed)
    if not progress:
        progress = models.UserLessonProgress(user_id=user_id, lesson_id=lesson_id, completed=False, score=0, attempts=0, best_score=0)
        db.add(progress)
    progress.attempts += 1
    progress.score = score
    progress.best_score = max(progress.best_score, score)
    progress.completed = True
    progress.completed_at = progress.completed_at or datetime.utcnow()
    if already_completed:
        reward = {"earned_xp": 0, "stats": stats}
    else:
        reward = gamification_service.award_lesson_rewards(db, lesson, score, 0, user_id)
        course_progress = db.query(models.UserCourseProgress).filter_by(
            user_id=user_id,
            course_id=lesson.skill.unit.course_id,
        ).first()
        if not course_progress:
            course_progress = models.UserCourseProgress(
                user_id=user_id,
                course_id=lesson.skill.unit.course_id,
                current_unit_id=lesson.skill.unit_id,
                current_skill_id=lesson.skill_id,
                completed_lessons=0,
            )
            db.add(course_progress)
        course_progress.completed_lessons += 1
        course_progress.current_unit_id = lesson.skill.unit_id
        course_progress.current_skill_id = lesson.skill_id
    skill_progress = progression_service.update_skill_progress(db, user_id, lesson.skill_id)
    db.commit()
    return {
        "earned_xp": reward["earned_xp"],
        "score": score,
        "correct_count": correct_count,
        "total_count": total_count,
        "stats": stats_payload(reward["stats"]),
        "skill_progress": skill_progress.progress,
    }


def stats_payload(stats: models.UserStats) -> dict:
    return {
        "total_xp": stats.total_xp,
        "daily_xp": stats.daily_xp,
        "streak": stats.streak,
        "longest_streak": stats.longest_streak,
        "hearts": stats.hearts,
        "gems": stats.gems,
        "daily_goal": stats.daily_goal,
        "today_goal_progress": stats.today_goal_progress,
    }
