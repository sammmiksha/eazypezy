"""Base connector interface for e-commerce platforms."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.schemas.search import SareeQueryAttributes

class BasePlatformConnector(ABC):
    """Abstract connector. Adding a new platform means implementing this class."""

    def __init__(self, platform_name: str):
        self.platform_name = platform_name

    @abstractmethod
    async def search(
        self,
        query: str,
        attributes: SareeQueryAttributes,
        max_budget: Optional[float] = None
    ) -> List[Dict[str, Any]]:
        """Query platform catalog or affiliate feed for products."""
        pass

    @abstractmethod
    async def check_serviceability(
        self,
        pincode: str,
        product_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Check delivery serviceability and estimated delivery days for a pincode."""
        pass
