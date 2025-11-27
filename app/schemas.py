from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    sub: Optional[str] = None


class ContentCreate(BaseModel):
    title: str = Field(max_length=255)
    body: str = Field(min_length=10)


class ContentUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=255)
    body: str | None = Field(default=None, min_length=10)


class ContentOut(BaseModel):
    id: int
    title: str
    body: str
    summary: str | None = None
    sentiment: Optional[Literal["positive", "negative", "neutral"]] = None
    sentiment_score: float | None = None
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

