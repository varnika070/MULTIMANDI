"""
Product schemas for API requests/responses
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import date, datetime
from app.models.product import ProductCategory, Unit, QualityGrade


class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    category: ProductCategory
    seasonal_availability: List[int] = Field(default_factory=list)
    standard_units: List[str] = Field(default_factory=list)
    quality_grades: List[str] = Field(default_factory=list)
    regional_names: Dict[str, str] = Field(default_factory=dict)


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class MandiRecordBase(BaseModel):
    market_name: str = Field(..., max_length=100)
    state: str = Field(..., max_length=50)
    district: str = Field(..., max_length=50)
    product_name: str = Field(..., max_length=100)
    variety: Optional[str] = Field(None, max_length=50)
    min_price: float = Field(..., gt=0)
    max_price: float = Field(..., gt=0)
    modal_price: float = Field(..., gt=0)
    date: date
    arrival_quantity: float = Field(..., gt=0)
    unit: str = Field(default="quintal", max_length=20)


class MandiRecordCreate(MandiRecordBase):
    pass


class MandiRecordResponse(MandiRecordBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class PriceDataResponse(BaseModel):
    id: str
    product_id: str
    market_location: str
    price_per_unit: float
    unit_type: Unit
    quality_grade: QualityGrade
    date_recorded: date
    confidence_score: float
    seasonal_factor: float

    class Config:
        from_attributes = True


class PriceSuggestion(BaseModel):
    product_name: str
    suggested_price: float
    unit: str
    confidence_level: float
    price_range: Dict[str, float]  # min, max
    factors: List[str]
    explanation: str