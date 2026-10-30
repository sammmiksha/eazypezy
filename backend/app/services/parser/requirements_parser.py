"""Rule-based query understanding for product discovery.

The parser separates *must haves* from *preferences*. A request such as
"5G phone under 40,000 with the best screen" removes non-5G offers before
ranking the remaining phones by display quality and price.
"""
import datetime
import re
from typing import Dict, Optional, Tuple

from app.schemas.search import ExtractedAttributes, ParsedSearchRequest


KNOWN_COLORS = [
    "natural titanium", "navy blue", "royal blue", "bottle green", "emerald",
    "magenta", "purple", "violet", "maroon", "mustard", "golden", "silver",
    "pink", "blue", "teal", "green", "yellow", "black", "white", "cream",
    "beige", "orange", "peach", "grey", "brown",
]

BRANDS = {
    "apple": "Apple", "samsung": "Samsung", "oneplus": "OnePlus",
    "google": "Google", "xiaomi": "Xiaomi", "redmi": "Redmi", "nothing": "Nothing",
    "sony": "Sony", "nike": "Nike", "adidas": "Adidas", "puma": "Puma",
    "dyson": "Dyson", "dell": "Dell", "hp": "HP", "lenovo": "Lenovo",
    "asus": "ASUS", "mitera": "Mitera", "suta": "Suta",
}

MONTH_NAMES = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}


def _amount(value: str, unit: Optional[str]) -> float:
    number = float(value.replace(",", ""))
    unit = (unit or "").lower()
    if unit in {"k", "thousand"}:
        return number * 1_000
    if unit in {"l", "lakh", "lakhs"}:
        return number * 100_000
    return number


def parse_budget(text: str) -> Tuple[Optional[float], Optional[float]]:
    """Extract INR budgets without confusing 5G or dates for money."""
    amount = r"(?:₹|rs\.?|inr)?\s*(\d{1,3}(?:,\d{2,3})+|\d+(?:\.\d+)?)\s*(k|thousand|lakh|lakhs)?"
    range_match = re.search(rf"(?:between|from)\s*{amount}\s*(?:and|to|-)\s*{amount}", text, re.I)
    if range_match:
        low = _amount(range_match.group(1), range_match.group(2))
        high = _amount(range_match.group(3), range_match.group(4))
        return min(low, high), max(low, high)

    maximum = re.search(
        rf"(?:under|below|less\s+than|up\s*to|upto|budget(?:\s+(?:of|is|around|under|up\s*to))?|for|around)\s*{amount}",
        text,
        re.I,
    )
    if maximum:
        return None, _amount(maximum.group(1), maximum.group(2))

    explicit = re.search(rf"{amount}\s*(?:rs\.?|rupees|inr)\b", text, re.I)
    if explicit:
        return None, _amount(explicit.group(1), explicit.group(2))
    return None, None


def parse_deadline_days(text: str) -> Optional[int]:
    today = datetime.date.today()
    date_match = re.search(
        r"\b(?:by|before|on|delivered by|deliver by)?\s*(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?([a-z]+)\b",
        text,
        re.I,
    )
    if date_match and date_match.group(2).lower() in MONTH_NAMES:
        month = MONTH_NAMES[date_match.group(2).lower()]
        year = today.year + (month < today.month)
        try:
            days = (datetime.date(year, month, int(date_match.group(1))) - today).days
            if days >= 0:
                return max(days, 1)
        except ValueError:
            pass
    days_match = re.search(r"(?:in|within|deliver in|by)\s*(\d+)\s*days?", text, re.I)
    if days_match:
        return int(days_match.group(1))
    if "tomorrow" in text or "next day" in text:
        return 1
    return None


def _category_and_model(text: str) -> Tuple[str, Optional[str]]:
    if re.search(r"\b(phone|smartphone|iphone|android)\b", text):
        iphone = re.search(r"\biphone\s*(\d+(?:\s*(?:pro\s*max|pro|plus))?)?", text, re.I)
        return "smartphones", f"iPhone {iphone.group(1).title()}" if iphone and iphone.group(1) else None
    if re.search(r"\b(headphones?|earphones?|earbuds?)\b", text):
        return "audio", "WH-1000XM5" if re.search(r"\b(?:xm5|wh-1000xm5)\b", text, re.I) else None
    if re.search(r"\b(laptop|macbook|notebook)\b", text):
        return "laptops", "MacBook Air" if "macbook" in text else None
    if re.search(r"\b(tv|television)\b", text):
        return "television", None
    if re.search(r"\b(shirt|t-?shirt|jeans|trousers?|pants|saree|sari|kurti|kurta|dress|jacket|hoodie|shoes?|sneakers?|sandals?|heels?|blazer|suit)\b", text):
        return "clothing", None
    if re.search(r"\b(fridge|refrigerator|washing machine|air conditioner|ac|microwave|vacuum)\b", text):
        return "appliances", None
    return "general", None


def _specifications(text: str) -> Tuple[Dict[str, object], Dict[str, object], Dict[str, object]]:
    """Return visible specs, strict requirements, and weighted preferences."""
    specs: Dict[str, object] = {}
    required: Dict[str, object] = {}
    preferred: Dict[str, object] = {}

    if re.search(r"\b5\s*g\b", text, re.I):
        specs["network"] = "5G"
        required["network"] = "5G"
    if re.search(r"\b4\s*g\b", text, re.I) and "network" not in specs:
        specs["network"] = "4G"
        required["network"] = "4G"

    storage = re.search(r"\b(64|128|256|512)\s*(gb)\b|\b(1|2)\s*(tb)\b", text, re.I)
    if storage:
        storage_value = f"{storage.group(1) or storage.group(3)}{(storage.group(2) or storage.group(4)).upper()}"
        specs["storage"] = storage_value
        required["storage"] = storage_value

    ram = re.search(r"\b(4|6|8|12|16)\s*gb\s*(?:ram|memory)\b", text, re.I)
    if ram:
        specs["ram"] = f"{ram.group(1)}GB"
        required["ram"] = f"{ram.group(1)}GB"

    # Category-neutral measurements keep the parser useful for appliances,
    # furniture, fitness equipment, and many other product types.
    measurement = re.search(r"\b(\d+(?:\.\d+)?)\s*(kg|lit(?:re|er)s?|mah|watts?|w|inches|inch)\b", text, re.I)
    if measurement:
        amount, unit = measurement.group(1), measurement.group(2).lower()
        if unit == "kg" or unit.startswith("lit"):
            key, value = "capacity", f"{amount}{'kg' if unit == 'kg' else 'L'}"
        elif unit == "mah":
            key, value = "battery_capacity", f"{amount}mAh"
        elif unit in {"w", "watt", "watts"}:
            key, value = "wattage", f"{amount}W"
        else:
            key, value = "size", f"{amount} inch"
        specs[key] = value
        required[key] = value

    if re.search(r"\bfront[ -]?load\b", text, re.I):
        specs["loading"] = "front load"
        required["loading"] = "front load"
    fabric = re.search(r"\b(cotton|silk|wool|leather|linen|denim|polyester)\b", text, re.I)
    if fabric:
        specs["fabric"] = fabric.group(1).lower()
        required["fabric"] = fabric.group(1).lower()
    for feature in ("ergonomic", "quiet", "waterproof", "wireless", "foldable", "portable"):
        if re.search(rf"\b{feature}\b", text, re.I):
            key = f"feature_{feature}"
            specs[key] = True
            required[key] = True

    refresh = re.search(r"\b(60|90|120|144)\s*hz\b", text, re.I)
    if refresh:
        specs["refresh_rate_hz"] = int(refresh.group(1))
        required["refresh_rate_hz"] = int(refresh.group(1))

    display_type = re.search(r"\b(amoled|oled|ltpo|lcd)\b", text, re.I)
    if display_type:
        specs["display"] = display_type.group(1).upper()
        required["display"] = display_type.group(1).upper()
    if re.search(r"\b(best|great|top|excellent)\s+(?:screen|display)|\bbest display\b", text, re.I):
        specs["screen_priority"] = "best"
        preferred["display_priority"] = "best"
    if re.search(r"\b(best|great|top|excellent)\s+camera\b", text, re.I):
        preferred["camera_priority"] = "best"
    if re.search(r"\b(best|long|strong)\s+battery\b|\blong battery\b", text, re.I):
        preferred["battery_priority"] = "best"
    if re.search(r"\b(gaming|fast|powerful|performance)\b", text, re.I):
        preferred["performance_priority"] = "high"
    if re.search(r"\b(best|high)\s+rated\b", text, re.I):
        preferred["rating_priority"] = "high"
    return specs, required, preferred


def fallback_universal_parser(query: str) -> ParsedSearchRequest:
    text = query.lower().strip()
    budget_min, budget_max = parse_budget(text)
    category, model_name = _category_and_model(text)

    color = next((color for color in KNOWN_COLORS if re.search(rf"\b{re.escape(color)}\b", text)), None)
    brand = next((display for token, display in BRANDS.items() if re.search(rf"\b{re.escape(token)}\b", text)), None)
    if "iphone" in text:
        brand = "Apple"

    specs, required_specs, preferred_specs = _specifications(text)
    if color:
        specs["color"] = color.title()

    pin = re.search(r"\b([1-9][0-9]{5})\b", text)
    clean_search_phrase = " ".join(part for part in [brand, model_name, category if category != "general" else None] if part)
    if not clean_search_phrase:
        clean_search_phrase = re.sub(r"\b(?:under|below|budget|best|screen|display|with|and|for|in|of|the|a|an)\b", " ", text)
        clean_search_phrase = re.sub(r"\s+", " ", clean_search_phrase).strip()

    language = "hi" if any(word in text for word in ["chahiye", "sasta", "sabse", "batao", "mujhe"]) else "en"
    clarifications = []
    if budget_max is None:
        clarifications.append("Add a budget to compare the best value across stores.")

    return ParsedSearchRequest(
        raw_query=query,
        detected_language=language,
        translated_query=clean_search_phrase,
        clean_search_phrase=clean_search_phrase,
        attributes=ExtractedAttributes(
            category=category,
            brand=brand,
            model_name=model_name,
            specs=specs,
            required_specs=required_specs,
            preferred_specs=preferred_specs,
            color=color,
        ),
        budget_min=budget_min,
        budget_max=budget_max,
        deadline_days=parse_deadline_days(text),
        pincode=pin.group(1) if pin else None,
        sort_by="relevance",
        clarifications_needed=clarifications,
    )


async def extract_search_intent(query: str) -> ParsedSearchRequest:
    """Public parser hook; an LLM provider can replace this without API changes."""
    return fallback_universal_parser(query)
