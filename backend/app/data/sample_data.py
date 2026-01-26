"""
Sample mandi data for OpenMandi
"""

from datetime import date, timedelta
import random
from typing import List, Dict

# Sample products with regional names
SAMPLE_PRODUCTS = [
    {
        "name": "Rice",
        "category": "grains",
        "regional_names": {
            "hi": "चावल",
            "te": "బియ్యం",
            "ta": "அரிசி",
            "kn": "ಅಕ್ಕಿ",
            "ml": "അരി"
        },
        "seasonal_availability": [1, 2, 3, 10, 11, 12],
        "standard_units": ["quintal", "kg", "bag"],
        "quality_grades": ["premium", "good", "average"]
    },
    {
        "name": "Wheat",
        "category": "grains",
        "regional_names": {
            "hi": "गेहूं",
            "te": "గోధుమ",
            "ta": "கோதுமை",
            "kn": "ಗೋಧಿ",
            "ml": "ഗോതമ്പ്"
        },
        "seasonal_availability": [3, 4, 5, 6],
        "standard_units": ["quintal", "kg", "bag"],
        "quality_grades": ["premium", "good", "average"]
    },
    {
        "name": "Onion",
        "category": "vegetables",
        "regional_names": {
            "hi": "प्याज",
            "te": "ఉల్లిపాయ",
            "ta": "வெங்காயம்",
            "kn": "ಈರುಳ್ಳಿ",
            "ml": "സവാള"
        },
        "seasonal_availability": [1, 2, 3, 10, 11, 12],
        "standard_units": ["quintal", "kg"],
        "quality_grades": ["premium", "good", "average", "below_average"]
    },
    {
        "name": "Potato",
        "category": "vegetables",
        "regional_names": {
            "hi": "आलू",
            "te": "బంగాళాదుంప",
            "ta": "உருளைக்கிழங்கு",
            "kn": "ಆಲೂಗಡ್ಡೆ",
            "ml": "ഉരുളക്കിഴങ്ങ്"
        },
        "seasonal_availability": [1, 2, 3, 11, 12],
        "standard_units": ["quintal", "kg"],
        "quality_grades": ["premium", "good", "average"]
    },
    {
        "name": "Tomato",
        "category": "vegetables",
        "regional_names": {
            "hi": "टमाटर",
            "te": "టమాటో",
            "ta": "தக்காளி",
            "kn": "ಟೊಮೇಟೊ",
            "ml": "തക്കാളി"
        },
        "seasonal_availability": [1, 2, 3, 4, 10, 11, 12],
        "standard_units": ["quintal", "kg"],
        "quality_grades": ["premium", "good", "average", "below_average"]
    },
    {
        "name": "Cotton",
        "category": "cash_crops",
        "regional_names": {
            "hi": "कपास",
            "te": "పత్తి",
            "ta": "பருத்தி",
            "kn": "ಹತ್ತಿ",
            "ml": "പരുത്തി"
        },
        "seasonal_availability": [10, 11, 12, 1, 2],
        "standard_units": ["quintal", "kg"],
        "quality_grades": ["premium", "good", "average"]
    },
    {
        "name": "Sugarcane",
        "category": "cash_crops",
        "regional_names": {
            "hi": "गन्ना",
            "te": "చెరకు",
            "ta": "கரும்பு",
            "kn": "ಕಬ್ಬು",
            "ml": "കരിമ്പ്"
        },
        "seasonal_availability": [1, 2, 3, 4, 11, 12],
        "standard_units": ["quintal", "ton"],
        "quality_grades": ["premium", "good", "average"]
    },
    {
        "name": "Turmeric",
        "category": "spices",
        "regional_names": {
            "hi": "हल्दी",
            "te": "పసుపు",
            "ta": "மஞ்சள்",
            "kn": "ಅರಿಶಿನ",
            "ml": "മഞ്ഞൾ"
        },
        "seasonal_availability": [1, 2, 3, 4],
        "standard_units": ["quintal", "kg"],
        "quality_grades": ["premium", "good", "average"]
    }
]

# Sample markets across India
SAMPLE_MARKETS = [
    {"name": "Azadpur Mandi", "state": "Delhi", "district": "Delhi"},
    {"name": "Vashi APMC", "state": "Maharashtra", "district": "Mumbai"},
    {"name": "Koyambedu Market", "state": "Tamil Nadu", "district": "Chennai"},
    {"name": "Yeshwanthpur Market", "state": "Karnataka", "district": "Bangalore"},
    {"name": "Gaddiannaram Market", "state": "Telangana", "district": "Hyderabad"},
    {"name": "Kochi Spices Market", "state": "Kerala", "district": "Kochi"},
    {"name": "Lasalgaon Market", "state": "Maharashtra", "district": "Nashik"},
    {"name": "Indore Mandi", "state": "Madhya Pradesh", "district": "Indore"},
    {"name": "Siliguri Market", "state": "West Bengal", "district": "Siliguri"},
    {"name": "Ludhiana Grain Market", "state": "Punjab", "district": "Ludhiana"}
]

# Base prices for products (per quintal in INR)
BASE_PRICES = {
    "Rice": {"min": 2000, "max": 3500, "modal": 2500},
    "Wheat": {"min": 1800, "max": 2800, "modal": 2200},
    "Onion": {"min": 1500, "max": 4000, "modal": 2500},
    "Potato": {"min": 1200, "max": 2500, "modal": 1800},
    "Tomato": {"min": 2000, "max": 6000, "modal": 3500},
    "Cotton": {"min": 5000, "max": 8000, "modal": 6200},
    "Sugarcane": {"min": 300, "max": 400, "modal": 350},
    "Turmeric": {"min": 8000, "max": 15000, "modal": 12000}
}


def generate_sample_mandi_data(days_back: int = 30) -> List[Dict]:
    """Generate sample mandi data for the last N days"""
    data = []
    
    for i in range(days_back):
        current_date = date.today() - timedelta(days=i)
        
        for product in SAMPLE_PRODUCTS:
            # Generate data for 3-5 random markets per product per day
            num_markets = random.randint(3, 5)
            selected_markets = random.sample(SAMPLE_MARKETS, num_markets)
            
            for market in selected_markets:
                base_price = BASE_PRICES[product["name"]]
                
                # Add seasonal and random variations
                seasonal_factor = 1.0
                if current_date.month in product["seasonal_availability"]:
                    seasonal_factor = random.uniform(0.8, 1.0)  # In season - lower prices
                else:
                    seasonal_factor = random.uniform(1.1, 1.4)  # Out of season - higher prices
                
                # Random daily variation
                daily_factor = random.uniform(0.9, 1.1)
                
                # Calculate prices
                modal_price = base_price["modal"] * seasonal_factor * daily_factor
                min_price = modal_price * random.uniform(0.85, 0.95)
                max_price = modal_price * random.uniform(1.05, 1.15)
                
                # Random arrival quantity
                arrival_qty = random.uniform(50, 500)
                
                record = {
                    "market_name": market["name"],
                    "state": market["state"],
                    "district": market["district"],
                    "product_name": product["name"],
                    "variety": f"{product['name']} Grade A",
                    "min_price": round(min_price, 2),
                    "max_price": round(max_price, 2),
                    "modal_price": round(modal_price, 2),
                    "date": current_date,
                    "arrival_quantity": round(arrival_qty, 2),
                    "unit": "quintal"
                }
                
                data.append(record)
    
    return data


def get_current_price_trends() -> Dict[str, Dict]:
    """Get current price trends for display"""
    trends = {}
    
    for product_name, base_price in BASE_PRICES.items():
        # Simulate current trend
        trend_direction = random.choice(["up", "down", "stable"])
        
        if trend_direction == "up":
            current_price = base_price["modal"] * random.uniform(1.05, 1.2)
            trend_symbol = "↑"
        elif trend_direction == "down":
            current_price = base_price["modal"] * random.uniform(0.8, 0.95)
            trend_symbol = "↓"
        else:
            current_price = base_price["modal"] * random.uniform(0.95, 1.05)
            trend_symbol = "→"
        
        trends[product_name] = {
            "current_price": round(current_price, 2),
            "trend": trend_direction,
            "trend_symbol": trend_symbol,
            "unit": "quintal"
        }
    
    return trends