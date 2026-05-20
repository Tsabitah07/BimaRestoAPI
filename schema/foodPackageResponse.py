from pydantic import BaseModel
from typing import Optional, List

class FoodPackageSchema(BaseModel):
    id: Optional[int] = None
    name: str
    description: str
    menu_id: int
    session_id: int
    available_quantity: int

    class Config:
        from_attributes = True

class FoodPackageCreateSchema(BaseModel):
    name: str
    description: str
    menu_id: int
    session_id: int
    available_quantity: int

class FoodPackageUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    menu_id: Optional[int] = None
    session_id: Optional[int] = None
    available_quantity: Optional[int] = None

class FoodPackageResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[FoodPackageSchema] = None

class FoodPackageListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[FoodPackageSchema]

