"""
Price discovery and mandi data endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import List, Optional
from datetime import date, timedelta

from app.core.database import get_db
from app.models.product import MandiRecord, Product
from app.schemas.product import MandiRecordResponse, PriceSuggestion
from app.data.sample_data import generate_sample_mandi_data, get_current_price_trends, SAMPLE_PRODUCTS

router = APIRouter()


@router.get("/trends", response_model=dict)
async def get_price_trends():
    """Get current price trends for all products"""
    return get_current_price_trends()


@router.get("/mandi-data", response_model=List[MandiRecordResponse])
async def get_mandi_data(
    product_name: Optional[str] = Query(None, description="Filter by product name"),
    state: Optional[str] = Query(None, description="Filter by state"),
    days: int = Query(7, description="Number of days to look back", ge=1, le=30),
    db: AsyncSession = Depends(get_db)
):
    """Get mandi data with optional filters"""
    
    # For demo purposes, return sample data if no data in DB
    result = await db.execute(select(MandiRecord).limit(1))
    if not result.scalar_one_or_none():
        # Generate and insert sample data
        sample_data = generate_sample_mandi_data(days)
        for record_data in sample_data[:50]:  # Limit for demo
            record = MandiRecord(**record_data)
            db.add(record)
        await db.commit()
    
    # Build query
    query = select(MandiRecord).where(
        MandiRecord.date >= date.today() - timedelta(days=days)
    )
    
    if product_name:
        query = query.where(MandiRecord.product_name.ilike(f"%{product_name}%"))
    
    if state:
        query = query.where(MandiRecord.state.ilike(f"%{state}%"))
    
    query = query.order_by(desc(MandiRecord.date)).limit(100)
    
    result = await db.execute(query)
    records = result.scalars().all()
    
    return records


@router.get("/suggestion/{product_name}", response_model=PriceSuggestion)
async def get_price_suggestion(
    product_name: str,
    quantity: float = Query(1.0, description="Quantity in quintals"),
    location: Optional[str] = Query(None, description="Market location"),
    quality_grade: str = Query("good", description="Quality grade")
):
    """Get AI-powered price suggestion for a product"""
    
    # Find product in sample data
    product_info = None
    for product in SAMPLE_PRODUCTS:
        if product["name"].lower() == product_name.lower():
            product_info = product
            break
    
    if not product_info:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Get current trends
    trends = get_current_price_trends()
    if product_name not in trends:
        raise HTTPException(status_code=404, detail="Price data not available")
    
    trend_data = trends[product_name]
    base_price = trend_data["current_price"]
    
    # Adjust price based on quality grade
    quality_multipliers = {
        "premium": 1.2,
        "good": 1.0,
        "average": 0.85,
        "below_average": 0.7
    }
    
    quality_multiplier = quality_multipliers.get(quality_grade, 1.0)
    suggested_price = base_price * quality_multiplier
    
    # Calculate price range
    price_range = {
        "min": round(suggested_price * 0.9, 2),
        "max": round(suggested_price * 1.1, 2)
    }
    
    # Generate factors and explanation
    factors = [
        f"Current market trend: {trend_data['trend']}",
        f"Quality grade: {quality_grade}",
        "Seasonal availability",
        "Regional demand patterns"
    ]
    
    if location:
        factors.append(f"Location: {location}")
    
    explanation = f"Based on current market data, {product_name} is trading at ₹{suggested_price:.2f} per quintal for {quality_grade} quality. "
    explanation += f"The price trend is {trend_data['trend']} with a confidence level of 85%."
    
    return PriceSuggestion(
        product_name=product_name,
        suggested_price=round(suggested_price, 2),
        unit="quintal",
        confidence_level=0.85,
        price_range=price_range,
        factors=factors,
        explanation=explanation
    )


@router.get("/products", response_model=List[dict])
async def get_available_products():
    """Get list of available products"""
    return [
        {
            "name": product["name"],
            "category": product["category"],
            "regional_names": product["regional_names"]
        }
        for product in SAMPLE_PRODUCTS
    ]


@router.get("/markets", response_model=List[dict])
async def get_available_markets():
    """Get list of available markets"""
    from app.data.sample_data import SAMPLE_MARKETS
    return SAMPLE_MARKETS