"""Universal search API endpoint orchestrating parsing, filtering, and ranking."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.schemas.search import SearchResponse, SearchRequest, ProductOut, ParsedSearchRequest
from app.services.parser.requirements_parser import extract_search_intent
from app.services.connectors.mock_catalog import UniversalCatalogConnector
from app.services.connectors.live_shopping import LiveShoppingConnector
from app.services.delivery.checker import DeliveryChecker
from app.services.ranker.requirement_ranker import RequirementRanker

router = APIRouter()
catalog_connector = UniversalCatalogConnector()
live_connector = LiveShoppingConnector()


def _normalise(value: Any) -> str:
    return "".join(str(value).lower().split())


def _satisfies_required_specs(product: Dict[str, Any], required_specs: Dict[str, Any]) -> bool:
    """Apply non-negotiable feature filters before scoring preferences."""
    product_specs = product.get("specs", {})
    for key, required in required_specs.items():
        actual = product_specs.get(key)
        # Some marketplace feeds expose a feature only in the listing title.
        # Searching that normalized text is still stricter than treating a
        # missing requirement as a preference, and preserves generic traits.
        if actual is None and key.startswith("feature_"):
            feature = key.removeprefix("feature_")
            listing_text = " ".join([str(product.get("title", "")), str(product.get("description", "")), str(product_specs)])
            actual = feature if _normalise(feature) in _normalise(listing_text) else None
        if actual is None:
            return False
        if key == "refresh_rate_hz":
            try:
                if float(actual) < float(required):
                    return False
            except (TypeError, ValueError):
                return False
        elif _normalise(required) not in _normalise(actual):
            return False
    return True

@router.post("/search", response_model=SearchResponse)
async def search_products(payload: SearchRequest):
    """Universal search across gadgets, fashion, appliances, etc. with cross-platform best discount ranking."""
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    # Step 1: Multilingual extraction of intent, brand, model, specifications, and budget
    parsed: ParsedSearchRequest = await extract_search_intent(payload.query)

    # Apply any explicit overrides
    if payload.pincode:
        parsed.pincode = payload.pincode
    if payload.deadline_days:
        parsed.deadline_days = payload.deadline_days
    if payload.budget_max:
        parsed.budget_max = payload.budget_max

    # Step 2: Query the configured, licensed live provider first. In local
    # development we intentionally fall back to the labelled demo catalog.
    raw_products = await live_connector.search(
        # Keep the complete natural-language request for a live provider. It
        # may understand product categories and traits that are not in our
        # local demo taxonomy (for example an ergonomic chair or a mixer).
        query=parsed.raw_query,
        attributes=parsed.attributes,
        max_budget=parsed.budget_max
    )
    active_connector = live_connector
    data_source = "live_shopping_api"
    if not raw_products:
        raw_products = await catalog_connector.search(
            query=parsed.clean_search_phrase,
            attributes=parsed.attributes,
            max_budget=parsed.budget_max
        )
        active_connector = catalog_connector
        data_source = "demo_catalog"

    # Step 3: Hard filters & SLA evaluation
    survivors: List[Dict[str, Any]] = []
    
    for raw in raw_products:
        if not raw.get("in_stock", True):
            continue

        price = float(raw["price"])
        if parsed.budget_min and price < parsed.budget_min:
            continue
        if parsed.budget_max and price > parsed.budget_max:
            continue
        if not _satisfies_required_specs(raw, parsed.attributes.required_specs):
            continue

        serviceability = await active_connector.check_serviceability(
            pincode=parsed.pincode or "",
            product_id=raw["platform_product_id"]
        )

        delivery_eval = DeliveryChecker.evaluate_delivery(
            pincode=parsed.pincode,
            deadline_days=parsed.deadline_days,
            platform_serviceability=serviceability
        )

        if not delivery_eval["is_deliverable_by_deadline"]:
            continue

        item_ready = dict(raw)
        item_ready["estimated_delivery_days"] = delivery_eval["estimated_delivery_days"]
        item_ready["delivery_status"] = delivery_eval["delivery_status"]
        survivors.append(item_ready)

    # Step 4: Rank hard-requirement matches by stated preferences and value.
    ranked_products, deal_comparison = RequirementRanker.process_and_rank_products(survivors, parsed)

    return SearchResponse(
        parsed_query=parsed,
        total_found=len(ranked_products),
        deal_comparison=deal_comparison,
        results=ranked_products,
        data_source=data_source,
    )
