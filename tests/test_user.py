import pytest
from tests.conftest import client, setup_database


class TestUserEndpoints:
    """Test User CRUD Endpoints"""

    def test_get_all_users(self, setup_database):
        """Test get all users"""
        response = client.get("/users/")
        assert response.status_code == 200
        assert response.json()["message"] == "Users retrieved successfully"
        assert len(response.json()["data"]) >= 3

    def test_get_user_by_id(self, setup_database):
        """Test get user by ID"""
        response = client.get("/users/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1
        assert response.json()["data"]["username"] == "admin"

    def test_get_user_by_id_not_found(self, setup_database):
        """Test get user by ID when user doesn't exist"""
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "User tidak ditemukan" in response.json()["detail"]

    def test_get_current_user_profile(self, admin_token, setup_database):
        """Test get current user profile with valid token"""
        response = client.get(
            "/users/profile/me",
            headers={"Authorization": f"Bearer {admin_token}"}
        )
        assert response.status_code == 200
        assert response.json()["data"]["username"] == "admin"

    def test_get_current_user_profile_no_token(self, setup_database):
        """Test get current user profile without token"""
        response = client.get("/users/profile/me")
        assert response.status_code == 401

    def test_get_current_user_profile_invalid_token(self, setup_database):
        """Test get current user profile with invalid token"""
        response = client.get(
            "/users/profile/me",
            headers={"Authorization": "Bearer invalid_token"}
        )
        assert response.status_code == 401

    def test_create_user(self, setup_database):
        """Test create new user"""
        response = client.post(
            "/users/",
            json={
                "name": "New Employee",
                "username": "newemployee",
                "email": "newemployee@example.com",
                "phone_number": "08888888888",
                "password": "password123",
                "role_id": 2
            }
        )
        assert response.status_code == 201
        assert response.json()["message"] == "User created successfully"
        assert response.json()["data"]["username"] == "newemployee"
        assert response.json()["data"]["role_id"] == 2

    def test_create_user_duplicate_username(self, setup_database):
        """Test create user with duplicate username"""
        response = client.post(
            "/users/",
            json={
                "name": "Duplicate",
                "username": "admin",
                "email": "duplicate@example.com",
                "phone_number": "08888888888",
                "password": "password123",
                "role_id": 2
            }
        )
        assert response.status_code == 400
        assert "Username sudah digunakan" in response.json()["detail"]

    def test_create_user_duplicate_email(self, setup_database):
        """Test create user with duplicate email"""
        response = client.post(
            "/users/",
            json={
                "name": "Duplicate",
                "username": "newuser",
                "email": "admin@example.com",
                "phone_number": "08888888888",
                "password": "password123",
                "role_id": 2
            }
        )
        assert response.status_code == 400
        assert "Email sudah terdaftar" in response.json()["detail"]

    def test_create_user_invalid_role(self, setup_database):
        """Test create user with invalid role"""
        response = client.post(
            "/users/",
            json={
                "name": "New User",
                "username": "newuser2",
                "email": "newuser2@example.com",
                "phone_number": "08888888888",
                "password": "password123",
                "role_id": 999
            }
        )
        assert response.status_code == 404
        assert "Role tidak ditemukan" in response.json()["detail"]

    def test_update_user(self, setup_database):
        """Test update user"""
        response = client.put(
            "/users/1",
            json={
                "name": "Admin Updated",
                "phone_number": "08111111111"
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "User updated successfully"
        assert response.json()["data"]["name"] == "Admin Updated"
        assert response.json()["data"]["phone_number"] == "08111111111"

    def test_update_user_not_found(self, setup_database):
        """Test update user when user doesn't exist"""
        response = client.put(
            "/users/999",
            json={"name": "Updated"}
        )
        assert response.status_code == 404
        assert "User tidak ditemukan" in response.json()["detail"]

    def test_update_user_duplicate_username(self, setup_database):
        """Test update user with duplicate username"""
        response = client.put(
            "/users/1",
            json={"username": "employee1"}
        )
        assert response.status_code == 400
        assert "Username sudah digunakan" in response.json()["detail"]

    def test_delete_user(self, setup_database):
        """Test delete user"""
        response = client.delete("/users/3")
        assert response.status_code == 200
        assert response.json()["message"] == "User deleted successfully"

        # Verify user is deleted
        verify_response = client.get("/users/3")
        assert verify_response.status_code == 404

    def test_delete_user_not_found(self, setup_database):
        """Test delete user when user doesn't exist"""
        response = client.delete("/users/999")
        assert response.status_code == 404
        assert "User tidak ditemukan" in response.json()["detail"]

    def test_search_user_by_username(self, setup_database):
        """Test search user by username"""
        response = client.get("/users/search/username/admin")
        assert response.status_code == 200
        assert response.json()["data"]["username"] == "admin"

    def test_search_user_by_username_not_found(self, setup_database):
        """Test search user by username when not found"""
        response = client.get("/users/search/username/nonexistent")
        assert response.status_code == 404

    def test_search_user_by_email(self, setup_database):
        """Test search user by email"""
        response = client.get("/users/search/email/admin@example.com")
        assert response.status_code == 200
        assert response.json()["data"]["email"] == "admin@example.com"

    def test_search_user_by_email_not_found(self, setup_database):
        """Test search user by email when not found"""
        response = client.get("/users/search/email/nonexistent@example.com")
        assert response.status_code == 404

    def test_get_users_by_role(self, setup_database):
        """Test get users by role"""
        response = client.get("/users/role/2")
        assert response.status_code == 200
        assert len(response.json()["data"]) >= 1
        assert response.json()["data"][0]["role_id"] == 2

    def test_change_password_success(self, setup_database):
        """Test successful password change"""
        response = client.post(
            "/users/1/change-password",
            json={
                "old_password": "admin123",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Password changed successfully"

    def test_change_password_wrong_old_password(self, setup_database):
        """Test change password with wrong old password"""
        response = client.post(
            "/users/1/change-password",
            json={
                "old_password": "wrongpassword",
                "new_password": "newpassword123",
                "confirm_password": "newpassword123"
            }
        )
        assert response.status_code == 401
        assert "Password lama tidak cocok" in response.json()["detail"]

    def test_change_password_new_password_mismatch(self, setup_database):
        """Test change password with mismatched new passwords"""
        response = client.post(
            "/users/1/change-password",
            json={
                "old_password": "admin123",
                "new_password": "newpassword123",
                "confirm_password": "differentpassword123"
            }
        )
        assert response.status_code == 400
        assert "Password baru tidak cocok" in response.json()["detail"]

    def test_change_password_same_as_old(self, setup_database):
        """Test change password with same password as old"""
        response = client.post(
            "/users/1/change-password",
            json={
                "old_password": "admin123",
                "new_password": "admin123",
                "confirm_password": "admin123"
            }
        )
        assert response.status_code == 400
        assert "Password baru harus berbeda dengan password lama" in response.json()["detail"]

    def test_change_password_too_short(self, setup_database):
        """Test change password with password less than 6 characters"""
        response = client.post(
            "/users/1/change-password",
            json={
                "old_password": "admin123",
                "new_password": "12345",
                "confirm_password": "12345"
            }
        )
        assert response.status_code == 400
        assert "Password baru harus minimal 6 karakter" in response.json()["detail"]

