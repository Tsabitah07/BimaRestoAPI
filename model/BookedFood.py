from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class BookedFood(Base):
    __tablename__ = "booked_food"

    id = Column(Integer, primary_key=True, index=True)
    booking_id = Column(Integer, ForeignKey('bookings.id'), nullable=False)
    food_id = Column(Integer, ForeignKey('food_packages.id'), nullable=False)
    quantity = Column(Integer, nullable=False)

    # Relationships
    booking = relationship("Booking", back_populates="booked_foods")
    food_package = relationship("FoodPackage", back_populates="booked_foods")
