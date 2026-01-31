"""
Regional Unit Conversion Service for Agricultural Trading
"""

from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
import re

class UnitCategory(Enum):
    WEIGHT = "weight"
    AREA = "area"
    VOLUME = "volume"
    LENGTH = "length"

@dataclass
class ConversionResult:
    original_value: float
    original_unit: str
    converted_value: float
    converted_unit: str
    conversion_factor: float
    regional_context: str
    confidence: float

@dataclass
class UnitDefinition:
    name: str
    category: UnitCategory
    base_conversion: float  # Conversion to standard unit (kg for weight, m² for area, etc.)
    regional_usage: List[str]
    common_names: List[str]
    cultural_context: str

class RegionalUnitConverter:
    """Comprehensive regional unit conversion for agricultural trading"""
    
    def __init__(self):
        # Comprehensive unit definitions
        self.unit_definitions = {
            # Weight units
            "quintal": UnitDefinition(
                name="quintal",
                category=UnitCategory.WEIGHT,
                base_conversion=100.0,  # 1 quintal = 100 kg
                regional_usage=["north_india", "west_india", "south_india", "central_india"],
                common_names=["quintal", "q", "qtl"],
                cultural_context="Standard agricultural trading unit across India"
            ),
            "maund": UnitDefinition(
                name="maund",
                category=UnitCategory.WEIGHT,
                base_conversion=37.32,  # 1 maund = 37.32 kg (varies by region)
                regional_usage=["north_india", "east_india"],
                common_names=["maund", "man", "मन"],
                cultural_context="Traditional North Indian weight unit"
            ),
            "ser": UnitDefinition(
                name="ser",
                category=UnitCategory.WEIGHT,
                base_conversion=0.933,  # 1 ser = 933 grams
                regional_usage=["north_india", "central_india"],
                common_names=["ser", "seer", "सेर"],
                cultural_context="Traditional small weight unit"
            ),
            "candy": UnitDefinition(
                name="candy",
                category=UnitCategory.WEIGHT,
                base_conversion=254.0,  # 1 candy = 254 kg (varies)
                regional_usage=["west_india", "south_india"],
                common_names=["candy", "kandi", "कैंडी"],
                cultural_context="Traditional South/West Indian large weight unit"
            ),
            "bag": UnitDefinition(
                name="bag",
                category=UnitCategory.WEIGHT,
                base_conversion=50.0,  # 1 bag = 50 kg (standard)
                regional_usage=["south_india", "east_india"],
                common_names=["bag", "bori", "बोरी"],
                cultural_context="Common packaging unit in South India"
            ),
            "tonne": UnitDefinition(
                name="tonne",
                category=UnitCategory.WEIGHT,
                base_conversion=1000.0,  # 1 tonne = 1000 kg
                regional_usage=["all_regions"],
                common_names=["tonne", "ton", "mt", "metric ton"],
                cultural_context="International standard for large quantities"
            ),
            
            # Area units
            "acre": UnitDefinition(
                name="acre",
                category=UnitCategory.AREA,
                base_conversion=4047.0,  # 1 acre = 4047 m²
                regional_usage=["all_regions"],
                common_names=["acre", "ac"],
                cultural_context="Standard land measurement unit"
            ),
            "hectare": UnitDefinition(
                name="hectare",
                category=UnitCategory.AREA,
                base_conversion=10000.0,  # 1 hectare = 10000 m²
                regional_usage=["all_regions"],
                common_names=["hectare", "ha"],
                cultural_context="Metric system land unit"
            ),
            "bigha": UnitDefinition(
                name="bigha",
                category=UnitCategory.AREA,
                base_conversion=2529.0,  # 1 bigha = 2529 m² (varies by region)
                regional_usage=["north_india", "east_india"],
                common_names=["bigha", "बीघा"],
                cultural_context="Traditional North Indian land unit"
            ),
            "guntha": UnitDefinition(
                name="guntha",
                category=UnitCategory.AREA,
                base_conversion=101.17,  # 1 guntha = 101.17 m²
                regional_usage=["west_india"],
                common_names=["guntha", "gunta", "गुंठा"],
                cultural_context="Traditional Maharashtra land unit"
            ),
            "cent": UnitDefinition(
                name="cent",
                category=UnitCategory.AREA,
                base_conversion=40.47,  # 1 cent = 40.47 m²
                regional_usage=["south_india"],
                common_names=["cent", "cents"],
                cultural_context="Common South Indian land unit"
            ),
            "katha": UnitDefinition(
                name="katha",
                category=UnitCategory.AREA,
                base_conversion=338.0,  # 1 katha = 338 m² (varies)
                regional_usage=["east_india"],
                common_names=["katha", "cottah", "कठा"],
                cultural_context="Traditional Bengali land unit"
            ),
            
            # Volume units
            "liter": UnitDefinition(
                name="liter",
                category=UnitCategory.VOLUME,
                base_conversion=1.0,  # Base unit
                regional_usage=["all_regions"],
                common_names=["liter", "litre", "l"],
                cultural_context="Standard liquid measurement"
            ),
            "gallon": UnitDefinition(
                name="gallon",
                category=UnitCategory.VOLUME,
                base_conversion=3.785,  # 1 gallon = 3.785 liters
                regional_usage=["north_india", "east_india"],
                common_names=["gallon", "gal"],
                cultural_context="Traditional liquid measurement"
            ),
            "kalash": UnitDefinition(
                name="kalash",
                category=UnitCategory.VOLUME,
                base_conversion=12.0,  # 1 kalash = 12 liters (approximate)
                regional_usage=["south_india"],
                common_names=["kalash", "kalasa", "कलश"],
                cultural_context="Traditional South Indian volume unit"
            ),
            "pot": UnitDefinition(
                name="pot",
                category=UnitCategory.VOLUME,
                base_conversion=10.0,  # 1 pot = 10 liters (approximate)
                regional_usage=["west_india"],
                common_names=["pot", "ghada", "घड़ा"],
                cultural_context="Traditional water/grain storage unit"
            )
        }
        
        # Regional preferences mapping
        self.regional_preferences = {
            "north_india": {
                UnitCategory.WEIGHT: ["quintal", "maund", "ser", "kg"],
                UnitCategory.AREA: ["bigha", "acre", "hectare"],
                UnitCategory.VOLUME: ["liter", "gallon"]
            },
            "south_india": {
                UnitCategory.WEIGHT: ["quintal", "bag", "candy", "kg"],
                UnitCategory.AREA: ["acre", "cent", "hectare"],
                UnitCategory.VOLUME: ["liter", "kalash"]
            },
            "west_india": {
                UnitCategory.WEIGHT: ["quintal", "candy", "kg"],
                UnitCategory.AREA: ["acre", "guntha", "hectare"],
                UnitCategory.VOLUME: ["liter", "pot"]
            },
            "east_india": {
                UnitCategory.WEIGHT: ["maund", "quintal", "bag", "kg"],
                UnitCategory.AREA: ["bigha", "katha", "acre"],
                UnitCategory.VOLUME: ["liter", "gallon"]
            },
            "central_india": {
                UnitCategory.WEIGHT: ["quintal", "maund", "ser", "kg"],
                UnitCategory.AREA: ["acre", "bigha", "hectare"],
                UnitCategory.VOLUME: ["liter", "gallon"]
            }
        }
        
        # Colloquial term mappings
        self.colloquial_mappings = {
            # Hindi colloquial terms
            "किलो": "kg",
            "क्विंटल": "quintal",
            "मन": "maund",
            "सेर": "ser",
            "बोरी": "bag",
            "एकड़": "acre",
            "बीघा": "bigha",
            "लीटर": "liter",
            
            # Telugu colloquial terms
            "కిలో": "kg",
            "క్వింటల్": "quintal",
            "బ్యాగ్": "bag",
            "ఎకరం": "acre",
            "లీటర్": "liter",
            
            # Tamil colloquial terms
            "கிலோ": "kg",
            "குவிண்டல்": "quintal",
            "பை": "bag",
            "ஏக்கர்": "acre",
            "லிட்டர்": "liter",
            
            # Kannada colloquial terms
            "ಕಿಲೋ": "kg",
            "ಕ್ವಿಂಟಲ್": "quintal",
            "ಬ್ಯಾಗ್": "bag",
            "ಎಕರೆ": "acre",
            "ಲೀಟರ್": "liter",
            
            # Common abbreviations and variations
            "qtl": "quintal",
            "q": "quintal",
            "mt": "tonne",
            "ha": "hectare",
            "ac": "acre",
            "l": "liter",
            "gal": "gallon"
        }
        
        # Product-specific unit preferences
        self.product_unit_preferences = {
            "rice": {
                "primary": ["quintal", "bag", "tonne"],
                "regional_variations": {
                    "north_india": ["quintal", "maund"],
                    "south_india": ["bag", "quintal"],
                    "west_india": ["quintal", "candy"],
                    "east_india": ["maund", "quintal"]
                }
            },
            "wheat": {
                "primary": ["quintal", "tonne"],
                "regional_variations": {
                    "north_india": ["quintal", "maund"],
                    "south_india": ["quintal", "bag"],
                    "west_india": ["quintal"],
                    "east_india": ["maund", "quintal"]
                }
            },
            "onion": {
                "primary": ["quintal", "bag"],
                "regional_variations": {
                    "north_india": ["quintal", "maund"],
                    "south_india": ["bag", "quintal"],
                    "west_india": ["quintal"],
                    "east_india": ["quintal", "bag"]
                }
            },
            "cotton": {
                "primary": ["quintal", "candy", "bale"],
                "regional_variations": {
                    "north_india": ["quintal"],
                    "south_india": ["candy", "quintal"],
                    "west_india": ["candy", "quintal"],
                    "east_india": ["quintal"]
                }
            }
        }
    
    def parse_quantity_text(self, text: str) -> List[Tuple[float, str, float]]:
        """Parse text to extract quantities with units"""
        
        # Patterns to match quantity expressions
        patterns = [
            r'(\d+(?:\.\d+)?)\s*([a-zA-Z]+)',  # "100 quintal"
            r'(\d+(?:\.\d+)?)\s*([a-zA-Zा-ह०-९]+)',  # "100 क्विंटल"
            r'(\d+(?:\.\d+)?)\s*([కా-హ౦-౯]+)',  # Telugu units
            r'(\d+(?:\.\d+)?)\s*([கா-ஹ௦-௯]+)',  # Tamil units
            r'(\d+(?:\.\d+)?)\s*([ಕಾ-ಹ೦-೯]+)',  # Kannada units
        ]
        
        results = []
        text_lower = text.lower()
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                try:
                    value = float(match[0])
                    unit_text = match[1].strip()
                    
                    # Normalize unit
                    normalized_unit = self._normalize_unit(unit_text)
                    if normalized_unit:
                        confidence = self._calculate_parse_confidence(unit_text, normalized_unit)
                        results.append((value, normalized_unit, confidence))
                except ValueError:
                    continue
        
        return results
    
    def _normalize_unit(self, unit_text: str) -> Optional[str]:
        """Normalize unit text to standard unit name"""
        
        unit_lower = unit_text.lower().strip()
        
        # Direct mapping
        if unit_lower in self.colloquial_mappings:
            return self.colloquial_mappings[unit_lower]
        
        # Check unit definitions
        for unit_name, unit_def in self.unit_definitions.items():
            if unit_lower in [name.lower() for name in unit_def.common_names]:
                return unit_name
        
        # Fuzzy matching for common variations
        fuzzy_matches = {
            "quintal": ["quintal", "quntal", "kwintal", "kwintl"],
            "maund": ["maund", "mand", "mann", "mon"],
            "acre": ["acre", "acer", "aker"],
            "hectare": ["hectare", "hector", "hektare"],
            "liter": ["liter", "litre", "ltr"],
            "kg": ["kg", "kilo", "kilogram"]
        }
        
        for standard_unit, variations in fuzzy_matches.items():
            if any(var in unit_lower for var in variations):
                return standard_unit
        
        return None
    
    def _calculate_parse_confidence(self, original_unit: str, normalized_unit: str) -> float:
        """Calculate confidence in unit parsing"""
        
        if original_unit.lower() == normalized_unit.lower():
            return 1.0
        
        if original_unit.lower() in self.colloquial_mappings:
            return 0.9
        
        # Check if it's a common name
        if normalized_unit in self.unit_definitions:
            unit_def = self.unit_definitions[normalized_unit]
            if original_unit.lower() in [name.lower() for name in unit_def.common_names]:
                return 0.85
        
        return 0.7  # Fuzzy match confidence
    
    def convert_units(
        self, 
        value: float, 
        from_unit: str, 
        to_unit: str,
        region: Optional[str] = None
    ) -> ConversionResult:
        """Convert between units with regional context"""
        
        from_unit_norm = self._normalize_unit(from_unit)
        to_unit_norm = self._normalize_unit(to_unit)
        
        if not from_unit_norm or not to_unit_norm:
            raise ValueError(f"Unknown unit: {from_unit} or {to_unit}")
        
        if from_unit_norm not in self.unit_definitions or to_unit_norm not in self.unit_definitions:
            raise ValueError(f"Unit not supported: {from_unit_norm} or {to_unit_norm}")
        
        from_def = self.unit_definitions[from_unit_norm]
        to_def = self.unit_definitions[to_unit_norm]
        
        # Check if units are in same category
        if from_def.category != to_def.category:
            raise ValueError(f"Cannot convert between {from_def.category.value} and {to_def.category.value}")
        
        # Convert via base unit
        base_value = value * from_def.base_conversion
        converted_value = base_value / to_def.base_conversion
        conversion_factor = from_def.base_conversion / to_def.base_conversion
        
        # Regional context
        regional_context = self._get_regional_context(from_unit_norm, to_unit_norm, region)
        
        # Calculate confidence
        confidence = self._calculate_conversion_confidence(from_unit_norm, to_unit_norm, region)
        
        return ConversionResult(
            original_value=value,
            original_unit=from_unit_norm,
            converted_value=round(converted_value, 4),
            converted_unit=to_unit_norm,
            conversion_factor=conversion_factor,
            regional_context=regional_context,
            confidence=confidence
        )
    
    def _get_regional_context(self, from_unit: str, to_unit: str, region: Optional[str]) -> str:
        """Get regional context for the conversion"""
        
        context_parts = []
        
        if region and region in self.regional_preferences:
            regional_prefs = self.regional_preferences[region]
            
            # Check if units are regionally appropriate
            from_def = self.unit_definitions[from_unit]
            to_def = self.unit_definitions[to_unit]
            
            category_prefs = regional_prefs.get(from_def.category, [])
            
            if from_unit in category_prefs:
                context_parts.append(f"{from_unit} is commonly used in {region}")
            
            if to_unit in category_prefs:
                context_parts.append(f"{to_unit} is preferred in {region}")
            else:
                # Suggest regional alternative
                if category_prefs:
                    context_parts.append(f"Consider using {category_prefs[0]} (common in {region})")
        
        # Add cultural context
        from_cultural = self.unit_definitions[from_unit].cultural_context
        to_cultural = self.unit_definitions[to_unit].cultural_context
        
        if from_cultural != to_cultural:
            context_parts.append(f"Converting from {from_cultural.lower()} to {to_cultural.lower()}")
        
        return " | ".join(context_parts) if context_parts else "Standard conversion"
    
    def _calculate_conversion_confidence(self, from_unit: str, to_unit: str, region: Optional[str]) -> float:
        """Calculate confidence in conversion accuracy"""
        
        base_confidence = 0.95  # High confidence for standard conversions
        
        # Reduce confidence for regional variations
        from_def = self.unit_definitions[from_unit]
        to_def = self.unit_definitions[to_unit]
        
        # Traditional units may have regional variations
        traditional_units = ["maund", "bigha", "katha", "guntha", "candy", "kalash", "pot"]
        
        if from_unit in traditional_units or to_unit in traditional_units:
            base_confidence -= 0.1  # Traditional units can vary by region
        
        # Boost confidence if units are regionally appropriate
        if region and region in self.regional_preferences:
            regional_prefs = self.regional_preferences[region]
            category_prefs = regional_prefs.get(from_def.category, [])
            
            if from_unit in category_prefs and to_unit in category_prefs:
                base_confidence += 0.05
        
        return min(base_confidence, 1.0)
    
    def get_regional_recommendations(
        self, 
        product: str, 
        region: str, 
        current_unit: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get unit recommendations for a product and region"""
        
        recommendations = {
            "product": product,
            "region": region,
            "recommended_units": [],
            "current_unit_analysis": None,
            "conversion_suggestions": []
        }
        
        # Get product-specific recommendations
        if product in self.product_unit_preferences:
            product_prefs = self.product_unit_preferences[product]
            
            if region in product_prefs["regional_variations"]:
                recommendations["recommended_units"] = product_prefs["regional_variations"][region]
            else:
                recommendations["recommended_units"] = product_prefs["primary"]
        
        # Get general regional preferences
        elif region in self.regional_preferences:
            # Assume weight category for agricultural products
            recommendations["recommended_units"] = self.regional_preferences[region][UnitCategory.WEIGHT]
        
        # Analyze current unit if provided
        if current_unit:
            normalized_unit = self._normalize_unit(current_unit)
            if normalized_unit and normalized_unit in self.unit_definitions:
                unit_def = self.unit_definitions[normalized_unit]
                
                recommendations["current_unit_analysis"] = {
                    "unit": normalized_unit,
                    "category": unit_def.category.value,
                    "regional_appropriateness": region in unit_def.regional_usage or "all_regions" in unit_def.regional_usage,
                    "cultural_context": unit_def.cultural_context
                }
                
                # Suggest conversions to recommended units
                for rec_unit in recommendations["recommended_units"][:3]:  # Top 3 recommendations
                    if rec_unit != normalized_unit:
                        try:
                            conversion = self.convert_units(1.0, normalized_unit, rec_unit, region)
                            recommendations["conversion_suggestions"].append({
                                "to_unit": rec_unit,
                                "conversion_factor": conversion.conversion_factor,
                                "example": f"1 {normalized_unit} = {conversion.converted_value} {rec_unit}",
                                "confidence": conversion.confidence
                            })
                        except ValueError:
                            continue
        
        return recommendations
    
    def detect_and_convert_text(
        self, 
        text: str, 
        target_region: str,
        product: Optional[str] = None
    ) -> Dict[str, Any]:
        """Detect quantities in text and suggest regional conversions"""
        
        # Parse quantities from text
        parsed_quantities = self.parse_quantity_text(text)
        
        results = {
            "original_text": text,
            "target_region": target_region,
            "detected_quantities": [],
            "conversion_suggestions": [],
            "regional_context": {}
        }
        
        for value, unit, confidence in parsed_quantities:
            quantity_info = {
                "value": value,
                "unit": unit,
                "parse_confidence": confidence
            }
            
            # Get regional recommendations for this unit
            if product:
                recommendations = self.get_regional_recommendations(product, target_region, unit)
                quantity_info["recommendations"] = recommendations
                
                # Generate conversion suggestions
                for suggestion in recommendations["conversion_suggestions"]:
                    converted_value = value * suggestion["conversion_factor"]
                    results["conversion_suggestions"].append({
                        "original": f"{value} {unit}",
                        "converted": f"{converted_value:.2f} {suggestion['to_unit']}",
                        "explanation": f"In {target_region}, {suggestion['to_unit']} is commonly used",
                        "confidence": suggestion["confidence"]
                    })
            
            results["detected_quantities"].append(quantity_info)
        
        # Add regional context
        if target_region in self.regional_preferences:
            results["regional_context"] = {
                "preferred_units": self.regional_preferences[target_region],
                "cultural_notes": f"Units commonly used in {target_region}"
            }
        
        return results


# Global unit converter instance
unit_converter = RegionalUnitConverter()