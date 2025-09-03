from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship

from app.core.db import Base


class Contractor(Base):
    __tablename__ = "contractors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    created_at = Column(TIMESTAMP)

    parking_lots = relationship("ParkingLot", back_populates="contractor", cascade="all, delete-orphan")
