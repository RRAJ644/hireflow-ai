
from datetime import datetime, timezone

import httpx
from sqlalchemy.ext.asyncio import AsyncSession

from hireflow.db.models import IngestionRun, JobBoard
from hireflow.ingestion.adapters.factory import get_adapter
from hireflow.ingestion.normalizer import (
    normalize_greenhouse_job,
    normalize_lever_job,
    normalize_ashby_job,
)
from hireflow.ingestion.upsert import JobUpsertService
from hireflow.ingestion.registry import JobBoardRegistry


NORMALIZERS = {
    "greenhouse": normalize_greenhouse_job,
    "lever": normalize_lever_job,
    "ashby": normalize_ashby_job,
}




class IngestionService:

    def __init__(self, session: AsyncSession, client: httpx.AsyncClient):
        self.session = session
        self.client = client

    async def ingest_board(self, board: JobBoard) -> int:

        ingestion_run = IngestionRun(
            job_board_id=board.id,
            status="running",
            started_at=datetime.now(timezone.utc),
        )

        self.session.add(ingestion_run)

        # Persist the running record before network requests.
        await self.session.commit()

        try:
            adapter = get_adapter(board.provider, self.client)

            raw_jobs = await adapter.fetch_jobs(board.board_token)

            normalizer = NORMALIZERS[board.provider]

            normalized_jobs = []

            for raw_job in raw_jobs:
                normalized_job = normalizer(raw_job)

                if normalized_job is not None:
                    normalized_jobs.append(normalized_job)

            upsert_service = JobUpsertService(self.session)

            await upsert_service.bulk_upsert_jobs(
                job_board_id=board.id,
                company_id=board.company_id,
                normalized_jobs=normalized_jobs,
            )

            ingestion_run.jobs_fetched = len(raw_jobs)
            ingestion_run.status = "success"
            ingestion_run.finished_at = datetime.now(timezone.utc)

            await self.session.commit()

            return len(normalized_jobs)

        except Exception as exc:

            await self.session.rollback()

            ingestion_run.status = "failed"
            ingestion_run.finished_at = datetime.now(timezone.utc)
            ingestion_run.error_message = str(exc)

            await self.session.commit()

            raise


    async def ingest_all_boards(self) -> dict:
        registry = JobBoardRegistry(self.session)

        boards = await registry.get_active_boards()

        results = {
            "total_boards": len(boards),
            "successful": 0,
            "failed": 0,
            "jobs_processed": 0,
            "errors": [],
        }

        for board in boards:
            try:
                processed = await self.ingest_board(board)

                results["successful"] += 1
                results["jobs_processed"] += processed

            except Exception as exc:
                results["failed"] += 1

                results["errors"].append({
                    "board_id": str(board.id),
                    "error": str(exc),
                })

        return results