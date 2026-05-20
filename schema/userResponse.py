from pydantic import BaseModel, EmailStr
from typing import List, Optional

class RoleSchema(BaseModel):
    id: Optional[int] = None
    name: str

    class Config:
        from_attributes = True

class UserSchema(BaseModel):
    id: Optional[int] = None
    name: str
    username: str
    email: str
    phone_number: str
    role_id: int
    role: Optional[RoleSchema] = None

    class Config:
        from_attributes = True

class UserCreateSchema(BaseModel):
    name: str
    username: str
    email: str
    phone_number: str
    password: str
    role_id: int = 3  # Default role is User

class UserUpdateSchema(BaseModel):
    name: Optional[str] = None
    username: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    role_id: Optional[int] = None

class UserChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str

class UserResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[UserSchema] = None

class UserListResponseSchema(BaseModel):
    message: str
    status: int
    data: List[UserSchema]

# Auth schemas
class LoginSchema(BaseModel):
    username: str
    password: str

class LoginResponseSchema(BaseModel):
    message: str
    status: int
    access_token: str
    token_type: str
    user: Optional[UserSchema] = None

class RegisterSchema(BaseModel):
    name: str
    username: str
    email: str
    phone_number: str
    password: str
    confirm_password: str

class RegisterResponseSchema(BaseModel):
    message: str
    status: int
    data: Optional[UserSchema] = None

class TokenSchema(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
    exp: Optional[int] = None

