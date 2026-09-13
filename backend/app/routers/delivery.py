from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.deps import get_db
from app.models.delivery import Delivery, DeliveryStatus
from app.models.match import Match
from app.models.listing import FoodListing, ListingStatus
from app.schemas.match import DeliveryOut
from app.services.router_opt import optimize_route
from app.services.notify import send_notification

router = APIRouter(prefix="/deliveries", tags=["delivery"])


@router.post("/{match_id}/start", response_model=DeliveryOut)
def start_delivery(match_id: int, db: Session = Depends(get_db)):
    match = db.get(Match, match_id)
    if not match:
        raise HTTPException(status_code=404, detail="Match not found")
    delivery = Delivery(match_id=match_id, pickup_time=datetime.utcnow(), tracking_status=DeliveryStatus.picked_up)
    listing = db.get(FoodListing, match.listing_id)
    listing.status = ListingStatus.picked_up
    db.add(delivery)
    db.commit()
    db.refresh(delivery)
    send_notification("delivery-update", f"Pickup started for match {match_id}")
    return delivery


@router.post("/{delivery_id}/complete", response_model=DeliveryOut)
def complete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    delivery = db.get(Delivery, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Delivery not found")
    delivery.delivery_time = datetime.utcnow()
    delivery.tracking_status = DeliveryStatus.delivered
    listing = db.get(FoodListing, db.get(Match, delivery.match_id).listing_id)
    listing.status = ListingStatus.delivered
    db.commit()
    db.refresh(delivery)
    send_notification("delivery-update", f"Delivery {delivery_id} completed")
    return delivery


class RouteRequest(BaseModel):
    start_lat: float
    start_lng: float
    stop_lats: list[float]
    stop_lngs: list[float]


@router.post("/route")
def get_optimized_route(payload: RouteRequest):
    stops = list(zip(payload.stop_lats, payload.stop_lngs))
    order = optimize_route((payload.start_lat, payload.start_lng), stops)
    return {"visit_order": order, "stops_in_order": [stops[i] for i in order]}
