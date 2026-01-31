"""
Advanced Dialect Recognition and Cultural Context Processing
"""

import re
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum

class DialectRegion(Enum):
    NORTH_INDIA = "north_india"
    SOUTH_INDIA = "south_india"
    WEST_INDIA = "west_india"
    EAST_INDIA = "east_india"
    CENTRAL_INDIA = "central_india"

@dataclass
class DialectMatch:
    language: str
    region: DialectRegion
    confidence: float
    dialect_markers: List[str]
    cultural_context: Dict[str, Any]

@dataclass
class AgriculturalTerm:
    standard_term: str
    regional_variants: Dict[str, str]
    cultural_significance: str
    seasonal_context: Optional[str] = None
    measurement_units: Optional[Dict[str, str]] = None

class DialectRecognitionService:
    """Advanced dialect recognition and cultural context processing"""
    
    def __init__(self):
        # Comprehensive agricultural terminology database
        self.agricultural_terms = {
            "rice": AgriculturalTerm(
                standard_term="rice",
                regional_variants={
                    "hindi": "चावल (chawal), धान (dhan)",
                    "telugu": "బియ్యం (biyyam), వరి (vari)",
                    "tamil": "அரிசி (arisi), நெல் (nel)",
                    "kannada": "ಅಕ್ಕಿ (akki), ಧಾನ್ಯ (dhanya)",
                    "malayalam": "അരി (ari), നെല്ല് (nellu)",
                    "bengali": "চাল (chal), ধান (dhan)",
                    "marathi": "तांदूळ (tandool), भात (bhat)",
                    "gujarati": "ચોખા (chokha), ધાન (dhan)"
                },
                cultural_significance="Staple food, used in religious ceremonies",
                seasonal_context="Kharif crop (monsoon season)",
                measurement_units={
                    "north": "quintal, maund",
                    "south": "bag, quintal", 
                    "west": "quintal, candy",
                    "east": "maund, quintal"
                }
            ),
            "wheat": AgriculturalTerm(
                standard_term="wheat",
                regional_variants={
                    "hindi": "गेहूं (gehun), गोधूम (godhum)",
                    "telugu": "గోధుమ (godhuma)",
                    "tamil": "கோதுமை (kodhumai)",
                    "kannada": "ಗೋಧಿ (godhi)",
                    "malayalam": "ഗോതമ്പ് (gothambu)",
                    "bengali": "গম (gom)",
                    "marathi": "गहू (gahu)",
                    "gujarati": "ઘઉં (ghaun)"
                },
                cultural_significance="Primary grain for bread, festival significance",
                seasonal_context="Rabi crop (winter season)"
            ),
            "onion": AgriculturalTerm(
                standard_term="onion",
                regional_variants={
                    "hindi": "प्याज (pyaz), कांदा (kanda)",
                    "telugu": "ఉల్లిపాయ (ullipaya), వెంగాయం (vengayam)",
                    "tamil": "வெங்காயம் (vengayam)",
                    "kannada": "ಈರುಳ್ಳಿ (eerulli)",
                    "malayalam": "സവാള (saval), ഉള്ളി (ulli)",
                    "bengali": "পেঁয়াজ (peyaj)",
                    "marathi": "कांदा (kanda)",
                    "gujarati": "ડુંગળી (dungali)"
                },
                cultural_significance="Essential cooking ingredient, price sensitive",
                seasonal_context="Multiple seasons, storage dependent"
            ),
            "potato": AgriculturalTerm(
                standard_term="potato",
                regional_variants={
                    "hindi": "आलू (aloo), बटाटा (batata)",
                    "telugu": "బంగాళాదుంప (bangaladumpa), ఆలూగడ్డ (alugadda)",
                    "tamil": "உருளைக்கிழங்கு (urulaikizhangu)",
                    "kannada": "ಆಲೂಗಡ್ಡೆ (alugadde)",
                    "malayalam": "ഉരുളക്കിഴങ്ങ് (urulakizhangu)",
                    "bengali": "আলু (alu)",
                    "marathi": "बटाटा (batata)",
                    "gujarati": "બટાકા (bataka)"
                },
                cultural_significance="Versatile vegetable, storage crop",
                seasonal_context="Cool season crop, good storage"
            ),
            "tomato": AgriculturalTerm(
                standard_term="tomato",
                regional_variants={
                    "hindi": "टमाटर (tamatar)",
                    "telugu": "టమాటో (tamato), టక్కాలి (takkali)",
                    "tamil": "தக்காளி (thakkali)",
                    "kannada": "ಟೊಮೇಟೊ (tometo)",
                    "malayalam": "തക്കാളി (thakkali)",
                    "bengali": "টমেটো (tometo)",
                    "marathi": "टोमॅटो (tomato)",
                    "gujarati": "ટમેટા (tameta)"
                },
                cultural_significance="Essential cooking ingredient, high perishability",
                seasonal_context="Multiple seasons, weather sensitive"
            ),
            "cotton": AgriculturalTerm(
                standard_term="cotton",
                regional_variants={
                    "hindi": "कपास (kapas), रुई (rui)",
                    "telugu": "పత్తి (patti), కార్పాస్ (karpas)",
                    "tamil": "பருத்தி (paruthi)",
                    "kannada": "ಹತ್ತಿ (hatti)",
                    "malayalam": "പരുത്തി (paruthi)",
                    "bengali": "তুলা (tula)",
                    "marathi": "कापूस (kapus)",
                    "gujarati": "કપાસ (kapas)"
                },
                cultural_significance="Cash crop, textile industry importance",
                seasonal_context="Kharif crop, export commodity"
            )
        }
        
        # Dialect markers and patterns
        self.dialect_patterns = {
            "hindi_north": {
                "markers": ["जी हाँ", "अच्छा", "ठीक है", "क्या भाव", "दाम क्या"],
                "region": DialectRegion.NORTH_INDIA,
                "formal_indicators": ["आप", "जी", "कृपया"],
                "informal_indicators": ["तू", "तुम", "यार"]
            },
            "hindi_west": {
                "markers": ["काय", "बरं", "चांगलं", "किती भाव", "दर काय"],
                "region": DialectRegion.WEST_INDIA,
                "formal_indicators": ["तुम्ही", "साहेब"],
                "informal_indicators": ["तू", "रे"]
            },
            "telugu": {
                "markers": ["అవును", "సరే", "ఎంత రేట్", "ధర ఎంత", "బాగుంది"],
                "region": DialectRegion.SOUTH_INDIA,
                "formal_indicators": ["మీరు", "గారు", "దయచేసి"],
                "informal_indicators": ["నువ్వు", "రా", "రే"]
            },
            "tamil": {
                "markers": ["ஆமாம்", "சரி", "எவ்வளவு விலை", "நல்லது", "பரவாயில்லை"],
                "region": DialectRegion.SOUTH_INDIA,
                "formal_indicators": ["நீங்கள்", "ஐயா", "தயவுசெய்து"],
                "informal_indicators": ["நீ", "டா", "டி"]
            },
            "kannada": {
                "markers": ["ಹೌದು", "ಸರಿ", "ಎಷ್ಟು ದರ", "ಬೆಲೆ ಎಷ್ಟು", "ಚೆನ್ನಾಗಿದೆ"],
                "region": DialectRegion.SOUTH_INDIA,
                "formal_indicators": ["ನೀವು", "ಸರ್", "ದಯವಿಟ್ಟು"],
                "informal_indicators": ["ನೀನು", "ರಾ", "ರೀ"]
            },
            "malayalam": {
                "markers": ["അതെ", "ശരി", "എത്ര വില", "നല്ലത്", "കുഴപ്പമില്ല"],
                "region": DialectRegion.SOUTH_INDIA,
                "formal_indicators": ["നിങ്ങൾ", "സാർ", "ദയവായി"],
                "informal_indicators": ["നീ", "ടാ", "ടി"]
            }
        }
        
        # Regional measurement units
        self.regional_units = {
            DialectRegion.NORTH_INDIA: {
                "weight": ["quintal", "maund", "ser", "kg"],
                "area": ["bigha", "acre", "hectare"],
                "volume": ["liter", "gallon"]
            },
            DialectRegion.SOUTH_INDIA: {
                "weight": ["quintal", "bag", "kg", "tonne"],
                "area": ["acre", "cent", "hectare"],
                "volume": ["liter", "kalash"]
            },
            DialectRegion.WEST_INDIA: {
                "weight": ["quintal", "candy", "kg", "maund"],
                "area": ["acre", "guntha", "hectare"],
                "volume": ["liter", "pot"]
            },
            DialectRegion.EAST_INDIA: {
                "weight": ["maund", "quintal", "kg", "ser"],
                "area": ["bigha", "katha", "acre"],
                "volume": ["liter", "gallon"]
            }
        }
        
        # Cultural context patterns
        self.cultural_contexts = {
            "festival_seasons": {
                "diwali": {"months": [10, 11], "impact": "increased_demand", "products": ["rice", "wheat", "sugar"]},
                "harvest": {"months": [3, 4, 10, 11], "impact": "supply_increase", "products": ["wheat", "rice", "cotton"]},
                "monsoon": {"months": [6, 7, 8, 9], "impact": "price_volatility", "products": ["onion", "tomato", "potato"]}
            },
            "regional_preferences": {
                DialectRegion.NORTH_INDIA: {"staples": ["wheat", "rice"], "cash_crops": ["cotton", "sugarcane"]},
                DialectRegion.SOUTH_INDIA: {"staples": ["rice"], "cash_crops": ["cotton", "coconut", "spices"]},
                DialectRegion.WEST_INDIA: {"staples": ["wheat", "rice"], "cash_crops": ["cotton", "sugarcane", "onion"]},
                DialectRegion.EAST_INDIA: {"staples": ["rice"], "cash_crops": ["jute", "tea"]}
            }
        }
    
    async def detect_dialect(self, text: str, audio_features: Optional[Dict] = None) -> DialectMatch:
        """Detect dialect and regional context from text and optional audio features"""
        
        text_lower = text.lower()
        best_match = None
        highest_confidence = 0.0
        
        # Check each dialect pattern
        for dialect_key, pattern_info in self.dialect_patterns.items():
            confidence = 0.0
            matched_markers = []
            
            # Check for dialect markers
            for marker in pattern_info["markers"]:
                if marker.lower() in text_lower or self._transliterate_check(marker, text_lower):
                    confidence += 0.3
                    matched_markers.append(marker)
            
            # Check for formality indicators
            formal_score = sum(1 for indicator in pattern_info["formal_indicators"] 
                             if indicator.lower() in text_lower or self._transliterate_check(indicator, text_lower))
            informal_score = sum(1 for indicator in pattern_info["informal_indicators"] 
                                if indicator.lower() in text_lower or self._transliterate_check(indicator, text_lower))
            
            if formal_score > 0:
                confidence += 0.2
                matched_markers.extend(["formal_speech"])
            if informal_score > 0:
                confidence += 0.1
                matched_markers.extend(["informal_speech"])
            
            # Audio features boost (if available)
            if audio_features:
                confidence += self._analyze_audio_features(audio_features, dialect_key) * 0.2
            
            if confidence > highest_confidence:
                highest_confidence = confidence
                language = dialect_key.split('_')[0]
                
                # Get cultural context
                cultural_context = self._get_cultural_context(pattern_info["region"], text)
                
                best_match = DialectMatch(
                    language=language,
                    region=pattern_info["region"],
                    confidence=min(confidence, 1.0),
                    dialect_markers=matched_markers,
                    cultural_context=cultural_context
                )
        
        # Default to English if no strong match
        if not best_match or highest_confidence < 0.3:
            best_match = DialectMatch(
                language="english",
                region=DialectRegion.NORTH_INDIA,  # Default region
                confidence=0.5,
                dialect_markers=["english_default"],
                cultural_context={"formality": "neutral", "region": "general"}
            )
        
        return best_match
    
    def _transliterate_check(self, native_text: str, input_text: str) -> bool:
        """Check if transliterated version of native text appears in input"""
        # Simple transliteration mapping (in production, use proper transliteration library)
        transliteration_map = {
            "चावल": ["chawal", "chaval", "chaawal"],
            "गेहूं": ["gehun", "gehu", "gehoon"],
            "प्याज": ["pyaz", "pyaaz", "piaz"],
            "आलू": ["aloo", "alu", "aaloo"],
            "टमाटर": ["tamatar", "tomato", "tamater"],
            "कपास": ["kapas", "cotton", "rui"],
            "बियाम": ["biyyam", "rice", "vari"],
            "गोधुम": ["godhuma", "wheat", "godhumai"]
        }
        
        if native_text in transliteration_map:
            return any(variant in input_text for variant in transliteration_map[native_text])
        
        return False
    
    def _analyze_audio_features(self, audio_features: Dict, dialect_key: str) -> float:
        """Analyze audio features for dialect detection (mock implementation)"""
        # In production, this would analyze:
        # - Accent patterns
        # - Pronunciation variations
        # - Intonation patterns
        # - Speech rhythm
        
        confidence_boost = 0.0
        
        if "accent_score" in audio_features:
            # Mock accent scoring based on dialect
            regional_accents = {
                "hindi_north": 0.8,
                "hindi_west": 0.7,
                "telugu": 0.9,
                "tamil": 0.85,
                "kannada": 0.8,
                "malayalam": 0.75
            }
            expected_score = regional_accents.get(dialect_key, 0.5)
            actual_score = audio_features["accent_score"]
            confidence_boost = 1.0 - abs(expected_score - actual_score)
        
        return confidence_boost
    
    def _get_cultural_context(self, region: DialectRegion, text: str) -> Dict[str, Any]:
        """Extract cultural context from text and region"""
        
        context = {
            "region": region.value,
            "formality": "neutral",
            "agricultural_focus": [],
            "seasonal_context": None,
            "measurement_preferences": self.regional_units.get(region, {})
        }
        
        # Detect formality level
        formal_indicators = ["please", "sir", "madam", "kindly", "आप", "जी", "साहेब", "गारु", "ஐயா"]
        informal_indicators = ["bro", "yaar", "dude", "तू", "तुम", "నువ్వు", "நீ"]
        
        text_lower = text.lower()
        if any(indicator in text_lower for indicator in formal_indicators):
            context["formality"] = "formal"
        elif any(indicator in text_lower for indicator in informal_indicators):
            context["formality"] = "informal"
        
        # Detect agricultural focus
        for term_key, term_info in self.agricultural_terms.items():
            if term_key in text_lower:
                context["agricultural_focus"].append(term_key)
            
            # Check regional variants
            for lang, variants in term_info.regional_variants.items():
                if any(variant.split('(')[0].strip() in text_lower for variant in variants.split(',')):
                    context["agricultural_focus"].append(term_key)
        
        # Add regional preferences
        if region in self.cultural_contexts["regional_preferences"]:
            context["regional_staples"] = self.cultural_contexts["regional_preferences"][region]
        
        return context
    
    async def translate_agricultural_terms(
        self, 
        text: str, 
        source_dialect: DialectMatch, 
        target_language: str
    ) -> Dict[str, Any]:
        """Translate agricultural terms considering dialect and cultural context"""
        
        translations = {}
        cultural_adaptations = []
        
        # Find agricultural terms in text
        for term_key, term_info in self.agricultural_terms.items():
            if term_key in text.lower():
                # Get appropriate translation
                if target_language in term_info.regional_variants:
                    translations[term_key] = term_info.regional_variants[target_language]
                    
                    # Add cultural context
                    if term_info.cultural_significance:
                        cultural_adaptations.append({
                            "term": term_key,
                            "significance": term_info.cultural_significance,
                            "seasonal_context": term_info.seasonal_context
                        })
        
        # Regional unit conversions
        unit_conversions = {}
        if source_dialect.region in self.regional_units:
            source_units = self.regional_units[source_dialect.region]
            # Mock unit conversion logic
            for unit_type, units in source_units.items():
                unit_conversions[unit_type] = {
                    "preferred_units": units[:2],  # Top 2 preferred units
                    "conversion_note": f"Common {unit_type} units in {source_dialect.region.value}"
                }
        
        return {
            "original_text": text,
            "source_dialect": {
                "language": source_dialect.language,
                "region": source_dialect.region.value,
                "confidence": source_dialect.confidence
            },
            "target_language": target_language,
            "term_translations": translations,
            "cultural_adaptations": cultural_adaptations,
            "unit_conversions": unit_conversions,
            "formality_adaptation": self._adapt_formality(
                source_dialect.cultural_context.get("formality", "neutral"),
                target_language
            )
        }
    
    def _adapt_formality(self, source_formality: str, target_language: str) -> Dict[str, str]:
        """Adapt formality level for target language"""
        
        formality_adaptations = {
            "hindi": {
                "formal": "आप का उपयोग करें, जी लगाएं",
                "informal": "तुम/तू का उपयोग करें",
                "neutral": "सामान्य भाषा का उपयोग करें"
            },
            "telugu": {
                "formal": "మీరు, గారు का उपयोग करें",
                "informal": "నువ్వు का उपयोग करें",
                "neutral": "సాధారణ భాష का उपयोग करें"
            },
            "tamil": {
                "formal": "நீங்கள், ஐயா का उपयोग करें",
                "informal": "நீ का उपयोग करें", 
                "neutral": "சாதாரண மொழி का उपयोग करें"
            }
        }
        
        return formality_adaptations.get(target_language, {
            "formal": "Use respectful language",
            "informal": "Use casual language",
            "neutral": "Use standard language"
        }).get(source_formality, "Use appropriate language level")
    
    async def get_regional_market_context(self, region: DialectRegion, product: str) -> Dict[str, Any]:
        """Get regional market context for better price understanding"""
        
        context = {
            "region": region.value,
            "product": product,
            "market_characteristics": {},
            "seasonal_patterns": {},
            "cultural_factors": {}
        }
        
        # Regional market characteristics
        market_chars = {
            DialectRegion.NORTH_INDIA: {
                "major_markets": ["Delhi", "Chandigarh", "Ludhiana"],
                "trading_style": "formal_structured",
                "price_negotiation": "moderate",
                "preferred_units": ["quintal", "maund"]
            },
            DialectRegion.SOUTH_INDIA: {
                "major_markets": ["Chennai", "Bangalore", "Hyderabad"],
                "trading_style": "relationship_based",
                "price_negotiation": "high",
                "preferred_units": ["bag", "quintal"]
            },
            DialectRegion.WEST_INDIA: {
                "major_markets": ["Mumbai", "Pune", "Ahmedabad"],
                "trading_style": "business_focused",
                "price_negotiation": "moderate_high",
                "preferred_units": ["quintal", "candy"]
            }
        }
        
        context["market_characteristics"] = market_chars.get(region, {})
        
        # Product-specific regional context
        if product in self.agricultural_terms:
            term_info = self.agricultural_terms[product]
            context["cultural_factors"] = {
                "significance": term_info.cultural_significance,
                "seasonal_context": term_info.seasonal_context,
                "regional_variants": term_info.regional_variants
            }
        
        return context


# Global dialect recognition service instance
dialect_service = DialectRecognitionService()