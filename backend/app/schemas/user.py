"""
User schemas for API requests/responses
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserType, LiteracyLevel


class UserBase(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=20)
    preferred_language: str = Field(default="en", max_length=10)
    dialect_region: Optional[str] = Field(None, max_length=50)
    literacy_level: LiteracyLevel = LiteracyLevel.MEDIUM
    user_type: UserType = UserType.BOTH


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    preferred_language: Optional[str] = None
    dialect_region: Optional[str] = None
    literacy_level: Optional[LiteracyLevel] = None
    user_type: Optional[UserType] = None


class UserResponse(UserBase):
    id: str
    trust_score: float
    is_active: bool
    created_at: datetime
    last_active: datetime

    class Config:
        from_attributes = True