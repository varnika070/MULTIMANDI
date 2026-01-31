"""
AI Negotiation Assistant endpoints
"""

from fastapi import APIRouter, HTTPException, Form
from typing import Optional
from app.services.negotiation import negotiation_service, NegotiationOffer
import uuid

router = APIRouter()


@router.post("/analyze-offer")
async def analyze_offer(
    session_id: str = Form(...),
    user_id: str = Form(...),
    product: str = Form(...),
    quantity: float = Form(...),
    unit: str = Form("quintal"),
    price_per_unit: float = Form(...),
    offer_type: str = Form("buy")  # "buy" or "sell"
):
    """Analyze a negotiation offer and provide AI guidance"""
    
    if offer_type not in ["buy", "sell"]:
        raise HTTPException(status_code=400, detail="offer_type must be 'buy' or 'sell'")
    
    if quantity <= 0 or price_per_unit <= 0:
        raise HTTPException(status_code=400, detail="Quantity and price must be positive")
    
    # Create offer object
    offer = NegotiationOffer(
        offer_id=str(uuid.uuid4()),
        session_id=session_id,
        user_id=user_id,
        product=product,
        quantity=quantity,
        unit=unit,
        price_per_unit=price_per_unit,
        total_price=price_per_unit * quantity,
        offer_type=offer_type
    )
    
    # Analyze the offer
    analysis = await negotiation_service.analyze_offer(offer)
    
    return {
        "offer": offer.to_dict(),
        "analysis": analysis.to_dict(),
        "recommendation": get_recommendation_text(analysis, offer_type)
    }


@router.post("/negotiation-advice")
async def get_negotiation_advice(
    user_role: str = Form(...),  # "buyer" or "seller"
    product: str = Form(...),
    current_offer: float = Form(...),
    target_price: Optional[float] = Form(None)
):
    """Get AI negotiation strategy advice"""
    
    if user_role not in ["buyer", "seller"]:
        raise HTTPException(status_code=400, detail="user_role must be 'buyer' or 'seller'")
    
    if current_offer <= 0:
        raise HTTPException(status_code=400, detail="Current offer must be positive")
    
    advice = await negotiation_service.generate_negotiation_advice(
        user_role=user_role,
        product=product,
        current_offer=current_offer,
        target_price=target_price
    )
    
    return advice


@router.post("/evaluate-deal")
async def evaluate_deal(
    product: str = Form(...),
    quantity: float = Form(...),
    final_price: float = Form(...),
    buyer_id: str = Form(...),
    seller_id: str = Form(...)
):
    """Evaluate a completed deal and provide summary"""
    
    if quantity <= 0 or final_price <= 0:
        raise HTTPException(status_code=400, detail="Quantity and price must be positive")
    
    evaluation = await negotiation_service.evaluate_deal_completion(
        final_price=final_price,
        product=product,
        quantity=quantity,
        buyer_id=buyer_id,
        seller_id=seller_id
    )
    
    return evaluation


@router.get("/market-insights/{product}")
async def get_market_insights(product: str):
    """Get market insights for a specific product"""
    
    market_data = negotiation_service.market_prices.get(product.lower())
    if not market_data:
        raise HTTPException(status_code=404, detail="Product not found in market database")
    
    return {
        "product": product,
        "market_data": market_data,
        "insights": {
            "volatility": "moderate",  # Could be calculated from historical data
            "seasonal_trend": "stable",
            "demand_level": "high",
            "supply_status": "adequate"
        },
        "trading_tips": [
            f"Current market range: ₹{market_data['range'][0]} - ₹{market_data['range'][1]} per {market_data['unit']}",
            f"Average price: ₹{market_data['base_price']} per {market_data['unit']}",
            "Consider quality factors when negotiating price",
            "Payment terms can be as important as price"
        ]
    }


def get_recommendation_text(analysis, offer_type: str) -> str:
    """Generate human-readable recommendation text"""
    
    fairness_score = analysis.fairness_score
    
    if fairness_score >= 0.8:
        if offer_type == "buy":
            return "This is an excellent offer for you as a buyer. Consider accepting it."
        else:
            return "This is a great price for you as a seller. You should accept this offer."
    
    elif fairness_score >= 0.6:
        if offer_type == "buy":
            return "This is a reasonable offer. You might try to negotiate slightly lower, but it's acceptable."
        else:
            return "This is a fair offer. You could try to get a bit more, but it's within market range."
    
    elif fairness_score >= 0.4:
        if offer_type == "buy":
            return "The price is higher than ideal. Try to negotiate down to market average."
        else:
            return "The price is lower than you should accept. Negotiate for a higher price."
    
    else:
        if offer_type == "buy":
            return "This offer is significantly overpriced. Make a strong counter-offer closer to market rates."
        else:
            return "This offer is too low. Don't accept it - counter with a much higher price."