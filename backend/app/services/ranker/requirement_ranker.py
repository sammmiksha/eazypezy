"""Requirement-aware ranking for cross-store product discovery."""
from typing import Any, Dict, List, Optional, Tuple

from app.schemas.search import ParsedSearchRequest, PlatformDealComparison, ProductOut


def _display_quality(product: Dict[str, Any]) -> float:
    specs = product.get("specs", {})
    if specs.get("display_score") is not None:
        return min(float(specs["display_score"]), 100.0) / 100.0
    text = str(specs.get("display", "")).lower()
    score = 0.45
    if "ltpo" in text:
        score += 0.25
    if "amoled" in text or "oled" in text:
        score += 0.20
    refresh = float(specs.get("refresh_rate_hz", 0) or 0)
    if refresh >= 120:
        score += 0.10
    elif refresh >= 90:
        score += 0.05
    return min(score, 1.0)


def _preference_score(product: Dict[str, Any], preferences: Dict[str, Any]) -> Tuple[float, List[str]]:
    if not preferences:
        return 0.5, []
    parts: List[float] = []
    reasons: List[str] = []
    specs = product.get("specs", {})
    if "display_priority" in preferences:
        display = _display_quality(product)
        parts.append(display)
        reasons.append(f"display quality {round(display * 100)}/100")
    if "rating_priority" in preferences:
        parts.append(min(float(product.get("rating", 0)) / 5, 1.0))
    if "battery_priority" in preferences:
        battery = str(specs.get("battery", "0"))
        digits = "".join(char for char in battery if char.isdigit())
        parts.append(min(float(digits or 0) / 6000, 1.0))
    if "camera_priority" in preferences:
        camera = str(specs.get("camera", "0"))
        digits = "".join(char for char in camera if char.isdigit())
        parts.append(min(float(digits or 0) / 50, 1.0))
    if "performance_priority" in preferences:
        ram = str(specs.get("ram", "0"))
        digits = "".join(char for char in ram if char.isdigit())
        parts.append(min(float(digits or 0) / 12, 1.0))
    return (sum(parts) / len(parts) if parts else 0.5), reasons


class RequirementRanker:
    @staticmethod
    def process_and_rank_products(
        products: List[Dict[str, Any]], parsed: ParsedSearchRequest
    ) -> Tuple[List[ProductOut], Optional[PlatformDealComparison]]:
        if not products:
            return [], None

        prices = [float(product["price"]) for product in products]
        min_price, max_price = min(prices), max(prices)
        lowest = next(product for product in products if float(product["price"]) == min_price)
        highest = next(product for product in products if float(product["price"]) == max_price)
        spread = max_price - min_price
        comparison = None
        if len(products) > 1 and spread:
            comparison = PlatformDealComparison(
                product_group=parsed.clean_search_phrase,
                lowest_platform=lowest["platform"],
                lowest_price=min_price,
                highest_price=max_price,
                max_savings=spread,
                total_sellers_found=len(products),
            )

        enriched = []
        hard_requirement_count = len(parsed.attributes.required_specs)
        for product in products:
            price = float(product["price"])
            preferences, preference_reasons = _preference_score(product, parsed.attributes.preferred_specs)
            budget_value = 1.0 if not parsed.budget_max else max(0.0, 1 - (price / parsed.budget_max))
            rating_value = min(float(product.get("rating", 0)) / 5, 1.0)
            # All candidates reached this point only after satisfying hard filters.
            requirement_value = 1.0 if hard_requirement_count else 0.7
            score = (0.40 * requirement_value) + (0.32 * preferences) + (0.18 * budget_value) + (0.10 * rating_value)
            summary = []
            if hard_requirement_count:
                summary.append(f"Meets {hard_requirement_count} must-have requirement{'s' if hard_requirement_count > 1 else ''}")
            summary.extend(preference_reasons)
            if parsed.budget_max:
                summary.append(f"₹{int(parsed.budget_max - price):,} under budget")
            enriched.append((score, summary, product))

        enriched.sort(key=lambda item: (-item[0], item[2]["price"], -float(item[2].get("rating", 0))))
        outputs: List[ProductOut] = []
        for index, (score, summary, product) in enumerate(enriched):
            price = float(product["price"])
            mrp = float(product.get("mrp") or price)
            discount = product.get("discount_percent")
            if discount is None:
                discount = round(((mrp - price) / mrp) * 100, 1) if mrp > price else 0.0
            reasons = list(summary)
            if price == min_price:
                reasons.append("lowest price in these matching offers")
            if product.get("estimated_delivery_days"):
                reasons.append(f"{product['estimated_delivery_days']}-day delivery")
            outputs.append(ProductOut(
                id=product.get("platform_product_id", ""),
                platform=product["platform"],
                platform_product_id=product["platform_product_id"],
                title=product["title"],
                category=product.get("category", "general"),
                description=product.get("description"),
                brand=product.get("brand"),
                seller=product.get("seller"),
                product_url=product["product_url"],
                image_urls=product.get("image_urls", []),
                price=price,
                mrp=mrp,
                discount_percent=float(discount),
                currency=product.get("currency", "INR"),
                specs=product.get("specs", {}),
                in_stock=product.get("in_stock", True),
                rating=float(product.get("rating", 0)),
                rating_count=int(product.get("rating_count", 0)),
                estimated_delivery_days=product.get("estimated_delivery_days"),
                delivery_status=product.get("delivery_status", "estimated"),
                match_score=round(score, 2),
                is_best_deal=price == min_price,
                requirement_score=round(score * 100),
                requirement_summary=summary,
                price_difference_vs_highest=(max_price - price) if price == min_price else None,
                why_matched=" • ".join(reasons),
            ))
        return outputs, comparison
