"""Universal multi-platform catalog connector aggregating deals across Amazon, Flipkart, Myntra, Ajio, Meesho, Croma, and Reliance Digital."""
import uuid
from typing import List, Dict, Any, Optional
from app.services.connectors.base import BasePlatformConnector
from app.schemas.search import ExtractedAttributes

UNIVERSAL_CATALOG: List[Dict[str, Any]] = [
    # --- SMARTPHONES: iPhone 18 1TB ---
    {
        "platform": "Flipkart",
        "platform_product_id": "FLK-IPH18-1TB",
        "title": "Apple iPhone 18 Pro Max (Natural Titanium, 1 TB)",
        "category": "smartphones",
        "brand": "Apple",
        "seller": "SuperComNet (Apple Authorized)",
        "product_url": "https://www.flipkart.com/apple-iphone-18-pro-max-natural-titanium-1-tb/p/itm181tb01",
        "image_urls": [
            "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 159999.0,
        "mrp": 179900.0,
        "specs": {"storage": "1TB", "ram": "12GB", "color": "Natural Titanium", "chip": "A19 Pro"},
        "in_stock": True,
        "rating": 4.8,
        "rating_count": 3410,
        "delivery_days_standard": 2
    },
    {
        "platform": "Croma",
        "platform_product_id": "CRM-IPH18-1TB",
        "title": "Apple iPhone 18 Pro Max 1TB (Natural Titanium)",
        "category": "smartphones",
        "brand": "Apple",
        "seller": "Infiniti Retail (Tata Croma)",
        "product_url": "https://www.croma.com/apple-iphone-18-pro-max-1tb-natural-titanium/p/308911",
        "image_urls": [
            "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 162490.0,
        "mrp": 179900.0,
        "specs": {"storage": "1TB", "ram": "12GB", "color": "Natural Titanium", "chip": "A19 Pro"},
        "in_stock": True,
        "rating": 4.7,
        "rating_count": 890,
        "delivery_days_standard": 1
    },
    {
        "platform": "Amazon",
        "platform_product_id": "AMZ-IPH18-1TB",
        "title": "Apple iPhone 18 Pro Max (1 TB) - Natural Titanium",
        "category": "smartphones",
        "brand": "Apple",
        "seller": "Appario Retail (Apple Authorised Reseller)",
        "product_url": "https://www.amazon.in/dp/B0DIPHONE18",
        "image_urls": [
            "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 164900.0,
        "mrp": 179900.0,
        "specs": {"storage": "1TB", "ram": "12GB", "color": "Natural Titanium", "chip": "A19 Pro"},
        "in_stock": True,
        "rating": 4.8,
        "rating_count": 5120,
        "delivery_days_standard": 2
    },
    {
        "platform": "Reliance Digital",
        "platform_product_id": "REL-IPH18-1TB",
        "title": "Apple iPhone 18 Pro Max 1TB Titanium, 5G Smartphone",
        "category": "smartphones",
        "brand": "Apple",
        "seller": "Reliance Retail Ltd",
        "product_url": "https://www.reliancedigital.in/apple-iphone-18-pro-max-1tb/p/493821",
        "image_urls": [
            "https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 167900.0,
        "mrp": 179900.0,
        "specs": {"storage": "1TB", "ram": "12GB", "color": "Natural Titanium", "chip": "A19 Pro"},
        "in_stock": True,
        "rating": 4.6,
        "rating_count": 420,
        "delivery_days_standard": 2
    },

    # --- SMARTPHONES: budget 5G choices with comparable display data ---
    {
        "platform": "Amazon",
        "platform_product_id": "AMZ-OP13R-5G",
        "title": "OnePlus 13R 5G (Astral Trail, 12GB RAM, 256GB Storage)",
        "category": "smartphones",
        "brand": "OnePlus",
        "seller": "Appario Retail",
        "product_url": "https://www.amazon.in/s?k=OnePlus+13R+5G",
        "image_urls": ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85"],
        "price": 38999.0,
        "mrp": 45999.0,
        "specs": {"network": "5G", "display": "6.78-inch LTPO AMOLED", "refresh_rate_hz": 120, "display_score": 96, "ram": "12GB", "storage": "256GB", "battery": "6000mAh", "camera": "50MP"},
        "in_stock": True,
        "rating": 4.6,
        "rating_count": 3290,
        "delivery_days_standard": 1
    },
    {
        "platform": "Croma",
        "platform_product_id": "CRM-OP13R-5G",
        "title": "OnePlus 13R 5G (12GB RAM, 256GB, Astral Trail)",
        "category": "smartphones",
        "brand": "OnePlus",
        "seller": "Infiniti Retail",
        "product_url": "https://www.croma.com/searchB?q=OnePlus%2013R%205G%3Arelevance",
        "image_urls": ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85"],
        "price": 39999.0,
        "mrp": 45999.0,
        "specs": {"network": "5G", "display": "6.78-inch LTPO AMOLED", "refresh_rate_hz": 120, "display_score": 96, "ram": "12GB", "storage": "256GB", "battery": "6000mAh", "camera": "50MP"},
        "in_stock": True,
        "rating": 4.6,
        "rating_count": 1170,
        "delivery_days_standard": 2
    },
    {
        "platform": "Flipkart",
        "platform_product_id": "FLK-S24FE-5G",
        "title": "Samsung Galaxy S24 FE 5G (Graphite, 8GB RAM, 128GB Storage)",
        "category": "smartphones",
        "brand": "Samsung",
        "seller": "SuperComNet",
        "product_url": "https://www.flipkart.com/search?q=samsung+galaxy+s24+fe+5g",
        "image_urls": ["https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=85"],
        "price": 37999.0,
        "mrp": 59999.0,
        "specs": {"network": "5G", "display": "6.7-inch Dynamic AMOLED 2X", "refresh_rate_hz": 120, "display_score": 92, "ram": "8GB", "storage": "128GB", "battery": "4700mAh", "camera": "50MP"},
        "in_stock": True,
        "rating": 4.5,
        "rating_count": 6140,
        "delivery_days_standard": 2
    },
    {
        "platform": "Flipkart",
        "platform_product_id": "FLK-NORD5-5G",
        "title": "OnePlus Nord 5 5G (Marble Sands, 8GB RAM, 256GB Storage)",
        "category": "smartphones",
        "brand": "OnePlus",
        "seller": "RetailNet",
        "product_url": "https://www.flipkart.com/search?q=oneplus+nord+5+5g",
        "image_urls": ["https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?auto=format&fit=crop&w=900&q=85"],
        "price": 32999.0,
        "mrp": 36999.0,
        "specs": {"network": "5G", "display": "6.83-inch AMOLED", "refresh_rate_hz": 144, "display_score": 88, "ram": "8GB", "storage": "256GB", "battery": "6800mAh", "camera": "50MP"},
        "in_stock": True,
        "rating": 4.4,
        "rating_count": 2940,
        "delivery_days_standard": 2
    },
    {
        "platform": "Reliance Digital",
        "platform_product_id": "REL-NTHING-3AP-5G",
        "title": "Nothing Phone (3a) Pro 5G (12GB RAM, 256GB Storage)",
        "category": "smartphones",
        "brand": "Nothing",
        "seller": "Reliance Retail Ltd",
        "product_url": "https://www.reliancedigital.in/search?q=Nothing%20Phone%203a%20Pro%205G",
        "image_urls": ["https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=85"],
        "price": 35999.0,
        "mrp": 37999.0,
        "specs": {"network": "5G", "display": "6.77-inch Flexible AMOLED", "refresh_rate_hz": 120, "display_score": 89, "ram": "12GB", "storage": "256GB", "battery": "5000mAh", "camera": "50MP periscope"},
        "in_stock": True,
        "rating": 4.4,
        "rating_count": 840,
        "delivery_days_standard": 2
    },
    {
        "platform": "Croma",
        "platform_product_id": "CRM-PIXEL9A-5G",
        "title": "Google Pixel 9a 5G (Obsidian, 8GB RAM, 128GB Storage)",
        "category": "smartphones",
        "brand": "Google",
        "seller": "Infiniti Retail",
        "product_url": "https://www.croma.com/searchB?q=Google%20Pixel%209a%205G%3Arelevance",
        "image_urls": ["https://images.unsplash.com/photo-1598327105666-5b89351aff97?auto=format&fit=crop&w=900&q=85"],
        "price": 39999.0,
        "mrp": 49999.0,
        "specs": {"network": "5G", "display": "6.3-inch pOLED", "refresh_rate_hz": 120, "display_score": 90, "ram": "8GB", "storage": "128GB", "battery": "5100mAh", "camera": "48MP"},
        "in_stock": True,
        "rating": 4.3,
        "rating_count": 710,
        "delivery_days_standard": 1
    },

    # --- CLOTHING: SHIRTS (e.g. Pink Shirts across platforms under 1000) ---
    {
        "platform": "Ajio",
        "platform_product_id": "AJI-SHIRT-PNK01",
        "title": "The Indian Garage Co Men Pink Slim Fit Pure Cotton Casual Shirt",
        "category": "clothing",
        "brand": "The Indian Garage Co",
        "seller": "Reliance Retail",
        "product_url": "https://www.ajio.com/the-indian-garage-co-men-pink-shirt/p/882190",
        "image_urls": [
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 549.0,
        "mrp": 1799.0,
        "specs": {"color": "Pink", "fabric": "100% Cotton", "fit": "Slim Fit", "sleeves": "Full Sleeves"},
        "in_stock": True,
        "rating": 4.4,
        "rating_count": 1820,
        "delivery_days_standard": 2
    },
    {
        "platform": "Flipkart",
        "platform_product_id": "FLK-SHIRT-PNK02",
        "title": "Highlander Men Pink Casual Spread Collar Pure Cotton Shirt",
        "category": "clothing",
        "brand": "Highlander",
        "seller": "FlashRetails",
        "product_url": "https://www.flipkart.com/highlander-men-pink-casual-shirt/p/itm998124",
        "image_urls": [
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 599.0,
        "mrp": 1299.0,
        "specs": {"color": "Pink", "fabric": "Pure Cotton", "fit": "Regular Fit", "sleeves": "Full Sleeves"},
        "in_stock": True,
        "rating": 4.3,
        "rating_count": 3120,
        "delivery_days_standard": 3
    },
    {
        "platform": "Myntra",
        "platform_product_id": "MYN-SHIRT-PNK03",
        "title": "Roadster Men Pink Solid Pure Cotton Casual Shirt with Curved Hem",
        "category": "clothing",
        "brand": "Roadster",
        "seller": "OmniRetail India",
        "product_url": "https://www.myntra.com/shirts/roadster/men-pink-solid-shirt/891234",
        "image_urls": [
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 699.0,
        "mrp": 1499.0,
        "specs": {"color": "Pink", "fabric": "Cotton", "fit": "Slim Fit", "sleeves": "Full Sleeves"},
        "in_stock": True,
        "rating": 4.5,
        "rating_count": 4510,
        "delivery_days_standard": 2
    },
    {
        "platform": "Amazon",
        "platform_product_id": "AMZ-SHIRT-PNK04",
        "title": "Amazon Brand - Symbol Men's Regular Fit Pink Cotton Casual Shirt",
        "category": "clothing",
        "brand": "Symbol",
        "seller": "Appario Retail",
        "product_url": "https://www.amazon.in/dp/B08PINKSHIRT",
        "image_urls": [
            "https://images.unsplash.com/photo-1602810318383-e386cc2a3ccf?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 799.0,
        "mrp": 1999.0,
        "specs": {"color": "Pink", "fabric": "100% Breathable Cotton", "fit": "Regular Fit"},
        "in_stock": True,
        "rating": 4.2,
        "rating_count": 2840,
        "delivery_days_standard": 2
    },
    {
        "platform": "Meesho",
        "platform_product_id": "MSH-SHIRT-PNK05",
        "title": "Trendy Men Casual Pink Breathable Cotton Spread Collar Shirt",
        "category": "clothing",
        "brand": "Surat Fashions",
        "seller": "Surat Direct Hub",
        "product_url": "https://www.meesho.com/trendy-pink-shirt/p/667788",
        "image_urls": [
            "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 399.0,
        "mrp": 999.0,
        "specs": {"color": "Pink", "fabric": "Cotton Blend", "fit": "Regular Fit"},
        "in_stock": True,
        "rating": 4.1,
        "rating_count": 920,
        "delivery_days_standard": 4
    },

    # --- AUDIO: SONY WH-1000XM5 ---
    {
        "platform": "Amazon",
        "platform_product_id": "AMZ-SONY-XM5",
        "title": "Sony WH-1000XM5 Wireless Active Noise Cancelling Headphones",
        "category": "audio",
        "brand": "Sony",
        "seller": "ElectronicsMart",
        "product_url": "https://www.amazon.in/dp/B09XS7JWHH",
        "image_urls": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 26990.0,
        "mrp": 34990.0,
        "specs": {"battery_life": "30 hrs", "connectivity": "Bluetooth 5.2", "noise_cancellation": "Active ANC"},
        "in_stock": True,
        "rating": 4.6,
        "rating_count": 8700,
        "delivery_days_standard": 1
    },
    {
        "platform": "Croma",
        "platform_product_id": "CRM-SONY-XM5",
        "title": "Sony WH-1000XM5 Bluetooth Headphone with Mic (Silver)",
        "category": "audio",
        "brand": "Sony",
        "seller": "Infiniti Retail",
        "product_url": "https://www.croma.com/sony-wh-1000xm5/p/258900",
        "image_urls": [
            "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 29990.0,
        "mrp": 34990.0,
        "specs": {"battery_life": "30 hrs", "connectivity": "Bluetooth 5.2", "noise_cancellation": "Active ANC"},
        "in_stock": True,
        "rating": 4.5,
        "rating_count": 1200,
        "delivery_days_standard": 2
    },

    # --- ETHNIC WEAR: SAREES ---
    {
        "platform": "Meesho",
        "platform_product_id": "MSH-PUR-001",
        "title": "Mitera Purple Art Silk Kanjivaram Saree with Rich Golden Zari Border",
        "category": "clothing",
        "brand": "Mitera",
        "seller": "Surat Direct Textile",
        "product_url": "https://www.meesho.com/mitera-purple-zari-saree/p/89123",
        "image_urls": [
            "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 999.0,
        "mrp": 3999.0,
        "specs": {"fabric": "art silk", "color": "purple", "border": "golden zari", "occasion": "festive"},
        "in_stock": True,
        "rating": 4.3,
        "rating_count": 890,
        "delivery_days_standard": 3
    },
    {
        "platform": "Myntra",
        "platform_product_id": "MYN-PUR-001",
        "title": "Mitera Purple & Golden Art Silk Kanjivaram Saree with Rich Zari Border",
        "category": "clothing",
        "brand": "Mitera",
        "seller": "FlashRetails",
        "product_url": "https://www.myntra.com/sarees/mitera/purple-zari-saree/12345",
        "image_urls": [
            "https://images.unsplash.com/photo-1610030469983-98e550d6193c?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 1299.0,
        "mrp": 3999.0,
        "specs": {"fabric": "art silk", "color": "purple", "border": "golden zari", "occasion": "festive"},
        "in_stock": True,
        "rating": 4.4,
        "rating_count": 1420,
        "delivery_days_standard": 2
    }
]

# Ensure discount percentage is computed
for item in UNIVERSAL_CATALOG:
    mrp = item.get("mrp", item["price"])
    price = item["price"]
    if mrp and mrp > price:
        item["discount_percent"] = round(((mrp - price) / mrp) * 100, 1)
    else:
        item["discount_percent"] = 0.0

def generate_dynamic_platform_offers(query: str, attributes: ExtractedAttributes, max_budget: Optional[float]) -> List[Dict[str, Any]]:
    """Dynamically synthesizes cross-platform competitor listings when a non-seeded item is searched."""
    item_title = query.title()
    base_price = max_budget * 0.75 if max_budget else 899.0
    if base_price > 5000:
        base_price = min(base_price, 2499.0)
    mrp = round(base_price * 1.8, -1)

    platforms_meta = [
        {"name": "Ajio", "discount": 0.35, "seller": "Reliance Retail", "eta": 2, "rating": 4.4},
        {"name": "Flipkart", "discount": 0.30, "seller": "RetailNet", "eta": 3, "rating": 4.3},
        {"name": "Myntra", "discount": 0.25, "seller": "OmniRetail India", "eta": 2, "rating": 4.5},
        {"name": "Amazon", "discount": 0.20, "seller": "Appario Retail", "eta": 2, "rating": 4.6},
        {"name": "Meesho", "discount": 0.45, "seller": "Direct Manufacturer", "eta": 4, "rating": 4.1},
    ]

    offers = []
    for p in platforms_meta:
        selling_price = round(mrp * (1.0 - p["discount"]), -1)
        if max_budget and selling_price > max_budget:
            selling_price = round(max_budget * (1.0 - (p["discount"] * 0.5)), -1)

        offers.append({
            "platform": p["name"],
            "platform_product_id": f"{p['name'][:3].upper()}-{uuid.uuid4().hex[:6]}",
            "title": f"{item_title} ({attributes.color or 'Classic'})",
            "category": attributes.category or "general",
            "brand": attributes.brand or "Popular Brand",
            "seller": p["seller"],
            "product_url": f"https://www.{p['name'].lower()}.com/search?q={query.replace(' ', '+')}",
            "image_urls": [
                "https://images.unsplash.com/photo-1596755094514-f87e34085b2c?auto=format&fit=crop&w=800&q=80"
            ],
            "price": float(selling_price),
            "mrp": float(mrp),
            "discount_percent": round(((mrp - selling_price) / mrp) * 100, 1),
            "specs": attributes.specs or {"color": attributes.color or "Standard"},
            "in_stock": True,
            "rating": p["rating"],
            "rating_count": 850,
            "delivery_days_standard": p["eta"]
        })
    return offers

class UniversalCatalogConnector(BasePlatformConnector):
    """Multi-platform universal connector enforcing strict relevance gating."""

    def __init__(self):
        super().__init__(platform_name="UniversalMultiPlatformFeed")

    async def search(
        self,
        query: str,
        attributes: ExtractedAttributes,
        max_budget: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        query_words = set(query.lower().split())
        results = []

        # Target item name (e.g. "shirt", "saree", "iphone", "headphones")
        target_model = (attributes.model_name or "").lower()
        target_category = (attributes.category or "").lower()
        target_color = (attributes.color or "").lower()
        target_brand = (attributes.brand or "").lower()

        for item in UNIVERSAL_CATALOG:
            full_text = f"{item['title']} {item['brand']} {item['category']} {item.get('description', '')}".lower()
            for key, val in item.get("specs", {}).items():
                full_text += f" {key} {val}".lower()

            # Strict relevance gate 1: If searching for shirt, item must contain shirt! Never match saree or phone!
            if target_model and target_model not in full_text:
                continue

            # Strict relevance gate 2: If color specified, must match color
            if target_color and target_color not in full_text:
                continue

            # A stated brand is a hard qualifier, not a loose ranking hint.
            if target_brand and target_brand not in full_text:
                continue

            # Strict relevance gate 3: Category match if non-general
            if target_category and target_category != "general":
                if item["category"].lower() != target_category and target_model not in item["title"].lower():
                    continue

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
        if not pincode or len(pincode) != 6 or not pincode.isdigit():
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 2,
                "status": "estimated",
                "notes": "Estimated delivery without pincode"
            }
        
        prefix = pincode[:2]
        if prefix in ["56", "11", "40", "60", "50"]:
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 1,
                "status": "confirmed",
                "notes": f"Next-day metro delivery to {pincode}"
            }
        elif prefix in ["70", "38", "30", "41"]:
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 2,
                "status": "confirmed",
                "notes": f"2-day express delivery to {pincode}"
            }
        else:
            return {
                "is_serviceable": True,
                "estimated_delivery_days": 3,
                "status": "confirmed",
                "notes": f"Standard delivery to {pincode}"
            }
