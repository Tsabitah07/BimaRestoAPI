from pydantic import BaseModel
from typing import Optional, List

class BookingSessionSchema(BaseModel):
    id: Optional[int] = None
    name: str
    time: str

    class Config:
        from_attributes = True

class BookingSessionCreateSchema(BaseModel):
    name: str
    time: str

class BookingSessionUpdateSchema(BaseModel):
    name: Optional[str] = None
    time: Optional[str] = None

class BookingSessionResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[BookingSessionSchema] = None

class BookingSessionListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[BookingSessionSchema]

