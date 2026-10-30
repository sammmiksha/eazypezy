"""Optional, API-backed live shopping source.

Retailer pages are not scraped. Deployments can set ``SERPAPI_API_KEY`` to use
a licensed shopping-search provider, while local development stays deterministic
with the demo catalog.
"""
import re
from typing import Any, Dict, List, Optional

import httpx

from app.core.config import settings
from app.schemas.search import ExtractedAttributes
from app.services.connectors.base import BasePlatformConnector


def _price(value: Any) -> Optional[float]:
    if value is None:
        return None
    match = re.search(r"(?:₹|Rs\.?|INR)?\s*([\d,]+(?:\.\d+)?)", str(value), re.I)
    return float(match.group(1).replace(",", "")) if match else None


def _specs_from_title(title: str) -> Dict[str, Any]:
    specs: Dict[str, Any] = {}
    if re.search(r"\b5\s*g\b", title, re.I):
        specs["network"] = "5G"
    storage = re.search(r"\b(64|128|256|512)\s*(GB)\b|\b(1|2)\s*(TB)\b", title, re.I)
    if storage:
        specs["storage"] = f"{storage.group(1) or storage.group(3)}{storage.group(2) or storage.group(4)}".upper()
    measurement = re.search(r"\b(\d+(?:\.\d+)?)\s*(kg|lit(?:re|er)s?|mah|watts?|w|inches|inch)\b", title, re.I)
    if measurement:
        amount, unit = measurement.group(1), measurement.group(2).lower()
        if unit == "kg" or unit.startswith("lit"):
            specs["capacity"] = f"{amount}{'kg' if unit == 'kg' else 'L'}"
        elif unit == "mah":
            specs["battery_capacity"] = f"{amount}mAh"
        elif unit in {"w", "watt", "watts"}:
            specs["wattage"] = f"{amount}W"
        else:
            specs["size"] = f"{amount} inch"
    if re.search(r"\bfront[ -]?load\b", title, re.I):
        specs["loading"] = "front load"
    fabric = re.search(r"\b(cotton|silk|wool|leather|linen|denim|polyester)\b", title, re.I)
    if fabric:
        specs["fabric"] = fabric.group(1).lower()
    for feature in ("ergonomic", "quiet", "waterproof", "wireless", "foldable", "portable"):
        if re.search(rf"\b{feature}\b", title, re.I):
            specs[f"feature_{feature}"] = True
    return specs


class LiveShoppingConnector(BasePlatformConnector):
    """Normalizes results from an approved shopping-search API."""

    def __init__(self) -> None:
        super().__init__(platform_name="Live shopping feed")

    @property
    def is_configured(self) -> bool:
        return bool(settings.SERPAPI_API_KEY)

    async def search(
        self,
        query: str,
        attributes: ExtractedAttributes,
        max_budget: Optional[float] = None,
    ) -> List[Dict[str, Any]]:
        if not self.is_configured:
            return []

        terms = [query]
        terms.extend(str(value) for value in attributes.required_specs.values())
        params = {
            "engine": "google_shopping",
            "q": " ".join(dict.fromkeys(term for term in terms if term)),
            "gl": "in",
            "hl": "en",
            "api_key": settings.SERPAPI_API_KEY,
        }
        try:
            async with httpx.AsyncClient(timeout=12) as client:
                response = await client.get(settings.SERPAPI_ENDPOINT, params=params)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError:
            # An unavailable provider should not break a user search. The caller
            # falls back to the clearly labelled local catalog.
            return []

        products: List[Dict[str, Any]] = []
        for index, result in enumerate(payload.get("shopping_results", [])):
            price = _price(result.get("extracted_price") or result.get("price"))
            if price is None or (max_budget is not None and price > max_budget):
                continue
            title = result.get("title", "Product listing")
            products.append({
                "platform": result.get("source") or "Marketplace",
                "platform_product_id": f"live-{index}-{abs(hash(result.get('link', title))) % 10_000_000}",
                "title": title,
                "category": attributes.category or "general",
                "brand": attributes.brand,
                "seller": result.get("source") or "Marketplace listing",
                "product_url": result.get("link") or result.get("product_link") or "#",
                "image_urls": [result["thumbnail"]] if result.get("thumbnail") else [],
                "price": price,
                "mrp": _price(result.get("extracted_old_price") or result.get("old_price")),
                "specs": _specs_from_title(title),
                "in_stock": True,
                "rating": float(result.get("rating") or 0),
                "rating_count": int(result.get("reviews") or 0) if str(result.get("reviews") or "").isdigit() else 0,
                "delivery_days_standard": 3,
            })
        return products

    async def check_serviceability(self, pincode: str, product_id: Optional[str] = None) -> Dict[str, Any]:
        return {
            "is_serviceable": True,
            "estimated_delivery_days": 3,
            "status": "unverified",
            "notes": "Confirm delivery timing with the retailer at checkout.",
        }
