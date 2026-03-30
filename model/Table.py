from sqlalchemy import Column, Integer, String
from database import Base

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)