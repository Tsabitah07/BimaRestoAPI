from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from controller import AuthController
from schema.userResponse import (
    LoginSchema, LoginResponseSchema,
    RegisterSchema, RegisterResponseSchema,
    UserSchema
)

router = APIRouter()

@router.post("/login", tags=["Authentication"], response_model=LoginResponseSchema)
def login(payload: LoginSchema, db: Session = Depends(get_db)):
    """Login with username and password"""
    try:
        result = AuthController.login(db, payload.username, payload.password)
        # Convert user model to dict to ensure serialization
        user = result.get("user")
        if hasattr(user, "__table__"):
            user = {c.name: getattr(user, c.name) for c in user.__table__.columns}

        return {
            "message": "Login berhasil",
            "status": 200,
            "access_token": result["access_token"],
            "token_type": result["token_type"],
            "user": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/register", tags=["Authentication"], response_model=RegisterResponseSchema, status_code=201)
def register(payload: RegisterSchema, db: Session = Depends(get_db)):
    """Register new user"""
    try:
        user = AuthController.register(
            db,
            payload.name,
            payload.username,
            payload.email,
            payload.phone_number,
            payload.password,
            payload.confirm_password
        )
        # Serialize user model to dict
        if hasattr(user, "__table__"):
            user = {c.name: getattr(user, c.name) for c in user.__table__.columns}
        return {
            "message": "Registrasi berhasil",
            "status": 201,
            "data": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/verify-token", tags=["Authentication"], response_model=dict)
def verify_token(token: str, db: Session = Depends(get_db)):
    """Verify JWT token and get user info"""
    try:
        user = AuthController.verify_token_and_get_user(db, token)
        # Serialize user model to dict
        if hasattr(user, "__table__"):
            user = {c.name: getattr(user, c.name) for c in user.__table__.columns}
        return {
            "message": "Token valid",
            "status": 200,
            "user": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
