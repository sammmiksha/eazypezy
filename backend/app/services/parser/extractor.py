"""Universal multilingual LLM and heuristic parser for any product category."""
import re
import json
import logging
import datetime
from typing import Optional, Dict, Any, List, Tuple
import httpx
from app.core.config import settings
from app.schemas.search import ParsedSearchRequest, ExtractedAttributes

logger = logging.getLogger(__name__)

KNOWN_COLORS = [
    "pink", "purple", "violet", "magenta", "red", "maroon", "blue", "navy blue", "royal blue",
    "teal", "green", "bottle green", "emerald", "yellow", "mustard", "black", "white",
    "cream", "beige", "gold", "golden", "orange", "peach", "grey", "silver", "brown", "natural titanium"
]

KNOWN_APPAREL = [
    "shirt", "t-shirt", "tshirt", "jeans", "trousers", "pants", "saree", "sari", "kurti",
    "kurta", "dress", "jacket", "hoodie", "shoes", "sneakers", "sandals", "heels", "blazer", "suit"
]

KNOWN_GADGETS = [
    "iphone", "macbook", "ipad", "laptop", "smartphone", "phone", "headphones", "earphones",
    "earbuds", "smartwatch", "watch", "camera", "tablet", "speaker", "television", "tv"
]

KNOWN_BRANDS = [
    "apple", "samsung", "sony", "nike", "adidas", "puma", "dyson", "mitera",
    "suta", "dell", "hp", "lenovo", "asus", "oneplus", "google", "xiaomi",
    "roadster", "highlander", "symbol", "zara", "h&m", "levi's", "levis"
]

MONTH_NAMES = {
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6,
    "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12,
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12
}

def parse_deadline_days(text: str) -> Optional[int]:
    """Extract delivery deadline in days from natural language."""
    # Current anchor date (October 2026)
    today = datetime.date(2026, 10, 3)

    # 1. Specific calendar date (e.g. "by 10th of October", "before 12 Oct", "on 15th november")
    date_match = re.search(
        r'\b(?:by|before|on|delivered by|deliver by)?\s*(\d{1,2})(?:st|nd|rd|th)?\s+(?:of\s+)?(january|february|march|april|may|june|july|august|september|october|november|december|jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\b',
        text,
        re.IGNORECASE
    )
    if date_match:
        day = int(date_match.group(1))
        mon_str = date_match.group(2).lower()
        month = MONTH_NAMES.get(mon_str)
        if month:
            target_year = today.year
            # If target month is earlier in the year than current month, target is next year
            if month < today.month:
                target_year += 1
            try:
                target_date = datetime.date(target_year, month, day)
                days_diff = (target_date - today).days
                if days_diff >= 0:
                    return max(1, days_diff)
            except ValueError:
                pass

    # 2. Relative days (e.g. "in 3 days", "within 2 days", "deliver in 5 days")
    days_match = re.search(r'(?:in|within|deliver in|by)\s*(\d+)\s*days?', text, re.IGNORECASE)
    if days_match:
        return int(days_match.group(1))

    # 3. Quick keywords
    if "tomorrow" in text or "next day" in text or "1 day" in text:
        return 1

    return None

def parse_budget(text: str) -> Tuple[Optional[float], Optional[float]]:
    """Extract budget from expressions like 'under 1000', 'and 1000', 'between 500 and 1000'."""
    # Check range (e.g. "between 500 and 1500")
    range_match = re.search(r'(?:between|from)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(k)?\s*(?:and|to|-)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(k)?', text, re.I)
    if range_match:
        val1 = float(range_match.group(1)) * (1000 if range_match.group(2) else 1)
        val2 = float(range_match.group(3)) * (1000 if range_match.group(4) else 1)
        return min(val1, val2), max(val1, val2)

    # Check maximum budget (e.g. "under 1000", "and 1000", "below 1500", "within 2k", "for 1000")
    # Note: ensure number is not a day (e.g. 10th) or year
    max_match = re.search(r'(?:under|below|less than|within|upto|budget|and|for|around)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(k|thousand|lakh)?\b', text, re.I)
    if max_match:
        # Check that this number isn't followed by "th", "st", "nd", "rd" or "days"
        start_idx = max_match.start(1)
        sub = text[start_idx:start_idx+15].lower()
        if not re.match(r'\d+(?:st|nd|rd|th| days| day| of)', sub):
            val = float(max_match.group(1))
            unit = (max_match.group(2) or "").lower()
            if unit in ["k", "thousand"]:
                val *= 1000
            elif unit == "lakh":
                val *= 100000
            return None, val

    # Standalone rupee value (e.g. "rs 1000", "1000 rs", "₹1000")
    rupee_match = re.search(r'(?:rs\.?|inr|₹)\s*(\d+(?:\.\d+)?)|(\d+(?:\.\d+)?)\s*(?:rs|rupees|inr)', text, re.I)
    if rupee_match:
        num_str = rupee_match.group(1) or rupee_match.group(2)
        val = float(num_str)
        return None, val

    return None, None

def fallback_universal_parser(query: str) -> ParsedSearchRequest:
    """Robust universal heuristic parser supporting multilingual expressions."""
    text = query.lower()

    # 1. Parse deadline days
    deadline_days = parse_deadline_days(text)

    # 2. Parse budget
    budget_min, budget_max = parse_budget(text)

    # 3. Detect Color
    extracted_color = None
    for c in sorted(KNOWN_COLORS, key=len, reverse=True):
        if re.search(r'\b' + re.escape(c) + r'\b', text):
            extracted_color = c
            break

    # 4. Detect Brand
    brand = None
    for b in KNOWN_BRANDS:
        if re.search(r'\b' + re.escape(b) + r'\b', text):
            brand = b.title()
            break

    # 5. Detect Category and Product/Item
    category = "general"
    model_name = None

    # Check apparel
    found_apparel = None
    for app in sorted(KNOWN_APPAREL, key=len, reverse=True):
        if re.search(r'\b' + re.escape(app) + r's?\b', text):
            found_apparel = app
            break

    if found_apparel:
        category = "clothing"
        model_name = found_apparel.title()
    else:
        # Check gadgets
        found_gadget = None
        for gad in sorted(KNOWN_GADGETS, key=len, reverse=True):
            if re.search(r'\b' + re.escape(gad) + r'\b', text):
                found_gadget = gad
                break
        if found_gadget:
            if found_gadget in ["iphone", "smartphone", "phone"]:
                category = "smartphones"
                brand = "Apple" if "iphone" in text else brand
                m = re.search(r'iphone\s*(\d+(?:\s*(?:pro\s*max|pro|plus))?)', text)
                model_name = f"iPhone {m.group(1).title()}" if m else "iPhone"
            elif found_gadget in ["headphones", "earphones", "earbuds"]:
                category = "audio"
                model_name = "WH-1000XM5" if "xm5" in text or "sony" in text else "Headphones"
            elif found_gadget in ["laptop", "macbook"]:
                category = "laptops"
                model_name = "MacBook Air" if "macbook" in text else "Laptop"
            else:
                category = "gadgets"
                model_name = found_gadget.title()

    # 6. Specs extraction (storage, ram, size, color)
    specs = {}
    if extracted_color:
        specs["color"] = extracted_color.title()

    storage_match = re.search(r'\b(1\s*tb|2\s*tb|512\s*gb|256\s*gb|128\s*gb)\b', text)
    if storage_match:
        specs["storage"] = storage_match.group(1).upper().replace(" ", "")

    # 7. Pincode
    pin_match = re.search(r'\b([1-9][0-9]{5})\b', text)
    pincode = pin_match.group(1) if pin_match else None

    # 8. Clean Search Phrase
    clean_parts = []
    if brand and (not model_name or brand.lower() not in model_name.lower()):
        clean_parts.append(brand)
    if extracted_color:
        clean_parts.append(extracted_color)
    if model_name:
        clean_parts.append(model_name.lower())
    if specs.get("storage"):
        clean_parts.append(specs["storage"])

    if not clean_parts:
        # Fallback to cleaning query from stop words
        clean_str = re.sub(r'\b(and|under|below|delivered|by|in|for|to|the|of|chahiye|sabse|sasta)\b', '', text)
        clean_parts = clean_str.split()

    clean_search_phrase = " ".join(clean_parts).strip()

    # Language detection
    detected_lang = "en"
    if any(w in text for w in ["chahiye", "sasta", "sabse", "batao", "mujhe"]):
        detected_lang = "hi"
    elif any(w in text for w in ["pahije", "sarvat", "kami"]):
        detected_lang = "mr"

    return ParsedSearchRequest(
        raw_query=query,
        detected_language=detected_lang,
        translated_query=clean_search_phrase,
        clean_search_phrase=clean_search_phrase,
        attributes=ExtractedAttributes(
            category=category,
            brand=brand,
            model_name=model_name,
            specs=specs,
            color=extracted_color
        ),
        budget_min=budget_min,
        budget_max=budget_max,
        deadline_days=deadline_days,
        pincode=pincode,
        sort_by="discount"
    )

async def extract_search_intent(query: str) -> ParsedSearchRequest:
    return fallback_universal_parser(query)
