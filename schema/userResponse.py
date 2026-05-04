# from pydantic import BaseModel
# from typing import List
#
# class UserResponse(BaseModel):
#     message: str
#     id: int
#     username: str
#     email: str
#
#     class Config:
#         orm_mode = True
#
# class UserListResponse(BaseModel):
#     message: str
#     status: int
#     data: List[UserResponse]
#
#     class Config:
#         orm_mode = True
#
# class ResponseUserCreate(BaseModel):
#     username: str
#     email: str
#     password: str
#
#     class Config:
#         orm_mode = True
#
# class ResponseUserUpdate(BaseModel):
#     username: str
#     email: str
#     password: str
#
#     class Config:
#         orm_mode = True
