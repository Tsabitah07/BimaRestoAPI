import pytest
from tests.conftest import client, setup_database


class TestRoleEndpoints:
    """Test Role CRUD Endpoints"""

    def test_get_all_roles(self, setup_database):
        """Test get all roles"""
        response = client.get("/roles/")
        assert response.status_code == 200
        assert response.json()["message"] == "Roles retrieved successfully"
        assert len(response.json()["data"]) == 3

    def test_get_role_by_id(self, setup_database):
        """Test get role by ID"""
        response = client.get("/roles/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1
        assert response.json()["data"]["name"] == "Admin"

    def test_get_role_by_id_not_found(self, setup_database):
        """Test get role by ID when role doesn't exist"""
        response = client.get("/roles/999")
        assert response.status_code == 404
        assert "Role tidak ditemukan" in response.json()["detail"]

    def test_create_role(self, setup_database):
        """Test create new role"""
        response = client.post(
            "/roles/",
            json={"name": "Manager"}
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Role created successfully"
        assert response.json()["data"]["name"] == "Manager"

    def test_update_role(self, setup_database):
        """Test update role"""
        response = client.put(
            "/roles/1",
            json={"name": "Super Admin"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Role updated successfully"
        assert response.json()["data"]["name"] == "Super Admin"

    def test_update_role_not_found(self, setup_database):
        """Test update role when role doesn't exist"""
        response = client.put(
            "/roles/999",
            json={"name": "Updated"}
        )
        assert response.status_code == 404
        assert "Role tidak ditemukan" in response.json()["detail"]

    def test_delete_role(self, setup_database):
        """Test delete role"""
        # Create a new role first
        create_response = client.post(
            "/roles/",
            json={"name": "Temporary Role"}
        )
        role_id = create_response.json()["data"]["id"]

        # Delete the role
        response = client.delete(f"/roles/{role_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Role deleted successfully"

        # Verify role is deleted
        verify_response = client.get(f"/roles/{role_id}")
        assert verify_response.status_code == 404

    def test_delete_role_not_found(self, setup_database):
        """Test delete role when role doesn't exist"""
        response = client.delete("/roles/999")
        assert response.status_code == 404
        assert "Role tidak ditemukan" in response.json()["detail"]

