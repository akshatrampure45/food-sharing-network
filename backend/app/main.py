from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, engine
from app import models  # noqa: F401  (ensures models are registered before create_all)
from app.routers import auth, listings, matching, delivery, feedback

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Food Sharing & Donation Network")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten to your frontend URL before production
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(listings.router)
app.include_router(matching.router)
app.include_router(delivery.router)
app.include_router(feedback.router)


@app.get("/")
def health_check():
    return {"status": "ok", "service": "food-sharing-network"}
