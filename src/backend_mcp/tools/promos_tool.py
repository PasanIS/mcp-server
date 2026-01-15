
"""Promo code-related MCP tools"""

from typing import Dict, Any
from ..client import client


async def apply_promo_code(promo_code: str, order_amount: float) -> Dict[str, Any]:

    """Validate and apply a promo code to calculate discount"""

    payload = {"promo_code": promo_code, "order_amount": order_amount}
    response = await client.post("/promos/apply", json=payload)
    return response.json()


async def get_promo_details(promo_id: int) -> Dict[str, Any]:

    """Get details about a specific promo code"""

    response = await client.get(f"/promos/{promo_id}")
    return response.json()