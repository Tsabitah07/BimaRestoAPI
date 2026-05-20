import pytest
from tests.conftest import client, setup_database


class TestFoodPackageEndpoints:
    """Test Food Package CRUD Endpoints"""

    def test_get_all_food_packages(self, setup_database):
        """Test get all food packages"""
        response = client.get("/food-packages/")
        assert response.status_code == 200
        assert response.json()["message"] == "Food packages retrieved successfully"
        assert len(response.json()["data"]) >= 2

    def test_get_food_package_by_id(self, setup_database):
        """Test get food package by ID"""
        response = client.get("/food-packages/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1
        assert response.json()["data"]["name"] == "Paket Lunch Premium"

    def test_get_food_package_by_id_not_found(self, setup_database):
        """Test get food package by ID when not found"""
        response = client.get("/food-packages/999")
        assert response.status_code == 404
        assert "Food package tidak ditemukan" in response.json()["detail"]

    def test_create_food_package(self, setup_database):
        """Test create new food package"""
        response = client.post(
            "/food-packages/",
            json={
                "name": "Paket Dinner Premium",
                "description": "Nasi, Steak, Sayur, Wine, Dessert",
                "menu_id": 1,
                "session_id": 2,
                "available_quantity": 30
            }
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Food package created successfully"
        assert response.json()["data"]["name"] == "Paket Dinner Premium"
        assert response.json()["data"]["available_quantity"] == 30

    def test_create_food_package_invalid_menu(self, setup_database):
        """Test create food package with invalid menu"""
        response = client.post(
            "/food-packages/",
            json={
                "name": "Test Package",
                "description": "Test Description",
                "menu_id": 999,
                "session_id": 1,
                "available_quantity": 10
            }
        )
        assert response.status_code == 404
        assert "Menu tidak ditemukan" in response.json()["detail"]

    def test_create_food_package_invalid_session(self, setup_database):
        """Test create food package with invalid session"""
        response = client.post(
            "/food-packages/",
            json={
                "name": "Test Package",
                "description": "Test Description",
                "menu_id": 1,
                "session_id": 999,
                "available_quantity": 10
            }
        )
        assert response.status_code == 404
        assert "Booking session tidak ditemukan" in response.json()["detail"]

    def test_update_food_package(self, setup_database):
        """Test update food package"""
        response = client.put(
            "/food-packages/1",
            json={
                "name": "Paket Lunch Premium Updated",
                "available_quantity": 60
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Food package updated successfully"
        assert response.json()["data"]["name"] == "Paket Lunch Premium Updated"
        assert response.json()["data"]["available_quantity"] == 60

    def test_update_food_package_not_found(self, setup_database):
        """Test update food package when not found"""
        response = client.put(
            "/food-packages/999",
            json={"name": "Updated"}
        )
        assert response.status_code == 404
        assert "Food package tidak ditemukan" in response.json()["detail"]

    def test_delete_food_package(self, setup_database):
        """Test delete food package"""
        # Create a new food package first
        create_response = client.post(
            "/food-packages/",
            json={
                "name": "Temporary Package",
                "description": "Temporary Description",
                "menu_id": 1,
                "session_id": 1,
                "available_quantity": 10
            }
        )
        food_id = create_response.json()["data"]["id"]

        # Delete the food package
        response = client.delete(f"/food-packages/{food_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Food package deleted successfully"

        # Verify food package is deleted
        verify_response = client.get(f"/food-packages/{food_id}")
        assert verify_response.status_code == 404

    def test_delete_food_package_not_found(self, setup_database):
        """Test delete food package when not found"""
        response = client.delete("/food-packages/999")
        assert response.status_code == 404
        assert "Food package tidak ditemukan" in response.json()["detail"]

    def test_get_food_packages_by_menu(self, setup_database):
        """Test get food packages by menu ID"""
        response = client.get("/food-packages/menu/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Food packages retrieved successfully"
        assert len(response.json()["data"]) >= 2
        assert all(pkg["menu_id"] == 1 for pkg in response.json()["data"])

    def test_get_food_packages_by_session(self, setup_database):
        """Test get food packages by session ID"""
        response = client.get("/food-packages/session/1")
        assert response.status_code == 200
        assert response.json()["message"] == "Food packages retrieved successfully"
        assert all(pkg["session_id"] == 1 for pkg in response.json()["data"])

