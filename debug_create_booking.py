from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from datetime import datetime

from database import Base
from model.Role import Role
from model.User import User
from model.BookingSession import BookingSession
from model.Menu import Menu
from model.FoodPackage import FoodPackage
from model.Booking import Booking
from model.BookedFood import BookedFood
from model.MenuPoster import MenuPoster
from controller.AuthController import _hash_password
from controller import BookingController

# Setup in-memory SQLite engine like tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# create session
db = TestingSessionLocal()

# Seed data similar to tests
admin_role = Role(id=1, name="Admin")
employee_role = Role(id=2, name="Employee")
user_role = Role(id=3, name="User")
db.add_all([admin_role, employee_role, user_role])
db.commit()

admin_user = User(
    id=1,
    name="Administrator",
    username="admin",
    email="admin@example.com",
    phone_number="08123456789",
    password=_hash_password("admin123"),
    role_id=1
)
employee_user = User(
    id=2,
    name="Employee 1",
    username="employee1",
    email="employee1@example.com",
    phone_number="08222222222",
    password=_hash_password("employee123"),
    role_id=2
)
user_user = User(
    id=3,
    name="User 1",
    username="user1",
    email="user1@example.com",
    phone_number="08333333333",
    password=_hash_password("user123"),
    role_id=3
)
db.add_all([admin_user, employee_user, user_user])
db.commit()

session1 = BookingSession(id=1, name="Lunch Session", time="11:00 - 13:00")
session2 = BookingSession(id=2, name="Dinner Session", time="17:00 - 21:00")
db.add_all([session1, session2])
db.commit()

# Create menu and food packages
now = datetime.now()
menu1 = Menu(id=1, name="Menu Mei", start_date=now, end_date=now)
db.add(menu1)
db.commit()

food1 = FoodPackage(id=1, name="Paket Lunch Premium", description="Desc", menu_id=1, session_id=1, available_quantity=50)
food2 = FoodPackage(id=2, name="Paket Lunch Ekonomi", description="Desc2", menu_id=1, session_id=1, available_quantity=100)
db.add_all([food1, food2])
db.commit()

# existing booking
booking1 = Booking(id=1, user_id=1, booking_status="pending", booking_date=now, booking_session_id=1, number_of_people=4, notes="None")
db.add(booking1)
db.commit()

booked_food1 = BookedFood(id=1, booking_id=1, food_id=1, quantity=2)
booked_food2 = BookedFood(id=2, booking_id=1, food_id=2, quantity=2)
db.add_all([booked_food1, booked_food2])
db.commit()

print("Seed complete")

# Now call controller.create_booking directly
payload = {
    "user_id": 2,
    "booking_status": "confirmed",
    "booking_date": now,
    "booking_session_id": 2,
    "number_of_people": 6,
    "notes": "Near window seat",
    "booked_foods": [
        {"food_id": 1, "quantity": 3},
        {"food_id": 2, "quantity": 3}
    ]
}

try:
    result = BookingController.create_booking(
        db,
        payload["user_id"],
        payload["booking_status"],
        payload["booking_date"],
        payload["booking_session_id"],
        payload["number_of_people"],
        payload["notes"],
        payload["booked_foods"]
    )
    print("create_booking returned:", result)
    # fetch details
    details = BookingController.get_booking_by_id_with_details(db, result.id)
    print("details:", details)
except Exception as e:
    import traceback
    print("Exception during create_booking:")
    traceback.print_exc()

# close
db.close()
