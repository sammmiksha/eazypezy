"""Search API endpoint orchestrating parser, connectors, filters, and ranker."""
from fastapi import APIRouter, Query, HTTPException, Depends
from typing import Optional, List
from app.schemas.search import SearchResponse, SearchRequest, ProductOut, ParsedSearchRequest
from app.services.parser.extractor import extract_search_intent
from app.services.connectors.mock_catalog import MockCatalogConnector
from app.services.delivery.checker import DeliveryChecker
from app.services.ranker.scorer import ProductRanker

router = APIRouter()
catalog_connector = MockCatalogConnector()

@router.post("/search", response_model=SearchResponse)
async def search_sarees(payload: SearchRequest):
    """Orchestrates query parsing, platform search, hard filters, delivery checks, and ranking."""
    if not payload.query or not payload.query.strip():
        raise HTTPException(status_code=400, detail="Search query cannot be empty")

    # Step 1: LLM attribute & intent extraction
    parsed: ParsedSearchRequest = await extract_search_intent(payload.query)

    # Apply any explicit query overrides passed in the payload
    if payload.pincode:
        parsed.pincode = payload.pincode
    if payload.deadline_days:
        parsed.deadline_days = payload.deadline_days
    if payload.budget_max:
        parsed.budget_max = payload.budget_max

    # Step 2: Query product sources via connector
    raw_products = await catalog_connector.search(
        query=parsed.clean_search_phrase,
        attributes=parsed.attributes,
        max_budget=parsed.budget_max
    )

    # Step 3: Hard filters & Delivery evaluation
    survivors: List[ProductOut] = []
    
    for raw in raw_products:
        # Stock filter
        if not raw.get("in_stock", True):
            continue

        # Budget hard filter (if budget_min is specified)
        price = float(raw["price"])
        if parsed.budget_min and price < parsed.budget_min:
            continue
        if parsed.budget_max and price > parsed.budget_max:
            continue

        # Serviceability & Deadline check
        serviceability = await catalog_connector.check_serviceability(
            pincode=parsed.pincode or "",
            product_id=raw["platform_product_id"]
        )

        delivery_eval = DeliveryChecker.evaluate_delivery(
            pincode=parsed.pincode,
            deadline_days=parsed.deadline_days,
            platform_serviceability=serviceability
        )

        # If user explicitly requested a deadline and item cannot meet it, filter out
        if not delivery_eval["is_deliverable_by_deadline"]:
            continue

        item_for_scoring = dict(raw)
        item_for_scoring["estimated_delivery_days"] = delivery_eval["estimated_delivery_days"]

        # Step 4: Multi-factor ranking & match reason generation
        score, why_matched = ProductRanker.score_product(item_for_scoring, parsed)

        product_out = ProductOut(
            id=raw.get("platform_product_id", ""),
            platform=raw["platform"],
            platform_product_id=raw["platform_product_id"],
            title=raw["title"],
            description=raw.get("description"),
            brand=raw.get("brand"),
            seller=raw.get("seller"),
            product_url=raw["product_url"],
            image_urls=raw["image_urls"],
            price=price,
            mrp=raw.get("mrp"),
            currency=raw.get("currency", "INR"),
            primary_color=raw.get("primary_color"),
            secondary_color=raw.get("secondary_color"),
            border_type=raw.get("border_type"),
            zari_type=raw.get("zari_type"),
            finish=raw.get("finish"),
            fabric=raw.get("fabric"),
            occasion=raw.get("occasion"),
            in_stock=raw.get("in_stock", True),
            rating=raw.get("rating", 4.0),
            rating_count=raw.get("rating_count", 0),
            estimated_delivery_days=delivery_eval["estimated_delivery_days"],
            delivery_status=delivery_eval["delivery_status"],
            match_score=score,
            why_matched=why_matched
        )
        survivors.append(product_out)

    # Sort survivors by match_score descending
    survivors.sort(key=lambda p: p.match_score, reverse=True)

    return SearchResponse(
        parsed_query=parsed,
        total_found=len(survivors),
        results=survivors
    )

@router.get("/parse-only", response_model=ParsedSearchRequest)
async def parse_query_only(q: str = Query(..., description="Shopping query string")):
    """Helper endpoint to view LLM extraction results directly."""
    return await extract_search_intent(q)
