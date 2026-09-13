import enum
from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from app.database import Base


class UserRole(str, enum.Enum):
    donor = "donor"
    recipient = "recipient"
    volunteer = "volunteer"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.donor)
    lat = Column(Float, nullable=True)
    lng = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
