from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Menu(Base):
    __tablename__ = 'menu'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(250), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
