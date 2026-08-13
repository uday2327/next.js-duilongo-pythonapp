from fastapi import APIRouter, Depends, Query
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.database import get_db
from app import models

router = APIRouter(tags=["languages"])


def language_payload(language: models.Language) -> dict:
    return {
        "id": language.id,
        "name": language.name,
        "native_name": language.native_name,
        "code": language.code,
        "flag": language.flag,
        "available": language.available,
    }


@router.get("/languages")
@router.get("/api/languages")
def languages(search: str | None = Query(default=None), db: Session = Depends(get_db)):
    query = db.query(models.Language)
    if search:
        pattern = f"%{search.lower()}%"
        query = query.filter(
            or_(
                models.Language.name.ilike(pattern),
                models.Language.native_name.ilike(pattern),
                models.Language.code.ilike(pattern),
            )
        )
    rows = query.order_by(models.Language.name).all()
    if search:
        term = search.lower()
        rows.sort(key=lambda language: (
            not language.code.lower().startswith(term),
            not language.name.lower().startswith(term),
            not term in language.name.lower(),
            language.name,
        ))
    return [language_payload(row) for row in rows]


@router.get("/api/languages/course-status")
def course_status(base: str, target: str, db: Session = Depends(get_db)):
    base_language = db.query(models.Language).filter_by(code=base).first()
    target_language = db.query(models.Language).filter_by(code=target).first()
    if not base_language or not target_language:
        return {"available": False, "message": "Language selection unavailable.", "course_id": None}
    course = db.query(models.Course).filter(
        models.Course.source_language_id == base_language.id,
        models.Course.target_language_id == target_language.id,
    ).first()
    if not course:
        return {"available": False, "message": f"{target_language.name} course coming soon.", "course_id": None}
    return {"available": True, "message": f"{target_language.name} course available.", "course_id": course.id}
