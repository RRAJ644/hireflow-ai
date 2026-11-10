
from typing import Any
from urllib.parse import quote

import httpx

from hireflow.core.config import settings
from hireflow.ingestion.adapters.base import BaseATSAdapter


class AshbyAdapter(BaseATSAdapter):

    def __init__(self, client: httpx.AsyncClient):
        self.client = client

    async def fetch_jobs(
        self,
        board_token: str,
    ) -> list[dict[str, Any]]:

        if not board_token or not board_token.strip():
            raise ValueError("Ashby board token cannot be empty")

        encoded_token = quote(board_token.strip(), safe="")

        url = (
            f"{settings.ASHBY_JOB_POSTING_API_BASE_URL.rstrip('/')}"
            f"/{encoded_token}"
        )

        response = await self.client.get(
            url,
            params={"includeCompensation": "true"},
        )

        response.raise_for_status()

        payload = response.json()

        if not isinstance(payload, dict):
            raise ValueError("Invalid Ashby API response")

        jobs = payload.get("jobs")

        if not isinstance(jobs, list):
            raise ValueError("Ashby response does not contain a valid jobs list")

        if not all(isinstance(job, dict) for job in jobs):
            raise ValueError("Ashby response contains an invalid job record")

        return jobs
