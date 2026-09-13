import enum
from datetime import datetime

from sqlalchemy import Column, Integer, DateTime, Enum, ForeignKey
from app.database import Base


class MatchStatus(str, enum.Enum):
    proposed = "proposed"
    accepted = "accepted"
    rejected = "rejected"
    completed = "completed"


class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)
    listing_id = Column(Integer, ForeignKey("food_listings.id"), nullable=False)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    volunteer_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(Enum(MatchStatus), default=MatchStatus.proposed)
    matched_at = Column(DateTime, default=datetime.utcnow)
