import hashlib
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from fastapi import HTTPException
from model.User import User as UserModel
from model.Role import Role as RoleModel
import jwt

# Secret key untuk JWT (seharusnya di environment variable)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production").strip()
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 600

# Create password context for bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def _verify_password(plain: str, hashed: str) -> bool:
    """Verify password against bcrypt hash"""
    return pwd_context.verify(plain, hashed)



def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def _verify_token(token: str) -> dict:
    """Verify JWT token"""
    try:
        print(f"DEBUG: Verifying token with SECRET_KEY: {SECRET_KEY}")
        print(f"DEBUG: Token: {token}")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(f"DEBUG: Token decoded successfully. Payload: {payload}")
        return payload
    except jwt.ExpiredSignatureError as e:
        print(f"DEBUG: Token expired: {e}")
        raise HTTPException(status_code=401, detail="Token telah expired")
    except jwt.InvalidTokenError as e:
        print(f"DEBUG: Invalid token error: {e}")
        raise HTTPException(status_code=401, detail="Token tidak valid")


# User CRUD Operations
def get_all_users(db: Session):
    """Get all users"""
    return db.query(UserModel).all()


def get_user_by_id(db: Session, user_id: int):
    """Get user by ID"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user


def get_user_by_username(db: Session, username: str):
    """Get user by username"""
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user


def get_user_by_email(db: Session, email: str):
    """Get user by email"""
    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")
    return user


def get_users_by_role(db: Session, role_id: int):
    """Get users by role"""
    return db.query(UserModel).filter(UserModel.role_id == role_id).all()


def create_user(db: Session, name: str, username: str, email: str,
                phone_number: str, password: str, role_id: int = 3):
    """Create new user"""
    # Check if username already exists
    if db.query(UserModel).filter(UserModel.username == username).first():
        raise HTTPException(status_code=400, detail="Username sudah digunakan")

    # Check if email already exists
    if db.query(UserModel).filter(UserModel.email == email).first():
        raise HTTPException(status_code=400, detail="Email sudah terdaftar")

    # Verify role exists
    role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role tidak ditemukan")

    # Hash password
    hashed_password = _hash_password(password)

    # Create user
    user = UserModel(
        name=name,
        username=username,
        email=email,
        phone_number=phone_number,
        password=hashed_password,
        role_id=role_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, name: str = None, username: str = None,
                email: str = None, phone_number: str = None, role_id: int = None):
    """Update user"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Check if new username is unique
    if username and username != user.username:
        if db.query(UserModel).filter(UserModel.username == username).first():
            raise HTTPException(status_code=400, detail="Username sudah digunakan")
        user.username = username

    # Check if new email is unique
    if email and email != user.email:
        if db.query(UserModel).filter(UserModel.email == email).first():
            raise HTTPException(status_code=400, detail="Email sudah terdaftar")
        user.email = email

    # Verify role exists if changing role
    if role_id and role_id != user.role_id:
        role = db.query(RoleModel).filter(RoleModel.id == role_id).first()
        if not role:
            raise HTTPException(status_code=404, detail="Role tidak ditemukan")
        user.role_id = role_id

    if name:
        user.name = name
    if phone_number:
        user.phone_number = phone_number

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    """Delete user"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    db.delete(user)
    db.commit()
    return user


# Authentication Operations
def register(db: Session, name: str, username: str, email: str,
             phone_number: str, password: str, confirm_password: str):
    """Register new user"""
    # Validate passwords match
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Password tidak cocok")

    # Validate password length
    if len(password) < 6:
        raise HTTPException(status_code=400, detail="Password harus minimal 6 karakter")

    # Validate required fields
    if not all([name, username, email, phone_number, password]):
        raise HTTPException(status_code=400, detail="Semua field harus diisi")

    # Create user with default role (User = 3)
    user = create_user(db, name, username, email, phone_number, password, role_id=3)
    return user


def login(db: Session, username: str, password: str):
    """Login user"""
    # Find user by username
    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user:
        raise HTTPException(status_code=401, detail="Username atau password salah")

    # Verify password
    if not _verify_password(password, str(user.password)):
        raise HTTPException(status_code=401, detail="Username atau password salah")

    # Create access token with user_id as string (JWT spec requires sub to be string)
    access_token = _create_access_token(data={"sub": str(user.id)})
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


def change_password(db: Session, user_id: int, old_password: str,
                   new_password: str, confirm_password: str):
    """Change user password"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Verify old password
    if not _verify_password(old_password, str(user.password)):
        raise HTTPException(status_code=401, detail="Password lama tidak cocok")

    # Validate new password
    if len(new_password) < 6:
        raise HTTPException(status_code=400, detail="Password baru harus minimal 6 karakter")

    # Check if new passwords match
    if new_password != confirm_password:
        raise HTTPException(status_code=400, detail="Password baru tidak cocok")

    # Check if new password is different from old password
    if new_password == old_password:
        raise HTTPException(status_code=400, detail="Password baru harus berbeda dengan password lama")

    # Hash and update password
    user.password = _hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user


def verify_token_and_get_user(db: Session, token: str):
    """Verify token and get user"""
    payload = _verify_token(token)
    user_id = payload.get("sub")

    if user_id is None:
        raise HTTPException(status_code=401, detail="Token tidak valid")

    # Convert user_id from string to integer
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        raise HTTPException(status_code=401, detail="Token tidak valid")

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="User tidak ditemukan")

    return user
