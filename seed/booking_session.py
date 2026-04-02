from model.BookingSession import BookingSession as booking_session_model
from sqlalchemy.orm import Session

data = [
    {
        "name": "Lunch Session",
        "time": "11:30 - 13:00"
    },
    {
        "name": "Early Dinner Session",
        "time": "16:30 - 18:00"
    }
]

def seed_data(db: Session):
    if not db.query(booking_session_model).first():
        for item in data:
            session = booking_session_model(
                name=item["name"],
                time=item["time"]
            )
            db.add(session)
        db.commit()
        print("Database seeded with initial booking sessions.")
    else:
        print("Booking sessions already exist, skipping seeding.")
