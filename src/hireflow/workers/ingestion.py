from typing import Any

import httpx

from hireflow.db.session import AsyncSessionLocal
from hireflow.ingestion.service import IngestionService

async def run_ingestion(ctx: dict[str, Any]) -> dict:

    async with AsyncSessionLocal() as session:
        client: httpx.AsyncClient = ctx["http_client"]

        ingestion_service = IngestionService(
            session = session,
            client = client
        )

        result = await ingestion_service.ingest_all_boards()
        return result
