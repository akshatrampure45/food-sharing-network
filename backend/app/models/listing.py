import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum, ForeignKey
from geoalchemy2 import Geography
from app.database import Base, IS_POSTGRES


class ListingStatus(str, enum.Enum):
    available = "available"
    matched = "matched"
    picked_up = "picked_up"
    delivered = "delivered"
    expired = "expired"


class FoodListing(Base):
    __tablename__ = "food_listings"

    id = Column(Integer, primary_key=True, index=True)
    donor_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    quantity = Column(String, nullable=False)
    photo_url = Column(String, nullable=True)
    expiry_time = Column(DateTime, nullable=False)
    freshness_score = Column(Float, nullable=True)
    status = Column(Enum(ListingStatus), default=ListingStatus.available)
    lat = Column(Float, nullable=False)
    lng = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    if IS_POSTGRES:
        # PostGIS geography column, kept in sync with lat/lng on create.
        # Enables fast ST_DWithin / ST_Distance queries — see services/matcher.py
        location = Column(Geography(geometry_type="POINT", srid=4326), nullable=True)
