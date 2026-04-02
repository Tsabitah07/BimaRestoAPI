from model.BookingStatus import BookingStatus as booking_status_model
from sqlalchemy.orm import Session

data = [
    {
        "name": "Pending"
    },
    {
        "name": "Confirmed"
    },
    {
        "name": "Cancelled"
    },
    {
        "name": "Completed"
    },
    {
        "name": "No Show"
    }
]

def seed_data(db: Session):
    if not db.query(booking_status_model).first():
        for item in data:
            status = booking_status_model(
                name=item["name"]
            )
            db.add(status)
        db.commit()
        print("Database seeded with initial booking statuses.")
    else:
        print("Booking statuses already exist, skipping seeding.")
