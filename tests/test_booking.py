import pytest
from datetime import datetime, timedelta
from tests.conftest import client, setup_database


class TestBookingEndpoints:
    """Test Booking CRUD Endpoints"""

    def test_get_all_bookings(self, setup_database):
        """Test get all bookings"""
        response = client.get("/bookings/")
        assert response.status_code == 200
        assert response.json()["message"] == "Bookings retrieved successfully"
        assert len(response.json()["data"]) >= 1

    def test_get_booking_by_id(self, setup_database):
        """Test get booking by ID"""
        response = client.get("/bookings/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1
        assert response.json()["data"]["user_id"] == 1

    def test_get_booking_by_id_not_found(self, setup_database):
        """Test get booking by ID when not found"""
        response = client.get("/bookings/999")
        assert response.status_code == 404
        assert "Booking tidak ditemukan" in response.json()["detail"]

    def test_create_booking(self, setup_database):
        """Test create new booking"""
        today = datetime.now()
        response = client.post(
            "/bookings/",
            json={
                "user_id": 2,
                "booking_status": "confirmed",
                "booking_date": today.isoformat(),
                "booking_session_id": 2,
                "number_of_people": 6,
                "notes": "Near window seat",
                "booked_foods": [
                    {"food_id": 1, "quantity": 3},
                    {"food_id": 2, "quantity": 3}
                ]
            }
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Booking created successfully"
        assert response.json()["data"]["user_id"] == 2
        assert response.json()["data"]["number_of_people"] == 6

    def test_create_booking_invalid_user(self, setup_database):
        """Test create booking with invalid user"""
        today = datetime.now()
        response = client.post(
            "/bookings/",
            json={
                "user_id": 999,
                "booking_status": "pending",
                "booking_date": today.isoformat(),
                "booking_session_id": 1,
                "number_of_people": 4,
                "booked_foods": []
            }
        )
        assert response.status_code == 404
        assert "User tidak ditemukan" in response.json()["detail"]

    def test_create_booking_invalid_session(self, setup_database):
        """Test create booking with invalid session"""
        today = datetime.now()
        response = client.post(
            "/bookings/",
            json={
                "user_id": 1,
                "booking_status": "pending",
                "booking_date": today.isoformat(),
                "booking_session_id": 999,
                "number_of_people": 4,
                "booked_foods": []
            }
        )
        assert response.status_code == 404
        assert "Booking session tidak ditemukan" in response.json()["detail"]

    def test_create_booking_invalid_food(self, setup_database):
        """Test create booking with invalid food package"""
        today = datetime.now()
        response = client.post(
            "/bookings/",
            json={
                "user_id": 1,
                "booking_status": "pending",
                "booking_date": today.isoformat(),
                "booking_session_id": 1,
                "number_of_people": 4,
                "booked_foods": [
                    {"food_id": 999, "quantity": 2}
                ]
            }
        )
        assert response.status_code == 404
        assert "Food package" in response.json()["detail"]

    def test_update_booking(self, setup_database):
        """Test update booking"""
        response = client.put(
            "/bookings/1",
            json={
                "booking_status": "confirmed",
                "number_of_people": 5,
                "notes": "Updated notes"
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Booking updated successfully"
        assert response.json()["data"]["booking_status"] == "confirmed"
        assert response.json()["data"]["number_of_people"] == 5

    def test_update_booking_not_found(self, setup_database):
        """Test update booking when not found"""
        response = client.put(
            "/bookings/999",
            json={"booking_status": "cancelled"}
        )
        assert response.status_code == 404
        assert "Booking tidak ditemukan" in response.json()["detail"]

    def test_delete_booking(self, setup_database):
        """Test delete booking"""
        # Create a new booking first
        today = datetime.now()
        create_response = client.post(
            "/bookings/",
            json={
                "user_id": 2,
                "booking_status": "pending",
                "booking_date": today.isoformat(),
                "booking_session_id": 1,
                "number_of_people": 2,
                "booked_foods": []
            }
        )
        booking_id = create_response.json()["data"]["id"]

        # Delete the booking
        response = client.delete(f"/bookings/{booking_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Booking deleted successfully"

        # Verify booking is deleted
        verify_response = client.get(f"/bookings/{booking_id}")
        assert verify_response.status_code == 404

    def test_delete_booking_not_found(self, setup_database):
        """Test delete booking when not found"""
        response = client.delete("/bookings/999")
        assert response.status_code == 404
        assert "Booking tidak ditemukan" in response.json()["detail"]

    def test_get_bookings_by_user(self, setup_database):
        """Test get bookings by user ID"""
        response = client.get("/bookings/user/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Bookings retrieved successfully"
        assert len(response.json()["data"]) >= 1
        assert all(booking["user_id"] == 1 for booking in response.json()["data"])

    def test_get_bookings_by_status(self, setup_database):
        """Test get bookings by status"""
        response = client.get("/bookings/status/pending")
        assert response.status_code == 200
        assert response.json()["message"] == "Bookings retrieved successfully"
        assert all(booking["booking_status"] == "pending" for booking in response.json()["data"])

    def test_get_all_booked_foods(self, setup_database):
        """Test get all booked foods"""
        response = client.get("/bookings/foods/all")
        assert response.status_code == 200
        assert response.json()["message"] == "Booked foods retrieved successfully"
        assert len(response.json()["data"]) >= 2

    def test_get_booked_food_by_id(self, setup_database):
        """Test get booked food by ID"""
        response = client.get("/bookings/foods/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1
        assert response.json()["data"]["booking_id"] == 1

    def test_get_booked_food_by_id_not_found(self, setup_database):
        """Test get booked food by ID when not found"""
        response = client.get("/bookings/foods/999")
        assert response.status_code == 404
        assert "Booked food tidak ditemukan" in response.json()["detail"]

    def test_create_booked_food(self, setup_database):
        """Test create new booked food"""
        response = client.post(
            "/bookings/foods",
            json={
                "booking_id": 1,
                "food_id": 2,
                "quantity": 3
            }
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Booked food created successfully"
        assert response.json()["data"]["booking_id"] == 1
        assert response.json()["data"]["food_id"] == 2
        assert response.json()["data"]["quantity"] == 3

    def test_create_booked_food_invalid_booking(self, setup_database):
        """Test create booked food with invalid booking"""
        response = client.post(
            "/bookings/foods",
            json={
                "booking_id": 999,
                "food_id": 1,
                "quantity": 2
            }
        )
        assert response.status_code == 404
        assert "Booking tidak ditemukan" in response.json()["detail"]

    def test_create_booked_food_invalid_food(self, setup_database):
        """Test create booked food with invalid food"""
        response = client.post(
            "/bookings/foods",
            json={
                "booking_id": 1,
                "food_id": 999,
                "quantity": 2
            }
        )
        assert response.status_code == 404
        assert "Food package tidak ditemukan" in response.json()["detail"]

    def test_update_booked_food(self, setup_database):
        """Test update booked food"""
        response = client.put(
            "/bookings/foods/1",
            json={"quantity": 5}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Booked food updated successfully"
        assert response.json()["data"]["quantity"] == 5

    def test_update_booked_food_not_found(self, setup_database):
        """Test update booked food when not found"""
        response = client.put(
            "/bookings/foods/999",
            json={"quantity": 2}
        )
        assert response.status_code == 404
        assert "Booked food tidak ditemukan" in response.json()["detail"]

    def test_delete_booked_food(self, setup_database):
        """Test delete booked food"""
        # Create a new booked food first
        create_response = client.post(
            "/bookings/foods",
            json={
                "booking_id": 1,
                "food_id": 1,
                "quantity": 2
            }
        )
        booked_food_id = create_response.json()["data"]["id"]

        # Delete the booked food
        response = client.delete(f"/bookings/foods/{booked_food_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Booked food deleted successfully"

        # Verify booked food is deleted
        verify_response = client.get(f"/bookings/foods/{booked_food_id}")
        assert verify_response.status_code == 404

    def test_delete_booked_food_not_found(self, setup_database):
        """Test delete booked food when not found"""
        response = client.delete("/bookings/foods/999")
        assert response.status_code == 404
        assert "Booked food tidak ditemukan" in response.json()["detail"]

    def test_get_booked_foods_by_booking(self, setup_database):
        """Test get booked foods by booking ID"""
        response = client.get("/bookings/1/foods")
        assert response.status_code == 200
        assert response.json()["message"] == "Booked foods retrieved successfully"
        assert len(response.json()["data"]) >= 2
        assert all(food["booking_id"] == 1 for food in response.json()["data"])

