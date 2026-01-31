"""
Advanced Price Analysis Service with Market Intelligence
"""

import asyncio
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import math

class MarketTrend:
    def __init__(self, direction: str, strength: float, confidence: float, factors: List[str]):
        self.direction = direction  # "up", "down", "stable"
        self.strength = strength    # 0.0 to 1.0
        self.confidence = confidence # 0.0 to 1.0
        self.factors = factors

class PriceAnalysis:
    def __init__(
        self,
        product: str,
        current_price: float,
        suggested_price: float,
        confidence_band: Dict[str, float],
        market_trend: MarketTrend,
        seasonal_factors: Dict[str, Any],
        quality_adjustments: Dict[str, float],
        explanation: str,
        risk_assessment: Dict[str, Any]
    ):
        self.product = product
        self.current_price = current_price
        self.suggested_price = suggested_price
        self.confidence_band = confidence_band
        self.market_trend = market_trend
        self.seasonal_factors = seasonal_factors
        self.quality_adjustments = quality_adjustments
        self.explanation = explanation
        self.risk_assessment = risk_assessment

class PriceAnalysisService:
    """Advanced price analysis with market intelligence"""
    
    def __init__(self):
        # Enhanced market data with seasonal and quality factors
        self.market_data = {
            "rice": {
                "base_price": 2500,
                "seasonal_multipliers": {
                    "jan": 1.05, "feb": 1.03, "mar": 1.0, "apr": 0.98,
                    "may": 0.95, "jun": 0.93, "jul": 0.95, "aug": 0.98,
                    "sep": 1.02, "oct": 1.08, "nov": 1.12, "dec": 1.10
                },
                "quality_grades": {
                    "premium": 1.25, "good": 1.0, "standard": 0.85, "low": 0.70
                },
                "volatility": 0.15,
                "demand_elasticity": -0.8
            },
            "wheat": {
                "base_price": 2200,
                "seasonal_multipliers": {
                    "jan": 1.08, "feb": 1.10, "mar": 1.05, "apr": 1.0,
                    "may": 0.95, "jun": 0.90, "jul": 0.92, "aug": 0.95,
                    "sep": 1.0, "oct": 1.05, "nov": 1.08, "dec": 1.10
                },
                "quality_grades": {
                    "premium": 1.20, "good": 1.0, "standard": 0.88, "low": 0.75
                },
                "volatility": 0.12,
                "demand_elasticity": -0.6
            },
            "onion": {
                "base_price": 3000,
                "seasonal_multipliers": {
                    "jan": 1.20, "feb": 1.25, "mar": 1.15, "apr": 1.0,
                    "may": 0.85, "jun": 0.80, "jul": 0.75, "aug": 0.80,
                    "sep": 0.90, "oct": 1.05, "nov": 1.15, "dec": 1.18
                },
                "quality_grades": {
                    "premium": 1.30, "good": 1.0, "standard": 0.80, "low": 0.60
                },
                "volatility": 0.35,
                "demand_elasticity": -1.2
            },
            "potato": {
                "base_price": 1800,
                "seasonal_multipliers": {
                    "jan": 1.15, "feb": 1.20, "mar": 1.10, "apr": 1.0,
                    "may": 0.90, "jun": 0.85, "jul": 0.80, "aug": 0.85,
                    "sep": 0.95, "oct": 1.05, "nov": 1.10, "dec": 1.12
                },
                "quality_grades": {
                    "premium": 1.25, "good": 1.0, "standard": 0.85, "low": 0.70
                },
                "volatility": 0.25,
                "demand_elasticity": -1.0
            },
            "tomato": {
                "base_price": 4000,
                "seasonal_multipliers": {
                    "jan": 1.30, "feb": 1.35, "mar": 1.20, "apr": 1.0,
                    "may": 0.80, "jun": 0.70, "jul": 0.65, "aug": 0.70,
                    "sep": 0.85, "oct": 1.10, "nov": 1.25, "dec": 1.28
                },
                "quality_grades": {
                    "premium": 1.40, "good": 1.0, "standard": 0.75, "low": 0.50
                },
                "volatility": 0.45,
                "demand_elasticity": -1.5
            },
            "cotton": {
                "base_price": 5500,
                "seasonal_multipliers": {
                    "jan": 1.05, "feb": 1.03, "mar": 1.0, "apr": 0.98,
                    "may": 0.95, "jun": 0.93, "jul": 0.95, "aug": 0.98,
                    "sep": 1.02, "oct": 1.08, "nov": 1.10, "dec": 1.08
                },
                "quality_grades": {
                    "premium": 1.35, "good": 1.0, "standard": 0.80, "low": 0.65
                },
                "volatility": 0.20,
                "demand_elasticity": -0.7
            }
        }
    
    async def analyze_price_suggestion(
        self,
        product: str,
        quantity: float = 100,
        quality_grade: str = "good",
        location: Optional[str] = None,
        urgency: str = "normal"
    ) -> PriceAnalysis:
        """Generate comprehensive price analysis with market intelligence"""
        
        product_lower = product.lower()
        if product_lower not in self.market_data:
            raise ValueError(f"Product {product} not found in market database")
        
        market_info = self.market_data[product_lower]
        base_price = market_info["base_price"]
        
        # Calculate seasonal adjustment
        current_month = datetime.now().strftime("%b").lower()
        seasonal_multiplier = market_info["seasonal_multipliers"].get(current_month, 1.0)
        
        # Calculate quality adjustment
        quality_multiplier = market_info["quality_grades"].get(quality_grade.lower(), 1.0)
        
        # Calculate quantity adjustment (bulk discount/premium)
        quantity_multiplier = self._calculate_quantity_adjustment(quantity)
        
        # Calculate urgency adjustment
        urgency_multiplier = self._calculate_urgency_adjustment(urgency)
        
        # Calculate location adjustment (mock implementation)
        location_multiplier = self._calculate_location_adjustment(location)
        
        # Calculate suggested price
        suggested_price = (
            base_price * 
            seasonal_multiplier * 
            quality_multiplier * 
            quantity_multiplier * 
            urgency_multiplier * 
            location_multiplier
        )
        
        # Calculate confidence bands
        volatility = market_info["volatility"]
        confidence_band = {
            "min": suggested_price * (1 - volatility),
            "max": suggested_price * (1 + volatility),
            "conservative": suggested_price * (1 - volatility * 0.5),
            "aggressive": suggested_price * (1 + volatility * 0.5)
        }
        
        # Analyze market trend
        market_trend = self._analyze_market_trend(product_lower, seasonal_multiplier)
        
        # Calculate seasonal factors
        seasonal_factors = self._calculate_seasonal_factors(product_lower, current_month)
        
        # Calculate quality adjustments
        quality_adjustments = {
            "base_adjustment": quality_multiplier - 1.0,
            "grade": quality_grade,
            "impact_percent": (quality_multiplier - 1.0) * 100
        }
        
        # Generate explanation
        explanation = self._generate_price_explanation(
            product, suggested_price, base_price, seasonal_multiplier,
            quality_multiplier, quantity_multiplier, market_trend
        )
        
        # Risk assessment
        risk_assessment = self._assess_price_risks(
            product_lower, suggested_price, volatility, market_trend
        )
        
        return PriceAnalysis(
            product=product,
            current_price=base_price,
            suggested_price=round(suggested_price, 2),
            confidence_band={k: round(v, 2) for k, v in confidence_band.items()},
            market_trend=market_trend,
            seasonal_factors=seasonal_factors,
            quality_adjustments=quality_adjustments,
            explanation=explanation,
            risk_assessment=risk_assessment
        )
    
    def _calculate_quantity_adjustment(self, quantity: float) -> float:
        """Calculate price adjustment based on quantity (bulk discounts)"""
        if quantity >= 1000:
            return 0.95  # 5% bulk discount
        elif quantity >= 500:
            return 0.97  # 3% bulk discount
        elif quantity >= 100:
            return 0.99  # 1% bulk discount
        elif quantity < 10:
            return 1.05  # 5% small quantity premium
        else:
            return 1.0
    
    def _calculate_urgency_adjustment(self, urgency: str) -> float:
        """Calculate price adjustment based on urgency"""
        urgency_multipliers = {
            "urgent": 1.08,    # 8% premium for urgent delivery
            "normal": 1.0,     # No adjustment
            "flexible": 0.95   # 5% discount for flexible timing
        }
        return urgency_multipliers.get(urgency.lower(), 1.0)
    
    def _calculate_location_adjustment(self, location: Optional[str]) -> float:
        """Calculate price adjustment based on location (mock implementation)"""
        if not location:
            return 1.0
        
        # Mock location adjustments (in reality, this would use real geographic data)
        location_adjustments = {
            "mumbai": 1.10,    # Higher prices in metro cities
            "delhi": 1.08,
            "bangalore": 1.06,
            "pune": 1.04,
            "rural": 0.92,     # Lower prices in rural areas
            "remote": 0.88
        }
        
        return location_adjustments.get(location.lower(), 1.0)
    
    def _analyze_market_trend(self, product: str, seasonal_multiplier: float) -> MarketTrend:
        """Analyze current market trend for the product"""
        
        # Mock trend analysis (in reality, this would use historical data)
        if seasonal_multiplier > 1.1:
            direction = "up"
            strength = min((seasonal_multiplier - 1.0) * 2, 1.0)
            factors = ["Seasonal demand increase", "Supply constraints", "Festival season"]
        elif seasonal_multiplier < 0.9:
            direction = "down"
            strength = min((1.0 - seasonal_multiplier) * 2, 1.0)
            factors = ["Harvest season", "Increased supply", "Lower demand"]
        else:
            direction = "stable"
            strength = 0.3
            factors = ["Balanced supply-demand", "Normal market conditions"]
        
        confidence = 0.75 + (strength * 0.2)  # Higher confidence for stronger trends
        
        return MarketTrend(direction, strength, confidence, factors)
    
    def _calculate_seasonal_factors(self, product: str, current_month: str) -> Dict[str, Any]:
        """Calculate detailed seasonal factors"""
        
        market_info = self.market_data[product]
        seasonal_data = market_info["seasonal_multipliers"]
        
        # Find peak and low seasons
        peak_month = max(seasonal_data, key=seasonal_data.get)
        low_month = min(seasonal_data, key=seasonal_data.get)
        
        current_multiplier = seasonal_data.get(current_month, 1.0)
        
        return {
            "current_month": current_month,
            "current_multiplier": current_multiplier,
            "peak_season": {
                "month": peak_month,
                "multiplier": seasonal_data[peak_month],
                "price_increase": (seasonal_data[peak_month] - 1.0) * 100
            },
            "low_season": {
                "month": low_month,
                "multiplier": seasonal_data[low_month],
                "price_decrease": (1.0 - seasonal_data[low_month]) * 100
            },
            "seasonal_volatility": max(seasonal_data.values()) - min(seasonal_data.values())
        }
    
    def _generate_price_explanation(
        self,
        product: str,
        suggested_price: float,
        base_price: float,
        seasonal_multiplier: float,
        quality_multiplier: float,
        quantity_multiplier: float,
        market_trend: MarketTrend
    ) -> str:
        """Generate human-readable price explanation"""
        
        explanations = []
        
        # Base price explanation
        explanations.append(f"Base market price for {product}: ₹{base_price:.0f} per quintal")
        
        # Seasonal adjustment
        if seasonal_multiplier > 1.05:
            explanations.append(f"Seasonal premium: +{(seasonal_multiplier-1)*100:.1f}% (high demand period)")
        elif seasonal_multiplier < 0.95:
            explanations.append(f"Seasonal discount: {(1-seasonal_multiplier)*100:.1f}% (harvest/low demand period)")
        
        # Quality adjustment
        if quality_multiplier > 1.05:
            explanations.append(f"Quality premium: +{(quality_multiplier-1)*100:.1f}% (above standard grade)")
        elif quality_multiplier < 0.95:
            explanations.append(f"Quality discount: {(1-quality_multiplier)*100:.1f}% (below standard grade)")
        
        # Quantity adjustment
        if quantity_multiplier < 0.98:
            explanations.append(f"Bulk discount: {(1-quantity_multiplier)*100:.1f}% (large quantity)")
        elif quantity_multiplier > 1.02:
            explanations.append(f"Small quantity premium: +{(quantity_multiplier-1)*100:.1f}%")
        
        # Market trend
        explanations.append(f"Market trend: {market_trend.direction} ({market_trend.confidence*100:.0f}% confidence)")
        
        # Final price
        price_change = ((suggested_price - base_price) / base_price) * 100
        if abs(price_change) > 1:
            explanations.append(f"Final suggested price: ₹{suggested_price:.0f} ({price_change:+.1f}% vs base)")
        else:
            explanations.append(f"Final suggested price: ₹{suggested_price:.0f} (close to base price)")
        
        return " | ".join(explanations)
    
    def _assess_price_risks(
        self,
        product: str,
        suggested_price: float,
        volatility: float,
        market_trend: MarketTrend
    ) -> Dict[str, Any]:
        """Assess risks associated with the suggested price"""
        
        risks = []
        risk_level = "low"
        
        # Volatility risk
        if volatility > 0.3:
            risks.append("High price volatility - prices may change rapidly")
            risk_level = "high"
        elif volatility > 0.2:
            risks.append("Moderate price volatility - monitor market closely")
            if risk_level == "low":
                risk_level = "medium"
        
        # Trend risk
        if market_trend.strength > 0.7:
            if market_trend.direction == "up":
                risks.append("Strong upward trend - prices may continue rising")
            else:
                risks.append("Strong downward trend - prices may continue falling")
            if risk_level != "high":
                risk_level = "medium"
        
        # Seasonal risk
        current_month = datetime.now().month
        if current_month in [11, 12, 1, 2]:  # Winter months
            risks.append("Winter season - potential supply chain disruptions")
        elif current_month in [6, 7, 8]:  # Monsoon months
            risks.append("Monsoon season - weather-related price fluctuations possible")
        
        return {
            "level": risk_level,
            "factors": risks,
            "volatility": volatility,
            "confidence_interval": f"±{volatility*100:.0f}%",
            "recommendation": self._get_risk_recommendation(risk_level)
        }
    
    def _get_risk_recommendation(self, risk_level: str) -> str:
        """Get risk-based recommendation"""
        recommendations = {
            "low": "Stable market conditions - good time for trading",
            "medium": "Monitor market closely - consider smaller quantities initially",
            "high": "High risk period - consider waiting or hedging strategies"
        }
        return recommendations.get(risk_level, "Monitor market conditions")


# Global price analysis service instance
price_analysis_service = PriceAnalysisService()