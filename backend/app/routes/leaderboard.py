from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.gamification_service import DEFAULT_USER_ID

router = APIRouter(prefix="/api/leaderboard", tags=["leaderboard"])


@router.get("")
def leaderboard(db: Session = Depends(get_db)):
    entries = db.query(models.LeaderboardEntry).order_by(models.LeaderboardEntry.rank).all()
    return {
        "league": "Silver League",
        "entries": [
            {
                "id": entry.id,
                "display_name": entry.display_name,
                "weekly_xp": entry.weekly_xp,
                "rank": entry.rank,
                "is_current_user": entry.user_id == DEFAULT_USER_ID,
            }
            for entry in entries
        ],
    }
