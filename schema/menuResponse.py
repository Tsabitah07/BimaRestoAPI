from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

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

    class Config:
        from_attributes = True

    @staticmethod
    def from_orm_with_posters(menu):
        """Convert Menu ORM object to schema with poster paths as strings"""
        return MenuSchema(
            id=menu.id,
            name=menu.name,
            start_date=menu.start_date,
            end_date=menu.end_date,
            posters=[poster.poster_path for poster in menu.posters] if menu.posters else []
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
