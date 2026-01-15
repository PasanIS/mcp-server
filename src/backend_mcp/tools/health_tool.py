
"""Health check MCP tools"""

from typing import Dict, Any
from ..client import client


async def check_backend_health() -> Dict[str, Any]:

    """Check if the backend API is healthy and responding"""

    response = await client.get("/health")
    return {"status": "healthy", "response": response.json()}