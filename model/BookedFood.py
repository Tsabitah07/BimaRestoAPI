from sqlalchemy import Column, Integer, ForeignKey
from database import Base

class BookedFood(Base):
    __tablename__ = "booked_food"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    food_id = Column(Integer, ForeignKey('food_packages.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

