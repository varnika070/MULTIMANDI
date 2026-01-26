"""
Product and Mandi data models
"""

from sqlalchemy import Column, String, DateTime, Enum, Float, Integer, JSON, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
import uuid
import enum

from app.core.database import Base


class ProductCategory(str, enum.Enum):
    GRAINS = "grains"
    VEGETABLES = "vegetables"
    FRUITS = "fruits"
    PULSES = "pulses"
    SPICES = "spices"
    CASH_CROPS = "cash_crops"


class Unit(str, enum.Enum):
    QUINTAL = "quintal"
    KG = "kg"
    TON = "ton"
    BAG = "bag"


class QualityGrade(str, enum.Enum):
    PREMIUM = "premium"
    GOOD = "good"
    AVERAGE = "average"
    BELOW_AVERAGE = "below_average"


class Product(Base):
    __tablename__ = "products"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    category = Column(Enum(ProductCategory), nullable=False)
    seasonal_availability = Column(JSON, default=list)  # List of months
    standard_units = Column(JSON, default=list)  # List of units
    quality_grades = Column(JSON, default=list)  # List of quality grades
    regional_names = Column(JSON, default=dict)  # Language -> local name mapping
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Product {self.name}>"


class MandiRecord(Base):
    __tablename__ = "mandi_records"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    market_name = Column(String(100), nullable=False)
    state = Column(String(50), nullable=False)
    district = Column(String(50), nullable=False)
    product_name = Column(String(100), nullable=False, index=True)
    variety = Column(String(50), nullable=True)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    modal_price = Column(Float, nullable=False)  # Most common price
    date = Column(Date, nullable=False, index=True)
    arrival_quantity = Column(Float, nullable=False)
    unit = Column(String(20), default="quintal")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<MandiRecord {self.product_name} - {self.market_name}>"


class PriceData(Base):
    __tablename__ = "price_data"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    market_location = Column(String(100), nullable=False)
    price_per_unit = Column(Float, nullable=False)
    unit_type = Column(Enum(Unit), nullable=False)
    quality_grade = Column(Enum(QualityGrade), nullable=False)
    date_recorded = Column(Date, nullable=False, index=True)
    source = Column(String(50), default="mandi")
    confidence_score = Column(Float, default=0.8)
    seasonal_factor = Column(Float, default=1.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<PriceData {self.product_id} - ₹{self.price_per_unit}>"