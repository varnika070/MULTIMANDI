"""
Ethical Safeguards and Protection API endpoints
"""

from fastapi import APIRouter, HTTPException, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List, Dict, Any
from app.core.database import get_db
from app.services.ethical_safeguards import ethical_safeguards_service, RiskLevel

router = APIRouter()


@router.post("/assess-vulnerability")
async def assess_user_vulnerability(
    user_id: str = Form(...),
    literacy_level: str = Form("intermediate"),
    trading_experience: str = Form("beginner"),
    language_proficiency: float = Form(0.7),
    location: Optional[str] = Form(None),
    primary_language: Optional[str] = Form(None)
):
    """Assess user vulnerability to exploitation"""
    
    user_data = {
        "literacy_level": literacy_level,
        "trading_experience": trading_experience,
        "language_proficiency": language_proficiency,
        "location": location,
        "primary_language": primary_language
    }
    
    profile = await ethical_safeguards_service.assess_user_vulnerability(user_id, user_data)
    
    return {
        "user_id": profile.user_id,
        "vulnerability_score": profile.vulnerability_score,
        "literacy_level": profile.literacy_level,
        "experience_level": profile.experience_level,
        "language_proficiency": profile.language_proficiency,
        "protection_measures": profile.protection_measures,
        "risk_category": "high" if profile.vulnerability_score > 0.6 else "medium" if profile.vulnerability_score > 0.3 else "low"
    }


@router.post("/analyze-price-fairness")
async def analyze_price_fairness(
    product: str = Form(...),
    offered_price: float = Form(...),
    market_price: float = Form(...),
    user_id: str = Form(...),
    urgency: Optional[str] = Form("normal"),
    negotiation_pressure: Optional[bool] = Form(False)
):
    """Analyze price fairness and detect potential exploitation"""
    
    context = {
        "urgency": urgency,
        "negotiation_pressure": negotiation_pressure
    }
    
    analysis = await ethical_safeguards_service.analyze_price_fairness(
        product=product,
        offered_price=offered_price,
        market_price=market_price,
        user_id=user_id,
        context=context
    )
    
    return {
        "product": analysis.product,
        "offered_price": analysis.offered_price,
        "market_price": analysis.market_price,
        "fairness_score": analysis.fairness_score,
        "exploitation_risk": analysis.exploitation_risk.value,
        "factors": analysis.factors,
        "recommendations": analysis.recommendations,
        "verdict": _get_fairness_verdict(analysis.fairness_score),
        "action_required": analysis.exploitation_risk in [RiskLevel.HIGH, RiskLevel.CRITICAL]
    }


@router.post("/detect-predatory-pricing")
async def detect_predatory_pricing(
    session_id: str = Form(...),
    user_id: str = Form(...),
    price_history: str = Form(...),  # JSON string
    conversation_context: str = Form(...)  # JSON string
):
    """Detect predatory pricing patterns in a trading session"""
    
    try:
        import json
        price_history_data = json.loads(price_history)
        conversation_data = json.loads(conversation_context)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in price_history or conversation_context")
    
    alerts = await ethical_safeguards_service.detect_predatory_pricing(
        session_id=session_id,
        user_id=user_id,
        price_history=price_history_data,
        conversation_context=conversation_data
    )
    
    # Log alerts
    for alert in alerts:
        await ethical_safeguards_service.log_ethical_alert(alert)
    
    return {
        "session_id": session_id,
        "alerts_detected": len(alerts),
        "alerts": [
            {
                "alert_id": alert.alert_id,
                "type": alert.alert_type.value,
                "risk_level": alert.risk_level.value,
                "description": alert.description,
                "recommendations": alert.recommendations,
                "requires_intervention": alert.requires_intervention
            }
            for alert in alerts
        ],
        "overall_risk": max([alert.risk_level for alert in alerts], default=RiskLevel.LOW, key=lambda x: x.value).value if alerts else "low"
    }


@router.post("/monitor-market-manipulation")
async def monitor_market_manipulation(
    product: str = Form(...),
    price_data: str = Form(...),  # JSON string
    trading_volume: str = Form(...)  # JSON string
):
    """Monitor for market manipulation indicators"""
    
    try:
        import json
        price_data_parsed = json.loads(price_data)
        volume_data_parsed = json.loads(trading_volume)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in price_data or trading_volume")
    
    alerts = await ethical_safeguards_service.monitor_market_manipulation(
        product=product,
        price_data=price_data_parsed,
        trading_volume=volume_data_parsed
    )
    
    # Log alerts
    for alert in alerts:
        await ethical_safeguards_service.log_ethical_alert(alert)
    
    return {
        "product": product,
        "manipulation_alerts": len(alerts),
        "alerts": [
            {
                "alert_id": alert.alert_id,
                "type": alert.alert_type.value,
                "risk_level": alert.risk_level.value,
                "description": alert.description,
                "evidence": alert.evidence,
                "recommendations": alert.recommendations
            }
            for alert in alerts
        ],
        "market_status": "suspicious" if any(alert.risk_level == RiskLevel.HIGH for alert in alerts) else "normal"
    }


@router.get("/protection-guidance/{user_id}")
async def get_protection_guidance(
    user_id: str,
    risk_level: str = "medium",
    context: Optional[str] = None
):
    """Get personalized protection guidance for a user"""
    
    try:
        risk_enum = RiskLevel(risk_level.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid risk_level. Use: low, medium, high, critical")
    
    context_data = {}
    if context:
        try:
            import json
            context_data = json.loads(context)
        except json.JSONDecodeError:
            context_data = {"raw_context": context}
    
    guidance = await ethical_safeguards_service.generate_protection_guidance(
        user_id=user_id,
        risk_level=risk_enum,
        context=context_data
    )
    
    return guidance


@router.get("/user-protection-status/{user_id}")
async def get_user_protection_status(user_id: str):
    """Get current protection status for a user"""
    
    status = await ethical_safeguards_service.get_user_protection_status(user_id)
    
    return {
        "user_id": status["user_id"],
        "vulnerability_score": status["vulnerability_score"],
        "protection_level": "high" if status["vulnerability_score"] > 0.6 else "medium" if status["vulnerability_score"] > 0.3 else "standard",
        "active_alerts": status["active_alerts"],
        "recent_risk_level": status["recent_risk_level"].value,
        "protection_measures": status["protection_measures"],
        "current_recommendations": status["recommendations"],
        "status_summary": _get_protection_status_summary(status)
    }


@router.post("/report-suspicious-activity")
async def report_suspicious_activity(
    reporter_user_id: str = Form(...),
    reported_user_id: Optional[str] = Form(None),
    session_id: Optional[str] = Form(None),
    activity_type: str = Form(...),
    description: str = Form(...),
    evidence: Optional[str] = Form(None)
):
    """Report suspicious trading activity"""
    
    # Create alert for suspicious activity
    from app.services.ethical_safeguards import EthicalAlert, AlertType
    from datetime import datetime
    import uuid
    
    alert = EthicalAlert(
        alert_id=str(uuid.uuid4()),
        alert_type=AlertType.SUSPICIOUS_ACTIVITY,
        risk_level=RiskLevel.MEDIUM,
        user_id=reported_user_id or "unknown",
        session_id=session_id,
        description=f"Suspicious activity reported: {description}",
        evidence={
            "reporter": reporter_user_id,
            "activity_type": activity_type,
            "description": description,
            "evidence": evidence,
            "timestamp": datetime.now().isoformat()
        },
        recommendations=[
            "Investigate reported activity",
            "Monitor involved users closely",
            "Consider temporary restrictions if necessary"
        ],
        timestamp=datetime.now(),
        requires_intervention=True
    )
    
    await ethical_safeguards_service.log_ethical_alert(alert)
    
    return {
        "report_id": alert.alert_id,
        "status": "received",
        "message": "Thank you for reporting suspicious activity. Our team will investigate.",
        "next_steps": [
            "Your report has been logged",
            "Investigation will begin within 24 hours",
            "You may be contacted for additional information",
            "Continue trading with normal caution"
        ]
    }


@router.get("/market-health/{product}")
async def get_market_health(product: str):
    """Get overall market health indicators for a product"""
    
    # Mock market health analysis (in production, this would analyze real data)
    health_indicators = {
        "product": product,
        "overall_health": "good",
        "price_stability": 0.85,
        "trading_volume": "normal",
        "manipulation_risk": "low",
        "fairness_score": 0.82,
        "recent_alerts": 0,
        "recommendations": [
            "Market conditions are stable",
            "Normal trading precautions apply",
            "Monitor for seasonal price variations"
        ],
        "risk_factors": [],
        "protective_measures": [
            "Standard price comparison tools available",
            "Automated fairness checking enabled",
            "Educational resources accessible"
        ]
    }
    
    # Add some realistic variations based on product
    if product.lower() in ["onion", "tomato"]:
        health_indicators["price_stability"] = 0.65
        health_indicators["overall_health"] = "volatile"
        health_indicators["risk_factors"] = ["High price volatility", "Weather-dependent supply"]
        health_indicators["recommendations"] = [
            "Exercise extra caution due to price volatility",
            "Verify prices from multiple sources",
            "Consider smaller transaction sizes"
        ]
    
    return health_indicators


def _get_fairness_verdict(fairness_score: float) -> str:
    """Get human-readable fairness verdict"""
    if fairness_score >= 0.9:
        return "Fair price - within normal market range"
    elif fairness_score >= 0.7:
        return "Acceptable price - minor deviation from market rate"
    elif fairness_score >= 0.5:
        return "Questionable price - significant deviation from market rate"
    elif fairness_score >= 0.3:
        return "Unfair price - major deviation from market rate"
    else:
        return "Extremely unfair price - potential exploitation"


def _get_protection_status_summary(status: Dict[str, Any]) -> str:
    """Get summary of user protection status"""
    
    vulnerability = status["vulnerability_score"]
    alerts = status["active_alerts"]
    risk = status["recent_risk_level"]
    
    if alerts > 0 and risk in ["high", "critical"]:
        return "High risk - Enhanced protection measures active"
    elif vulnerability > 0.6:
        return "Vulnerable user - Additional safeguards enabled"
    elif alerts > 0:
        return "Monitoring active - Recent alerts detected"
    else:
        return "Normal protection - Standard safeguards active"