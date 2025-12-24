from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    name: str
    email: str
    password: str


class UserRegister(UserBase):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserProfile(UserBase):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True


class UserResponse(UserBase):
    id: UUID
    name: str
    created_at: datetime
    updated_at: datetime
    is_active: bool = True