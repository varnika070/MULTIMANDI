"""
Price discovery and mandi data endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, desc
from typing import List, Optional, Dict
from datetime import date, timedelta

from app.core.database import get_db
from app.models.product import MandiRecord, Product
from app.schemas.product import MandiRecordResponse, PriceSuggestion
from app.data.sample_data import generate_sample_mandi_data, get_current_price_trends, SAMPLE_PRODUCTS
from app.services.price_analysis import price_analysis_service

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
    
    try:
        # Use the advanced price analysis service
        analysis = await price_analysis_service.analyze_price_suggestion(
            product=product_name,
            quantity=quantity,
            quality_grade=quality_grade,
            location=location,
            urgency="normal"
        )
        
        return PriceSuggestion(
            product_name=analysis.product,
            suggested_price=analysis.suggested_price,
            unit="quintal",
            confidence_level=analysis.market_trend.confidence,
            price_range={
                "min": analysis.confidence_band["min"],
                "max": analysis.confidence_band["max"]
            },
            factors=[
                f"Base price: ₹{analysis.current_price}",
                f"Quality grade: {quality_grade}",
                f"Quantity: {quantity} quintals",
                f"Market trend: {analysis.market_trend.direction}",
                f"Risk level: {analysis.risk_assessment['level']}"
            ],
            explanation=analysis.explanation
        )
        
    except ValueError:
        # Fallback to original logic for unknown products
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


@router.get("/explanation/{product}")
async def get_price_explanation(
    product: str,
    target_price: float = Query(..., description="Target price to explain"),
    quantity: float = Query(100, description="Quantity in quintals"),
    quality: str = Query("good", description="Quality grade")
):
    """Get detailed explanation for a specific price point"""
    try:
        analysis = await price_analysis_service.analyze_price_suggestion(
            product=product,
            quantity=quantity,
            quality_grade=quality
        )
        
        # Calculate how the target price compares to our analysis
        price_difference = target_price - analysis.suggested_price
        price_difference_percent = (price_difference / analysis.suggested_price) * 100
        
        # Generate explanation for the target price
        explanation_parts = []
        
        if abs(price_difference_percent) < 5:
            explanation_parts.append(f"The target price of ₹{target_price} is very close to our market analysis.")
        elif price_difference_percent > 5:
            explanation_parts.append(f"The target price of ₹{target_price} is {price_difference_percent:.1f}% above our suggested price.")
            explanation_parts.append("This could be justified by premium quality, urgent delivery, limited supply, or special processing.")
        else:
            explanation_parts.append(f"The target price of ₹{target_price} is {abs(price_difference_percent):.1f}% below our suggested price.")
            explanation_parts.append("This could indicate bulk discount, lower quality, seller urgency, or market oversupply.")
        
        return {
            "product": product,
            "target_price": target_price,
            "market_suggested_price": analysis.suggested_price,
            "price_difference": price_difference,
            "price_difference_percent": price_difference_percent,
            "explanation": " ".join(explanation_parts),
            "market_context": {
                "base_price": analysis.current_price,
                "seasonal_factor": analysis.seasonal_factors["current_multiplier"],
                "market_trend": analysis.market_trend.direction,
                "volatility": analysis.risk_assessment["volatility"]
            },
            "recommendation": _get_price_recommendation(price_difference_percent),
            "confidence_band": analysis.confidence_band
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating explanation: {str(e)}")


@router.get("/trends/{product}")
async def get_price_trends_detailed(product: str):
    """Get detailed price trends and market analysis for a product"""
    try:
        analysis = await price_analysis_service.analyze_price_suggestion(product=product)
        
        return {
            "product": product,
            "current_analysis": {
                "suggested_price": analysis.suggested_price,
                "market_trend": {
                    "direction": analysis.market_trend.direction,
                    "strength": analysis.market_trend.strength,
                    "confidence": analysis.market_trend.confidence
                }
            },
            "seasonal_analysis": analysis.seasonal_factors,
            "risk_factors": analysis.risk_assessment,
            "historical_context": {
                "base_price": analysis.current_price,
                "volatility": analysis.risk_assessment["volatility"],
                "demand_factors": analysis.market_trend.factors
            }
        }
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating trends: {str(e)}")


def _get_price_recommendation(price_difference_percent: float) -> str:
    """Generate recommendation based on price difference"""
    if abs(price_difference_percent) < 3:
        return "Fair price - within normal market range"
    elif price_difference_percent > 10:
        return "High price - negotiate or consider alternatives"
    elif price_difference_percent > 5:
        return "Above market rate - try to negotiate down"
    elif price_difference_percent < -10:
        return "Very low price - verify quality and terms"
    elif price_difference_percent < -5:
        return "Below market rate - good deal if quality is assured"
    else:
        return "Reasonable price - acceptable for trading"