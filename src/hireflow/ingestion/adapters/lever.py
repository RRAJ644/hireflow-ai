
from typing import Any
from urllib.parse import quote

import httpx

from hireflow.core.config import settings
from hireflow.ingestion.adapters.base import BaseATSAdapter


class LeverAdapter(BaseATSAdapter):

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def fetch_jobs(
        self,
        board_token: str,
    ) -> list[dict[str, Any]]:

        if not board_token or not board_token.strip():
            raise ValueError("Lever board token cannot be empty")

        encoded_token = quote(board_token.strip(), safe="")

        url = (
            f"{settings.LEVER_POSTINGS_API_BASE_URL.rstrip('/')}"
            f"/{encoded_token}"
        )

        response = await self.client.get(
            url,
            params={"mode": "json"},
        )

        response.raise_for_status()

        payload = response.json()

        if not isinstance(payload, list):
            raise ValueError("Invalid Lever API response")

        if not all(isinstance(job, dict) for job in payload):
            raise ValueError("Lever response contains an invalid job record")

        return payload
