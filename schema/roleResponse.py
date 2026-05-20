from pydantic import BaseModel
from typing import Optional, List

class RoleSchema(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True

class RoleCreateSchema(BaseModel):
    name: str

class RoleUpdateSchema(BaseModel):
    name: Optional[str] = None

class RoleResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[RoleSchema] = None

class RoleListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[RoleSchema]
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class BookedFoodSchema(BaseModel):
    id: Optional[int] = None
    booking_id: Optional[int] = None
    food_id: int
    quantity: int

    class Config:
        from_attributes = True

class BookingSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    booking_status: str
    booking_date: datetime
    booking_session_id: int
    number_of_people: int
    notes: Optional[str] = None
    booked_foods: List[BookedFoodSchema] = []

    class Config:
        from_attributes = True

class BookingCreateSchema(BaseModel):
    user_id: int
    booking_status: str
    booking_date: datetime
    booking_session_id: int
    number_of_people: int
    notes: Optional[str] = None
    booked_foods: List[BookedFoodSchema] = []

class BookingUpdateSchema(BaseModel):
    booking_status: Optional[str] = None
    number_of_people: Optional[int] = None
    notes: Optional[str] = None

class BookingResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[BookingSchema] = None

class BookingListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[BookingSchema]

class BookedFoodResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[BookedFoodSchema] = None

class BookedFoodListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[BookedFoodSchema]

