from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class FoodPackage(Base):
    __tablename__ = 'food_packages'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    menu_id = Column(Integer, ForeignKey('menu.id'), nullable=False)
    session_id = Column(Integer, ForeignKey('booking_sessions.id'), nullable=False)
    available_quantity = Column(Integer, nullable=False)

    # Relationships
    menu = relationship("Menu", back_populates="food_packages")
    booked_foods = relationship("BookedFood", back_populates="food_package")
