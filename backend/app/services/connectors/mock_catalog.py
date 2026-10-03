"""Universal catalog connector aggregating deals across Amazon, Flipkart, Croma, Reliance Digital, Myntra, Ajio, and Meesho."""
from typing import List, Dict, Any, Optional
from app.services.connectors.base import BasePlatformConnector
from app.schemas.search import ExtractedAttributes

UNIVERSAL_CATALOG: List[Dict[str, Any]] = [
    # --- SMARTPHONES & GADGETS: iPhone 18 1TB Multi-Platform Deal Comparison ---
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
        "specs": {"storage": "1TB", "ram": "12GB", "color": "Natural Titanium", "display": "6.9 inch OLED", "chip": "A19 Pro"},
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
        "specs": {"storage": "1TB", "ram": "12GB", "color": "Natural Titanium", "display": "6.9 inch OLED", "chip": "A19 Pro"},
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
        "specs": {"storage": "1TB", "ram": "12GB", "color": "Natural Titanium", "display": "6.9 inch OLED", "chip": "A19 Pro"},
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
        "specs": {"storage": "1TB", "ram": "12GB", "color": "Natural Titanium", "display": "6.9 inch OLED", "chip": "A19 Pro"},
        "in_stock": True,
        "rating": 4.6,
        "rating_count": 420,
        "delivery_days_standard": 2
    },

    # --- SONY HEADPHONES ---
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

    # --- LAPTOPS: MacBook Air ---
    {
        "platform": "Amazon",
        "platform_product_id": "AMZ-MBA-M3",
        "title": "Apple MacBook Air 15-inch M3 Chip (16GB Unified Memory, 512GB SSD) - Starlight",
        "category": "laptops",
        "brand": "Apple",
        "seller": "Appario Retail",
        "product_url": "https://www.amazon.in/dp/B0CX237890",
        "image_urls": [
            "https://images.unsplash.com/photo-1517336714731-489689fd1ca8?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 139900.0,
        "mrp": 154900.0,
        "specs": {"ram": "16GB", "storage": "512GB", "screen": "15.3 inch Liquid Retina", "chip": "Apple M3"},
        "in_stock": True,
        "rating": 4.8,
        "rating_count": 1240,
        "delivery_days_standard": 2
    },

    # --- CLOTHING & ETHNIC WEAR: Sarees ---
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
    },
    {
        "platform": "Ajio",
        "platform_product_id": "AJI-PUR-002",
        "title": "Suta Jamuni Violet Banarasi Saree with Intricate Golden Zari Border",
        "category": "clothing",
        "brand": "Suta",
        "seller": "Reliance Retail",
        "product_url": "https://www.ajio.com/suta-violet-banarasi-zari-saree/p/4612345",
        "image_urls": [
            "https://images.unsplash.com/photo-1583391733956-3750e0ff4e8b?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 1449.0,
        "mrp": 2999.0,
        "specs": {"fabric": "banarasi", "color": "violet", "border": "golden zari", "occasion": "wedding"},
        "in_stock": True,
        "rating": 4.5,
        "rating_count": 512,
        "delivery_days_standard": 2
    },

    # --- SNEAKERS & FOOTWEAR ---
    {
        "platform": "Myntra",
        "platform_product_id": "MYN-NIKE-AJ1",
        "title": "Nike Air Jordan 1 Retro High OG Men's High-Top Sneakers",
        "category": "footwear",
        "brand": "Nike",
        "seller": "Nike India Retail",
        "product_url": "https://www.myntra.com/sneakers/nike/air-jordan-1-retro-high/99812",
        "image_urls": [
            "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 13995.0,
        "mrp": 16995.0,
        "specs": {"color": "Chicago Red / Black / White", "material": "Genuine Leather", "sole": "Rubber Cupsole"},
        "in_stock": True,
        "rating": 4.7,
        "rating_count": 2100,
        "delivery_days_standard": 2
    },
    {
        "platform": "Ajio Luxe",
        "platform_product_id": "AJI-NIKE-AJ1",
        "title": "Nike Men Air Jordan 1 Retro High Top Lace-Up Sneakers",
        "category": "footwear",
        "brand": "Nike",
        "seller": "Ajio Luxe Retailing",
        "product_url": "https://luxe.ajio.com/nike-air-jordan-1/p/88219",
        "image_urls": [
            "https://images.unsplash.com/photo-1552346154-21d32810aba3?auto=format&fit=crop&w=800&q=80"
        ],
        "price": 15495.0,
        "mrp": 16995.0,
        "specs": {"color": "Chicago Red / Black / White", "material": "Genuine Leather", "sole": "Rubber Cupsole"},
        "in_stock": True,
        "rating": 4.6,
        "rating_count": 480,
        "delivery_days_standard": 3
    }
]

# Calculate discount percent dynamically
for item in UNIVERSAL_CATALOG:
    mrp = item.get("mrp", item["price"])
    price = item["price"]
    if mrp and mrp > price:
        item["discount_percent"] = round(((mrp - price) / mrp) * 100, 1)
    else:
        item["discount_percent"] = 0.0

class UniversalCatalogConnector(BasePlatformConnector):
    """Multi-platform universal connector."""

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

        for item in UNIVERSAL_CATALOG:
            # Budget check
            if max_budget is not None and item["price"] > max_budget:
                continue

            full_text = f"{item['title']} {item['brand']} {item['category']} {item.get('description', '')}".lower()
            for key, val in item.get("specs", {}).items():
                full_text += f" {key} {val}".lower()

            # If user explicitly searched for a specific model (e.g. iPhone 18, WH-1000XM5)
            if attributes.model_name:
                clean_model = attributes.model_name.lower().replace("pro max", "").replace("pro", "").strip()
                if clean_model not in full_text:
                    continue

            # Check specs if provided (e.g. storage like 1TB)
            if attributes.specs.get("storage"):
                storage_val = attributes.specs["storage"].lower()
                if storage_val not in full_text:
                    continue

            # Check color if provided
            if attributes.color and attributes.color.lower() not in full_text:
                continue

            results.append(dict(item))

        # If strict overlap yielded nothing, return broad matching
        if not results:
            for item in UNIVERSAL_CATALOG:
                if max_budget is None or item["price"] <= max_budget:
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
                "estimated_delivery_days": 4,
                "status": "confirmed",
                "notes": f"Standard delivery to {pincode}"
            }
