import json
import os

TEMPLATES_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "templates.json")

def load_templates():
    """Load message templates from JSON file"""
    try:
        with open(TEMPLATES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print("  Warning: templates.json not found, using default message")
        return {}
    except json.JSONDecodeError:
        print("  Warning: templates.json is invalid, using default message")
        return {}


def detect_category(business_name):
    """Detect business category from business name keywords"""
    name_lower = business_name.lower()

    if any(word in name_lower for word in ["restaurant", "cafe", "food", "kitchen", "bakery", "hotel"]):
        return "restaurant"
    elif any(word in name_lower for word in ["hardware", "tools", "steel", "iron"]):
        return "hardware"
    elif any(word in name_lower for word in ["shop", "store", "retail", "mart", "bazaar"]):
        return "retail"
    elif any(word in name_lower for word in ["it", "tech", "software", "digital", "computer"]):
        return "it"
    else:
        return "default"


def generate_message(name, business_name):
    """Generate personalized message based on business category"""
    templates = load_templates()
    category = detect_category(business_name)

    # fall back to default if category not in templates
    template = templates.get(category) or templates.get("default")

    # fall back to hardcoded if templates.json is missing entirely
    if not template:
        return (
            f"Dear {name}, "
            f"Exciting offers are now available for {business_name}! "
            f"Call us at 9811111111 or visit our website "
            f"to learn more. Reply STOP to unsubscribe."
        )

    return template.format(name=name, business_name=business_name)