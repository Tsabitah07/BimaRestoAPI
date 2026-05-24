from model.Booking import Booking as booking_model
from model.BookedFood import BookedFood as booked_food_model
from model.FoodPackage import FoodPackage as food_package_model
from sqlalchemy.orm import Session
from datetime import datetime

data = [
  {
    "user_id": 5,
    "booking_status": "completed",
    "booking_date": "2026-03-05",
    "booking_session_id": 1,
    "number_of_people": 4,
    "notes": "Family Dinner",
    "booked_foods": [
      { "food_id": 1, "quantity": 2 },
      { "food_id": 2, "quantity": 2 }
    ]
  },
  {
    "user_id": 6,
    "booking_status": "completed",
    "booking_date": "2026-03-12",
    "booking_session_id": 2,
    "number_of_people": 2,
    "notes": "No spicy for one",
    "booked_foods": [
      { "food_id": 3, "quantity": 1 },
      { "food_id": 4, "quantity": 1 }
    ]
  },
  {
    "user_id": 6,
    "booking_status": "completed",
    "booking_date": "2026-03-25",
    "booking_session_id": 1,
    "number_of_people": 3,
    "notes": "Window seat please",
    "booked_foods": [
      { "food_id": 1, "quantity": 3 }
    ]
  },
  {
    "user_id": 5,
    "booking_status": "completed",
    "booking_date": "2026-04-05",
    "booking_session_id": 1,
    "number_of_people": 5,
    "notes": "Anniversary",
    "booked_foods": [
      { "food_id": 5, "quantity": 3 },
      { "food_id": 6, "quantity": 2 }
    ]
  },
  {
    "user_id": 5,
    "booking_status": "completed",
    "booking_date": "2026-04-18",
    "booking_session_id": 2,
    "number_of_people": 2,
    "notes": "",
    "booked_foods": [
      { "food_id": 7, "quantity": 1 },
      { "food_id": 8, "quantity": 1 }
    ]
  },
  {
    "user_id": 6,
    "booking_status": "completed",
    "booking_date": "2026-04-28",
    "booking_session_id": 1,
    "number_of_people": 4,
    "notes": "Company lunch",
    "booked_foods": [
      { "food_id": 5, "quantity": 4 }
    ]
  },
  {
    "user_id": 7,
    "booking_status": "completed",
    "booking_date": "2026-05-02",
    "booking_session_id": 1,
    "number_of_people": 6,
    "notes": "Large table",
    "booked_foods": [
      { "food_id": 9, "quantity": 3 },
      { "food_id": 10, "quantity": 3 }
    ]
  },
  {
    "user_id": 7,
    "booking_status": "completed",
    "booking_date": "2026-05-15",
    "booking_session_id": 2,
    "number_of_people": 2,
    "notes": "Birthday surprise",
    "booked_foods": [
      { "food_id": 11, "quantity": 2 }
    ]
  },
  {
    "user_id": 7,
    "booking_status": "completed",
    "booking_date": "2026-05-22",
    "booking_session_id": 2,
    "number_of_people": 3,
    "notes": "",
    "booked_foods": [
      { "food_id": 12, "quantity": 3 }
    ]
  },
  {
    "user_id": 7,
    "booking_status": "completed",
    "booking_date": "2026-05-29",
    "booking_session_id": 1,
    "number_of_people": 4,
    "notes": "Reunion",
    "booked_foods": [
      { "food_id": 9, "quantity": 2 },
      { "food_id": 10, "quantity": 2 }
    ]
  },
  {
    "user_id": 6,
    "booking_status": "completed",
    "booking_date": "2026-06-05",
    "booking_session_id": 1,
    "number_of_people": 2,
    "notes": "Date night",
    "booked_foods": [
      { "food_id": 13, "quantity": 1 },
      { "food_id": 14, "quantity": 1 }
    ]
  },
  {
    "user_id": 5,
    "booking_status": "completed",
    "booking_date": "2026-06-12",
    "booking_session_id": 2,
    "number_of_people": 5,
    "notes": "Extra crackers please",
    "booked_foods": [
      { "food_id": 15, "quantity": 3 },
      { "food_id": 16, "quantity": 2 }
    ]
  },
  {
    "user_id": 6,
    "booking_status": "completed",
    "booking_date": "2026-06-18",
    "booking_session_id": 1,
    "number_of_people": 4,
    "notes": "",
    "booked_foods": [
      { "food_id": 13, "quantity": 4 }
    ]
  },
  {
    "user_id": 7,
    "booking_status": "completed",
    "booking_date": "2026-06-25",
    "booking_session_id": 2,
    "number_of_people": 3,
    "notes": "Farewell dinner",
    "booked_foods": [
      { "food_id": 16, "quantity": 3 }
    ]
  },
  {
    "user_id": 6,
    "booking_status": "completed",
    "booking_date": "2026-06-29",
    "booking_session_id": 1,
    "number_of_people": 2,
    "notes": "Last minute booking",
    "booked_foods": [
      { "food_id": 14, "quantity": 2 }
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

