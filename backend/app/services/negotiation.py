"""
AI Negotiation Assistant Service
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class NegotiationOffer:
    def __init__(
        self,
        offer_id: str,
        session_id: str,
        user_id: str,
        product: str,
        quantity: float,
        unit: str,
        price_per_unit: float,
        total_price: float,
        offer_type: str = "buy",  # "buy" or "sell"
        timestamp: Optional[datetime] = None
    ):
        self.offer_id = offer_id
        self.session_id = session_id
        self.user_id = user_id
        self.product = product
        self.quantity = quantity
        self.unit = unit
        self.price_per_unit = price_per_unit
        self.total_price = total_price
        self.offer_type = offer_type
        self.timestamp = timestamp or datetime.utcnow()
    
    def to_dict(self) -> Dict:
        return {
            "offer_id": self.offer_id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "product": self.product,
            "quantity": self.quantity,
            "unit": self.unit,
            "price_per_unit": self.price_per_unit,
            "total_price": self.total_price,
            "offer_type": self.offer_type,
            "timestamp": self.timestamp.isoformat()
        }


class NegotiationAnalysis:
    def __init__(
        self,
        fairness_score: float,
        market_comparison: Dict,
        suggested_counter: Optional[Dict] = None,
        reasoning: List[str] = None,
        risk_factors: List[str] = None
    ):
        self.fairness_score = fairness_score
        self.market_comparison = market_comparison
        self.suggested_counter = suggested_counter
        self.reasoning = reasoning or []
        self.risk_factors = risk_factors or []
    
    def to_dict(self) -> Dict:
        return {
            "fairness_score": self.fairness_score,
            "market_comparison": self.market_comparison,
            "suggested_counter": self.suggested_counter,
            "reasoning": self.reasoning,
            "risk_factors": self.risk_factors
        }


class NegotiationService:
    """AI-powered negotiation assistance service"""
    
    def __init__(self):
        # Market price data (in production, this would come from real market APIs)
        self.market_prices = {
            "rice": {"base_price": 2500, "range": (2200, 2800), "unit": "quintal"},
            "wheat": {"base_price": 2200, "range": (2000, 2400), "unit": "quintal"},
            "onion": {"base_price": 3000, "range": (2500, 3500), "unit": "quintal"},
            "potato": {"base_price": 1800, "range": (1500, 2100), "unit": "quintal"},
            "tomato": {"base_price": 4000, "range": (3200, 4800), "unit": "quintal"},
            "cotton": {"base_price": 5500, "range": (5000, 6000), "unit": "quintal"},
            "sugarcane": {"base_price": 350, "range": (320, 380), "unit": "quintal"},
            "turmeric": {"base_price": 8000, "range": (7200, 8800), "unit": "quintal"}
        }
    
    async def analyze_offer(self, offer: NegotiationOffer) -> NegotiationAnalysis:
        """Analyze an offer and provide negotiation guidance"""
        
        # Get market data for the product
        market_data = self.market_prices.get(offer.product.lower())
        if not market_data:
            # Default analysis for unknown products
            return NegotiationAnalysis(
                fairness_score=0.5,
                market_comparison={"status": "unknown_product"},
                reasoning=["Product not found in market database"],
                risk_factors=["Unknown market conditions"]
            )
        
        # Calculate fairness score
        base_price = market_data["base_price"]
        price_range = market_data["range"]
        offered_price = offer.price_per_unit
        
        # Fairness score: 1.0 = perfectly fair, 0.0 = very unfair
        if price_range[0] <= offered_price <= price_range[1]:
            # Price is within market range
            fairness_score = 0.7 + 0.3 * (1 - abs(offered_price - base_price) / (price_range[1] - price_range[0]))
        elif offered_price < price_range[0]:
            # Price is below market range
            fairness_score = max(0.1, 0.5 * (offered_price / price_range[0]))
        else:
            # Price is above market range
            fairness_score = max(0.1, 0.5 * (price_range[1] / offered_price))
        
        # Market comparison
        market_comparison = {
            "market_price": base_price,
            "market_range": price_range,
            "offered_price": offered_price,
            "price_difference": offered_price - base_price,
            "price_difference_percent": ((offered_price - base_price) / base_price) * 100
        }
        
        # Generate reasoning
        reasoning = []
        if offered_price < price_range[0]:
            reasoning.append(f"Offered price (₹{offered_price}) is {price_range[0] - offered_price:.0f} below market minimum")
            reasoning.append("This is significantly below fair market value")
        elif offered_price > price_range[1]:
            reasoning.append(f"Offered price (₹{offered_price}) is {offered_price - price_range[1]:.0f} above market maximum")
            reasoning.append("This is significantly above fair market value")
        else:
            reasoning.append(f"Offered price (₹{offered_price}) is within market range")
            if abs(offered_price - base_price) < 100:
                reasoning.append("Price is very close to market average")
            elif offered_price > base_price:
                reasoning.append("Price is above market average but reasonable")
            else:
                reasoning.append("Price is below market average but acceptable")
        
        # Generate counter-offer suggestion
        suggested_counter = None
        if fairness_score < 0.6:
            if offer.offer_type == "buy" and offered_price < base_price:
                # Buyer offering too low, suggest higher price
                suggested_price = min(base_price, offered_price * 1.15)
                suggested_counter = {
                    "price_per_unit": suggested_price,
                    "total_price": suggested_price * offer.quantity,
                    "reasoning": f"Counter with ₹{suggested_price:.0f} per {offer.unit} (closer to market rate)"
                }
            elif offer.offer_type == "sell" and offered_price > base_price:
                # Seller asking too high, suggest lower price
                suggested_price = max(base_price, offered_price * 0.9)
                suggested_counter = {
                    "price_per_unit": suggested_price,
                    "total_price": suggested_price * offer.quantity,
                    "reasoning": f"Counter with ₹{suggested_price:.0f} per {offer.unit} (more competitive rate)"
                }
        
        # Risk factors
        risk_factors = []
        if fairness_score < 0.4:
            risk_factors.append("Significant price deviation from market rates")
        if offer.quantity > 100:  # Large quantity
            risk_factors.append("Large quantity transaction - verify logistics capacity")
        if offered_price < price_range[0] * 0.8:
            risk_factors.append("Extremely low price - potential quality concerns")
        if offered_price > price_range[1] * 1.2:
            risk_factors.append("Extremely high price - verify product quality justification")
        
        return NegotiationAnalysis(
            fairness_score=fairness_score,
            market_comparison=market_comparison,
            suggested_counter=suggested_counter,
            reasoning=reasoning,
            risk_factors=risk_factors
        )
    
    async def generate_negotiation_advice(
        self, 
        user_role: str,  # "buyer" or "seller"
        product: str,
        current_offer: float,
        target_price: Optional[float] = None
    ) -> Dict[str, Any]:
        """Generate negotiation strategy advice"""
        
        market_data = self.market_prices.get(product.lower())
        if not market_data:
            return {
                "advice": "Product not found in market database. Research current market rates before negotiating.",
                "strategy": "information_gathering"
            }
        
        base_price = market_data["base_price"]
        price_range = market_data["range"]
        
        advice = []
        strategy = "balanced"
        
        if user_role == "buyer":
            if current_offer > price_range[1]:
                advice.append("The current offer is above market maximum. You have strong negotiating position.")
                advice.append(f"Consider countering with ₹{base_price} per quintal (market average).")
                strategy = "aggressive"
            elif current_offer > base_price:
                advice.append("The offer is above market average but reasonable.")
                advice.append("You can try to negotiate down slightly, but don't push too hard.")
                strategy = "moderate"
            else:
                advice.append("This is a fair or good price for you as a buyer.")
                advice.append("Consider accepting or making a small counter-offer.")
                strategy = "conservative"
        
        else:  # seller
            if current_offer < price_range[0]:
                advice.append("The current offer is below market minimum. Don't accept this.")
                advice.append(f"Counter with at least ₹{price_range[0]} per quintal.")
                strategy = "aggressive"
            elif current_offer < base_price:
                advice.append("The offer is below market average.")
                advice.append("You should negotiate for a higher price.")
                strategy = "moderate"
            else:
                advice.append("This is a good price for you as a seller.")
                advice.append("Consider accepting or asking for a small premium.")
                strategy = "conservative"
        
        # Add general negotiation tips
        general_tips = [
            "Be polite and respectful throughout the negotiation",
            "Highlight the quality and benefits of the product",
            "Be prepared to walk away if the deal isn't fair",
            "Consider non-price factors like payment terms and delivery"
        ]
        
        return {
            "advice": advice,
            "strategy": strategy,
            "general_tips": general_tips,
            "market_context": {
                "base_price": base_price,
                "price_range": price_range,
                "current_offer": current_offer
            }
        }
    
    async def evaluate_deal_completion(
        self,
        final_price: float,
        product: str,
        quantity: float,
        buyer_id: str,
        seller_id: str
    ) -> Dict[str, Any]:
        """Evaluate a completed deal and provide summary"""
        
        market_data = self.market_prices.get(product.lower())
        if not market_data:
            return {"status": "unknown_product"}
        
        base_price = market_data["base_price"]
        price_range = market_data["range"]
        
        # Calculate deal metrics
        price_vs_market = ((final_price - base_price) / base_price) * 100
        total_value = final_price * quantity
        
        # Determine deal quality
        if price_range[0] <= final_price <= price_range[1]:
            deal_quality = "fair"
        elif final_price < price_range[0]:
            deal_quality = "buyer_favored"
        else:
            deal_quality = "seller_favored"
        
        # Generate summary
        summary = {
            "deal_id": f"deal_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
            "product": product,
            "quantity": quantity,
            "unit": market_data["unit"],
            "final_price": final_price,
            "total_value": total_value,
            "market_price": base_price,
            "price_vs_market_percent": price_vs_market,
            "deal_quality": deal_quality,
            "buyer_id": buyer_id,
            "seller_id": seller_id,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        return summary


# Global negotiation service instance
negotiation_service = NegotiationService()