"""Universal search API endpoint orchestrating multilingual parsing, multi-platform search, and deal ranking."""
from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from app.schemas.search import SearchResponse, SearchRequest, ProductOut, ParsedSearchRequest
from app.services.parser.extractor import extract_search_intent
from app.services.connectors.mock_catalog import UniversalCatalogConnector
from app.services.delivery.checker import DeliveryChecker
from app.services.ranker.scorer import UniversalRanker

router = APIRouter()
catalog_connector = UniversalCatalogConnector()

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

    # Step 2: Query multi-platform catalog
    raw_products = await catalog_connector.search(
        query=parsed.clean_search_phrase,
        attributes=parsed.attributes,
        max_budget=parsed.budget_max
    )

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

        serviceability = await catalog_connector.check_serviceability(
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

    # Step 4: Multi-platform cross-comparison and discount ranking
    ranked_products, deal_comparison = UniversalRanker.process_and_rank_products(survivors, parsed)

    return SearchResponse(
        parsed_query=parsed,
        total_found=len(ranked_products),
        deal_comparison=deal_comparison,
        results=ranked_products
    )
