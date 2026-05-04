from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import seed_runner as _seed
from routes import user, authentication

Base.metadata.create_all(bind=engine)

openapi_tags = [
    {"name": "User", "description": "Endpoints terkait pengguna"},
    {"name": "Role", "description": "Endpoints terkait peran pengguna"},
    {"name": "Authentication", "description": "Endpoints terkait autentikasi pengguna"},
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

# app.include_router(authentication.router, prefix="/auth", tags=["Authentication"])
# app.include_router(user.router, prefix="/users", tags=["User"])