"""Pydantic schemas for search query, extracted attributes, and results."""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class SareeQueryAttributes(BaseModel):
    primary_color: Optional[str] = Field(None, description="Dominant color, e.g. purple, teal, red")
    secondary_color: Optional[str] = Field(None, description="Accent/border color, e.g. golden, silver")
    border_type: Optional[str] = Field(None, description="Border style: zari, temple, contrast, embroidered, etc.")
    zari_type: Optional[str] = Field(None, description="Zari finish: golden, silver, copper, antique, etc.")
    finish: Optional[str] = Field(None, description="Finish/luster: matte, glossy, sheer, etc.")
    fabric: Optional[str] = Field(None, description="Fabric: silk, kanjivaram, banarasi, georgette, chiffon, cotton, etc.")
    occasion: Optional[str] = Field(None, description="Occasion: wedding, festive, party, casual, etc.")

class ParsedSearchRequest(BaseModel):
    raw_query: str
    detected_language: str = "en"
    translated_query: str
    clean_search_phrase: str
    attributes: SareeQueryAttributes
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    deadline_days: Optional[int] = None
    pincode: Optional[str] = None
    clarifications_needed: List[str] = []

class SearchRequest(BaseModel):
    query: str
    pincode: Optional[str] = None
    deadline_days: Optional[int] = None
    budget_max: Optional[float] = None

class ProductOut(BaseModel):
    id: str
    platform: str
    platform_product_id: str
    title: str
    description: Optional[str] = None
    brand: Optional[str] = None
    seller: Optional[str] = None
    product_url: str
    image_urls: List[str]
    price: float
    mrp: Optional[float] = None
    currency: str = "INR"
    
    primary_color: Optional[str] = None
    secondary_color: Optional[str] = None
    border_type: Optional[str] = None
    zari_type: Optional[str] = None
    finish: Optional[str] = None
    fabric: Optional[str] = None
    occasion: Optional[str] = None
    
    in_stock: bool
    rating: float
    rating_count: int
    
    # Fulfillment & Search Match Metadata
    estimated_delivery_days: Optional[int] = None
    delivery_status: str  # "confirmed", "estimated", "unverified", "not_serviceable"
    match_score: float
    why_matched: str

class SearchResponse(BaseModel):
    parsed_query: ParsedSearchRequest
    total_found: int
    results: List[ProductOut]
