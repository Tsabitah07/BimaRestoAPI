from model.Booking import Booking as booking_model
from model.BookedFood import BookedFood as booked_food_model
from model.FoodPackage import FoodPackage as food_package_model
from sqlalchemy.orm import Session
from datetime import datetime

data = [
    {
        "user_id": 5,
        "booking_status": "completed",
        "booking_date": "2024-02-10",
        "booking_session_id": 1,
        "number_of_people": 4,
        "notes": "Birthday celebration",
        "booked_foods": [
            {
                "food_id": 1,
                "quantity": 3
            },
            {
                "food_id": 2,
                "quantity": 1
            }
        ]
    },
    {
        "user_id": 6,
        "booking_status": "pending",
        "booking_date": "2024-03-02",
        "booking_session_id": 1,
        "number_of_people": 2,
        "notes": "Anniversary dinner",
        "booked_foods": [
            {
                "food_id": 3,
                "quantity": 2
            }
        ]
    },
    {
        "user_id": 6,
        "booking_status": "confirmed",
        "booking_date": "2024-03-03",
        "booking_session_id": 2,
        "number_of_people": 11,
        "notes": "Family gathering",
        "booked_foods": [
            {
                "food_id": 9,
                "quantity": 4
            },
            {
                "food_id": 10,
                "quantity": 7
            }
        ]
    }
]

def seed_data(db: Session):
    # Seed bookings if none exist
    if not db.query(booking_model).first():
        for item in data:
            booking_entry = booking_model(
                user_id=item["user_id"],
                booking_status=item["booking_status"],
                booking_date=datetime.fromisoformat(item["booking_date"]),
                booking_session_id=item["booking_session_id"],
                number_of_people=item["number_of_people"],
                notes=item["notes"]
            )
            db.add(booking_entry)
        db.commit()
        print("Database seeded with initial bookings.")
    else:
        print("Bookings already exist, skipping seeding.")

    # Seed booked_foods: ensure referenced food packages exist and bookings are present
    if not db.query(booked_food_model).first():
        for item in data:
            # Try to find an existing booking that matches the seed item
            booking = db.query(booking_model).filter_by(
                user_id=item["user_id"],
                booking_status=item["booking_status"],
                booking_date=datetime.fromisoformat(item["booking_date"]),
                booking_session_id=item["booking_session_id"],
                number_of_people=item["number_of_people"],
                notes=item["notes"]
            ).first()

            # If booking wasn't found (because bookings existed but not these particular rows), create it now
            if booking is None:
                booking = booking_model(
                    user_id=item["user_id"],
                    booking_status=item["booking_status"],
                    booking_date=datetime.fromisoformat(item["booking_date"]),
                    booking_session_id=item["booking_session_id"],
                    number_of_people=item["number_of_people"],
                    notes=item["notes"]
                )
                db.add(booking)
                db.commit()  # commit so booking.id is available

            for booked_food in item.get("booked_foods", []):
                food_id = booked_food.get("food_id")
                quantity = booked_food.get("quantity", 0)

                # Check referenced food package exists to avoid FK errors
                food = db.query(food_package_model).filter_by(id=food_id).first()
                if not food:
                    print(f"Skipping booked_food insertion: food package id={food_id} does not exist.")
                    continue

                # Avoid duplicating the same booked_food entry
                exists = db.query(booked_food_model).filter_by(
                    booking_id=booking.id,
                    food_id=food_id
                ).first()
                if exists:
                    print(f"Booked food already exists for booking_id={booking.id}, food_id={food_id}; skipping.")
                    continue

                booked_food_entry = booked_food_model(
                    booking_id=booking.id,
                    food_id=food_id,
                    quantity=quantity
                )
                db.add(booked_food_entry)
        db.commit()
        print("Database seeded with initial booked foods.")
    else:
        print("Booked foods already exist, skipping seeding.")

