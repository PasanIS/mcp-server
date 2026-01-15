
"""Customer-related MCP tools"""

from typing import Optional, Dict, Any
from ..client import client


async def register_customer(
        email: str,
        first_name: str,
        last_name: str,
        password: str,
        phone: Optional[str] = None,
        address: Optional[str] = None
) -> Dict[str, Any]:

    """
    Register a new customer account.

    Args:
        email: Customer email address
        first_name: Customer first name
        last_name: Customer last name
        password: Account password (min 6 characters)
        phone: Phone number (optional)
        address: Delivery address (optional)

    Returns:
        Created customer profile
    """

    payload = {
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "password": password,
        "phone": phone,
        "address": address
    }

    response = await client.post("/customers/", json=payload)
    return response.json()


async def get_customer_profile(customer_id: int) -> Dict[str, Any]:

    """
    Get customer profile information.

    Args:
        customer_id: The customer ID

    Returns:
        Customer profile details
    """

    response = await client.get(f"/customers/{customer_id}")
    return response.json()


async def update_customer_profile(
        customer_id: int,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        phone: Optional[str] = None,
        address: Optional[str] = None,
        password: Optional[str] = None
) -> Dict[str, Any]:

    """
    Update customer profile information.

    Args:
        customer_id: The customer ID
        first_name: New first name (optional)
        last_name: New last name (optional)
        phone: New phone number (optional)
        address: New address (optional)
        password: New password (optional, min 6 characters)

    Returns:
        Updated customer profile
    """

    payload = {k: v for k, v in {
        "first_name": first_name,
        "last_name": last_name,
        "phone": phone,
        "address": address,
        "password": password
    }.items() if v is not None}

    response = await client.put(f"/customers/{customer_id}", json=payload)
    return response.json()


async def customer_login(email: str, password: str) -> Dict[str, Any]:

    """
    Authenticate a customer and get their profile.

    Args:
        email: Customer email address
        password: Account password

    Returns:
        Authentication response with customer profile
    """

    payload = {
        "email": email,
        "password": password
    }

    response = await client.post("/auth/login", json=payload)
    return response.json()