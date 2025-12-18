from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from .user import UserProfile


class Token(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str


class TokenData(BaseModel):
    user_id: UUID
    email: str
    exp: Optional[int] = None


class AuthResponse(BaseModel):
    access_token: str
    token_type: str
    refresh_token: str
    user: UserProfile


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    token_type: str