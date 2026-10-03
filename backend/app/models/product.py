"""SQLAlchemy Product and Delivery Models."""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, Numeric, Boolean, Integer, DateTime, Text, JSON
from app.core.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    platform = Column(String(50), nullable=False, index=True)
    platform_product_id = Column(String(100), nullable=False)
    title = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    brand = Column(String(100), nullable=True)
    seller = Column(String(100), nullable=True)
    product_url = Column(Text, nullable=False)
    image_urls = Column(JSON, nullable=False, default=list)

    # Pricing
    price = Column(Numeric(10, 2), nullable=False, index=True)
    mrp = Column(Numeric(10, 2), nullable=True)
    currency = Column(String(3), default="INR")

    # Saree Attributes
    primary_color = Column(String(50), nullable=True, index=True)
    secondary_color = Column(String(50), nullable=True)
    border_type = Column(String(50), nullable=True)   # 'zari', 'temple', 'contrast', 'embroidered'
    zari_type = Column(String(50), nullable=True)     # 'golden', 'silver', 'copper', 'antique'
    finish = Column(String(50), nullable=True)        # 'matte', 'glossy', 'sheer'
    fabric = Column(String(50), nullable=True, index=True)  # 'silk', 'kanjivaram', 'banarasi', 'georgette', 'chiffon'
    occasion = Column(String(50), nullable=True)

    # Embeddings (Stored as JSON array for cross-DB compatibility, or native vector in Postgres)
    text_embedding = Column(JSON, nullable=True)
    image_embedding = Column(JSON, nullable=True)

    # Fulfillment & Social proof
    in_stock = Column(Boolean, default=True, index=True)
    rating = Column(Numeric(2, 1), default=4.0)
    rating_count = Column(Integer, default=0)
    delivery_days_standard = Column(Integer, default=3)
    raw_metadata = Column(JSON, default=dict)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class DeliveryCache(Base):
    __tablename__ = "delivery_cache"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    platform = Column(String(50), nullable=False, index=True)
    pincode = Column(String(10), nullable=False, index=True)
    is_serviceable = Column(Boolean, nullable=False)
    estimated_delivery_days = Column(Integer, nullable=True)
    checked_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=False)
