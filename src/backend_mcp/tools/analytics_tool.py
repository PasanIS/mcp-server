
"""Analytics and statistics MCP tools"""

from typing import List, Dict, Any
from ..client import client


async def get_dashboard_stats() -> Dict[str, Any]:

    """Get overall dashboard statistics"""

    response = await client.get("/orders/stats/dashboard")
    return response.json()


async def get_popular_items(limit: int = 10, days: int = 1) -> List[Dict[str, Any]]:

    """Get popular menu items based on order frequency"""

    params = {"limit": limit, "days": days}
    response = await client.get("/orders/stats/popular-items", params=params)
    return response.json()


async def get_revenue_stats(
    start_date: str,
    end_date: str,
    group_by: str = "day"
) -> List[Dict[str, Any]]:

    """Get revenue statistics for a date range"""

    params = {
        "start_date": start_date,
        "end_date": end_date,
        "group_by": group_by
    }
    response = await client.get("/orders/stats/revenue", params=params)
    return response.json()