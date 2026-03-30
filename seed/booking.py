from model.Booking import Booking as booking_model
from model.BookedTable import BookedTable as booked_table_model
from sqlalchemy.orm import Session
from datetime import datetime

data = [
    {
        "user_id": 5,
        "worker_id": 3,
        "booking_status_id": 4,
        "booking_date": "2024-07-01",
        "booking_session_id": 1,
        "number_of_people": 4,
        "extra_chair": 0,
        "notes": "Birthday celebration",
        "booked_tables": [
            1
        ]
    },
    {
        "user_id": 6,
        "worker_id": 4,
        "booking_status_id": 4,
        "booking_date": "2024-07-02",
        "booking_session_id": 1,
        "number_of_people": 2,
        "extra_chair": 0,
        "notes": "Anniversary dinner",
        "booked_tables": [
            2
        ]
    },
    {
        "user_id": 6,
        "worker_id": 3,
        "booking_status_id": 1,
        "booking_date": "2024-07-03",
        "booking_session_id": 2,
        "number_of_people": 11,
        "extra_chair": 1,
        "notes": "Family gathering",
        "booked_tables": [
            2,
            3
        ]
    }
]

def seed_data(db: Session):
    if not db.query(booking_model).first():
        for item in data:
            role = booking_model(
                user_id=item["user_id"],
                worker_id=item["worker_id"],
                booking_status_id=item["booking_status_id"],
                booking_date=datetime.fromisoformat(item["booking_date"]),
                booking_session_id=item["booking_session_id"],
                number_of_people=item["number_of_people"],
                extra_chair=item["extra_chair"],
                notes=item["notes"]
            )
            db.add(role)
        db.commit()
        print("Database seeded with initial roles.")
    else:
        print("Roles already exist, skipping seeding.")

    if not db.query(booked_table_model).first():
        for item in data:
            booking = db.query(booking_model).filter_by(
                user_id=item["user_id"],
                worker_id=item["worker_id"],
                booking_status_id=item["booking_status_id"],
                booking_date=datetime.fromisoformat(item["booking_date"]),
                booking_session_id=item["booking_session_id"],
                number_of_people=item["number_of_people"],
                extra_chair=item["extra_chair"],
                notes=item["notes"]
            ).first()
            for table_id in item["booked_tables"]:
                booked_table = booked_table_model(
                    booking_id=booking.id,
                    table_id=table_id
                )
                db.add(booked_table)
        db.commit()
        print("Database seeded with initial booked tables.")
    else:
        print("Booked tables already exist, skipping seeding.")