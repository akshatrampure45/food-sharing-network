from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.deps import get_db, get_current_user
from app.models.match import Match, MatchStatus
from app.models.listing import FoodListing, ListingStatus
from app.models.user import User
from app.schemas.match import MatchCreate, MatchOut
from app.services.notify import send_notification

router = APIRouter(prefix="/matches", tags=["matching"])


@router.post("/", response_model=MatchOut)
def create_match(payload: MatchCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    listing = db.get(FoodListing, payload.listing_id)
    if not listing or listing.status != ListingStatus.available:
        raise HTTPException(status_code=400, detail="Listing not available")

    match = Match(
        listing_id=listing.id,
        recipient_id=payload.recipient_id or user.id,
        volunteer_id=payload.volunteer_id,
        status=MatchStatus.proposed,
    )
    listing.status = ListingStatus.matched
    db.add(match)
    db.commit()
    db.refresh(match)

    send_notification("new-match", f"Listing '{listing.title}' matched (match_id={match.id})")
    return match


@router.post("/{match_id}/accept", response_model=MatchOut)
def accept_match(match_id: int, db: Session = Depends(get_db)):
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    match.status = MatchStatus.accepted
    db.commit()
    db.refresh(match)
    send_notification("pickup-reminder", f"Match {match_id} accepted — pickup pending")
    return match
