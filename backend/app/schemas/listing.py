from datetime import datetime
from pydantic import BaseModel

from app.models.listing import ListingStatus


class ListingCreate(BaseModel):
    title: str
    quantity: str
    photo_url: str | None = None
    expiry_time: datetime
    lat: float
    lng: float


class ListingOut(BaseModel):
    id: int
    donor_id: int
    title: str
    quantity: str
    photo_url: str | None
    expiry_time: datetime
    freshness_score: float | None
    status: ListingStatus
    lat: float
    lng: float
    created_at: datetime
    distance_km: float | None = None  # populated on nearby-search responses

    class Config:
        from_attributes = True
