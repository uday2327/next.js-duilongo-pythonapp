from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import AnswerRequest, CompleteLessonRequest
from app.services import lesson_service

router = APIRouter(prefix="/api", tags=["lessons"])


def raise_service_error(exc: ValueError) -> None:
    code = str(exc)
    status = {"OUT_OF_HEARTS": 402, "LOCKED": 403, "NOT_FOUND": 404}.get(code, 400)
    raise HTTPException(status_code=status, detail=code)


@router.get("/lessons/{lesson_id}")
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    try:
        return lesson_service.get_lesson(db, lesson_id)
    except ValueError as exc:
        raise_service_error(exc)


@router.post("/exercises/{exercise_id}/answer")
def answer_exercise(exercise_id: int, payload: AnswerRequest, db: Session = Depends(get_db)):
    try:
        return lesson_service.validate_answer(db, exercise_id, payload.answer)
    except ValueError as exc:
        raise_service_error(exc)


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
    except ValueError as exc:
        raise_service_error(exc)
