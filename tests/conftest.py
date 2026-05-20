import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

from main import app
from database import Base, get_db
from model.Role import Role
from model.User import User
from model.BookingSession import BookingSession
from model.Menu import Menu
from model.FoodPackage import FoodPackage
from model.Booking import Booking
from model.BookedFood import BookedFood
from model.MenuPoster import MenuPoster
from controller.AuthController import _hash_password
from datetime import datetime, timedelta

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """Setup database with seed data before each test"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Create roles
    admin_role = Role(id=1, name="Admin")
    employee_role = Role(id=2, name="Employee")
    user_role = Role(id=3, name="User")
    db.add_all([admin_role, employee_role, user_role])
    db.commit()

    # Create users
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

    # Create booking sessions
    session1 = BookingSession(id=1, name="Lunch Session", time="11:00 - 13:00")
    session2 = BookingSession(id=2, name="Dinner Session", time="17:00 - 21:00")
    db.add_all([session1, session2])
    db.commit()

    # Create menus
    today = datetime.now()
    menu1 = Menu(
        id=1,
        name="Menu Mei",
        start_date=today,
        end_date=today + timedelta(days=30)
    )
    db.add(menu1)
    db.commit()

    # Create food packages
    food1 = FoodPackage(
        id=1,
        name="Paket Lunch Premium",
        description="Nasi, Ayam Goreng, Sayur, Dessert",
        menu_id=1,
        session_id=1,
        available_quantity=50
    )
    food2 = FoodPackage(
        id=2,
        name="Paket Lunch Ekonomi",
        description="Nasi, Telur, Sayur",
        menu_id=1,
        session_id=1,
        available_quantity=100
    )
    db.add_all([food1, food2])
    db.commit()

    # Create menu posters
    poster1 = MenuPoster(id=1, menu_id=1, poster_path="https://example.com/poster1.jpg")
    db.add(poster1)
    db.commit()

    # Create bookings
    booking1 = Booking(
        id=1,
        user_id=1,
        booking_status="pending",
        booking_date=today,
        booking_session_id=1,
        number_of_people=4,
        notes="Special request: vegetarian"
    )
    db.add(booking1)
    db.commit()

    # Create booked foods
    booked_food1 = BookedFood(id=1, booking_id=1, food_id=1, quantity=2)
    booked_food2 = BookedFood(id=2, booking_id=1, food_id=2, quantity=2)
    db.add_all([booked_food1, booked_food2])
    db.commit()

    yield db

    db.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def admin_token(setup_database):
    """Get admin token"""
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]


@pytest.fixture
def user_token(setup_database):
    """Get user token"""
    response = client.post(
        "/auth/login",
        json={"username": "user1", "password": "user123"}
    )
    return response.json()["access_token"]

