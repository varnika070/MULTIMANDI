"""
Accessible Error Communication API endpoints
"""
from typing import List

from fastapi import APIRouter, HTTPException, Form
from typing import Optional, Dict, Any
from app.services.accessible_errors import accessible_error_service, ErrorCategory, ErrorSeverity
import json

router = APIRouter()


@router.post("/network")
async def create_network_error(
    error_type: str = Form("connection_failed"),
    context: Optional[str] = Form(None)
):
    """Create accessible network error message"""
    
    context_data = {}
    if context:
        try:
            context_data = json.loads(context)
        except json.JSONDecodeError:
            context_data = {"raw_context": context}
    
    error = accessible_error_service.create_network_error(error_type, context_data)
    return accessible_error_service.format_for_frontend(error)


@router.post("/validation")
async def create_validation_error(
    error_type: str = Form(...),
    context: Optional[str] = Form(None)
):
    """Create accessible validation error message"""
    
    context_data = {}
    if context:
        try:
            context_data = json.loads(context)
        except json.JSONDecodeError:
            context_data = {"raw_context": context}
    
    error = accessible_error_service.create_validation_error(error_type, context_data)
    return accessible_error_service.format_for_frontend(error)


@router.post("/speech")
async def create_speech_error(
    error_type: str = Form(...),
    context: Optional[str] = Form(None)
):
    """Create accessible speech processing error message"""
    
    context_data = {}
    if context:
        try:
            context_data = json.loads(context)
        except json.JSONDecodeError:
            context_data = {"raw_context": context}
    
    error = accessible_error_service.create_speech_error(error_type, context_data)
    return accessible_error_service.format_for_frontend(error)


@router.post("/price")
async def create_price_error(
    error_type: str = Form(...),
    context: Optional[str] = Form(None)
):
    """Create accessible price data error message"""
    
    context_data = {}
    if context:
        try:
            context_data = json.loads(context)
        except json.JSONDecodeError:
            context_data = {"raw_context": context}
    
    error = accessible_error_service.create_price_error(error_type, context_data)
    return accessible_error_service.format_for_frontend(error)


@router.post("/negotiation")
async def create_negotiation_warning(
    error_type: str = Form(...),
    context: Optional[str] = Form(None)
):
    """Create accessible negotiation warning message"""
    
    context_data = {}
    if context:
        try:
            context_data = json.loads(context)
        except json.JSONDecodeError:
            context_data = {"raw_context": context}
    
    error = accessible_error_service.create_negotiation_warning(error_type, context_data)
    return accessible_error_service.format_for_frontend(error)


@router.post("/critical")
async def create_critical_error(
    message: str = Form(...),
    context: Optional[str] = Form(None)
):
    """Create critical system error message"""
    
    context_data = {}
    if context:
        try:
            context_data = json.loads(context)
        except json.JSONDecodeError:
            context_data = {"raw_context": context}
    
    error = accessible_error_service.create_critical_error(message, context_data)
    return accessible_error_service.format_for_frontend(error)


@router.post("/custom")
async def create_custom_error(
    category: str = Form(...),
    severity: str = Form("error"),
    title: str = Form(...),
    message: str = Form(...),
    context: Optional[str] = Form(None),
    user_language: str = Form("english")
):
    """Create custom accessible error message"""
    
    try:
        error_category = ErrorCategory(category.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    try:
        error_severity = ErrorSeverity(severity.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid severity: {severity}")
    
    context_data = {}
    if context:
        try:
            context_data = json.loads(context)
        except json.JSONDecodeError:
            context_data = {"raw_context": context}
    
    # Create custom error template
    custom_template = {
        "title": title,
        "simple": message,
        "detailed": message,
        "audio": message,
        "recovery": ["Try again", "Contact support if problem persists"]
    }
    
    # Temporarily add to templates
    if error_category not in accessible_error_service.error_templates:
        accessible_error_service.error_templates[error_category] = {}
    
    accessible_error_service.error_templates[error_category]["custom"] = custom_template
    
    error = accessible_error_service.create_accessible_error(
        "custom", error_category, error_severity, context_data, user_language
    )
    
    return accessible_error_service.format_for_frontend(error)


@router.get("/statistics")
async def get_error_statistics():
    """Get error statistics for monitoring"""
    
    stats = accessible_error_service.get_error_statistics()
    return {
        "statistics": stats,
        "accessibility_features": {
            "audio_feedback": "Available for all error messages",
            "simple_language": "Automatically enabled for low-literacy users",
            "multilingual": "Supports Hindi, Telugu, Tamil, Kannada",
            "visual_indicators": "Color-coded with animations",
            "voice_guidance": "Step-by-step audio instructions",
            "high_contrast": "Available for visually impaired users"
        },
        "supported_categories": [category.value for category in ErrorCategory],
        "supported_severities": [severity.value for severity in ErrorSeverity]
    }


@router.get("/templates")
async def get_error_templates():
    """Get available error templates for reference"""
    
    templates = {}
    for category, category_templates in accessible_error_service.error_templates.items():
        templates[category.value] = list(category_templates.keys())
    
    return {
        "templates": templates,
        "usage": {
            "network": ["connection_failed", "timeout"],
            "validation": ["invalid_price", "missing_product"],
            "speech_processing": ["microphone_access", "speech_not_recognized"],
            "price_data": ["price_unavailable", "stale_data"],
            "negotiation": ["unfair_offer", "high_risk_deal"]
        },
        "multilingual_support": list(accessible_error_service.multilingual_templates.keys())
    }


@router.post("/test")
async def test_error_accessibility(
    error_type: str = Form(...),
    category: str = Form(...),
    user_profile: Optional[str] = Form(None)
):
    """Test error accessibility features"""
    
    try:
        error_category = ErrorCategory(category.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail=f"Invalid category: {category}")
    
    context_data = {}
    if user_profile:
        try:
            context_data["user_profile"] = json.loads(user_profile)
        except json.JSONDecodeError:
            context_data["user_profile"] = {"literacy_level": "intermediate"}
    
    error = accessible_error_service.create_accessible_error(
        error_type, error_category, ErrorSeverity.WARNING, context_data
    )
    
    formatted_error = accessible_error_service.format_for_frontend(error)
    
    return {
        "test_error": formatted_error,
        "accessibility_analysis": {
            "audio_message_length": len(error.audio_message.split()),
            "recovery_steps_count": len(error.recovery_steps),
            "multilingual_variants": len(error.multilingual_messages),
            "accessibility_features_enabled": sum(1 for v in error.accessibility_features.values() if v),
            "readability_score": _calculate_readability_score(error.simple_message),
            "recommendations": _get_accessibility_recommendations(error)
        }
    }


def _calculate_readability_score(text: str) -> float:
    """Calculate simple readability score (mock implementation)"""
    
    words = text.split()
    sentences = text.count('.') + text.count('!') + text.count('?') + 1
    
    if sentences == 0:
        return 0.0
    
    avg_words_per_sentence = len(words) / sentences
    
    # Simple scoring: lower is better for accessibility
    if avg_words_per_sentence <= 10:
        return 0.9  # Excellent
    elif avg_words_per_sentence <= 15:
        return 0.7  # Good
    elif avg_words_per_sentence <= 20:
        return 0.5  # Fair
    else:
        return 0.3  # Needs improvement


def _get_accessibility_recommendations(error) -> List[str]:
    """Get recommendations for improving error accessibility"""
    
    recommendations = []
    
    if len(error.simple_message.split()) > 15:
        recommendations.append("Consider shortening the simple message for better accessibility")
    
    if len(error.recovery_steps) > 5:
        recommendations.append("Limit recovery steps to 3-5 for better comprehension")
    
    if not error.multilingual_messages:
        recommendations.append("Add multilingual support for better inclusivity")
    
    if len(error.audio_message.split()) > 20:
        recommendations.append("Shorten audio message for better listening experience")
    
    if not recommendations:
        recommendations.append("Error message meets accessibility guidelines")
    
    return recommendations