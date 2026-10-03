"""Verification script to test the Phase 1 search slice."""
import asyncio
from app.services.parser.extractor import fallback_heuristic_parser
from app.services.connectors.mock_catalog import MockCatalogConnector
from app.services.delivery.checker import DeliveryChecker
from app.services.ranker.scorer import ProductRanker
from app.schemas.search import SearchRequest
from app.api.v1.endpoints.search import search_sarees

async def run_tests():
    query_1 = "purple saree with golden border under 1500"
    print(f"\n--- Testing Query: '{query_1}' ---")
    
    parsed = fallback_heuristic_parser(query_1)
    print(f"Extracted Color: {parsed.attributes.primary_color}")
    print(f"Extracted Zari/Border: {parsed.attributes.zari_type} / {parsed.attributes.border_type}")
    print(f"Extracted Budget Max: {parsed.budget_max}")
    print(f"Clean Search Phrase: {parsed.clean_search_phrase}")
    
    # Run full endpoint
    request = SearchRequest(query=query_1, pincode="560034")
    response = await search_sarees(request)
    print(f"\nTotal Matching Products: {response.total_found}")
    
    for idx, p in enumerate(response.results, 1):
        print(f"\n{idx}. [{p.platform}] {p.title}")
        print(f"   Price: Rs. {p.price} (MRP: Rs. {p.mrp})")
        print(f"   Delivery: {p.estimated_delivery_days} days ({p.delivery_status})")
        print(f"   Score: {p.match_score}")
        print(f"   Why Matched: {p.why_matched}")

    # Query with deadline constraint
    query_2 = "purple saree with golden border under 1500 deliver in 2 days to 560034"
    print(f"\n--- Testing Query with Deadline: '{query_2}' ---")
    req_2 = SearchRequest(query=query_2)
    resp_2 = await search_sarees(req_2)
    print(f"Detected Deadline Days: {resp_2.parsed_query.deadline_days}")
    print(f"Detected Pincode: {resp_2.parsed_query.pincode}")
    print(f"Products meeting 2-day delivery: {resp_2.total_found}")
    for p in resp_2.results:
        print(f"- {p.title} -> ETA: {p.estimated_delivery_days} days")

if __name__ == "__main__":
    asyncio.run(run_tests())
