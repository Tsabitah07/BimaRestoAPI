from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Menu schema for nested display
class MenuSchema(BaseModel):
    id: int
    name: str
    start_date: datetime
    end_date: datetime

    class Config:
        from_attributes = True

# FoodPackage schema for nested display
class FoodPackageSchema(BaseModel):
    id: int
    name: str
    description: str
    menu_id: int
    session_id: int
    available_quantity: int
    menu: Optional[MenuSchema] = None

    class Config:
        from_attributes = True

# Simplified BookedFood schema with only required fields
class BookedFoodDetailSchema(BaseModel):
    menu_name: str
    food_package_name: str
    quantity: int
    description: str

    class Config:
        from_attributes = True

# Original BookedFood schema (kept for backward compatibility)
class BookedFoodSchema(BaseModel):
    id: Optional[int] = None
    booking_id: Optional[int] = None
    food_id: int
    quantity: int

    class Config:
        from_attributes = True

# Enhanced Booking schema with simplified booked foods
class BookingDetailSchema(BaseModel):
    id: Optional[int] = None
    user_id: int
    booking_status: str
    booking_date: datetime
    booking_session_id: int
    number_of_people: int
    notes: Optional[str] = None
    booked_foods: List[BookedFoodDetailSchema] = []

    class Config:
        from_attributes = True

# Original Booking schema (kept for backward compatibility)
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

# Response schemas with enhanced data
class BookingDetailResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[BookingDetailSchema] = None

class BookingDetailListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[BookingDetailSchema]

# Original response schemas (kept for backward compatibility)
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
