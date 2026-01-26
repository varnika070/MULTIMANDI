"""
User model for OpenMandi
"""

from sqlalchemy import Column, String, DateTime, Enum, Float, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class UserType(str, enum.Enum):
    BUYER = "buyer"
    SELLER = "seller"
    BOTH = "both"


class LiteracyLevel(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone_number = Column(String(20), unique=True, index=True, nullable=False)
    preferred_language = Column(String(10), default="en")
    dialect_region = Column(String(50), nullable=True)
    literacy_level = Column(Enum(LiteracyLevel), default=LiteracyLevel.MEDIUM)
    user_type = Column(Enum(UserType), default=UserType.BOTH)
    trust_score = Column(Float, default=5.0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_active = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.phone_number}>"