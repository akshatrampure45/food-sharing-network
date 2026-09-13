from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.database import IS_POSTGRES
from app.models.listing import FoodListing
from app.models.user import User
from app.schemas.listing import ListingCreate, ListingOut
from app.services.freshness_ai import estimate_freshness
from app.services.matcher import nearby_listings

router = APIRouter(prefix="/listings", tags=["listings"])


@router.post("/", response_model=ListingOut)
def create_listing(payload: ListingCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    listing = FoodListing(
        donor_id=user.id,
        title=payload.title,
        quantity=payload.quantity,
        photo_url=payload.photo_url,
        expiry_time=payload.expiry_time,
        freshness_score=estimate_freshness(payload.photo_url),
        lat=payload.lat,
        lng=payload.lng,
    )
    if IS_POSTGRES:
        listing.location = f"POINT({payload.lng} {payload.lat})"
    db.add(listing)
    db.commit()
    db.refresh(listing)
    return listing


@router.get("/", response_model=list[ListingOut])
def list_all(db: Session = Depends(get_db)):
    return db.query(FoodListing).order_by(FoodListing.created_at.desc()).all()


@router.get("/nearby", response_model=list[ListingOut])
def list_nearby(lat: float, lng: float, radius_km: float = 5.0, db: Session = Depends(get_db)):
    results = nearby_listings(db, lat, lng, radius_km)
    out = []
    for listing, dist in results:
        item = ListingOut.model_validate(listing)
        item.distance_km = round(dist, 2)
        out.append(item)
    return out


@router.get("/{listing_id}", response_model=ListingOut)
def get_listing(listing_id: int, db: Session = Depends(get_db)):
    listing = db.get(FoodListing, listing_id)
    if not listing:
        raise HTTPException(status_code=404, detail="Listing not found")
    return listing
