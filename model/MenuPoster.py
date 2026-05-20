from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class MenuPoster(Base):
    __tablename__ = 'menu_poster'

    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey('menu.id'), nullable=False)
    poster_path = Column(String(255), nullable=False)

    # Relationships
    menu = relationship("Menu", back_populates="posters")
