from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = Field(default=True)


class User(UserBase, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True) 
    email: str = Field(unique=True, index=True)
    name: str = Field(index=True)  # Add name field
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)

    # Relationships - using string annotations to avoid circular import
    tasks: List["Task"] = Relationship(back_populates="user")
    recurrence_patterns: List["RecurrencePattern"] = Relationship(back_populates="user")


class UserCreate(UserBase):
    name: str
    email: str
    password: str


class UserRegister(UserBase):
    name: str
    email: str
    password: str


class UserLogin(SQLModel):
    email: str
    password: str


class UserProfile(UserBase):
    id: UUID
    name: str  # Add name to the profile
    created_at: datetime
    updated_at: datetime