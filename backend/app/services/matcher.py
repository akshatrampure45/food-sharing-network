"""
Nearby-listing matching.

Two paths:
- Postgres + PostGIS: DB-side ST_DWithin / ST_Distance query, fast at scale.
- SQLite (local dev without Postgres set up yet): plain-Python haversine
  distance as a fallback so the app still runs without a Postgres install.
"""
import math

from geoalchemy2.functions import ST_DWithin, ST_Distance, ST_MakePoint, ST_SetSRID
from sqlalchemy.orm import Session

from app.database import IS_POSTGRES
from app.models.listing import FoodListing, ListingStatus


def haversine_km(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlambda / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def nearby_listings(db: Session, lat: float, lng: float, radius_km: float = 5.0) -> list[tuple[FoodListing, float]]:
    """Returns (listing, distance_km) tuples within radius_km, nearest first."""
    if IS_POSTGRES:
        point = ST_SetSRID(ST_MakePoint(lng, lat), 4326)
        radius_m = radius_km * 1000
        distance_expr = ST_Distance(FoodListing.location, point)
        rows = (
            db.query(FoodListing, distance_expr.label("dist_m"))
            .filter(FoodListing.status == ListingStatus.available)
            .filter(ST_DWithin(FoodListing.location, point, radius_m))
            .order_by(distance_expr)
            .all()
        )
        return [(listing, dist_m / 1000) for listing, dist_m in rows]

    candidates = db.query(FoodListing).filter(FoodListing.status == ListingStatus.available).all()
    scored = [(l, haversine_km(lat, lng, l.lat, l.lng)) for l in candidates]
    scored = [pair for pair in scored if pair[1] <= radius_km]
    scored.sort(key=lambda pair: pair[1])
    return scored
