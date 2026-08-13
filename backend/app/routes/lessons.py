from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AnswerRequest, CompleteLessonRequest
from app.services import lesson_service

router = APIRouter(prefix="/api", tags=["lessons"])


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    try:
        return lesson_service.get_lesson(db, lesson_id)
    except ValueError as exc:
        code = str(exc)
        status = 402 if code == "OUT_OF_HEARTS" else 403 if code == "LOCKED" else 404
        raise HTTPException(status_code=status, detail=code)


@router.post("/exercises/{exercise_id}/answer")
def answer_exercise(exercise_id: int, payload: AnswerRequest, db: Session = Depends(get_db)):
    try:
        return lesson_service.validate_answer(db, exercise_id, payload.answer)
    except ValueError:
        raise HTTPException(status_code=404, detail="Exercise not found")


@router.post("/lessons/{lesson_id}/complete")
def complete_lesson(lesson_id: int, payload: CompleteLessonRequest, db: Session = Depends(get_db)):
    try:
        return lesson_service.complete_lesson(
            db,
            lesson_id,
            payload.score,
            payload.mistakes,
            payload.correct_count,
            payload.total_count,
        )
    except ValueError:
        raise HTTPException(status_code=404, detail="Lesson not found")
