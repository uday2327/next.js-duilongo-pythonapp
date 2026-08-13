from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.services.progression_service import build_learning_path

router = APIRouter(prefix="/api", tags=["courses"])


@router.get("/learn")
def learn(db: Session = Depends(get_db)):
    return build_learning_path(db)


@router.get("/characters")
def characters():
    return {
        "cards": [
            {"sound": "a", "word": "apple", "hint": "Short, open vowel", "example": "A as in apple"},
            {"sound": "th", "word": "thanks", "hint": "Tongue lightly touches teeth", "example": "Th as in thanks"},
            {"sound": "v", "word": "very", "hint": "Lower lip touches upper teeth", "example": "V as in very"},
            {"sound": "w", "word": "water", "hint": "Round lips first", "example": "W as in water"},
        ]
    }
