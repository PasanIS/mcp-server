
"""Order-related MCP tools"""

from typing import Optional, List, Dict, Any
from ..client import client


async def create_order(
        customer_id: int,
        order_type: str,
        items: List[Dict[str, Any]],
        delivery_address: Optional[str] = None,
        special_instructions: Optional[str] = None,
        promo_code: Optional[str] = None
) -> Dict[str, Any]:

    """
    Create a new order for a customer.

    Args:
        customer_id: Customer ID placing the order
        order_type: Type of order (dine_in, takeaway, delivery)
        items: List of order items, each with menu_item_id, quantity, and optional special_instructions
        delivery_address: Delivery address (required for delivery orders)
        special_instructions: Special instructions for the entire order
        promo_code: Promo code to apply

    Returns:
        Created order details with total amount and status
    """

    payload = {
        "customer_id": customer_id,
        "order_type": order_type,
        "items": items,
        "delivery_address": delivery_address,
        "special_instructions": special_instructions,
        "promo_code": promo_code
    }

    response = await client.post("/orders/", json=payload)
    return response.json()


async def get_order_details(order_id: int) -> Dict[str, Any]:

    """
    Get detailed information about a specific order.

    Args:
        order_id: The ID of the order

    Returns:
        Complete order details
    """

    response = await client.get(f"/orders/{order_id}")
    return response.json()


async def get_customer_orders(customer_id: int) -> List[Dict[str, Any]]:

    """
    Get all orders for a specific customer.

    Args:
        customer_id: The customer ID

    Returns:
        List of all orders placed by the customer
    """

    response = await client.get(f"/orders/customer/{customer_id}")
    return response.json()


async def get_orders_by_status(status: str) -> List[Dict[str, Any]]:

    """
    Get all orders with a specific status.

    Args:
        status: Order status (pending, confirmed, preparing, ready, out_for_delivery, delivered, cancelled)

    Returns:
        List of orders with the specified status
    """

    response = await client.get(f"/orders/status/{status}")
    return response.json()


async def update_order_status(
        order_id: int,
        status: str,
        staff_id: Optional[int] = None,
        notes: Optional[str] = None
) -> Dict[str, Any]:

    """
    Update the status of an order (creates a journey step).

    Args:
        order_id: The ID of the order
        status: New status (pending, confirmed, preparing, ready, out_for_delivery, delivered, cancelled)
        staff_id: ID of staff member updating the status
        notes: Additional notes for the status update

    Returns:
        Updated order journey step
    """

    payload = {
        "order_id": order_id,
        "status": status,
        "staff_id": staff_id,
        "notes": notes
    }

    response = await client.post(f"/orders/{order_id}/journey", json=payload)
    return response.json()


async def get_order_journey(order_id: int) -> List[Dict[str, Any]]:

    """
    Get the complete journey/history of an order's status changes.

    Args:
        order_id: The ID of the order

    Returns:
        List of all status changes with timestamps and staff information
    """

    response = await client.get(f"/orders/{order_id}/journey")
    return response.json()


async def get_filtered_orders(
        status: Optional[str] = None,
        order_type: Optional[str] = None,
        customer_id: Optional[int] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        skip: int = 0,
        limit: int = 100
) -> List[Dict[str, Any]]:

    """
    Get orders with advanced filtering options.

    Args:
        status: Filter by order status
        order_type: Filter by order type (dine_in, takeaway, delivery)
        customer_id: Filter by customer ID
        start_date: Filter orders after this date (YYYY-MM-DD)
        end_date: Filter orders before this date (YYYY-MM-DD)
        min_amount: Filter orders with amount >= this value
        max_amount: Filter orders with amount <= this value
        skip: Number of records to skip (pagination)
        limit: Maximum number of records to return

    Returns:
        List of filtered orders
    """

    params = {}

    if status is not None:
        params["status"] = status
    if order_type is not None:
        params["order_type"] = order_type
    if customer_id is not None:
        params["customer_id"] = customer_id
    if start_date is not None:
        params["start_date"] = start_date
    if end_date is not None:
        params["end_date"] = end_date
    if min_amount is not None:
        params["min_amount"] = min_amount
    if max_amount is not None:
        params["max_amount"] = max_amount

    params["skip"] = skip
    params["limit"] = limit

    try:
        response = await client.get("/orders/filter", params=params)
        return response.json()
    except Exception as e:
        print(f"Warning: Failed to filter orders with params {params}: {e}")
        if status is not None:
            params_without_status = {k: v for k, v in params.items() if k != "status"}
            try:
                response = await client.get("/orders/filter", params=params_without_status)
                results = response.json()
                if status and results:
                    results = [order for order in results if order.get('status') == status]
                return results
            except Exception as e2:
                print(f"Warning: Retry also failed: {e2}")
        return []