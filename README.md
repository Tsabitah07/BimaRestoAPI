# BimaRestoAPI

A small FastAPI-based backend for managing restaurant menus, food packages, booking sessions, bookings, users and roles — including authentication (JWT), file uploads for menu posters, and seeded demo data on startup.

This README documents the current flow and features implemented in the repository and how to run and test the application locally.

---

## Key Features

- JWT-based authentication (login, register, verify token)
- User management (CRUD, change password, profile from token)
- Role management (CRUD)
- Menu management with poster images (upload and static serving)
- Food packages tied to menus and booking sessions (CRUD)
- Booking sessions management (CRUD)
- Bookings with booked foods (CRUD, filter by user/status)
- Automatic database creation and seed data runner executed on app startup
- OpenAPI docs available at `/docs` (Swagger UI) and `/redoc`

---

## Quick Start

Requirements
- Python 3.10+ (project tested with modern Python versions)

Recommended steps (Windows `cmd.exe`):

1. Create and activate a virtual environment

```cmd
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies

The repository includes `requirements-test.txt` containing test dependencies. The runtime also requires FastAPI, Uvicorn, SQLAlchemy and a few extras (file uploads, JWT, password hashing). If a `requirements.txt` is added later, prefer that. For now install the basics:

```cmd
pip install -r requirements-test.txt
pip install fastapi uvicorn sqlalchemy python-multipart passlib[bcrypt] python-jose
```

3. Run the app

```cmd
uvicorn main:app --reload
```

- The app will create the database schema on first run (`Base.metadata.create_all(bind=engine)`) and execute the seed runner (`seed_runner.run()`) during startup (lifespan).
- Uploaded images are stored under the `uploads/` folder which is created automatically by the app.
- Static files are served at `/uploads` (e.g. a poster saved as `uploads/myfile.png` is available at `http://localhost:8000/uploads/myfile.png`).

4. API docs
- Swagger UI: http://localhost:8000/docs
- Redoc: http://localhost:8000/redoc

---

## Running Tests

There are test helpers and pytest configuration in the repo. Use the bundled run scripts or run pytest directly.

```cmd
# bundled helper
run_tests.bat
# or run pytest directly
pytest -q
```

The `requirements-test.txt` file contains pytest, pytest-asyncio and httpx for tests.

---

## Authentication Flow

- POST /auth/register — register a new user (name, username, email, phone_number, password, confirm_password)
  - Returns new user data and 201 status on success.

- POST /auth/login — log in using username and password
  - Returns `access_token`, `token_type` and `user` on success.

- POST /auth/verify-token — verify a JWT token and return user info

Protected endpoints expect an `Authorization` header in the format:

```
Authorization: Bearer <token>
```

A convenience endpoint to fetch the current user's profile is available:
- GET /users/profile/me — extracts Bearer token from header, verifies it, returns full user profile

There is also a helper `get_current_user` in `routes/user.py` which demonstrates the token extraction/verification logic.

---

## Main Routes and Important Endpoints

The project uses FastAPI routers and prefixes as follows (showing the most important endpoints):

- Authentication (`/auth`)
  - POST /auth/register
  - POST /auth/login
  - POST /auth/verify-token

- Users (`/users`)
  - GET /users/ — list all users
  - POST /users/ — create user
  - GET /users/profile/me — get current user from token
  - GET /users/{user_id} — get user by id
  - PUT /users/{user_id} — update user
  - DELETE /users/{user_id} — delete user
  - POST /users/{user_id}/change-password — change password
  - Search helpers: /users/search/username/{username}, /users/search/email/{email}
  - /users/role/{role_id} — list users by role

- Roles (`/roles`)
  - GET /roles/ — list roles
  - POST /roles/ — create role
  - GET /roles/{role_id} — get role
  - PUT /roles/{role_id} — update role
  - DELETE /roles/{role_id} — delete role

- Menu (`/menus`)
  - GET /menus/ — list all menus (with posters)
  - POST /menus/ — create menu (accepts poster paths in payload)
  - GET /menus/{menu_id} — get menu (with posters)
  - PUT /menus/{menu_id} — update menu
  - DELETE /menus/{menu_id} — delete menu and associated poster files
  - Menu posters:
    - GET /menus/posters/all — list all posters
    - GET /menus/posters/{poster_id} — get specific poster
    - GET /menus/{menu_id}/posters — list posters for a menu
    - POST /menus/{menu_id}/posters/upload — upload a poster file (multipart/form-data)
      - This endpoint saves the file to `uploads/` and creates a `MenuPoster` record.
    - POST /menus/posters — create poster record using existing file path (legacy)
    - DELETE /menus/posters/{poster_id} — delete poster and remove file

- Food Packages (`/food-packages`)
  - CRUD endpoints: GET /, GET /{id}, POST /, PUT /{id}, DELETE /{id}
  - Helpers: GET /menu/{menu_id}, GET /session/{session_id}

- Booking Sessions (`/booking-sessions`)
  - CRUD endpoints: GET /, GET /{id}, POST /, PUT /{id}, DELETE /{id}

- Bookings (`/bookings`)
  - GET /bookings/ — list bookings with details (menu & booked foods)
  - GET /bookings/{booking_id} — get booking details
  - POST /bookings/ — create booking (with array of booked_foods)
  - PUT /bookings/{booking_id} — update booking (status, number_of_people, notes)
  - DELETE /bookings/{booking_id} — delete booking
  - GET /bookings/user/{user_id} — get bookings by user
  - GET /bookings/status/{status} — get bookings by status

- Booked Foods (nested under bookings endpoints)
  - GET /bookings/foods/all — list all booked foods
  - GET /bookings/foods/{booked_food_id} — get booked food
  - POST /bookings/foods — create booked food entry
  - PUT /bookings/foods/{booked_food_id} — update booked food (quantity)
  - DELETE /bookings/foods/{booked_food_id} — delete booked food
  - GET /bookings/{booking_id}/foods — list booked foods for a booking

---

## Database & Seeding

- Database engine and session management are in `database.py`.
- Models live under `model/`.
- On application start, `Base.metadata.create_all(bind=engine)` is executed and `seed_runner.run()` is called from the FastAPI lifespan handler to populate demo data.

If you want to re-seed or change seed data, check `seed/` and `seed_runner.py`.

---

## File Uploads

- The app saves uploaded menu poster files to the local `uploads/` directory. The folder is created automatically at startup.
- Files are served at `/uploads` as static files.
- Use `POST /menus/{menu_id}/posters/upload` with a multipart/form-data body and an `file` field.

---

## Development Notes

- The project exposes detailed debug prints in `routes/user.py` for token extraction/verification. Remove or lower logging level for production.
- Ensure JWT secret and hashing configs (if environment-based) are not committed in production.

---

## Troubleshooting

- If static uploads are not visible, ensure `uploads/` exists and the application process has write permission.
- If token verification fails, check the token format (Authorization: Bearer <token>) and ensure the token was issued by the running backend instance.

---

If you want, I can also:
- Generate a minimal `requirements.txt` with precise runtime dependencies based on imports in the repo.
- Add example requests for each endpoint in a `test_main.http` or Postman collection.
- Harden the token helper and add unit tests for authentication flows.
