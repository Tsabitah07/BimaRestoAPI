from sqlalchemy.orm import Session
from model.FoodPackage import FoodPackage as FoodPackageModel
from model.Menu import Menu as MenuModel
from model.BookingSession import BookingSession as BookingSessionModel
from fastapi import HTTPException

def get_all_food_packages(db: Session):
    return db.query(FoodPackageModel).all()

def get_food_package_by_id(db: Session, food_id: int):
    food = db.query(FoodPackageModel).filter(FoodPackageModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food package not found")
    return food

def create_food_package(db: Session, name: str, description: str, menu_id: int, session_id: int, available_quantity: int):
    # Verify menu exists
    menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
    if not menu:
        raise HTTPException(status_code=404, detail="Menu not found")

    # Verify booking session exists
    session = db.query(BookingSessionModel).filter(BookingSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Booking session not found")

    food = FoodPackageModel(
        name=name,
        description=description,
        menu_id=menu_id,
        session_id=session_id,
        available_quantity=available_quantity
    )
    db.add(food)
    db.commit()
    db.refresh(food)
    return food

def update_food_package(db: Session, food_id: int, name: str = None, description: str = None,
                       menu_id: int = None, session_id: int = None, available_quantity: int = None):
    food = db.query(FoodPackageModel).filter(FoodPackageModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food package not found")

    if menu_id:
        menu = db.query(MenuModel).filter(MenuModel.id == menu_id).first()
        if not menu:
            raise HTTPException(status_code=404, detail="Menu not found")
        food.menu_id = menu_id

    if session_id:
        session = db.query(BookingSessionModel).filter(BookingSessionModel.id == session_id).first()
        if not session:
            raise HTTPException(status_code=404, detail="Booking session not found")
        food.session_id = session_id

    if name:
        food.name = name
    if description:
        food.description = description
    if available_quantity is not None:
        food.available_quantity = available_quantity

    db.commit()
    db.refresh(food)
    return food

def delete_food_package(db: Session, food_id: int):
    food = db.query(FoodPackageModel).filter(FoodPackageModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food package not found")

    db.delete(food)
    db.commit()
    return food

def get_food_packages_by_menu(db: Session, menu_id: int):
    return db.query(FoodPackageModel).filter(FoodPackageModel.menu_id == menu_id).all()

def get_food_packages_by_session(db: Session, session_id: int):
    return db.query(FoodPackageModel).filter(FoodPackageModel.session_id == session_id).all()

