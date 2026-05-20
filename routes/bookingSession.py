from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controller import BookingSessionController
from schema.bookingSessionResponse import (
    BookingSessionSchema, BookingSessionCreateSchema, BookingSessionUpdateSchema,
    BookingSessionResponseSchema, BookingSessionListResponseSchema
)

router = APIRouter()

@router.get("/", tags=["Booking Session"], response_model=BookingSessionListResponseSchema)
def get_all_booking_sessions(db: Session = Depends(get_db)):
    """Get all booking sessions"""
    try:
        sessions = BookingSessionController.get_all_booking_sessions(db)
        return {
            "message": "Booking sessions retrieved successfully",
            "status": 200,
            "data": sessions
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{session_id}", tags=["Booking Session"], response_model=BookingSessionResponseSchema)
def get_booking_session(session_id: int, db: Session = Depends(get_db)):
    """Get a specific booking session by ID"""
    try:
        session = BookingSessionController.get_booking_session_by_id(db, session_id)
        return {
            "message": "Booking session retrieved successfully",
            "status": 200,
            "data": session
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/", tags=["Booking Session"], response_model=BookingSessionResponseSchema)
def create_booking_session(payload: BookingSessionCreateSchema, db: Session = Depends(get_db)):
    """Create a new booking session"""
    try:
        session = BookingSessionController.create_booking_session(db, payload.name, payload.time)
        return {
            "message": "Booking session created successfully",
            "status": 201,
            "data": session
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{session_id}", tags=["Booking Session"], response_model=BookingSessionResponseSchema)
def update_booking_session(session_id: int, payload: BookingSessionUpdateSchema, db: Session = Depends(get_db)):
    """Update a booking session"""
    try:
        session = BookingSessionController.update_booking_session(db, session_id, payload.name, payload.time)
        return {
            "message": "Booking session updated successfully",
            "status": 200,
            "data": session
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{session_id}", tags=["Booking Session"], response_model=BookingSessionResponseSchema)
def delete_booking_session(session_id: int, db: Session = Depends(get_db)):
    """Delete a booking session"""
    try:
        session = BookingSessionController.delete_booking_session(db, session_id)
        return {
            "message": "Booking session deleted successfully",
            "status": 200,
            "data": session
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

