from datetime import datetime
from pydantic import BaseModel

from app.models.match import MatchStatus
from app.models.delivery import DeliveryStatus


class MatchCreate(BaseModel):
    listing_id: int
    recipient_id: int | None = None
    volunteer_id: int | None = None


class MatchOut(BaseModel):
    id: int
    listing_id: int
    recipient_id: int | None
    volunteer_id: int | None
    status: MatchStatus
    matched_at: datetime

    class Config:
        from_attributes = True


class DeliveryOut(BaseModel):
    id: int
    match_id: int
    pickup_time: datetime | None
    delivery_time: datetime | None
    tracking_status: DeliveryStatus

    class Config:
        from_attributes = True


class FeedbackCreate(BaseModel):
    delivery_id: int
    rating: int
    comment: str | None = None
