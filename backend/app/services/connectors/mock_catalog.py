"""Realistic catalog connector simulating affiliate feeds for Myntra, Ajio, Amazon, and Meesho."""
from typing import List, Dict, Any, Optional
from app.services.connectors.base import BasePlatformConnector
from app.schemas.search import SareeQueryAttributes

SAMPLE_SAREES = [
    {
        "platform": "Myntra",
        "platform_product_id": "MYN-PUR-001",
        "title": "Mitera Purple & Golden Art Silk Kanjivaram Saree with Rich Zari Border",
        "description": "Exquisite purple woven design saree with traditional golden zari border and matching unstitched blouse piece.",
        "brand": "Mitera",
        "seller": "FlashRetails",
        "product_url": "https://www.myntra.com/sarees/mitera/purple-zari-saree/12345",
        "image_urls": [
            "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 1299.0,
        "mrp": 3999.0,
        "primary_color": "purple",
        "secondary_color": "golden",
        "border_type": "zari",
        "zari_type": "golden",
        "finish": "glossy",
        "fabric": "silk",
        "occasion": "festive",
        "in_stock": True,
        "rating": 4.3,
        "rating_count": 840,
        "delivery_days_standard": 3
    },
    {
        "platform": "Ajio",
        "platform_product_id": "AJI-PUR-002",
        "title": "Suta Jamuni Violet Banarasi Saree with Intricate Golden Zari Border",
        "description": "Rich violet hue featuring broad gold zari woven floral border and delicate pallu detailing.",
        "brand": "Suta",
        "seller": "Reliance Retail",
        "product_url": "https://www.ajio.com/suta-violet-banarasi-zari-saree/p/4612345",
        "image_urls": [
            "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 1449.0,
        "mrp": 2999.0,
        "primary_color": "purple",
        "secondary_color": "golden",
        "border_type": "zari",
        "zari_type": "golden",
        "finish": "matte",
        "fabric": "banarasi",
        "occasion": "wedding",
        "in_stock": True,
        "rating": 4.5,
        "rating_count": 512,
        "delivery_days_standard": 2
    },
    {
        "platform": "Meesho",
        "platform_product_id": "MSH-PUR-003",
        "title": "Kashvi Pretty Purple Georgette Saree with Fine Gold Border",
        "description": "Lightweight breathable georgette saree in royal purple with subtle golden border.",
        "brand": "Kashvi Creations",
        "seller": "Surat Textile Hub",
        "product_url": "https://www.meesho.com/kashvi-purple-georgette-saree/p/78910",
        "image_urls": [
            "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 899.0,
        "mrp": 1999.0,
        "primary_color": "purple",
        "secondary_color": "golden",
        "border_type": "zari",
        "zari_type": "golden",
        "finish": "sheer",
        "fabric": "georgette",
        "occasion": "party",
        "in_stock": True,
        "rating": 4.1,
        "rating_count": 320,
        "delivery_days_standard": 4
    },
    {
        "platform": "Amazon",
        "platform_product_id": "AMZ-PUR-004",
        "title": "Vardha Women's Kanjivaram Silk Saree in Magenta Purple with Antique Zari",
        "description": "Lustrous kanjivaram silk saree featuring antique golden zari work and contrast pallu.",
        "brand": "Vardha",
        "seller": "Cloudtail",
        "product_url": "https://www.amazon.in/dp/B08XYZ1234",
        "image_urls": [
            "https://images.unsplash.com/photo-1609357605129-26f69add5d6e?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 1499.0,
        "mrp": 4500.0,
        "primary_color": "purple",
        "secondary_color": "golden",
        "border_type": "zari",
        "zari_type": "antique",
        "finish": "matte",
        "fabric": "kanjivaram",
        "occasion": "festive",
        "in_stock": True,
        "rating": 4.2,
        "rating_count": 1150,
        "delivery_days_standard": 2
    },
    {
        "platform": "Myntra",
        "platform_product_id": "MYN-PUR-005",
        "title": "Kalini Deep Purple Chiffon Saree with Scalloped Gold Zari Lace",
        "description": "Flowy solid dark purple chiffon with exquisite scalloped zari border.",
        "brand": "Kalini",
        "seller": "OmniRetail",
        "product_url": "https://www.myntra.com/sarees/kalini/purple-chiffon-saree/889900",
        "image_urls": [
            "https://images.unsplash.com/photo-1594938298603-c8148c4dae35?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 1120.0,
        "mrp": 2499.0,
        "primary_color": "purple",
        "secondary_color": "golden",
        "border_type": "scallop",
        "zari_type": "golden",
        "finish": "sheer",
        "fabric": "chiffon",
        "occasion": "party",
        "in_stock": True,
        "rating": 4.4,
        "rating_count": 680,
        "delivery_days_standard": 3
    },
    {
        "platform": "Myntra",
        "platform_product_id": "MYN-PUR-EXP",
        "title": "Unnati Silks Pure Handloom Kanjivaram Silk Saree in Royal Purple",
        "description": "Pure silk certified handloom saree with heavy pure zari temple border for bridal wear.",
        "brand": "Unnati Silks",
        "seller": "Unnati Weaves",
        "product_url": "https://www.myntra.com/sarees/unnati/royal-purple-pure-silk/998877",
        "image_urls": [
            "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 4899.0,
        "mrp": 8999.0,
        "primary_color": "purple",
        "secondary_color": "golden",
        "border_type": "temple",
        "zari_type": "golden",
        "finish": "glossy",
        "fabric": "silk",
        "occasion": "wedding",
        "in_stock": True,
        "rating": 4.8,
        "rating_count": 210,
        "delivery_days_standard": 2
    },
    {
        "platform": "Ajio",
        "platform_product_id": "AJI-RED-001",
        "title": "Indie Picks Crimson Red Banarasi Silk Saree with Broad Zari Border",
        "description": "Traditional bridal red saree adorned with woven floral gold zari motifs and rich pallu.",
        "brand": "Indie Picks",
        "seller": "Reliance Retail",
        "product_url": "https://www.ajio.com/indie-picks-red-banarasi/p/991122",
        "image_urls": [
            "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 3299.0,
        "mrp": 6999.0,
        "primary_color": "red",
        "secondary_color": "golden",
        "border_type": "zari",
        "zari_type": "golden",
        "finish": "glossy",
        "fabric": "banarasi",
        "occasion": "wedding",
        "in_stock": True,
        "rating": 4.7,
        "rating_count": 430,
        "delivery_days_standard": 3
    },
    {
        "platform": "Amazon",
        "platform_product_id": "AMZ-YEL-001",
        "title": "Siril Festive Mustard Yellow Georgette Saree for Haldi",
        "description": "Bright turmeric yellow saree with subtle golden gota patti border.",
        "brand": "Siril",
        "seller": "Surat Fashions",
        "product_url": "https://www.amazon.in/dp/B09HALDI01",
        "image_urls": [
            "https://images.unsplash.com/photo-1617627143750-d86bc21e42bb?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 999.0,
        "mrp": 2200.0,
        "primary_color": "yellow",
        "secondary_color": "golden",
        "border_type": "zari",
        "zari_type": "golden",
        "finish": "matte",
        "fabric": "georgette",
        "occasion": "haldi",
        "in_stock": True,
        "rating": 4.0,
        "rating_count": 290,
        "delivery_days_standard": 2
    }
]

class MockCatalogConnector(BasePlatformConnector):
    """Unified catalog connector for mock seed data."""

    def __init__(self):
        super().__init__(platform_name="MultiPlatformFeed")

    async def search(
        self,
        query: str,
        attributes: SareeQueryAttributes,
        max_budget: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        results = []
        for item in SAMPLE_SAREES:
            # Budget check
            if max_budget is not None and item["price"] > max_budget:
                continue
            results.append(dict(item))
        return results

    async def check_serviceability(
        self,
        pincode: str,
        product_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Realistic pincode serviceability resolution."""
        if not pincode or len(pincode) != 6 or not pincode.isdigit():
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 3,
                "status": "estimated",
                "notes": "Estimated delivery without pincode"
            }
        
        # Major metro pin prefixes (56: Bangalore, 11: Delhi, 40: Mumbai, 60: Chennai, 50: Hyderabad)
        prefix = pincode[:2]
        if prefix in ["56", "11", "40", "60", "50"]:
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 2,
                "status": "confirmed",
                "notes": f"Fast metro delivery to {pincode}"
            }
        elif prefix in ["70", "38", "30", "41"]:
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 3,
                "status": "confirmed",
                "notes": f"Standard delivery to {pincode}"
            }
        elif pincode.startswith("79") or pincode.startswith("19"):
            # Remote / hilly areas
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 6,
                "status": "confirmed",
                "notes": f"Extended transit to {pincode}"
            }
        else:
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 4,
                "status": "confirmed",
                "notes": f"Deliverable to {pincode}"
            }
