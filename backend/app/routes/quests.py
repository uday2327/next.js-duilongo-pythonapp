from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.services.gamification_service import DEFAULT_USER_ID

router = APIRouter(prefix="/api/quests", tags=["quests"])


@router.get("")
def quests(db: Session = Depends(get_db)):
    rows = []
    for quest in db.query(models.Quest).filter_by(active=True).all():
        progress = db.query(models.UserQuestProgress).filter_by(user_id=DEFAULT_USER_ID, quest_id=quest.id).one()
        rows.append({
            "id": quest.id,
            "title": quest.title,
            "description": quest.description,
            "type": quest.type,
            "target": quest.target,
            "progress": progress.progress,
            "completed": progress.completed,
            "reward_xp": quest.reward_xp,
            "reward_gems": quest.reward_gems,
        })
    return {"quests": rows}
