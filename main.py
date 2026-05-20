from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
import seed_runner as _seed
from routes import user, authentication, role, booking, menu, foodPackage, bookingSession
import os
from pathlib import Path

Base.metadata.create_all(bind=engine)

# Create uploads folder if it doesn't exist
uploads_folder = Path("uploads")
uploads_folder.mkdir(exist_ok=True)

openapi_tags = [
    {"name": "User", "description": "Endpoints terkait pengguna"},
    {"name": "Role", "description": "Endpoints terkait peran pengguna"},
    {"name": "Authentication", "description": "Endpoints terkait autentikasi pengguna"},
    {"name": "Menu", "description": "Endpoints terkait menu restoran"},
    {"name": "Food Package", "description": "Endpoints terkait paket makanan"},
    {"name": "Booking Session", "description": "Endpoints terkait sesi pemesanan"},
    {"name": "Booking", "description": "Endpoints terkait pemesanan meja"},
    {"name": "Booking Status", "description": "Endpoints terkait status pemesanan meja"},
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        _seed.run()
        yield
    finally:
        pass
app = FastAPI(openapi_tags=openapi_tags, lifespan=lifespan)

origins = [
    "http://localhost",
    "http://localhost:8000",
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded images
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(authentication.router, prefix="/auth", tags=["Authentication"])
app.include_router(user.router, prefix="/users", tags=["User"])
app.include_router(role.router, prefix="/roles", tags=["Role"])
app.include_router(bookingSession.router, prefix="/booking-sessions", tags=["Booking Session"])
app.include_router(menu.router, prefix="/menus", tags=["Menu"])
app.include_router(foodPackage.router, prefix="/food-packages", tags=["Food Package"])
app.include_router(booking.router, prefix="/bookings", tags=["Booking"])
