import pytest
from tests.conftest import client, setup_database


class TestBookingSessionEndpoints:
    """Test Booking Session CRUD Endpoints"""

    def test_get_all_booking_sessions(self, setup_database):
        """Test get all booking sessions"""
        response = client.get("/booking-sessions/")
        assert response.status_code == 200
        assert response.json()["message"] == "Booking sessions retrieved successfully"
        assert len(response.json()["data"]) >= 2

    def test_get_booking_session_by_id(self, setup_database):
        """Test get booking session by ID"""
        response = client.get("/booking-sessions/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1
        assert response.json()["data"]["name"] == "Lunch Session"

    def test_get_booking_session_by_id_not_found(self, setup_database):
        """Test get booking session by ID when not found"""
        response = client.get("/booking-sessions/999")
        assert response.status_code == 404
        assert "Booking session tidak ditemukan" in response.json()["detail"]

    def test_create_booking_session(self, setup_database):
        """Test create new booking session"""
        response = client.post(
            "/booking-sessions/",
            json={
                "name": "Breakfast Session",
                "time": "07:00 - 09:00"
            }
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Booking session created successfully"
        assert response.json()["data"]["name"] == "Breakfast Session"
        assert response.json()["data"]["time"] == "07:00 - 09:00"

    def test_update_booking_session(self, setup_database):
        """Test update booking session"""
        response = client.put(
            "/booking-sessions/1",
            json={
                "name": "Lunch Session Updated",
                "time": "12:00 - 14:00"
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Booking session updated successfully"
        assert response.json()["data"]["name"] == "Lunch Session Updated"
        assert response.json()["data"]["time"] == "12:00 - 14:00"

    def test_update_booking_session_not_found(self, setup_database):
        """Test update booking session when not found"""
        response = client.put(
            "/booking-sessions/999",
            json={"name": "Updated"}
        )
        assert response.status_code == 404
        assert "Booking session tidak ditemukan" in response.json()["detail"]

    def test_delete_booking_session(self, setup_database):
        """Test delete booking session"""
        # Create a new session first
        create_response = client.post(
            "/booking-sessions/",
            json={
                "name": "Temporary Session",
                "time": "15:00 - 17:00"
            }
        )
        session_id = create_response.json()["data"]["id"]

        # Delete the session
        response = client.delete(f"/booking-sessions/{session_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Booking session deleted successfully"

        # Verify session is deleted
        verify_response = client.get(f"/booking-sessions/{session_id}")
        assert verify_response.status_code == 404

    def test_delete_booking_session_not_found(self, setup_database):
        """Test delete booking session when not found"""
        response = client.delete("/booking-sessions/999")
        assert response.status_code == 404
        assert "Booking session tidak ditemukan" in response.json()["detail"]

