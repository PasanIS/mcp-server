
"""Staff-related MCP tools"""

from typing import Dict, Any
from ..client import client


async def staff_login(email: str, password: str, user_type: str = "staff") -> Dict[str, Any]:

    """Authenticate a staff member"""

    payload = {
        "email": email,
        "password": password,
        "user_type": user_type
    }
    response = await client.post("/auth/staff/login", json=payload)
    return response.json()