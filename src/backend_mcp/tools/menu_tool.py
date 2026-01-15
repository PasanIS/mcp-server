
"""Menu-related MCP tools."""

from typing import Optional, List, Dict, Any
from ..client import client


async def get_menu_items(
        category: Optional[str] = None,
        is_available: Optional[bool] = None
) -> List[Dict[str, Any]]:

    """
    Get menu items from the restaurant.

    Args:
        category: Filter by category (appetizer, main_course, dessert, beverage, side)
        is_available: Filter by availability status

    Returns:
        List of menu items with details including name, price, description, category
    """

    params = {}
    if category:
        params["category"] = category
    if is_available is not None:
        params["is_available"] = is_available

    response = await client.get("/menu-items/", params=params)
    return response.json()


async def get_menu_item_details(item_id: int) -> Dict[str, Any]:

    """
    Get detailed information about a specific menu item.

    Args:
        item_id: The ID of the menu item

    Returns:
        Detailed menu item information including price, description, preparation time
    """

    response = await client.get(f"/menu-items/{item_id}")
    return response.json()


async def create_menu_item(
        name: str,
        price: float,
        category: str,
        description: Optional[str] = None,
        is_available: bool = True,
        image_url: Optional[str] = None,
        preparation_time: Optional[int] = None
) -> Dict[str, Any]:

    """
    Create a new menu item (staff/admin only).

    Args:
        name: Menu item name
        price: Item price
        category: Menu category (appetizer, main_course, dessert, beverage, side)
        description: Item description
        is_available: Availability status
        image_url: URL to item image
        preparation_time: Preparation time in minutes

    Returns:
        Created menu item details
    """

    payload = {
        "name": name,
        "price": price,
        "category": category,
        "description": description,
        "is_available": is_available,
        "image_url": image_url,
        "preparation_time": preparation_time
    }

    response = await client.post("/menu-items/", json=payload)
    return response.json()


async def update_menu_item(
        item_id: int,
        name: Optional[str] = None,
        price: Optional[float] = None,
        category: Optional[str] = None,
        description: Optional[str] = None,
        is_available: Optional[bool] = None,
        image_url: Optional[str] = None,
        preparation_time: Optional[int] = None
) -> Dict[str, Any]:

    """
    Update an existing menu item (staff/admin only).

    Args:
        item_id: The ID of the menu item to update
        name: New name (optional)
        price: New price (optional)
        category: New category (optional)
        description: New description (optional)
        is_available: New availability status (optional)
        image_url: New image URL (optional)
        preparation_time: New preparation time (optional)

    Returns:
        Updated menu item details
    """

    payload = {k: v for k, v in {
        "name": name,
        "price": price,
        "category": category,
        "description": description,
        "is_available": is_available,
        "image_url": image_url,
        "preparation_time": preparation_time
    }.items() if v is not None}

    response = await client.put(f"/menu-items/{item_id}", json=payload)
    return response.json()