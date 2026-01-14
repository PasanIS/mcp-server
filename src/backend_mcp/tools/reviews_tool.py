
"""Review-related MCP tools"""

from typing import Optional, Dict, Any
from ..client import client


async def get_order_reviews(order_id: int) -> Dict[str, Any]:

    """Get reviews for a specific order"""

    response = await client.get(f"/reviews/{order_id}")
    return response.json()


async def create_review(
    customer_id: int,
    rating: int,
    comment: Optional[str] = None,
    order_id: Optional[int] = None,
    menu_item_id: Optional[int] = None
) -> Dict[str, Any]:

    """Create a review for an order or menu item"""

    payload = {
        "customer_id": customer_id,
        "rating": rating,
        "comment": comment,
        "order_id": order_id,
        "menu_item_id": menu_item_id
    }
    response = await client.post("/reviews/", json=payload)
    return response.json()
