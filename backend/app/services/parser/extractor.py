"""Universal multilingual LLM and heuristic parser for any product category."""
import re
import json
import logging
from typing import Optional, Dict, Any, List
import httpx
from app.core.config import settings
from app.schemas.search import ParsedSearchRequest, ExtractedAttributes

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are EasyPezy's universal multilingual shopping assistant.
The user may search in ANY language (English, Hindi, Hinglish, Marathi, Tamil, Telugu, Spanish, etc.) for ANY product (gadgets, clothing, electronics, shoes, appliances, etc.).

Analyze the request and return strict JSON:
1. Detect input language ('en', 'hi', 'mr', 'es', etc.).
2. Translate query to English if non-English.
3. Identify brand (e.g. Apple, Sony, Samsung, Nike, etc.).
4. Identify model or product name (e.g. iPhone 18, WH-1000XM5, Air Jordan, Kanjivaram Saree).
5. Extract hardware/fashion specifications:
   - storage: '1TB', '512GB', etc.
   - ram: '16GB', etc.
   - color: 'natural titanium', 'purple', 'black', etc.
   - size, fabric, etc.
6. Extract budget in INR if specified ('under 1500', 'under 1.5 lakh', etc.).
7. Extract 6-digit Indian pincode if specified.
8. Extract delivery deadline in days.
9. Detect intent for discount / cheapest ('sasta', 'cheapest', 'best deal', 'discount' -> sort_by: 'discount').

JSON Schema:
{
  "detected_language": "string",
  "translated_query": "string",
  "clean_search_phrase": "string",
  "attributes": {
    "category": "string or null",
    "brand": "string or null",
    "model_name": "string or null",
    "specs": {},
    "color": "string or null"
  },
  "budget_min": float or null,
  "budget_max": float or null,
  "deadline_days": int or null,
  "pincode": "string or null",
  "sort_by": "discount",
  "clarifications_needed": []
}
"""

KNOWN_BRANDS = [
    "apple", "samsung", "sony", "nike", "adidas", "puma", "dyson", "mitera",
    "suta", "dell", "hp", "lenovo", "asus", "oneplus", "google", "xiaomi"
]

LANGUAGE_HINTS = {
    "hi": ["chahiye", "sasta", "sabse", "batao", "mujhe", "kam", "kimat", "daam", "mehenga"],
    "mr": ["pahije", "sarvat", "kami", "kimtit", "dakhva", "ahe"],
    "es": ["quiero", "barato", "precio", "descuento", "comprar"],
}

def fallback_universal_parser(query: str) -> ParsedSearchRequest:
    """Robust universal heuristic parser supporting multilingual expressions."""
    text = query.lower()
    
    # 1. Language detection
    detected_lang = "en"
    for lang, markers in LANGUAGE_HINTS.items():
        if any(m in text for m in markers):
            detected_lang = lang
            break

    # 2. Brand detection
    brand = None
    for b in KNOWN_BRANDS:
        if b in text:
            brand = b.title()
            break

    # 3. Model / Product recognition
    model_name = None
    category = "general"

    if "iphone" in text:
        category = "smartphones"
        brand = "Apple"
        m = re.search(r'iphone\s*(\d+(?:\s*(?:pro\s*max|pro|plus))?)', text)
        model_name = f"iPhone {m.group(1).title()}" if m else "iPhone"
    elif "macbook" in text:
        category = "laptops"
        brand = "Apple"
        model_name = "MacBook Air" if "air" in text else "MacBook Pro"
    elif "s25" in text or "galaxy" in text:
        category = "smartphones"
        brand = "Samsung"
        model_name = "Galaxy S25 Ultra"
    elif "wh-1000xm5" in text or "sony headphone" in text or "xm5" in text:
        category = "audio"
        brand = "Sony"
        model_name = "WH-1000XM5"
    elif "jordan" in text or "sneaker" in text:
        category = "footwear"
        brand = "Nike"
        model_name = "Air Jordan 1"
    elif "saree" in text or "sari" in text:
        category = "clothing"
        model_name = "Saree"

    # 4. Specifications extraction (e.g. 1TB, 512GB, 256GB, 128GB)
    specs = {}
    storage_match = re.search(r'\b(1\s*tb|2\s*tb|512\s*gb|256\s*gb|128\s*gb)\b', text)
    if storage_match:
        specs["storage"] = storage_match.group(1).upper().replace(" ", "")

    color_match = re.search(r'\b(natural titanium|titanium|black|silver|gold|purple|violet|red|yellow|blue)\b', text)
    extracted_color = color_match.group(1) if color_match else None
    if extracted_color:
        specs["color"] = extracted_color

    # 5. Budget extraction
    budget_max = None
    budget_min = None
    under_match = re.search(r'(?:under|below|less than|within|upto|budget|kam|sasta)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(k|lakh|thousand)?', text)
    if under_match:
        val = float(under_match.group(1))
        unit = under_match.group(2)
        if unit == 'k' or unit == 'thousand':
            val *= 1000
        elif unit == 'lakh':
            val *= 100000
        budget_max = val

    # 6. Pincode
    pin_match = re.search(r'\b([1-9][0-9]{5})\b', text)
    pincode = pin_match.group(1) if pin_match else None

    # 7. Deadline
    deadline_match = re.search(r'(?:in|within|deliver in|by)\s*(\d+)\s*days?', text)
    deadline_days = int(deadline_match.group(1)) if deadline_match else None
    if "tomorrow" in text or "1 day" in text:
        deadline_days = 1

    # 8. Clean search phrase
    clean_parts = []
    if brand:
        clean_parts.append(brand)
    if model_name and (not brand or model_name.lower() not in brand.lower()):
        clean_parts.append(model_name)
    if specs.get("storage"):
        clean_parts.append(specs["storage"])
    if extracted_color and extracted_color not in clean_parts:
        clean_parts.append(extracted_color)
    if not clean_parts:
        clean_parts = [query.strip()]
    clean_search_phrase = " ".join(clean_parts)

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
    if settings.OPENAI_API_KEY:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {settings.OPENAI_API_KEY}"},
                    json={
                        "model": "gpt-4o-mini",
                        "messages": [
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": query}
                        ],
                        "response_format": {"type": "json_object"}
                    }
                )
                if res.status_code == 200:
                    data = res.json()["choices"][0]["message"]["content"]
                    parsed_dict = json.loads(data)
                    return ParsedSearchRequest(raw_query=query, **parsed_dict)
        except Exception as e:
            logger.warning(f"OpenAI extraction call failed: {e}. Falling back to universal rule parser.")

    return fallback_universal_parser(query)
