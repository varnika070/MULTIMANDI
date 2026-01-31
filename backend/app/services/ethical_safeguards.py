"""
Ethical Safeguards and Exploitation Detection System
"""

import asyncio
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import json

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AlertType(Enum):
    PRICE_EXPLOITATION = "price_exploitation"
    PREDATORY_PRICING = "predatory_pricing"
    VULNERABLE_USER = "vulnerable_user"
    MARKET_MANIPULATION = "market_manipulation"
    SUSPICIOUS_ACTIVITY = "suspicious_activity"

@dataclass
class EthicalAlert:
    alert_id: str
    alert_type: AlertType
    risk_level: RiskLevel
    user_id: str
    session_id: Optional[str]
    description: str
    evidence: Dict[str, Any]
    recommendations: List[str]
    timestamp: datetime
    requires_intervention: bool

@dataclass
class UserVulnerabilityProfile:
    user_id: str
    literacy_level: str
    experience_level: str
    language_proficiency: float
    economic_indicators: Dict[str, Any]
    vulnerability_score: float
    protection_measures: List[str]

@dataclass
class PriceFairnessAnalysis:
    product: str
    offered_price: float
    market_price: float
    fairness_score: float
    exploitation_risk: RiskLevel
    factors: List[str]
    recommendations: List[str]

class EthicalSafeguardsService:
    """Comprehensive ethical safeguards and exploitation detection"""
    
    def __init__(self):
        # Price fairness thresholds
        self.fairness_thresholds = {
            "extreme_unfair": 0.3,    # 70%+ deviation from fair price
            "very_unfair": 0.5,       # 50%+ deviation
            "unfair": 0.7,            # 30%+ deviation
            "questionable": 0.8,      # 20%+ deviation
            "fair": 0.9               # Within 10% of fair price
        }
        
        # Vulnerability indicators
        self.vulnerability_indicators = {
            "literacy_level": {
                "low": 0.8,
                "basic": 0.6,
                "intermediate": 0.4,
                "high": 0.2
            },
            "experience_level": {
                "new": 0.7,
                "beginner": 0.5,
                "intermediate": 0.3,
                "experienced": 0.1
            },
            "language_proficiency": {
                "poor": 0.8,
                "basic": 0.6,
                "good": 0.4,
                "excellent": 0.2
            }
        }
        
        # Predatory pricing patterns
        self.predatory_patterns = {
            "extreme_lowball": {
                "threshold": 0.6,  # 40% below market price
                "description": "Extremely low offer, potential exploitation",
                "risk_level": RiskLevel.HIGH
            },
            "gradual_reduction": {
                "threshold": 0.05,  # 5% reduction per interaction
                "description": "Gradual price reduction to wear down seller",
                "risk_level": RiskLevel.MEDIUM
            },
            "pressure_tactics": {
                "keywords": ["urgent", "last offer", "take it or leave it", "limited time"],
                "description": "High-pressure negotiation tactics",
                "risk_level": RiskLevel.MEDIUM
            },
            "information_asymmetry": {
                "description": "Exploiting lack of market knowledge",
                "risk_level": RiskLevel.HIGH
            }
        }
        
        # Market manipulation indicators
        self.manipulation_indicators = {
            "artificial_scarcity": {
                "pattern": "sudden_demand_spike",
                "threshold": 2.0,  # 100% increase in demand
                "description": "Artificial scarcity creation"
            },
            "price_coordination": {
                "pattern": "synchronized_pricing",
                "threshold": 0.95,  # 95% price similarity
                "description": "Coordinated pricing behavior"
            },
            "wash_trading": {
                "pattern": "circular_transactions",
                "description": "Fake trading to inflate volumes"
            }
        }
        
        # Protection measures by vulnerability level
        self.protection_measures = {
            "high_vulnerability": [
                "Require price explanation before acceptance",
                "Mandatory cooling-off period (24 hours)",
                "Automatic market price comparison",
                "Simplified language explanations",
                "Audio warnings for unfair deals",
                "Suggest seeking second opinion"
            ],
            "medium_vulnerability": [
                "Price comparison with market rates",
                "Negotiation guidance",
                "Risk factor highlighting",
                "Educational content suggestions"
            ],
            "low_vulnerability": [
                "Standard market information",
                "Optional detailed analysis",
                "Advanced negotiation tools"
            ]
        }
        
        # Alert tracking
        self.active_alerts = {}
        self.user_profiles = {}
        self.session_monitoring = {}
    
    async def assess_user_vulnerability(
        self, 
        user_id: str,
        user_data: Dict[str, Any]
    ) -> UserVulnerabilityProfile:
        """Assess user vulnerability to exploitation"""
        
        # Extract vulnerability factors
        literacy_level = user_data.get("literacy_level", "intermediate")
        experience_level = user_data.get("trading_experience", "beginner")
        language_proficiency = user_data.get("language_proficiency", 0.7)
        
        # Economic indicators
        economic_indicators = {
            "transaction_size": user_data.get("avg_transaction_size", 0),
            "frequency": user_data.get("trading_frequency", "occasional"),
            "location": user_data.get("location", "unknown"),
            "primary_language": user_data.get("primary_language", "unknown")
        }
        
        # Calculate vulnerability score
        vulnerability_score = 0.0
        
        # Literacy factor
        if literacy_level in self.vulnerability_indicators["literacy_level"]:
            vulnerability_score += self.vulnerability_indicators["literacy_level"][literacy_level] * 0.4
        
        # Experience factor
        if experience_level in self.vulnerability_indicators["experience_level"]:
            vulnerability_score += self.vulnerability_indicators["experience_level"][experience_level] * 0.3
        
        # Language proficiency factor
        if language_proficiency < 0.5:
            vulnerability_score += 0.3
        elif language_proficiency < 0.7:
            vulnerability_score += 0.2
        elif language_proficiency < 0.9:
            vulnerability_score += 0.1
        
        # Normalize score
        vulnerability_score = min(vulnerability_score, 1.0)
        
        # Determine protection measures
        if vulnerability_score >= 0.7:
            protection_level = "high_vulnerability"
        elif vulnerability_score >= 0.4:
            protection_level = "medium_vulnerability"
        else:
            protection_level = "low_vulnerability"
        
        protection_measures = self.protection_measures[protection_level]
        
        profile = UserVulnerabilityProfile(
            user_id=user_id,
            literacy_level=literacy_level,
            experience_level=experience_level,
            language_proficiency=language_proficiency,
            economic_indicators=economic_indicators,
            vulnerability_score=vulnerability_score,
            protection_measures=protection_measures
        )
        
        # Cache profile
        self.user_profiles[user_id] = profile
        
        return profile
    
    async def analyze_price_fairness(
        self,
        product: str,
        offered_price: float,
        market_price: float,
        user_id: str,
        context: Dict[str, Any]
    ) -> PriceFairnessAnalysis:
        """Analyze price fairness and detect potential exploitation"""
        
        # Calculate fairness score
        if market_price > 0:
            price_ratio = offered_price / market_price
            
            # Fairness score based on deviation from market price
            if price_ratio >= 0.9 and price_ratio <= 1.1:
                fairness_score = 1.0  # Fair price
            elif price_ratio >= 0.8 and price_ratio <= 1.2:
                fairness_score = 0.8  # Acceptable
            elif price_ratio >= 0.7 and price_ratio <= 1.3:
                fairness_score = 0.6  # Questionable
            elif price_ratio >= 0.5 and price_ratio <= 1.5:
                fairness_score = 0.4  # Unfair
            else:
                fairness_score = 0.2  # Extremely unfair
        else:
            fairness_score = 0.5  # Unknown market price
        
        # Determine exploitation risk
        if fairness_score >= 0.8:
            exploitation_risk = RiskLevel.LOW
        elif fairness_score >= 0.6:
            exploitation_risk = RiskLevel.MEDIUM
        elif fairness_score >= 0.4:
            exploitation_risk = RiskLevel.HIGH
        else:
            exploitation_risk = RiskLevel.CRITICAL
        
        # Analyze contributing factors
        factors = []
        recommendations = []
        
        if offered_price < market_price * 0.7:
            factors.append("Offered price significantly below market rate")
            recommendations.append("Reject this offer - it's well below fair market value")
        elif offered_price > market_price * 1.3:
            factors.append("Offered price significantly above market rate")
            recommendations.append("This price is much higher than market rate - negotiate down")
        
        # Check user vulnerability
        if user_id in self.user_profiles:
            user_profile = self.user_profiles[user_id]
            if user_profile.vulnerability_score > 0.6:
                factors.append("User has high vulnerability to exploitation")
                recommendations.extend([
                    "Take time to consider this offer",
                    "Seek advice from experienced traders",
                    "Compare with multiple market sources"
                ])
        
        # Context-based factors
        if context.get("urgency") == "high":
            factors.append("High urgency may lead to poor decisions")
            recommendations.append("Avoid making rushed decisions under pressure")
        
        if context.get("negotiation_pressure"):
            factors.append("High-pressure negotiation tactics detected")
            recommendations.append("Be wary of pressure tactics - take your time")
        
        return PriceFairnessAnalysis(
            product=product,
            offered_price=offered_price,
            market_price=market_price,
            fairness_score=fairness_score,
            exploitation_risk=exploitation_risk,
            factors=factors,
            recommendations=recommendations
        )
    
    async def detect_predatory_pricing(
        self,
        session_id: str,
        user_id: str,
        price_history: List[Dict[str, Any]],
        conversation_context: Dict[str, Any]
    ) -> List[EthicalAlert]:
        """Detect predatory pricing patterns"""
        
        alerts = []
        
        # Check for extreme lowball offers
        if price_history:
            latest_offer = price_history[-1]
            market_price = latest_offer.get("market_price", 0)
            offered_price = latest_offer.get("offered_price", 0)
            
            if market_price > 0 and offered_price < market_price * 0.6:
                alert = EthicalAlert(
                    alert_id=f"predatory_{session_id}_{datetime.now().timestamp()}",
                    alert_type=AlertType.PREDATORY_PRICING,
                    risk_level=RiskLevel.HIGH,
                    user_id=user_id,
                    session_id=session_id,
                    description="Extremely low offer detected - potential exploitation",
                    evidence={
                        "offered_price": offered_price,
                        "market_price": market_price,
                        "deviation_percent": ((market_price - offered_price) / market_price) * 100
                    },
                    recommendations=[
                        "Do not accept this offer",
                        "The price is significantly below market rate",
                        "Consider seeking alternative buyers"
                    ],
                    timestamp=datetime.now(),
                    requires_intervention=True
                )
                alerts.append(alert)
        
        # Check for gradual price reduction pattern
        if len(price_history) >= 3:
            recent_prices = [p["offered_price"] for p in price_history[-3:]]
            if all(recent_prices[i] > recent_prices[i+1] for i in range(len(recent_prices)-1)):
                reduction_rate = (recent_prices[0] - recent_prices[-1]) / recent_prices[0]
                
                if reduction_rate > 0.15:  # 15% reduction
                    alert = EthicalAlert(
                        alert_id=f"gradual_reduction_{session_id}_{datetime.now().timestamp()}",
                        alert_type=AlertType.PREDATORY_PRICING,
                        risk_level=RiskLevel.MEDIUM,
                        user_id=user_id,
                        session_id=session_id,
                        description="Gradual price reduction pattern detected",
                        evidence={
                            "price_history": recent_prices,
                            "reduction_rate": reduction_rate * 100
                        },
                        recommendations=[
                            "Be aware of gradual price reduction tactics",
                            "Set a minimum acceptable price and stick to it",
                            "Don't let pressure tactics influence your decision"
                        ],
                        timestamp=datetime.now(),
                        requires_intervention=False
                    )
                    alerts.append(alert)
        
        # Check for pressure tactics in conversation
        conversation_text = conversation_context.get("messages", "").lower()
        pressure_keywords = self.predatory_patterns["pressure_tactics"]["keywords"]
        
        detected_pressure = [kw for kw in pressure_keywords if kw in conversation_text]
        if detected_pressure:
            alert = EthicalAlert(
                alert_id=f"pressure_tactics_{session_id}_{datetime.now().timestamp()}",
                alert_type=AlertType.PREDATORY_PRICING,
                risk_level=RiskLevel.MEDIUM,
                user_id=user_id,
                session_id=session_id,
                description="High-pressure negotiation tactics detected",
                evidence={
                    "detected_keywords": detected_pressure,
                    "conversation_context": conversation_text[:200]  # First 200 chars
                },
                recommendations=[
                    "Take your time to make decisions",
                    "Don't be pressured by urgency claims",
                    "Verify market conditions independently"
                ],
                timestamp=datetime.now(),
                requires_intervention=False
            )
            alerts.append(alert)
        
        return alerts
    
    async def monitor_market_manipulation(
        self,
        product: str,
        price_data: List[Dict[str, Any]],
        trading_volume: Dict[str, Any]
    ) -> List[EthicalAlert]:
        """Monitor for market manipulation indicators"""
        
        alerts = []
        
        # Check for artificial scarcity (sudden demand spikes)
        if trading_volume.get("recent_spike", 0) > 2.0:
            alert = EthicalAlert(
                alert_id=f"artificial_scarcity_{product}_{datetime.now().timestamp()}",
                alert_type=AlertType.MARKET_MANIPULATION,
                risk_level=RiskLevel.MEDIUM,
                user_id="system",
                session_id=None,
                description=f"Unusual demand spike detected for {product}",
                evidence={
                    "product": product,
                    "volume_spike": trading_volume.get("recent_spike", 0),
                    "normal_volume": trading_volume.get("average_volume", 0)
                },
                recommendations=[
                    "Verify market conditions from multiple sources",
                    "Be cautious of sudden price increases",
                    "Check for legitimate supply constraints"
                ],
                timestamp=datetime.now(),
                requires_intervention=False
            )
            alerts.append(alert)
        
        # Check for price coordination (similar prices across traders)
        if len(price_data) >= 5:
            prices = [p["price"] for p in price_data[-5:]]
            avg_price = sum(prices) / len(prices)
            price_variance = sum((p - avg_price) ** 2 for p in prices) / len(prices)
            
            if price_variance < (avg_price * 0.01) ** 2:  # Very low variance
                alert = EthicalAlert(
                    alert_id=f"price_coordination_{product}_{datetime.now().timestamp()}",
                    alert_type=AlertType.MARKET_MANIPULATION,
                    risk_level=RiskLevel.HIGH,
                    user_id="system",
                    session_id=None,
                    description=f"Suspicious price coordination detected for {product}",
                    evidence={
                        "product": product,
                        "price_variance": price_variance,
                        "average_price": avg_price,
                        "sample_prices": prices
                    },
                    recommendations=[
                        "Report suspicious pricing patterns",
                        "Seek alternative trading partners",
                        "Verify independent price sources"
                    ],
                    timestamp=datetime.now(),
                    requires_intervention=True
                )
                alerts.append(alert)
        
        return alerts
    
    async def generate_protection_guidance(
        self,
        user_id: str,
        risk_level: RiskLevel,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate personalized protection guidance"""
        
        guidance = {
            "risk_level": risk_level.value,
            "immediate_actions": [],
            "educational_content": [],
            "support_resources": [],
            "automated_protections": []
        }
        
        # Get user vulnerability profile
        user_profile = self.user_profiles.get(user_id)
        
        if risk_level == RiskLevel.CRITICAL:
            guidance["immediate_actions"] = [
                "STOP - Do not proceed with this transaction",
                "The terms are extremely unfavorable",
                "Seek immediate assistance from experienced traders",
                "Report this interaction if you suspect fraud"
            ]
            guidance["automated_protections"] = [
                "Transaction temporarily blocked",
                "Administrator notification sent",
                "Cooling-off period activated"
            ]
        
        elif risk_level == RiskLevel.HIGH:
            guidance["immediate_actions"] = [
                "Proceed with extreme caution",
                "Get a second opinion before accepting",
                "Verify market prices from multiple sources",
                "Consider waiting for better offers"
            ]
            guidance["automated_protections"] = [
                "24-hour cooling-off period recommended",
                "Additional price comparisons provided",
                "Educational content highlighted"
            ]
        
        elif risk_level == RiskLevel.MEDIUM:
            guidance["immediate_actions"] = [
                "Review the offer carefully",
                "Compare with current market rates",
                "Consider negotiating for better terms",
                "Take time to make your decision"
            ]
        
        # Add user-specific guidance
        if user_profile:
            if user_profile.vulnerability_score > 0.6:
                guidance["educational_content"] = [
                    "Understanding fair market prices",
                    "Recognizing exploitation tactics",
                    "Effective negotiation strategies",
                    "When to seek help"
                ]
                
                guidance["support_resources"] = [
                    "Connect with experienced trader mentors",
                    "Access to market price databases",
                    "Legal assistance contacts",
                    "Community support groups"
                ]
        
        return guidance
    
    async def log_ethical_alert(self, alert: EthicalAlert) -> None:
        """Log ethical alert for monitoring and analysis"""
        
        # Store alert
        self.active_alerts[alert.alert_id] = alert
        
        # In production, this would:
        # - Log to database
        # - Send notifications to administrators
        # - Trigger automated responses
        # - Update user protection measures
        
        print(f"ETHICAL ALERT: {alert.alert_type.value} - {alert.description}")
        print(f"Risk Level: {alert.risk_level.value}")
        print(f"User: {alert.user_id}")
        if alert.requires_intervention:
            print("REQUIRES IMMEDIATE INTERVENTION")
    
    async def get_user_protection_status(self, user_id: str) -> Dict[str, Any]:
        """Get current protection status for a user"""
        
        user_profile = self.user_profiles.get(user_id)
        active_user_alerts = [
            alert for alert in self.active_alerts.values() 
            if alert.user_id == user_id and 
            alert.timestamp > datetime.now() - timedelta(hours=24)
        ]
        
        return {
            "user_id": user_id,
            "vulnerability_score": user_profile.vulnerability_score if user_profile else 0.5,
            "protection_measures": user_profile.protection_measures if user_profile else [],
            "active_alerts": len(active_user_alerts),
            "recent_risk_level": max([alert.risk_level for alert in active_user_alerts], 
                                   default=RiskLevel.LOW, key=lambda x: x.value),
            "recommendations": self._get_current_recommendations(user_id, active_user_alerts)
        }
    
    def _get_current_recommendations(self, user_id: str, alerts: List[EthicalAlert]) -> List[str]:
        """Get current recommendations based on user status and alerts"""
        
        recommendations = []
        
        if not alerts:
            recommendations.append("Continue trading with normal caution")
            return recommendations
        
        high_risk_alerts = [a for a in alerts if a.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]]
        
        if high_risk_alerts:
            recommendations.extend([
                "Exercise extreme caution in current negotiations",
                "Verify all offers against market rates",
                "Consider seeking experienced trader advice",
                "Take time before making decisions"
            ])
        else:
            recommendations.extend([
                "Stay alert to market conditions",
                "Continue monitoring price fairness",
                "Use available educational resources"
            ])
        
        return recommendations


# Global ethical safeguards service instance
ethical_safeguards_service = EthicalSafeguardsService()