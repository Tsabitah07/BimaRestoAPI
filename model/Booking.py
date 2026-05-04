from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum as SQLEnum
from database import Base

class BookingStatusEnum(str, PyEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NOT_PAID = "not_paid"

class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    booking_status = Column(SQLEnum(BookingStatusEnum), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    booking_session_id = Column(Integer, ForeignKey("booking_sessions.id"), nullable=False)
    number_of_people = Column(Integer, nullable=False)
    notes = Column(String(500), nullable=True)