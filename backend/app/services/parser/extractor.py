"""LLM Parser for extracting structured saree attributes, budgets, and delivery constraints."""
import re
import json
import logging
from typing import Optional, Dict, Any, List
import httpx
from app.core.config import settings
from app.schemas.search import ParsedSearchRequest, SareeQueryAttributes

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an Indian ethnic wear shopping assistant specializing in sarees.
Extract structured saree shopping parameters from the query into strict JSON.

Rules:
1. Normalize fabric and weaving terms (e.g. 'Kanchi'/'Pattu' -> 'silk', 'Banarasi' -> 'banarasi').
2. Normalize colors (e.g. 'jamuni' -> 'purple', 'rani pink' -> 'pink', 'haldi yellow' -> 'yellow').
3. Extract budget in INR:
   - 'under 1500' -> budget_max: 1500
   - '1.5k' -> 1500
   - 'between 2000 and 4000' -> budget_min: 2000, budget_max: 4000
4. Extract 6-digit Indian pincode if present (e.g. 'to 560034').
5. Extract delivery deadline in days (e.g. 'in 3 days' -> deadline_days: 3, 'need tomorrow' -> deadline_days: 1).
6. Detect ambiguity: if numbers are ambiguous (e.g. '1500 or 15000'), populate clarifications_needed with options.
7. Return clean_search_phrase for vector and keyword search.

JSON Output Schema:
{
  "detected_language": "en",
  "translated_query": "string",
  "clean_search_phrase": "string",
  "attributes": {
    "primary_color": "string or null",
    "secondary_color": "string or null",
    "border_type": "string or null",
    "zari_type": "string or null",
    "finish": "string or null",
    "fabric": "string or null",
    "occasion": "string or null"
  },
  "budget_min": float or null,
  "budget_max": float or null,
  "deadline_days": int or null,
  "pincode": "string or null",
  "clarifications_needed": ["string"]
}
"""

KNOWN_COLORS = [
    "purple", "violet", "magenta", "lavender", "red", "maroon", "pink", "rani pink",
    "yellow", "mustard", "green", "bottle green", "emerald", "blue", "navy blue",
    "royal blue", "teal", "black", "white", "cream", "beige", "gold", "golden",
    "orange", "rust", "peach", "grey", "silver"
]

KNOWN_FABRICS = [
    "kanjivaram", "banarasi", "chanderi", "tussar", "paithani", "silk",
    "georgette", "chiffon", "cotton", "organza", "crepe", "linen", "satin", "velvet", "art silk"
]

KNOWN_BORDERS = [
    "zari", "temple", "contrast", "embroidered", "scallop", "woven", "broad", "thin"
]

KNOWN_ZARI = [
    "golden", "gold", "silver", "copper", "antique", "matte"
]

KNOWN_OCCASIONS = [
    "wedding", "bridal", "festive", "party", "haldi", "mehendi", "reception", "casual", "daily wear"
]

def fallback_heuristic_parser(query: str) -> ParsedSearchRequest:
    """Heuristic extraction pipeline when external LLM is offline or unconfigured."""
    text = query.lower()
    
    # 1. Budget extraction
    budget_min = None
    budget_max = None
    
    # Check for "under X" or "below X" or "< X"
    under_match = re.search(r'(?:under|below|less than|within|upto|budget)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(k|thousand)?', text)
    if under_match:
        val = float(under_match.group(1))
        if under_match.group(2) == 'k':
            val *= 1000
        budget_max = val
        
    range_match = re.search(r'(?:between|from)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(k)?\s*(?:and|to|-)\s*(?:rs\.?|inr|₹)?\s*(\d+(?:\.\d+)?)\s*(k)?', text)
    if range_match:
        val1 = float(range_match.group(1)) * (1000 if range_match.group(2) == 'k' else 1)
        val2 = float(range_match.group(3)) * (1000 if range_match.group(4) == 'k' else 1)
        budget_min = min(val1, val2)
        budget_max = max(val1, val2)

    # 2. Pincode extraction (6 digits)
    pincode = None
    pin_match = re.search(r'\b([1-9][0-9]{5})\b', text)
    if pin_match:
        pincode = pin_match.group(1)

    # 3. Deadline extraction
    deadline_days = None
    deadline_match = re.search(r'(?:in|within|deliver in|by)\s*(\d+)\s*days?', text)
    if deadline_match:
        deadline_days = int(deadline_match.group(1))
    elif "tomorrow" in text or "1 day" in text or "next day" in text:
        deadline_days = 1

    # 4. Color matching
    found_colors = []
    for c in sorted(KNOWN_COLORS, key=len, reverse=True):
        if re.search(r'\b' + re.escape(c) + r'\b', text):
            found_colors.append(c)
    primary_color = found_colors[0] if found_colors else None
    secondary_color = found_colors[1] if len(found_colors) > 1 else None

    # 5. Fabric matching
    fabric = None
    for f in sorted(KNOWN_FABRICS, key=len, reverse=True):
        if re.search(r'\b' + re.escape(f) + r'\b', text):
            fabric = f
            break

    # 6. Border type matching
    border_type = None
    if "border" in text:
        for b in KNOWN_BORDERS:
            if b in text:
                border_type = b
                break
        if not border_type:
            border_type = "standard"

    # 7. Zari type matching
    zari_type = None
    for z in KNOWN_ZARI:
        if z in text and ("zari" in text or "border" in text or z in ["golden", "silver"]):
            zari_type = z
            break

    # 8. Occasion matching
    occasion = None
    for o in KNOWN_OCCASIONS:
        if o in text:
            occasion = o
            break

    # Ambiguity check
    clarifications = []
    if "1500 or 15000" in text:
        clarifications = ["Did you mean under ₹1,500 or under ₹15,000?"]

    # Clean search phrase
    clean_parts = []
    if primary_color:
        clean_parts.append(primary_color)
    if zari_type:
        clean_parts.append(f"{zari_type} zari")
    elif border_type:
        clean_parts.append(f"{border_type} border")
    if fabric:
        clean_parts.append(fabric)
    clean_parts.append("saree")
    clean_search_phrase = " ".join(clean_parts)

    attrs = SareeQueryAttributes(
        primary_color=primary_color,
        secondary_color=secondary_color,
        border_type=border_type,
        zari_type=zari_type,
        finish="matte" if "matte" in text else ("glossy" if "glossy" in text else None),
        fabric=fabric,
        occasion=occasion
    )

    return ParsedSearchRequest(
        raw_query=query,
        detected_language="en",
        translated_query=query,
        clean_search_phrase=clean_search_phrase,
        attributes=attrs,
        budget_min=budget_min,
        budget_max=budget_max,
        deadline_days=deadline_days,
        pincode=pincode,
        clarifications_needed=clarifications
    )

async def extract_search_intent(query: str) -> ParsedSearchRequest:
    """Call LLM API if key is available, else fallback cleanly."""
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
            logger.warning(f"OpenAI extraction call failed: {e}. Falling back to rule parser.")

    return fallback_heuristic_parser(query)
