from sqlalchemy import Column, Integer, String
from database import Base

class BookingSession(Base):
    __tablename__ = "booking_sessions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    time = Column(String(255), nullable=False)