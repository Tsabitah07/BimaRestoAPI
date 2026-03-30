from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base, SessionLocal
import seed_runner as _seed

from model.User import User
from model.Role import Role

Base.metadata.create_all(bind=engine)

openapi_tags = [
    {"name": "User", "description": "Endpoints terkait pengguna"},
    {"name": "Role", "description": "Endpoints terkait peran pengguna"},
    {"name": "Authentication", "description": "Endpoints terkait autentikasi pengguna"},
    {"name": "Table", "description": "Endpoints terkait meja restoran"},
    {"name": "Menu", "description": "Endpoints terkait menu restoran"},
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