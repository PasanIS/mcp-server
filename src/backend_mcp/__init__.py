"""
Restaurant Backend MCP Server
"""

__version__ = "1.0.0"
__author__ = "Pasan Induwara"
__email__ = "pasan.samz@gmail.com"

from .server import mcp, main
from .config import settings
from .client import client

__all__ = [
    "mcp",
    "main",
    "settings",
    "client",
]