from sqlalchemy.orm import Session
from model.User import User as UserModel
from model.Role import Role as RoleModel
from fastapi import HTTPException
from controller import AuthController

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
    hashed_password = AuthController._hash_password(password)

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


def change_password(db: Session, user_id: int, old_password: str,
                   new_password: str, confirm_password: str):
    """Change user password"""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User tidak ditemukan")

    # Verify old password
    if not AuthController._verify_password(old_password, user.password):
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
    user.password = AuthController._hash_password(new_password)
    db.commit()
    db.refresh(user)
    return user

