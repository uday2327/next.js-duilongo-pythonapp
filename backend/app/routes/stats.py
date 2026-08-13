from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import GoalRequest, RefillRequest
from app.services import gamification_service
from app.services.lesson_service import stats_payload

router = APIRouter(prefix="/api/stats", tags=["stats"])


@router.get("")
def stats(db: Session = Depends(get_db)):
    return stats_payload(gamification_service.stats_for_user(db))


@router.post("/goal")
def set_goal(payload: GoalRequest, db: Session = Depends(get_db)):
    return stats_payload(gamification_service.set_daily_goal(db, payload.daily_goal))


@router.post("/shop")
def shop(payload: RefillRequest, db: Session = Depends(get_db)):
    return stats_payload(gamification_service.buy_shop_item(db, payload.item))
