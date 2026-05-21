from sqlalchemy.orm import Session
from model.Booking import Booking as BookingModel
from model.BookedFood import BookedFood as BookedFoodModel
from model.FoodPackage import FoodPackage as FoodPackageModel
from model.Menu import Menu as MenuModel
from model.User import User as UserModel
from model.BookingSession import BookingSession as BookingSessionModel
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy.orm import joinedload

# Helper function to transform booking data with simplified booked_foods
def transform_booking_to_detail(booking):
    """Transform booking object to include simplified booked_foods data"""
    booked_foods_data = []
    for booked_food in booking.booked_foods:
        booked_foods_data.append({
            "menu_name": booked_food.food_package.menu.name,
            "food_package_name": booked_food.food_package.name,
            "quantity": booked_food.quantity,
            "description": booked_food.food_package.description
        })

    return {
        "id": booking.id,
        "user_id": booking.user_id,
        "booking_status": booking.booking_status,
        "booking_date": booking.booking_date,
        "booking_session_id": booking.booking_session_id,
        "number_of_people": booking.number_of_people,
        "notes": booking.notes,
        "booked_foods": booked_foods_data
    }

# Enhanced functions that include related data
def get_all_bookings_with_details(db: Session):
    """Get all bookings with booked foods and their details"""
    bookings = db.query(BookingModel).options(
        joinedload(BookingModel.booked_foods).joinedload(BookedFoodModel.food_package).joinedload(FoodPackageModel.menu)
    ).all()
    return [transform_booking_to_detail(booking) for booking in bookings]

def get_booking_by_id_with_details(db: Session, booking_id: int):
    """Get a specific booking by ID with booked foods and their details"""
    booking = db.query(BookingModel).options(
        joinedload(BookingModel.booked_foods).joinedload(BookedFoodModel.food_package).joinedload(FoodPackageModel.menu)
    ).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking tidak ditemukan")
    return transform_booking_to_detail(booking)

def get_bookings_by_user_with_details(db: Session, user_id: int):
    """Get all bookings for a specific user with booked foods and their details"""
    bookings = db.query(BookingModel).options(
        joinedload(BookingModel.booked_foods).joinedload(BookedFoodModel.food_package).joinedload(FoodPackageModel.menu)
    ).filter(BookingModel.user_id == user_id).all()
    return [transform_booking_to_detail(booking) for booking in bookings]

def get_bookings_by_status_with_details(db: Session, status: str):
    """Get all bookings with a specific status with booked foods and their details"""
    bookings = db.query(BookingModel).options(
        joinedload(BookingModel.booked_foods).joinedload(BookedFoodModel.food_package).joinedload(FoodPackageModel.menu)
    ).filter(BookingModel.booking_status == status).all()
    return [transform_booking_to_detail(booking) for booking in bookings]

# Original functions
def get_all_bookings(db: Session):
    return db.query(BookingModel).all()

def get_booking_by_id(db: Session, booking_id: int):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking tidak ditemukan")
    return booking

def create_booking(db: Session, user_id: int, booking_status: str, booking_date: datetime,
                  booking_session_id: int, number_of_people: int, notes: str = None, booked_foods: list = None):
    # Verify user exists
    print(f"DEBUG create_booking: user_id={user_id}, session_id={booking_session_id}, booked_foods={booked_foods}")
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        print("DEBUG create_booking: user not found")
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Verify booking session exists
    session = db.query(BookingSessionModel).filter(BookingSessionModel.id == booking_session_id).first()
    if not session:
        print("DEBUG create_booking: session not found")
        raise HTTPException(status_code=404, detail="Booking session tidak ditemukan")

    booking = BookingModel(
        user_id=user_id,
        booking_status=booking_status,
        booking_date=booking_date,
        booking_session_id=booking_session_id,
        number_of_people=number_of_people,
        notes=notes
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    print(f"DEBUG create_booking: booking created id={booking.id}")

    if booked_foods:
        for food_item in booked_foods:
            try:
                # Support both dicts and Pydantic model instances
                if isinstance(food_item, dict):
                    food_id = food_item.get("food_id")
                    quantity = food_item.get("quantity", 1)
                else:
                    # Pydantic models: access attributes
                    food_id = getattr(food_item, "food_id", None)
                    quantity = getattr(food_item, "quantity", 1)

                # Verify food package exists
                print(f"DEBUG create_booking: verifying food_id={food_id}")
                food = db.query(FoodPackageModel).filter(FoodPackageModel.id == food_id).first()
                if not food:
                    print(f"DEBUG create_booking: food {food_id} not found")
                    raise HTTPException(status_code=404, detail="Food package tidak ditemukan")

                booked_food = BookedFoodModel(
                    booking_id=booking.id,
                    food_id=food_id,
                    quantity=quantity
                )
                db.add(booked_food)
            except HTTPException:
                # Re-raise HTTP exceptions directly
                raise
            except Exception as exc:
                print(f"DEBUG create_booking: unexpected error while creating booked_food: {exc}")
                raise
        db.commit()

    return booking

def update_booking(db: Session, booking_id: int, booking_status: str = None,
                  number_of_people: int = None, notes: str = None):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking tidak ditemukan")

    if booking_status:
        booking.booking_status = booking_status
    if number_of_people:
        booking.number_of_people = number_of_people
    if notes is not None:
        booking.notes = notes

    db.commit()
    db.refresh(booking)
    return booking

def delete_booking(db: Session, booking_id: int):
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking tidak ditemukan")

    # Delete associated booked foods
    db.query(BookedFoodModel).filter(BookedFoodModel.booking_id == booking_id).delete()
    db.delete(booking)
    db.commit()
    return booking

def get_bookings_by_user(db: Session, user_id: int):
    return db.query(BookingModel).filter(BookingModel.user_id == user_id).all()

def get_bookings_by_status(db: Session, status: str):
    return db.query(BookingModel).filter(BookingModel.booking_status == status).all()

def get_all_booked_foods(db: Session):
    return db.query(BookedFoodModel).all()

def get_booked_food_by_id(db: Session, booked_food_id: int):
    booked_food = db.query(BookedFoodModel).filter(BookedFoodModel.id == booked_food_id).first()
    if not booked_food:
        raise HTTPException(status_code=404, detail="Booked food tidak ditemukan")
    return booked_food

def create_booked_food(db: Session, booking_id: int, food_id: int, quantity: int):
    # Verify booking exists
    booking = db.query(BookingModel).filter(BookingModel.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking tidak ditemukan")

    # Verify food package exists
    food = db.query(FoodPackageModel).filter(FoodPackageModel.id == food_id).first()
    if not food:
        raise HTTPException(status_code=404, detail="Food package tidak ditemukan")

    booked_food = BookedFoodModel(booking_id=booking_id, food_id=food_id, quantity=quantity)
    db.add(booked_food)
    db.commit()
    db.refresh(booked_food)
    return booked_food

def update_booked_food(db: Session, booked_food_id: int, quantity: int = None):
    booked_food = db.query(BookedFoodModel).filter(BookedFoodModel.id == booked_food_id).first()
    if not booked_food:
        raise HTTPException(status_code=404, detail="Booked food tidak ditemukan")

    if quantity is not None:
        booked_food.quantity = quantity

    db.commit()
    db.refresh(booked_food)
    return booked_food

def delete_booked_food(db: Session, booked_food_id: int):
    booked_food = db.query(BookedFoodModel).filter(BookedFoodModel.id == booked_food_id).first()
    if not booked_food:
        raise HTTPException(status_code=404, detail="Booked food tidak ditemukan")

    db.delete(booked_food)
    db.commit()
    return booked_food

def get_booked_foods_by_booking(db: Session, booking_id: int):
    return db.query(BookedFoodModel).filter(BookedFoodModel.booking_id == booking_id).all()
from sqlalchemy.orm import Session
from model.Role import Role as RoleModel
from fastapi import HTTPException

def get_all_roles(db: Session):
    return db.query(RoleModel).all()

def get_role_by_id(db: Session, role_id: int):
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role tidak ditemukan")
    return role

def create_role(db: Session, name: str):
    role = RoleModel(name=name)
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def update_role(db: Session, role_id: int, name: str = None):
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role tidak ditemukan")

    if name:
        role.name = name

    db.commit()
    db.refresh(role)
    return role

def delete_role(db: Session, role_id: int):
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role tidak ditemukan")

    db.delete(role)
    db.commit()
    return role
