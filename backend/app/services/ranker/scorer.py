"""Multi-factor ranker and 'Why this matched' explanation generator."""
from typing import Dict, Any, Tuple
from app.schemas.search import ParsedSearchRequest

class ProductRanker:
    @staticmethod
    def score_product(product: Dict[str, Any], parsed: ParsedSearchRequest) -> Tuple[float, str]:
        """Calculates match score between 0.0 and 1.0 and generates the match rationale."""
        score = 0.0
        reasons = []

        attrs = parsed.attributes
        title_lower = product["title"].lower()
        desc_lower = (product.get("description") or "").lower()
        full_text = f"{title_lower} {desc_lower}"

        # 1. Color matching (up to 0.35)
        if attrs.primary_color:
            prod_color = (product.get("primary_color") or "").lower()
            if attrs.primary_color == prod_color or attrs.primary_color in full_text:
                score += 0.35
                reasons.append(f"Matches requested {attrs.primary_color.title()} color")
            else:
                score += 0.05

        # 2. Border & Zari matching (up to 0.25)
        border_matched = False
        if attrs.zari_type:
            prod_zari = (product.get("zari_type") or "").lower()
            if attrs.zari_type in prod_zari or attrs.zari_type in full_text:
                score += 0.25
                border_matched = True
                reasons.append(f"Features {attrs.zari_type.title()} zari border")
        elif attrs.border_type:
            prod_border = (product.get("border_type") or "").lower()
            if attrs.border_type in prod_border or attrs.border_type in full_text:
                score += 0.20
                border_matched = True
                reasons.append(f"{attrs.border_type.title()} border design")

        # 3. Fabric matching (up to 0.20)
        if attrs.fabric:
            prod_fabric = (product.get("fabric") or "").lower()
            if attrs.fabric in prod_fabric or attrs.fabric in full_text:
                score += 0.20
                reasons.append(f"{attrs.fabric.title()} fabric")
        else:
            # Baseline fabric match
            score += 0.10

        # 4. Budget fit explanation
        price = product.get("price", 0)
        if parsed.budget_max:
            if price <= parsed.budget_max:
                savings = parsed.budget_max - price
                if savings > 0:
                    reasons.append(f"Rs. {int(price):,} is Rs. {int(savings):,} below your Rs. {int(parsed.budget_max):,} budget")
                else:
                    reasons.append(f"Exactly meets your Rs. {int(parsed.budget_max):,} budget")

        # 5. Quality & Rating bonus
        rating = float(product.get("rating", 4.0))
        if rating >= 4.3:
            score += 0.08
            reasons.append(f"Highly rated ({rating}/5)")
        elif rating >= 4.0:
            score += 0.04

        # 6. Delivery note
        est_days = product.get("estimated_delivery_days")
        if est_days:
            if est_days <= 2:
                score += 0.07
                reasons.append(f"Express {est_days}-day delivery")
            else:
                reasons.append(f"Estimated {est_days}-day delivery")

        # Normalize score
        final_score = min(round(score, 2), 0.99)
        why_matched = " | ".join(reasons) if reasons else "Good overall semantic match"

        return final_score, why_matched
