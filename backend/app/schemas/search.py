"""Pydantic schemas for universal multilingual product search, attribute extraction, and price comparison."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class ExtractedAttributes(BaseModel):
    category: Optional[str] = Field(None, description="e.g. smartphones, electronics, clothing, footwear, appliances")
    brand: Optional[str] = Field(None, description="e.g. Apple, Samsung, Sony, Nike, Suta")
    model_name: Optional[str] = Field(None, description="e.g. iPhone 18, WH-1000XM5, Air Jordan")
    specs: Dict[str, Any] = Field(default_factory=dict, description="e.g. {'storage': '1TB', 'ram': '16GB', 'fabric': 'silk'}")
    required_specs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Non-negotiable requirements extracted from the query, e.g. {'network': '5G'}"
    )
    preferred_specs: Dict[str, Any] = Field(
        default_factory=dict,
        description="Ranking preferences extracted from the query, e.g. {'display_priority': 'best'}"
    )
    color: Optional[str] = Field(None, description="e.g. titanium black, purple, midnight blue")

class ParsedSearchRequest(BaseModel):
    raw_query: str
    detected_language: str = "en"
    translated_query: str
    clean_search_phrase: str
    attributes: ExtractedAttributes
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    deadline_days: Optional[int] = None
    pincode: Optional[str] = None
    sort_by: str = "discount"  # "discount", "price_asc", "relevance"
    clarifications_needed: List[str] = []

class SearchRequest(BaseModel):
    query: str
    pincode: Optional[str] = None
    deadline_days: Optional[int] = None
    budget_max: Optional[float] = None
    sort_by: Optional[str] = "discount"

class ProductOut(BaseModel):
    id: str
    platform: str
    platform_product_id: str
    title: str
    category: str
    description: Optional[str] = None
    brand: Optional[str] = None
    seller: Optional[str] = None
    product_url: str
    image_urls: List[str]
    price: float
    mrp: Optional[float] = None
    discount_percent: float = 0.0
    currency: str = "INR"
    specs: Dict[str, Any] = {}
    
    in_stock: bool
    rating: float
    rating_count: int
    
    estimated_delivery_days: Optional[int] = None
    delivery_status: str
    match_score: float
    is_best_deal: bool = False
    requirement_score: float = 0.0
    requirement_summary: List[str] = Field(default_factory=list)
    price_difference_vs_highest: Optional[float] = None
    why_matched: str

class PlatformDealComparison(BaseModel):
    product_group: str
    lowest_platform: str
    lowest_price: float
    highest_price: float
    max_savings: float
    total_sellers_found: int

class SearchResponse(BaseModel):
    parsed_query: ParsedSearchRequest
    total_found: int
    deal_comparison: Optional[PlatformDealComparison] = None
    results: List[ProductOut]
    data_source: str = "demo_catalog"
