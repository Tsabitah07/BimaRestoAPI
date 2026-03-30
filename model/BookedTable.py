from sqlalchemy import Column, Integer, String
from database import Base

class BookedTable(Base):
    __tablename__ = "booked_tables"

    id = Column(Integer, primary_key=True, index=True)
    table_id = Column(Integer, nullable=False)
    booking_id = Column(Integer, nullable=False)