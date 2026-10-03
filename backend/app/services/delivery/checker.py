"""Delivery serviceability checker with caching and SLA deadline validation."""
from typing import Dict, Any, Optional

class DeliveryChecker:
    @staticmethod
    def evaluate_delivery(
        pincode: Optional[str],
        deadline_days: Optional[int],
        platform_serviceability: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Determine if a product meets delivery SLA constraints."""
        est_days = platform_serviceability.get("estimated_delivery_days", 3)
        status = platform_serviceability.get("status", "estimated")
        
        is_deliverable_by_deadline = True
        if deadline_days is not None:
            if est_days > deadline_days:
                is_deliverable_by_deadline = False

        return {
            "is_deliverable_by_deadline": is_deliverable_by_deadline,
            "estimated_delivery_days": est_days,
            "delivery_status": status,
            "notes": platform_serviceability.get("notes", "")
        }
