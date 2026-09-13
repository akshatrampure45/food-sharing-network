from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.feedback import Feedback
from app.schemas.match import FeedbackCreate

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("/")
def submit_feedback(payload: FeedbackCreate, db: Session = Depends(get_db)):
    fb = Feedback(delivery_id=payload.delivery_id, rating=payload.rating, comment=payload.comment)
    db.add(fb)
    db.commit()
    db.refresh(fb)
    return fb
