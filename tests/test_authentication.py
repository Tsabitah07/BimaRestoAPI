import pytest
from datetime import datetime, timedelta
from tests.conftest import client, setup_database


class TestAuthenticationEndpoints:
    """Test Authentication Endpoints"""

    def test_login_success(self, setup_database):
        """Test successful login"""
        response = client.post(
            "/auth/login",
            json={"username": "admin", "password": "admin123"}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Login berhasil"
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"
        assert response.json()["user"]["username"] == "admin"

    def test_login_invalid_username(self, setup_database):
        """Test login with invalid username"""
        response = client.post(
            "/auth/login",
            json={"username": "invalid_user", "password": "password123"}
        )
        assert response.status_code == 401
        assert "Username atau password salah" in response.json()["detail"]

    def test_login_invalid_password(self, setup_database):
        """Test login with invalid password"""
        response = client.post(
            "/auth/login",
            json={"username": "admin", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        assert "Username atau password salah" in response.json()["detail"]

    def test_register_success(self, setup_database):
        """Test successful registration"""
        response = client.post(
            "/auth/register",
            json={
                "name": "New User",
                "username": "newuser",
                "email": "newuser@example.com",
                "phone_number": "08999999999",
                "password": "password123",
                "confirm_password": "password123"
            }
        )
        assert response.status_code == 201
        assert response.json()["message"] == "Registrasi berhasil"
        assert response.json()["data"]["username"] == "newuser"
        assert response.json()["data"]["email"] == "newuser@example.com"

    def test_register_password_mismatch(self, setup_database):
        """Test registration with mismatched passwords"""
        response = client.post(
            "/auth/register",
            json={
                "name": "New User",
                "username": "newuser2",
                "email": "newuser2@example.com",
                "phone_number": "08999999999",
                "password": "password123",
                "confirm_password": "password456"
            }
        )
        assert response.status_code == 400
        assert "Password tidak cocok" in response.json()["detail"]

    def test_register_password_too_short(self, setup_database):
        """Test registration with password less than 6 characters"""
        response = client.post(
            "/auth/register",
            json={
                "name": "New User",
                "username": "newuser3",
                "email": "newuser3@example.com",
                "phone_number": "08999999999",
                "password": "12345",
                "confirm_password": "12345"
            }
        )
        assert response.status_code == 400
        assert "Password harus minimal 6 karakter" in response.json()["detail"]

    def test_register_duplicate_username(self, setup_database):
        """Test registration with duplicate username"""
        response = client.post(
            "/auth/register",
            json={
                "name": "Duplicate User",
                "username": "admin",
                "email": "duplicate@example.com",
                "phone_number": "08999999999",
                "password": "password123",
                "confirm_password": "password123"
            }
        )
        assert response.status_code == 400
        assert "Username sudah digunakan" in response.json()["detail"]

    def test_register_duplicate_email(self, setup_database):
        """Test registration with duplicate email"""
        response = client.post(
            "/auth/register",
            json={
                "name": "Duplicate Email",
                "username": "newuser4",
                "email": "admin@example.com",
                "phone_number": "08999999999",
                "password": "password123",
                "confirm_password": "password123"
            }
        )
        assert response.status_code == 400
        assert "Email sudah terdaftar" in response.json()["detail"]

    def test_verify_token_success(self, admin_token, setup_database):
        """Test successful token verification"""
        response = client.post(
            "/auth/verify-token",
            params={"token": admin_token}
        )
        assert response.status_code == 200
        assert response.json()["message"] == "Token valid"
        assert response.json()["user"]["username"] == "admin"

    def test_verify_token_invalid(self, setup_database):
        """Test token verification with invalid token"""
        response = client.post(
            "/auth/verify-token",
            params={"token": "invalid_token_xyz"}
        )
        assert response.status_code == 401
        assert "Token tidak valid" in response.json()["detail"]

