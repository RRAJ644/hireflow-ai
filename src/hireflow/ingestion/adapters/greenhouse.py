from typing import Any 
from urllib.parse import quote

import httpx

from hireflow.core.config import settings
from hireflow.ingestion.adapters.base import BaseATSAdapter

class GreenhouseAdapter(BaseATSAdapter):

    def __init__(self, client: httpx.AsyncClient):
        self.client = client 

    async def fetch_jobs(self, board_token: str) -> list[dict[str, Any]]:
        if not board_token or not board_token.strip():
            raise ValueError("Greenhouse board token cannot be empty")

        encoded_token = quote(board_token.strip(), safe="")

        url = (
            f"{settings.GREENHOUSE_API_BASE_URL.rstrip('/')}"
            f"/{encoded_token}/jobs"
        )

        response = await self.client.get(
            url, params={"content": "true"}

        )

        response.raise_for_status()

        payload = response.json()
        if not isinstance(payload, dict):
            raise ValueError("Invalid Greenhouse API response")


        jobs =payload.get('jobs')
        if not isinstance(jobs, list):
            raise ValueError("Greenhouse response does not contain a valid jobs list")

        if not all(isinstance(job, dict) for job in jobs):
            raise ValueError(
                "Greenhouse response contains an invalid job record"
            )

        return jobs 

        