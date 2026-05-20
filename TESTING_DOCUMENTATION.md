# Unit Testing Documentation - BimaRestoAPI

## Overview
Telah dibuat comprehensive unit testing untuk semua endpoints dalam BimaRestoAPI menggunakan pytest dan FastAPI TestClient.

## Struktur Testing

```
tests/
├── __init__.py
├── conftest.py                 # Pytest configuration & fixtures
├── test_authentication.py       # Authentication endpoint tests
├── test_user.py               # User CRUD endpoint tests
├── test_role.py               # Role CRUD endpoint tests
├── test_booking_session.py     # Booking Session CRUD endpoint tests
├── test_menu.py               # Menu CRUD endpoint tests
├── test_food_package.py        # Food Package CRUD endpoint tests
└── test_booking.py            # Booking CRUD endpoint tests
```

## Test Coverage

### 1. Authentication Tests (`test_authentication.py`)
- ✅ Login dengan kredensial valid
- ✅ Login dengan username invalid
- ✅ Login dengan password invalid
- ✅ Register user baru
- ✅ Register dengan password tidak cocok
- ✅ Register dengan password terlalu pendek
- ✅ Register dengan username duplicate
- ✅ Register dengan email duplicate
- ✅ Verify token valid
- ✅ Verify token invalid

**Total: 10 tests**

### 2. User Tests (`test_user.py`)
- ✅ Get semua users
- ✅ Get user by ID
- ✅ Get user by ID (not found)
- ✅ Get current user profile (dengan token)
- ✅ Get current user profile (tanpa token)
- ✅ Get current user profile (invalid token)
- ✅ Create user baru
- ✅ Create user dengan duplicate username
- ✅ Create user dengan duplicate email
- ✅ Create user dengan invalid role
- ✅ Update user
- ✅ Update user (not found)
- ✅ Update user dengan duplicate username
- ✅ Delete user
- ✅ Delete user (not found)
- ✅ Search user by username
- ✅ Search user by username (not found)
- ✅ Search user by email
- ✅ Search user by email (not found)
- ✅ Get users by role
- ✅ Change password (success)
- ✅ Change password (wrong old password)
- ✅ Change password (new password mismatch)
- ✅ Change password (same as old)
- ✅ Change password (too short)

**Total: 25 tests**

### 3. Role Tests (`test_role.py`)
- ✅ Get semua roles
- ✅ Get role by ID
- ✅ Get role by ID (not found)
- ✅ Create role baru
- ✅ Update role
- ✅ Update role (not found)
- ✅ Delete role
- ✅ Delete role (not found)

**Total: 8 tests**

### 4. Booking Session Tests (`test_booking_session.py`)
- ✅ Get semua booking sessions
- ✅ Get booking session by ID
- ✅ Get booking session by ID (not found)
- ✅ Create booking session baru
- ✅ Update booking session
- ✅ Update booking session (not found)
- ✅ Delete booking session
- ✅ Delete booking session (not found)

**Total: 8 tests**

### 5. Menu Tests (`test_menu.py`)
- ✅ Get semua menus
- ✅ Get menu by ID
- ✅ Get menu by ID (not found)
- ✅ Create menu baru
- ✅ Update menu
- ✅ Update menu (not found)
- ✅ Delete menu
- ✅ Delete menu (not found)
- ✅ Get semua menu posters
- ✅ Get menu poster by ID
- ✅ Get menu poster by ID (not found)
- ✅ Get menu posters by menu ID
- ✅ Create menu poster baru
- ✅ Create menu poster (invalid menu)
- ✅ Delete menu poster
- ✅ Delete menu poster (not found)

**Total: 16 tests**

### 6. Food Package Tests (`test_food_package.py`)
- ✅ Get semua food packages
- ✅ Get food package by ID
- ✅ Get food package by ID (not found)
- ✅ Create food package baru
- ✅ Create food package (invalid menu)
- ✅ Create food package (invalid session)
- ✅ Update food package
- ✅ Update food package (not found)
- ✅ Delete food package
- ✅ Delete food package (not found)
- ✅ Get food packages by menu ID
- ✅ Get food packages by session ID

**Total: 12 tests**

### 7. Booking Tests (`test_booking.py`)
- ✅ Get semua bookings
- ✅ Get booking by ID
- ✅ Get booking by ID (not found)
- ✅ Create booking baru
- ✅ Create booking (invalid user)
- ✅ Create booking (invalid session)
- ✅ Create booking (invalid food)
- ✅ Update booking
- ✅ Update booking (not found)
- ✅ Delete booking
- ✅ Delete booking (not found)
- ✅ Get bookings by user ID
- ✅ Get bookings by status
- ✅ Get semua booked foods
- ✅ Get booked food by ID
- ✅ Get booked food by ID (not found)
- ✅ Create booked food baru
- ✅ Create booked food (invalid booking)
- ✅ Create booked food (invalid food)
- ✅ Update booked food
- ✅ Update booked food (not found)
- ✅ Delete booked food
- ✅ Delete booked food (not found)
- ✅ Get booked foods by booking ID

**Total: 25 tests**

## Total Test Coverage: 104 Tests

## Installation

### 1. Install Testing Dependencies
```bash
pip install -r requirements-test.txt
```

Atau install satu per satu:
```bash
pip install pytest==7.4.3
pip install pytest-asyncio==0.21.1
pip install httpx==0.24.1
```

### 2. Verify Installation
```bash
pytest --version
```

## Running Tests

### Run All Tests
```bash
pytest
```

### Run Tests with Verbose Output
```bash
pytest -v
```

### Run Specific Test File
```bash
pytest tests/test_user.py -v
```

### Run Specific Test Class
```bash
pytest tests/test_user.py::TestUserEndpoints -v
```

### Run Specific Test Function
```bash
pytest tests/test_user.py::TestUserEndpoints::test_login_success -v
```

### Run Tests with Coverage Report
```bash
pip install pytest-cov
pytest --cov=. --cov-report=html
```

### Run Tests by Marker
```bash
pytest -m authentication
pytest -m user
pytest -m booking
```

## Test Fixtures

### `setup_database`
Fixture yang menyiapkan database dengan seed data:
- 3 Roles (Admin, Employee, User)
- 3 Users dengan berbagai roles
- 2 Booking Sessions
- 1 Menu dengan 2 Food Packages
- 1 Menu Poster
- 1 Booking dengan 2 Booked Foods

```python
@pytest.fixture(scope="function")
def setup_database():
    # Setup dan teardown database
    yield db
```

### `admin_token`
Fixture untuk mendapatkan JWT token dari admin user:
```python
@pytest.fixture
def admin_token(setup_database):
    response = client.post(
        "/auth/login",
        json={"username": "admin", "password": "admin123"}
    )
    return response.json()["access_token"]
```

### `user_token`
Fixture untuk mendapatkan JWT token dari regular user:
```python
@pytest.fixture
def user_token(setup_database):
    response = client.post(
        "/auth/login",
        json={"username": "user1", "password": "user123"}
    )
    return response.json()["access_token"]
```

## Database Testing

Unit tests menggunakan SQLite in-memory database:
- Isolasi penuh antar tests
- Tidak mempengaruhi production database
- Setup dan teardown otomatis
- Performance testing yang cepat

## Contoh Test

### Contoh 1: Simple GET Test
```python
def test_get_all_users(self, setup_database):
    """Test get all users"""
    response = client.get("/users/")
    assert response.status_code == 200
    assert response.json()["message"] == "Users retrieved successfully"
    assert len(response.json()["data"]) >= 3
```

### Contoh 2: POST Test dengan Validasi
```python
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
```

### Contoh 3: Test dengan Token Authentication
```python
def test_get_current_user_profile(self, admin_token, setup_database):
    """Test get current user profile with valid token"""
    response = client.get(
        "/users/profile/me",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert response.status_code == 200
    assert response.json()["data"]["username"] == "admin"
```

### Contoh 4: Error Handling Test
```python
def test_get_user_by_id_not_found(self, setup_database):
    """Test get user by ID when user doesn't exist"""
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "User tidak ditemukan" in response.json()["detail"]
```

## Best Practices

1. **Isolation**: Setiap test function tidak bergantung pada test lain
2. **Clarity**: Test names menjelaskan apa yang ditest
3. **Coverage**: Test success dan error cases
4. **Fixtures**: Gunakan fixtures untuk setup yang kompleks
5. **Assertions**: Gunakan multiple assertions untuk validasi lengkap

## CI/CD Integration

Untuk mengintegrasikan dengan CI/CD pipeline:

### GitHub Actions Example
```yaml
name: Run Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - run: pip install -r requirements.txt
      - run: pip install -r requirements-test.txt
      - run: pytest --cov=. --cov-report=xml
```

## Troubleshooting

### Import Errors
```bash
# Make sure pytest dapat menemukan modules
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest
```

### Database Errors
```bash
# Pastikan semua model sudah ter-import di conftest.py
# Check database.py untuk connection issues
```

### Async Errors
```bash
# Install pytest-asyncio jika ada async tests
pip install pytest-asyncio
```

## Next Steps

1. ✅ Jalankan tests: `pytest`
2. ✅ Check coverage: `pytest --cov=.`
3. ✅ Integrate dengan CI/CD
4. ✅ Tambahkan performance tests
5. ✅ Tambahkan integration tests

## Commands Reference

```bash
# Basic
pytest                           # Run all tests
pytest -v                        # Verbose output
pytest -q                        # Quiet output

# Coverage
pytest --cov=.                   # Show coverage
pytest --cov=. --cov-report=html # HTML report

# Filtering
pytest tests/test_user.py        # Specific file
pytest -k "test_create"          # By name pattern
pytest -m authentication         # By marker

# Debugging
pytest -s                        # Show print statements
pytest --pdb                     # Drop into debugger on failure
pytest --lf                      # Last failed
pytest --ff                      # Failed first

# Performance
pytest --durations=10            # Slowest 10 tests
```

## Support

Untuk pertanyaan atau issues, silakan buat issue atau hubungi tim development.

