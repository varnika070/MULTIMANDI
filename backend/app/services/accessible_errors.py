"""
Accessible Error Communication Service
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json

class ErrorSeverity(Enum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    NETWORK = "network"
    VALIDATION = "validation"
    AUTHENTICATION = "authentication"
    PERMISSION = "permission"
    PRICE_DATA = "price_data"
    SPEECH_PROCESSING = "speech_processing"
    NEGOTIATION = "negotiation"
    SYSTEM = "system"

@dataclass
class AccessibleError:
    error_id: str
    category: ErrorCategory
    severity: ErrorSeverity
    title: str
    simple_message: str
    detailed_message: str
    audio_message: str
    visual_indicators: Dict[str, Any]
    recovery_steps: List[str]
    audio_recovery_steps: List[str]
    prevention_tips: List[str]
    multilingual_messages: Dict[str, str]
    accessibility_features: Dict[str, Any]

class AccessibleErrorService:
    """Service for creating accessible error messages and recovery guidance"""
    
    def __init__(self):
        # Error message templates
        self.error_templates = {
            ErrorCategory.NETWORK: {
                "connection_failed": {
                    "title": "Connection Problem",
                    "simple": "Cannot connect to server",
                    "detailed": "Unable to establish connection with the OpenMandi server. This may be due to internet connectivity issues or server maintenance.",
                    "audio": "Connection problem. Please check your internet and try again.",
                    "recovery": [
                        "Check your internet connection",
                        "Try refreshing the page",
                        "Wait a moment and try again",
                        "Contact support if problem persists"
                    ],
                    "audio_recovery": [
                        "First, check your internet connection",
                        "Then, try refreshing the page",
                        "If that doesn't work, wait a moment and try again"
                    ]
                },
                "timeout": {
                    "title": "Request Timeout",
                    "simple": "Request took too long",
                    "detailed": "The server is taking longer than expected to respond. This might be due to high traffic or server load.",
                    "audio": "The request is taking too long. Please try again.",
                    "recovery": [
                        "Try the request again",
                        "Check your internet speed",
                        "Try during off-peak hours",
                        "Contact support if issue continues"
                    ]
                }
            },
            
            ErrorCategory.VALIDATION: {
                "invalid_price": {
                    "title": "Invalid Price",
                    "simple": "Price format is incorrect",
                    "detailed": "The price you entered is not in a valid format. Please enter a positive number without special characters.",
                    "audio": "Invalid price format. Please enter a valid number.",
                    "recovery": [
                        "Enter only numbers for price",
                        "Use decimal point for cents (e.g., 2500.50)",
                        "Don't include currency symbols",
                        "Make sure price is greater than zero"
                    ]
                },
                "missing_product": {
                    "title": "Product Not Specified",
                    "simple": "Please select a product",
                    "detailed": "You need to specify which agricultural product you want to trade before proceeding.",
                    "audio": "Please select a product first.",
                    "recovery": [
                        "Choose a product from the list",
                        "Or say the product name clearly",
                        "Make sure the product is supported",
                        "Try spelling the product name differently"
                    ]
                }
            },
            
            ErrorCategory.SPEECH_PROCESSING: {
                "microphone_access": {
                    "title": "Microphone Access Denied",
                    "simple": "Cannot access microphone",
                    "detailed": "OpenMandi needs microphone access to process your voice commands. Please allow microphone access in your browser settings.",
                    "audio": "Microphone access is needed for voice features. Please allow access in your browser.",
                    "recovery": [
                        "Click 'Allow' when browser asks for microphone access",
                        "Check browser settings for microphone permissions",
                        "Make sure microphone is connected and working",
                        "Try refreshing the page and allowing access again"
                    ]
                },
                "speech_not_recognized": {
                    "title": "Speech Not Recognized",
                    "simple": "Could not understand speech",
                    "detailed": "The speech recognition system could not understand what you said. This might be due to background noise, unclear speech, or language settings.",
                    "audio": "Sorry, I couldn't understand what you said. Please try speaking clearly.",
                    "recovery": [
                        "Speak more clearly and slowly",
                        "Reduce background noise",
                        "Check your language settings",
                        "Try typing your message instead"
                    ]
                }
            },
            
            ErrorCategory.PRICE_DATA: {
                "price_unavailable": {
                    "title": "Price Data Unavailable",
                    "simple": "Cannot get current prices",
                    "detailed": "Current market price data is not available for this product. This might be due to market closure, data source issues, or product not being traded today.",
                    "audio": "Price data is not available right now. Please try again later.",
                    "recovery": [
                        "Try again in a few minutes",
                        "Check if market is open",
                        "Try a different product",
                        "Use historical price data as reference"
                    ]
                },
                "stale_data": {
                    "title": "Old Price Data",
                    "simple": "Price data may be outdated",
                    "detailed": "The price information shown is from earlier today and may not reflect current market conditions. Use with caution.",
                    "audio": "Warning: Price data may be outdated. Please verify current prices.",
                    "recovery": [
                        "Refresh to get latest prices",
                        "Verify prices from other sources",
                        "Consider market timing",
                        "Proceed with caution"
                    ]
                }
            },
            
            ErrorCategory.NEGOTIATION: {
                "unfair_offer": {
                    "title": "Potentially Unfair Offer",
                    "simple": "This offer seems unfair",
                    "detailed": "The offered price is significantly different from current market rates. Please review carefully before accepting.",
                    "audio": "Warning: This offer may not be fair. Please review carefully.",
                    "recovery": [
                        "Compare with current market prices",
                        "Ask for explanation of the price",
                        "Consider negotiating",
                        "Seek second opinion if unsure"
                    ]
                },
                "high_risk_deal": {
                    "title": "High Risk Transaction",
                    "simple": "This deal has high risk",
                    "detailed": "Our analysis indicates this transaction has higher than normal risk factors. Please review all terms carefully.",
                    "audio": "High risk transaction detected. Please review carefully.",
                    "recovery": [
                        "Review all transaction details",
                        "Verify the other party's credentials",
                        "Consider smaller test transaction first",
                        "Get advice from experienced traders"
                    ]
                }
            }
        }
        
        # Multilingual error messages
        self.multilingual_templates = {
            "hindi": {
                "connection_failed": "कनेक्शन की समस्या। कृपया अपना इंटरनेट जांचें और फिर कोशिश करें।",
                "invalid_price": "गलत कीमत। कृपया सही संख्या दर्ज करें।",
                "microphone_access": "माइक्रोफोन की अनुमति चाहिए। कृपया ब्राउज़र में अनुमति दें।",
                "speech_not_recognized": "आपकी बात समझ नहीं आई। कृपया स्पष्ट रूप से बोलें।",
                "unfair_offer": "चेतावनी: यह ऑफर उचित नहीं लग रहा। कृपया सावधानी से देखें।"
            },
            "telugu": {
                "connection_failed": "కనెక్షన్ సమస్య. దయచేసి మీ ఇంటర్నెట్ చెక్ చేసి మళ్లీ ప్రయత్నించండి.",
                "invalid_price": "తప్పు ధర. దయచేసి సరైన సంఖ్య నమోదు చేయండి.",
                "microphone_access": "మైక్రోఫోన్ అనుమతి అవసరం. దయచేసి బ్రౌజర్‌లో అనుమతించండి.",
                "speech_not_recognized": "మీ మాట అర్థం కాలేదు. దయచేసి స్పష్టంగా మాట్లాడండి.",
                "unfair_offer": "హెచ్చరిక: ఈ ఆఫర్ న్యాయంగా లేదు. దయచేసి జాగ్రత్తగా చూడండి."
            },
            "tamil": {
                "connection_failed": "இணைப்பு பிரச்சனை. தயவுசெய்து உங்கள் இணையத்தை சரிபார்த்து மீண்டும் முயற்சிக்கவும்.",
                "invalid_price": "தவறான விலை. தயவுசெய்து சரியான எண்ணை உள்ளிடவும்.",
                "microphone_access": "மைக்ரோஃபோன் அனுமதி தேவை. தயவுசெய்து உலாவியில் அனுமதிக்கவும்.",
                "speech_not_recognized": "உங்கள் பேச்சு புரியவில்லை. தயவுசெய்து தெளிவாக பேசவும்.",
                "unfair_offer": "எச்சரிக்கை: இந்த சலுகை நியாயமானதாக தெரியவில்லை. தயவுசெய்து கவனமாக பார்க்கவும்."
            }
        }
        
        # Visual indicators for different error types
        self.visual_indicators = {
            ErrorSeverity.INFO: {
                "color": "#3B82F6",  # Blue
                "icon": "info",
                "animation": "fade-in",
                "duration": 3000
            },
            ErrorSeverity.WARNING: {
                "color": "#F59E0B",  # Amber
                "icon": "warning",
                "animation": "pulse",
                "duration": 5000
            },
            ErrorSeverity.ERROR: {
                "color": "#EF4444",  # Red
                "icon": "error",
                "animation": "shake",
                "duration": 7000
            },
            ErrorSeverity.CRITICAL: {
                "color": "#DC2626",  # Dark red
                "icon": "critical",
                "animation": "flash",
                "duration": 10000
            }
        }
        
        # Accessibility features
        self.accessibility_features = {
            "high_contrast": True,
            "large_text": True,
            "audio_feedback": True,
            "keyboard_navigation": True,
            "screen_reader_support": True,
            "voice_guidance": True,
            "simple_language": True,
            "visual_indicators": True
        }
    
    def create_accessible_error(
        self,
        error_key: str,
        category: ErrorCategory,
        severity: ErrorSeverity = ErrorSeverity.ERROR,
        context: Optional[Dict[str, Any]] = None,
        user_language: str = "english"
    ) -> AccessibleError:
        """Create an accessible error message with all necessary components"""
        
        # Get error template
        template = None
        if category in self.error_templates and error_key in self.error_templates[category]:
            template = self.error_templates[category][error_key]
        
        if not template:
            # Fallback generic error
            template = {
                "title": "Error Occurred",
                "simple": "Something went wrong",
                "detailed": "An unexpected error occurred. Please try again or contact support.",
                "audio": "An error occurred. Please try again.",
                "recovery": ["Try again", "Contact support if problem persists"]
            }
        
        # Generate error ID
        error_id = f"{category.value}_{error_key}_{hash(str(context)) if context else 'generic'}"
        
        # Get multilingual messages
        multilingual_messages = {}
        for lang, translations in self.multilingual_templates.items():
            if error_key in translations:
                multilingual_messages[lang] = translations[error_key]
        
        # Add context to messages if provided
        simple_message = template["simple"]
        detailed_message = template["detailed"]
        audio_message = template["audio"]
        
        if context:
            # Customize messages based on context
            if "product" in context:
                simple_message = simple_message.replace("product", context["product"])
                detailed_message = detailed_message.replace("product", context["product"])
                audio_message = audio_message.replace("product", context["product"])
            
            if "price" in context:
                simple_message = simple_message.replace("price", str(context["price"]))
                detailed_message = detailed_message.replace("price", str(context["price"]))
        
        # Get visual indicators
        visual_indicators = self.visual_indicators[severity].copy()
        
        # Add accessibility features
        accessibility_features = self.accessibility_features.copy()
        
        # Customize for user needs
        if context and "user_profile" in context:
            user_profile = context["user_profile"]
            
            if user_profile.get("literacy_level") == "low":
                accessibility_features["simple_language"] = True
                accessibility_features["audio_priority"] = True
            
            if user_profile.get("visual_impairment"):
                accessibility_features["high_contrast"] = True
                accessibility_features["large_text"] = True
                accessibility_features["screen_reader_priority"] = True
        
        # Generate recovery steps
        recovery_steps = template.get("recovery", [])
        audio_recovery_steps = template.get("audio_recovery", recovery_steps[:3])  # Limit for audio
        
        # Add context-specific recovery steps
        if context:
            if "retry_action" in context:
                recovery_steps.insert(0, f"Try {context['retry_action']} again")
            
            if "alternative_action" in context:
                recovery_steps.append(f"Alternatively, try {context['alternative_action']}")
        
        # Prevention tips
        prevention_tips = self._generate_prevention_tips(category, error_key, context)
        
        return AccessibleError(
            error_id=error_id,
            category=category,
            severity=severity,
            title=template["title"],
            simple_message=simple_message,
            detailed_message=detailed_message,
            audio_message=audio_message,
            visual_indicators=visual_indicators,
            recovery_steps=recovery_steps,
            audio_recovery_steps=audio_recovery_steps,
            prevention_tips=prevention_tips,
            multilingual_messages=multilingual_messages,
            accessibility_features=accessibility_features
        )
    
    def _generate_prevention_tips(
        self,
        category: ErrorCategory,
        error_key: str,
        context: Optional[Dict[str, Any]]
    ) -> List[str]:
        """Generate prevention tips for future error avoidance"""
        
        prevention_tips = []
        
        if category == ErrorCategory.NETWORK:
            prevention_tips = [
                "Ensure stable internet connection before trading",
                "Use WiFi instead of mobile data when possible",
                "Close other apps that use internet heavily"
            ]
        
        elif category == ErrorCategory.SPEECH_PROCESSING:
            prevention_tips = [
                "Speak clearly and at moderate pace",
                "Reduce background noise when using voice features",
                "Check microphone settings regularly",
                "Have backup text input ready"
            ]
        
        elif category == ErrorCategory.VALIDATION:
            prevention_tips = [
                "Double-check all entered information",
                "Use suggested formats for prices and quantities",
                "Save frequently used values for quick access"
            ]
        
        elif category == ErrorCategory.NEGOTIATION:
            prevention_tips = [
                "Always verify market prices before negotiating",
                "Set your minimum acceptable price beforehand",
                "Take time to consider offers carefully",
                "Seek advice for large transactions"
            ]
        
        return prevention_tips
    
    def format_for_frontend(self, error: AccessibleError) -> Dict[str, Any]:
        """Format error for frontend consumption"""
        
        return {
            "error_id": error.error_id,
            "category": error.category.value,
            "severity": error.severity.value,
            "title": error.title,
            "message": {
                "simple": error.simple_message,
                "detailed": error.detailed_message,
                "audio": error.audio_message
            },
            "visual": {
                "color": error.visual_indicators["color"],
                "icon": error.visual_indicators["icon"],
                "animation": error.visual_indicators["animation"],
                "duration": error.visual_indicators["duration"]
            },
            "recovery": {
                "steps": error.recovery_steps,
                "audio_steps": error.audio_recovery_steps,
                "prevention_tips": error.prevention_tips
            },
            "multilingual": error.multilingual_messages,
            "accessibility": error.accessibility_features,
            "timestamp": "2024-01-01T00:00:00Z"  # Would be actual timestamp
        }
    
    def create_network_error(self, error_type: str = "connection_failed", context: Optional[Dict] = None) -> AccessibleError:
        """Create network-related error"""
        return self.create_accessible_error(error_type, ErrorCategory.NETWORK, ErrorSeverity.ERROR, context)
    
    def create_validation_error(self, error_type: str, context: Optional[Dict] = None) -> AccessibleError:
        """Create validation error"""
        return self.create_accessible_error(error_type, ErrorCategory.VALIDATION, ErrorSeverity.WARNING, context)
    
    def create_speech_error(self, error_type: str, context: Optional[Dict] = None) -> AccessibleError:
        """Create speech processing error"""
        return self.create_accessible_error(error_type, ErrorCategory.SPEECH_PROCESSING, ErrorSeverity.WARNING, context)
    
    def create_price_error(self, error_type: str, context: Optional[Dict] = None) -> AccessibleError:
        """Create price data error"""
        return self.create_accessible_error(error_type, ErrorCategory.PRICE_DATA, ErrorSeverity.WARNING, context)
    
    def create_negotiation_warning(self, error_type: str, context: Optional[Dict] = None) -> AccessibleError:
        """Create negotiation warning"""
        return self.create_accessible_error(error_type, ErrorCategory.NEGOTIATION, ErrorSeverity.WARNING, context)
    
    def create_critical_error(self, message: str, context: Optional[Dict] = None) -> AccessibleError:
        """Create critical system error"""
        
        return AccessibleError(
            error_id=f"critical_{hash(message)}",
            category=ErrorCategory.SYSTEM,
            severity=ErrorSeverity.CRITICAL,
            title="Critical Error",
            simple_message="System error occurred",
            detailed_message=message,
            audio_message="Critical system error. Please contact support immediately.",
            visual_indicators=self.visual_indicators[ErrorSeverity.CRITICAL],
            recovery_steps=[
                "Contact support immediately",
                "Do not proceed with current transaction",
                "Save any important information",
                "Try accessing the system later"
            ],
            audio_recovery_steps=[
                "Contact support immediately",
                "Do not continue with your current transaction"
            ],
            prevention_tips=[
                "Keep the app updated",
                "Report any unusual behavior",
                "Use stable internet connection"
            ],
            multilingual_messages={
                "hindi": "गंभीर त्रुटि। तुरंत सहायता से संपर्क करें।",
                "telugu": "తీవ్రమైన లోపం. వెంటనే మద్దతును సంప్రదించండి.",
                "tamil": "கடுமையான பிழை. உடனடியாக ஆதரவைத் தொடர்பு கொள்ளவும்."
            },
            accessibility_features=self.accessibility_features
        )
    
    def get_error_statistics(self) -> Dict[str, Any]:
        """Get error statistics for monitoring"""
        
        # Mock statistics (in production, this would track real errors)
        return {
            "total_errors": 0,
            "by_category": {
                "network": 0,
                "validation": 0,
                "speech_processing": 0,
                "price_data": 0,
                "negotiation": 0,
                "system": 0
            },
            "by_severity": {
                "info": 0,
                "warning": 0,
                "error": 0,
                "critical": 0
            },
            "resolution_rate": 0.95,
            "user_satisfaction": 0.88,
            "accessibility_usage": {
                "audio_feedback": 0.75,
                "simple_language": 0.60,
                "high_contrast": 0.25,
                "large_text": 0.40
            }
        }


# Global accessible error service instance
accessible_error_service = AccessibleErrorService()