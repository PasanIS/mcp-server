
"""Order-related MCP prompts(reusable)"""

from typing import Dict, Any, Optional


def create_order_prompt(customer_name: Optional[str] = None) -> Dict[str, Any]:

    """
    Generate a prompt template for creating orders.

    This prompt guides the conversation for order placement,
    including gathering necessary information step by step.

    Args:
        customer_name: Name of the customer (optional)

    Returns:
        Prompt template dict
    """

    greeting = f"Hello {customer_name}! " if customer_name else "Hello! "

    return {
        "name": "create_order",
        "description": "Guide customer through placing an order",
        "template": f"""{greeting}I'll help you place your order today.

To complete your order, I'll need to gather the following information:

1. **What would you like to order?**
   - Browse our menu by asking "show me the menu" or "what appetizers do you have?"
   - Add items one by one or tell me everything at once

2. **Order Type**
   - Dine-in
   - Takeaway
   - Delivery

3. **Delivery Address** (for delivery orders)
   - Where should we deliver your order?

4. **Special Instructions** (optional)
   - Any allergies, preferences, or special requests?

5. **Promo Code** (optional)
   - Do you have a promo code?

Let's start! What would you like to order?""",
        "suggested_tools":
        [
            "get_menu_items",
            "create_order",
            "apply_promo_code"
        ]
    }


def track_order_prompt(order_id: int) -> Dict[str, Any]:

    """
    Generate a prompt template for order tracking.

    Args:
        order_id: ID of the order to track

    Returns:
        Prompt template dict
    """

    return {
        "name": "track_order",
        "description": "Help customer track their order",
        "template": f"""I'll check the status of order #{order_id} for you.

I can provide:
- Current order status
- Order items and total
- Estimated completion/delivery time
- Complete order journey/history

What would you like to know about your order?""",
        "suggested_tools":
        [
            "get_order_details",
            "get_order_journey"
        ]
    }


def order_assistance_prompt() -> Dict[str, Any]:

    """
    General order assistance prompt.

    Returns:
        Prompt template dict
    """

    return {
        "name": "order_assistance",
        "description": "General order help and guidance",
        "template": """Welcome to our restaurant! I'm here to help you with:

**Ordering**
- Browse our menu
- Place new orders
- Modify existing orders

**Order Tracking**
- Check order status
- View order history
- Track delivery

**Account**
- Create/update profile
- Manage delivery addresses
- View past orders

**Promotions**
- Apply promo codes
- Check available offers

**Reviews**
- Rate your orders
- Leave feedback

How can I assist you today?""",
        "suggested_tools":
        [
            "get_menu_items",
            "create_order",
            "get_customer_orders",
            "get_order_details"
        ]
    }