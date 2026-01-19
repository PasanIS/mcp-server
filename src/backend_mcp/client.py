
"""Client for Restaurant Backend API"""

import httpx
from typing import Optional, Dict
from .config import settings


class BackendClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        timeout: Optional[int] = None,
        api_key: Optional[str] = None,
    ):
        self.base_url = base_url or settings.backend_url
        self.timeout = timeout or settings.backend_timeout
        self.api_key = api_key or settings.api_key

        self.headers = {"Content-Type": "application/json"}
        if self.api_key:
            self.headers["Authorization"] = f"Bearer {self.api_key}"

    async def _request(self, method: str, path: str, **kwargs) -> httpx.Response:
        async with httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers=self.headers,
        ) as client:
            response = await client.request(method, path, **kwargs)
            response.raise_for_status()
            return response

    async def get(self, path: str, params: Optional[Dict] = None) -> httpx.Response:
        return await self._request("GET", path, params=params)

    async def post(self, path: str, json: Optional[Dict] = None) -> httpx.Response:
        return await self._request("POST", path, json=json)

    async def put(self, path: str, json: Optional[Dict] = None) -> httpx.Response:
        return await self._request("PUT", path, json=json)

    async def delete(self, path: str) -> httpx.Response:
        return await self._request("DELETE", path)


# Safe global wrapper
client = BackendClient()
