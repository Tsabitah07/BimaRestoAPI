from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from database import get_db
from controller import UserController, AuthController
from schema.userResponse import (
    UserCreateSchema, UserUpdateSchema,
    UserResponseSchema, UserListResponseSchema,
    UserChangePasswordSchema
)

router = APIRouter()

# Helper function to get current user from token
def get_current_user(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Get current user from authorization header"""
    print(f"DEBUG get_current_user: authorization header = {authorization}")
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")

    try:
        parts = authorization.split()
        print(f"DEBUG: Parts after split = {parts}")
        if len(parts) != 2:
            raise HTTPException(status_code=401, detail=f"Invalid authorization header format. Got: {authorization}")

        scheme, token = parts
        print(f"DEBUG: Scheme = {scheme}, Token = {token[:50]}...")
        if scheme.lower() != "bearer":
            raise HTTPException(status_code=401, detail=f"Invalid authentication scheme: {scheme}")

        print(f"DEBUG: Calling verify_token_and_get_user")
        user = AuthController.verify_token_and_get_user(db, token)
        print(f"DEBUG: User retrieved successfully: {user.id}")
        return user
    except HTTPException as e:
        print(f"DEBUG: HTTPException raised: {e.detail}")
        raise e
    except Exception as e:
        print(f"DEBUG Error in get_current_user: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Invalid token: {str(e)}")


@router.get("/", tags=["User"], response_model=UserListResponseSchema)
def get_all_users(db: Session = Depends(get_db)):
    """Get all users"""
    try:
        users = UserController.get_all_users(db)
        return {
            "message": "Users retrieved successfully",
            "status": 200,
            "data": users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/profile/me", tags=["User"], response_model=UserResponseSchema)
def get_current_user_profile(authorization: str = Header(None), db: Session = Depends(get_db)):
    """Get current user profile from token

    Special logic:
    1. Extract token from Authorization header (format: Bearer <token>)
    2. Verify token and extract user ID from payload
    3. Fetch fresh user data from database
    4. Return user profile with complete information
    """
    try:
        # Validate authorization header is provided
        if not authorization:
            raise HTTPException(status_code=401, detail="Authorization header missing")

        print(f"DEBUG: /profile/me - Extracting token from header")

        # Extract and validate Bearer token format
        parts = authorization.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            raise HTTPException(status_code=401, detail="Invalid authorization header format. Use: Bearer <token>")

        token = parts[1]
        print(f"DEBUG: /profile/me - Token extracted: {token[:20]}...")

        # Verify token and get user from database
        print(f"DEBUG: /profile/me - Verifying token and fetching user data")
        user = AuthController.verify_token_and_get_user(db, token)

        if not user:
            raise HTTPException(status_code=401, detail="User not found or token invalid")

        print(f"DEBUG: /profile/me - User {user.id} retrieved from database successfully")

        return {
            "message": "Current user profile retrieved successfully",
            "status": 200,
            "data": user
        }
    except HTTPException as e:
        print(f"DEBUG: /profile/me - HTTPException: {e.detail}")
        raise e
    except Exception as e:
        print(f"DEBUG: /profile/me - Error: {str(e)}")
        raise HTTPException(status_code=401, detail=f"Failed to retrieve user profile: {str(e)}")


@router.get("/{user_id}", tags=["User"], response_model=UserResponseSchema)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get specific user by ID"""
    try:
        user = UserController.get_user_by_id(db, user_id)
        return {
            "message": "User retrieved successfully",
            "status": 200,
            "data": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/", tags=["User"], response_model=UserResponseSchema)
def create_user(payload: UserCreateSchema, db: Session = Depends(get_db)):
    """Create new user"""
    try:
        user = UserController.create_user(
            db,
            payload.name,
            payload.username,
            payload.email,
            payload.phone_number,
            payload.password,
            payload.role_id
        )
        return {
            "message": "User created successfully",
            "status": 201,
            "data": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", tags=["User"], response_model=UserResponseSchema)
def update_user(user_id: int, payload: UserUpdateSchema, db: Session = Depends(get_db)):
    """Update user"""
    try:
        user = UserController.update_user(
            db,
            user_id,
            payload.name,
            payload.username,
            payload.email,
            payload.phone_number,
            payload.role_id
        )
        return {
            "message": "User updated successfully",
            "status": 200,
            "data": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", tags=["User"], response_model=UserResponseSchema)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Delete user"""
    try:
        user = UserController.delete_user(db, user_id)
        return {
            "message": "User deleted successfully",
            "status": 200,
            "data": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/username/{username}", tags=["User"], response_model=UserResponseSchema)
def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Get user by username"""
    try:
        user = UserController.get_user_by_username(db, username)
        return {
            "message": "User retrieved successfully",
            "status": 200,
            "data": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search/email/{email}", tags=["User"], response_model=UserResponseSchema)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    """Get user by email"""
    try:
        user = UserController.get_user_by_email(db, email)
        return {
            "message": "User retrieved successfully",
            "status": 200,
            "data": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/role/{role_id}", tags=["User"], response_model=UserListResponseSchema)
def get_users_by_role(role_id: int, db: Session = Depends(get_db)):
    """Get users by role"""
    try:
        users = UserController.get_users_by_role(db, role_id)
        return {
            "message": "Users retrieved successfully",
            "status": 200,
            "data": users
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{user_id}/change-password", tags=["User"], response_model=dict)
def change_password(user_id: int, payload: UserChangePasswordSchema, db: Session = Depends(get_db)):
    """Change user password"""
    try:
        user = UserController.change_password(
            db,
            user_id,
            payload.old_password,
            payload.new_password,
            payload.confirm_password
        )
        return {
            "message": "Password changed successfully",
            "status": 200,
            "data": user
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
