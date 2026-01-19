
"""Menu-related MCP resources"""

from typing import Dict, Any
from ..client import client


async def get_menu_resource(category: str = "all") -> str:

    """
    Get menu items as a formatted resource.

    This provides the menu in a readable format that can be used
    as context for the chatbot without making function calls.

    Args:
        category: Menu category to fetch (all, appetizer, main_course, etc.)

    Returns:
        Formatted menu resource as string
    """

    params = {} if category == "all" else {"category": category}
    response = await client.get("/menu-items/", params=params)
    items = response.json()

    menu_text = f"# Restaurant Menu ({category.title()})\n\n" # -----menu items as readable text

    current_category = None
    for item in items:
        item_category = item.get('category', 'Unknown')

        # -----Add category header
        if item_category != current_category:
            current_category = item_category
            menu_text += f"\n## {item_category.replace('_', ' ').title()}\n\n"

        # -----Add item details
        name = item.get('name', 'Unknown')
        price = item.get('price', 0)
        desc = item.get('description', 'No description')
        available = "Item is available" if item.get('is_available') else "Item is not available"

        menu_text += f"**{name}** - ${price:.2f} [{available}]\n"
        menu_text += f"  {desc}\n\n"

    return menu_text
