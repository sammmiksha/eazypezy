"""Verification test for universal multilingual search and price comparison."""
import asyncio
from app.schemas.search import SearchRequest
from app.api.v1.endpoints.search import search_products

async def run_tests():
    queries = [
        "iPhone 18 1TB",
        "mujhe sabse sasta iPhone 18 1TB chahiye",
        "Sony WH-1000XM5",
        "purple saree with golden border under 1500"
    ]

    for q in queries:
        print(f"\n========================================================")
        print(f"SEARCH QUERY: '{q}'")
        print(f"========================================================")
        req = SearchRequest(query=q)
        resp = await search_products(req)

        print(f"Detected Language: {resp.parsed_query.detected_language}")
        print(f"Clean Search Phrase: {resp.parsed_query.clean_search_phrase}")
        print(f"Extracted Brand/Model: {resp.parsed_query.attributes.brand} / {resp.parsed_query.attributes.model_name}")
        print(f"Extracted Specs: {resp.parsed_query.attributes.specs}")

        if resp.deal_comparison:
            dc = resp.deal_comparison
            print(f"\nDEAL COMPARISON SUMMARY:")
            print(f"- Lowest Price Seller: {dc.lowest_platform} at Rs. {int(dc.lowest_price):,}")
            print(f"- Highest Price Seller: Rs. {int(dc.highest_price):,}")
            print(f"- Max Savings for User: Rs. {int(dc.max_savings):,} across {dc.total_sellers_found} platforms")

        print(f"\nTOP RESULTS RANKED BY BEST DEAL & DISCOUNT:")
        for idx, p in enumerate(resp.results, 1):
            deal_badge = "[BEST DEAL - LOWEST PRICE]" if p.is_best_deal else ""
            print(f"{idx}. [{p.platform}] {p.title} {deal_badge}")
            print(f"   Price: Rs. {int(p.price):,} | MRP: Rs. {int(p.mrp):,} ({p.discount_percent:.0f}% off)")
            print(f"   Delivery: {p.estimated_delivery_days} days ({p.delivery_status})")
            print(f"   Rationale: {p.why_matched}")

if __name__ == "__main__":
    asyncio.run(run_tests())
