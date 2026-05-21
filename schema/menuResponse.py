from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from schema.foodPackageResponse import FoodPackageSchema

class MenuPosterSchema(BaseModel):
    id: Optional[int] = None
    menu_id: Optional[int] = None
    poster_path: str

    class Config:
        from_attributes = True

class MenuSchema(BaseModel):
    id: Optional[int] = None
    name: str
    start_date: datetime
    end_date: datetime
    posters: List[str] = []
    food_packages: List[FoodPackageSchema] = []

    class Config:
        from_attributes = True

    @staticmethod
    def from_orm_with_posters(menu):
        """Convert Menu ORM object to schema with poster paths and food packages"""
        # Map posters to simple paths
        posters = [poster.poster_path for poster in menu.posters] if getattr(menu, 'posters', None) else []

        # Map food packages to FoodPackageSchema instances (or dicts)
        food_packages = []
        if getattr(menu, 'food_packages', None):
            for fp in menu.food_packages:
                # Create FoodPackageSchema from ORM attributes
                food_packages.append(FoodPackageSchema(
                    id=getattr(fp, 'id', None),
                    name=getattr(fp, 'name', ''),
                    description=getattr(fp, 'description', ''),
                    menu_id=getattr(fp, 'menu_id', None),
                    session_id=getattr(fp, 'session_id', None),
                    available_quantity=getattr(fp, 'available_quantity', 0)
                ))

        return MenuSchema(
            id=menu.id,
            name=menu.name,
            start_date=menu.start_date,
            end_date=menu.end_date,
            posters=posters,
            food_packages=food_packages
        )

class MenuCreateSchema(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    poster_paths: List[str] = []

class MenuUpdateSchema(BaseModel):
    name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class MenuPosterCreateSchema(BaseModel):
    menu_id: int
    poster_path: str

class MenuResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[MenuSchema] = None

class MenuListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[MenuSchema]

class MenuPosterResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[MenuPosterSchema] = None

class MenuPosterListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[MenuPosterSchema]
