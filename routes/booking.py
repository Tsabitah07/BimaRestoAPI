from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controller import BookingController
from schema.bookingResponse import (
    BookingSchema, BookingCreateSchema, BookingUpdateSchema,
    BookingResponseSchema, BookingListResponseSchema,
    BookedFoodSchema, BookedFoodResponseSchema, BookedFoodListResponseSchema,
    BookingDetailSchema, BookingDetailResponseSchema, BookingDetailListResponseSchema
)

router = APIRouter()

# Booking endpoints
@router.get("/", tags=["Booking"], response_model=BookingDetailListResponseSchema)
def get_all_bookings(db: Session = Depends(get_db)):
    """Get all bookings with menu and food details"""
    try:
        bookings = BookingController.get_all_bookings_with_details(db)
        return {
            "message": "Bookings retrieved successfully",
            "status": 200,
            "data": bookings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{booking_id}", tags=["Booking"], response_model=BookingDetailResponseSchema)
def get_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get a specific booking by ID with menu and food details"""
    try:
        booking = BookingController.get_booking_by_id_with_details(db, booking_id)
        return {
            "message": "Booking retrieved successfully",
            "status": 200,
            "data": booking
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", tags=["Booking"], response_model=BookingDetailResponseSchema)
def create_booking(payload: BookingCreateSchema, db: Session = Depends(get_db)):
    """Create a new booking"""
    try:
        booking = BookingController.create_booking(
            db,
            payload.user_id,
            payload.booking_status,
            payload.booking_date,
            payload.booking_session_id,
            payload.number_of_people,
            payload.notes,
            payload.booked_foods
        )
        # Return with details after creation
        booking = BookingController.get_booking_by_id_with_details(db, booking.id)
        return {
            "message": "Booking created successfully",
            "status": 201,
            "data": booking
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{booking_id}", tags=["Booking"], response_model=BookingDetailResponseSchema)
def update_booking(booking_id: int, payload: BookingUpdateSchema, db: Session = Depends(get_db)):
    """Update a booking"""
    try:
        booking = BookingController.update_booking(
            db,
            booking_id,
            payload.booking_status,
            payload.number_of_people,
            payload.notes
        )
        # Return with details after update
        booking = BookingController.get_booking_by_id_with_details(db, booking.id)
        return {
            "message": "Booking updated successfully",
            "status": 200,
            "data": booking
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{booking_id}", tags=["Booking"], response_model=BookingDetailResponseSchema)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """Delete a booking"""
    try:
        booking = BookingController.delete_booking(db, booking_id)
        return {
            "message": "Booking deleted successfully",
            "status": 200,
            "data": booking
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/user/{user_id}", tags=["Booking"], response_model=BookingDetailListResponseSchema)
def get_bookings_by_user(user_id: int, db: Session = Depends(get_db)):
    """Get all bookings for a specific user with menu and food details"""
    try:
        bookings = BookingController.get_bookings_by_user_with_details(db, user_id)
        return {
            "message": "Bookings retrieved successfully",
            "status": 200,
            "data": bookings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{status}", tags=["Booking Status"], response_model=BookingDetailListResponseSchema)
def get_bookings_by_status(status: str, db: Session = Depends(get_db)):
    """Get all bookings with a specific status with menu and food details"""
    try:
        bookings = BookingController.get_bookings_by_status_with_details(db, status)
        return {
            "message": "Bookings retrieved successfully",
            "status": 200,
            "data": bookings
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Booked Food endpoints
@router.get("/foods/all", tags=["Booking"], response_model=BookedFoodListResponseSchema)
def get_all_booked_foods(db: Session = Depends(get_db)):
    """Get all booked foods"""
    try:
        booked_foods = BookingController.get_all_booked_foods(db)
        return {
            "message": "Booked foods retrieved successfully",
            "status": 200,
            "data": booked_foods
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/foods/{booked_food_id}", tags=["Booking"], response_model=BookedFoodResponseSchema)
def get_booked_food(booked_food_id: int, db: Session = Depends(get_db)):
    """Get a specific booked food by ID"""
    try:
        booked_food = BookingController.get_booked_food_by_id(db, booked_food_id)
        return {
            "message": "Booked food retrieved successfully",
            "status": 200,
            "data": booked_food
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/foods", tags=["Booking"], response_model=BookedFoodResponseSchema)
def create_booked_food(payload: BookedFoodSchema, db: Session = Depends(get_db)):
    """Create a new booked food entry"""
    try:
        booked_food = BookingController.create_booked_food(
            db,
            payload.booking_id,
            payload.food_id,
            payload.quantity
        )
        return {
            "message": "Booked food created successfully",
            "status": 201,
            "data": booked_food
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/foods/{booked_food_id}", tags=["Booking"], response_model=BookedFoodResponseSchema)
def update_booked_food(booked_food_id: int, payload: dict, db: Session = Depends(get_db)):
    """Update a booked food entry"""
    try:
        booked_food = BookingController.update_booked_food(
            db,
            booked_food_id,
            payload.get("quantity")
        )
        return {
            "message": "Booked food updated successfully",
            "status": 200,
            "data": booked_food
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/foods/{booked_food_id}", tags=["Booking"], response_model=BookedFoodResponseSchema)
def delete_booked_food(booked_food_id: int, db: Session = Depends(get_db)):
    """Delete a booked food entry"""
    try:
        booked_food = BookingController.delete_booked_food(db, booked_food_id)
        return {
            "message": "Booked food deleted successfully",
            "status": 200,
            "data": booked_food
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{booking_id}/foods", tags=["Booking"], response_model=BookedFoodListResponseSchema)
def get_booked_foods_by_booking(booking_id: int, db: Session = Depends(get_db)):
    """Get all booked foods for a specific booking"""
    try:
        booked_foods = BookingController.get_booked_foods_by_booking(db, booking_id)
        return {
            "message": "Booked foods retrieved successfully",
            "status": 200,
            "data": booked_foods
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
