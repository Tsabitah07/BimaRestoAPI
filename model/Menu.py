from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)

    # Relationships
    food_packages = relationship("FoodPackage", back_populates="menu")
    posters = relationship("MenuPoster", back_populates="menu", cascade="all, delete-orphan")
