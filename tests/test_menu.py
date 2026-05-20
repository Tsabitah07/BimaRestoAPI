import pytest
from datetime import datetime, timedelta
from tests.conftest import client, setup_database


class TestMenuEndpoints:
    """Test Menu CRUD Endpoints"""

    def test_get_all_menus(self, setup_database):
        """Test get all menus"""
        response = client.get("/menus/")
        assert response.status_code == 200
        assert response.json()["message"] == "Menus retrieved successfully"
        assert len(response.json()["data"]) >= 1

    def test_get_menu_by_id(self, setup_database):
        """Test get menu by ID"""
        response = client.get("/menus/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1
        assert response.json()["data"]["name"] == "Menu Mei"

    def test_get_menu_by_id_not_found(self, setup_database):
        """Test get menu by ID when not found"""
        response = client.get("/menus/999")
        assert response.status_code == 404
        assert "Menu tidak ditemukan" in response.json()["detail"]

    def test_create_menu(self, setup_database):
        """Test create new menu"""
        today = datetime.now()
        response = client.post(
            "/menus/",
            json={
                "name": "Menu Juni",
                "start_date": today.isoformat(),
                "end_date": (today + timedelta(days=30)).isoformat(),
                "poster_paths": ["https://example.com/poster1.jpg"]
            }
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Menu created successfully"
        assert response.json()["data"]["name"] == "Menu Juni"

    def test_update_menu(self, setup_database):
        """Test update menu"""
        today = datetime.now()
        response = client.put(
            "/menus/1",
            json={
                "name": "Menu Mei Updated",
                "start_date": today.isoformat()
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Menu updated successfully"
        assert response.json()["data"]["name"] == "Menu Mei Updated"

    def test_update_menu_not_found(self, setup_database):
        """Test update menu when not found"""
        response = client.put(
            "/menus/999",
            json={"name": "Updated"}
        )
        assert response.status_code == 404
        assert "Menu tidak ditemukan" in response.json()["detail"]

    def test_delete_menu(self, setup_database):
        """Test delete menu"""
        # Create a new menu first
        today = datetime.now()
        create_response = client.post(
            "/menus/",
            json={
                "name": "Temporary Menu",
                "start_date": today.isoformat(),
                "end_date": (today + timedelta(days=30)).isoformat()
            }
        )
        menu_id = create_response.json()["data"]["id"]

        # Delete the menu
        response = client.delete(f"/menus/{menu_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Menu deleted successfully"

        # Verify menu is deleted
        verify_response = client.get(f"/menus/{menu_id}")
        assert verify_response.status_code == 404

    def test_delete_menu_not_found(self, setup_database):
        """Test delete menu when not found"""
        response = client.delete("/menus/999")
        assert response.status_code == 404
        assert "Menu tidak ditemukan" in response.json()["detail"]

    def test_get_all_menu_posters(self, setup_database):
        """Test get all menu posters"""
        response = client.get("/menus/posters/all")
        assert response.status_code == 200
        assert response.json()["message"] == "Menu posters retrieved successfully"
        assert len(response.json()["data"]) >= 1

    def test_get_menu_poster_by_id(self, setup_database):
        """Test get menu poster by ID"""
        response = client.get("/menus/posters/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1
        assert response.json()["data"]["menu_id"] == 1

    def test_get_menu_poster_by_id_not_found(self, setup_database):
        """Test get menu poster by ID when not found"""
        response = client.get("/menus/posters/999")
        assert response.status_code == 404
        assert "Menu poster tidak ditemukan" in response.json()["detail"]

    def test_get_menu_posters_by_menu(self, setup_database):
        """Test get menu posters by menu ID"""
        response = client.get("/menus/1/posters")
        assert response.status_code == 200
        assert response.json()["message"] == "Menu posters retrieved successfully"
        assert len(response.json()["data"]) >= 1

    def test_create_menu_poster(self, setup_database):
        """Test create new menu poster"""
        response = client.post(
            "/menus/posters",
            json={
                "menu_id": 1,
                "poster_path": "https://example.com/poster2.jpg"
            }
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Menu poster created successfully"
        assert response.json()["data"]["poster_path"] == "https://example.com/poster2.jpg"

    def test_create_menu_poster_invalid_menu(self, setup_database):
        """Test create menu poster with invalid menu"""
        response = client.post(
            "/menus/posters",
            json={
                "menu_id": 999,
                "poster_path": "https://example.com/poster.jpg"
            }
        )
        assert response.status_code == 404
        assert "Menu tidak ditemukan" in response.json()["detail"]

    def test_delete_menu_poster(self, setup_database):
        """Test delete menu poster"""
        # Create a new poster first
        create_response = client.post(
            "/menus/posters",
            json={
                "menu_id": 1,
                "poster_path": "https://example.com/temp_poster.jpg"
            }
        )
        poster_id = create_response.json()["data"]["id"]

        # Delete the poster
        response = client.delete(f"/menus/posters/{poster_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Menu poster deleted successfully"

        # Verify poster is deleted
        verify_response = client.get(f"/menus/posters/{poster_id}")
        assert verify_response.status_code == 404

    def test_delete_menu_poster_not_found(self, setup_database):
        """Test delete menu poster when not found"""
        response = client.delete("/menus/posters/999")
        assert response.status_code == 404
        assert "Menu poster tidak ditemukan" in response.json()["detail"]

