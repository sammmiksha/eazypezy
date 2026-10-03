"""Multi-platform deal ranker prioritizing maximum discount and lowest price across sellers."""
from typing import Dict, Any, Tuple, List, Optional
from app.schemas.search import ParsedSearchRequest, ProductOut, PlatformDealComparison

class UniversalRanker:
    @staticmethod
    def process_and_rank_products(
        products: List[Dict[str, Any]],
        parsed: ParsedSearchRequest
    ) -> Tuple[List[ProductOut], Optional[PlatformDealComparison]]:
        """Processes products, identifies the best deal among competing platforms, and ranks results."""
        if not products:
            return [], None

        # Determine min and max price among matching items to highlight price disparity
        prices = [float(p["price"]) for p in products]
        min_price = min(prices)
        max_price = max(prices)
        savings_spread = max_price - min_price

        deal_comparison = None
        lowest_platform = ""
        highest_platform = ""
        for p in products:
            if float(p["price"]) == min_price and not lowest_platform:
                lowest_platform = p["platform"]
            if float(p["price"]) == max_price and not highest_platform:
                highest_platform = p["platform"]

        if len(products) > 1 and savings_spread > 0:
            deal_comparison = PlatformDealComparison(
                product_group=parsed.clean_search_phrase,
                lowest_platform=lowest_platform,
                lowest_price=min_price,
                highest_price=max_price,
                max_savings=savings_spread,
                total_sellers_found=len(products)
            )

        ranked_outputs: List[ProductOut] = []

        for p in products:
            price = float(p["price"])
            mrp = float(p.get("mrp") or price)
            discount_pct = float(p.get("discount_percent", 0.0))
            is_best_deal = (price == min_price)

            # Score calculation: weighted heavily by discount & lowest price
            score = 0.50  # Base relevance

            # Brand & Model match boost
            title_lower = p["title"].lower()
            if parsed.attributes.brand and parsed.attributes.brand.lower() in title_lower:
                score += 0.15
            if parsed.attributes.model_name and parsed.attributes.model_name.lower() in title_lower:
                score += 0.15

            # Best price boost (+0.15 for lowest price across platforms)
            if is_best_deal:
                score += 0.15
            else:
                # Slight penalty proportional to how much more expensive it is than min_price
                diff_pct = (price - min_price) / max(min_price, 1)
                score -= min(diff_pct * 0.1, 0.10)

            # Delivery speed bonus
            est_days = p.get("estimated_delivery_days", 3)
            if est_days <= 1:
                score += 0.05
            elif est_days <= 2:
                score += 0.03

            score = min(max(round(score, 2), 0.1), 0.99)

            # Build transparent "Why this matched" explanation
            reasons = []
            if is_best_deal:
                if savings_spread > 0:
                    reasons.append(f"Lowest price across all platforms (Save Rs. {int(savings_spread):,} vs {highest_platform})")
                else:
                    reasons.append("Best price match")
            else:
                price_above_min = price - min_price
                reasons.append(f"Rs. {int(price_above_min):,} higher than {lowest_platform}")

            if discount_pct > 0:
                reasons.append(f"{discount_pct:.0f}% discount off MRP")

            rating = float(p.get("rating", 4.0))
            if rating >= 4.5:
                reasons.append(f"Top rated ({rating}/5)")

            if est_days:
                reasons.append(f"{est_days}-day delivery")

            why_matched = " | ".join(reasons)

            product_out = ProductOut(
                id=p.get("platform_product_id", ""),
                platform=p["platform"],
                platform_product_id=p["platform_product_id"],
                title=p["title"],
                category=p.get("category", "general"),
                description=p.get("description"),
                brand=p.get("brand"),
                seller=p.get("seller"),
                product_url=p["product_url"],
                image_urls=p["image_urls"],
                price=price,
                mrp=mrp,
                discount_percent=discount_pct,
                currency=p.get("currency", "INR"),
                specs=p.get("specs", {}),
                in_stock=p.get("in_stock", True),
                rating=rating,
                rating_count=p.get("rating_count", 0),
                estimated_delivery_days=est_days,
                delivery_status=p.get("delivery_status", "confirmed"),
                match_score=score,
                is_best_deal=is_best_deal,
                price_difference_vs_highest=max_price - price if is_best_deal else None,
                why_matched=why_matched
            )
            ranked_outputs.append(product_out)

        # Sort: Best deals and lowest price first, then by match_score
        ranked_outputs.sort(key=lambda x: (not x.is_best_deal, x.price, -x.match_score))

        return ranked_outputs, deal_comparison
