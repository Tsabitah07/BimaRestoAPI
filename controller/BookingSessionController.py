from sqlalchemy.orm import Session
from model.BookingSession import BookingSession as BookingSessionModel
from fastapi import HTTPException

def get_all_booking_sessions(db: Session):
    return db.query(BookingSessionModel).all()

def get_booking_session_by_id(db: Session, session_id: int):
    session = db.query(BookingSessionModel).filter(BookingSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Booking session not found")
    return session

def create_booking_session(db: Session, name: str, time: str):
    session = BookingSessionModel(name=name, time=time)
    db.add(session)
    db.commit()
    db.refresh(session)
    return session

def update_booking_session(db: Session, session_id: int, name: str = None, time: str = None):
    session = db.query(BookingSessionModel).filter(BookingSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Booking session not found")

    if name:
        session.name = name
    if time:
        session.time = time

    db.commit()
    db.refresh(session)
    return session

def delete_booking_session(db: Session, session_id: int):
    session = db.query(BookingSessionModel).filter(BookingSessionModel.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Booking session not found")

    db.delete(session)
    db.commit()
    return session

