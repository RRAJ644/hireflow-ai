
from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from hireflow.db.models import Job
from hireflow.ingestion.schemas import NormalizedJob

from sqlalchemy.engine import CursorResult

class JobUpsertService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def upsert_job(self, job_board_id: UUID, company_id: UUID, normalized_job: NormalizedJob) -> None:

        now = datetime.now(timezone.utc)

        values = normalized_job.model_dump()

        values.update({
            "job_board_id": job_board_id,
            "company_id": company_id,
            "is_active": True,
            "last_seen_at": now,
        })

        statement = insert(Job).values(**values)

        statement = statement.on_conflict_do_update(
            index_elements=[
                Job.job_board_id,
                Job.external_id,
            ],
            set_={
                **values,
                "first_seen_at": Job.first_seen_at,
            },
        )

        await self.session.execute(statement)

  
  
    async def bulk_upsert_jobs(
        self,
        job_board_id: UUID,
        company_id: UUID,
        normalized_jobs: list[NormalizedJob],
    ) -> int:

        if not normalized_jobs:
            return 0

        now = datetime.now(timezone.utc)

        job_values = []

        for normalized_job in normalized_jobs:

            values = normalized_job.model_dump()

            values.update({
                "job_board_id": job_board_id,
                "company_id": company_id,
                "is_active": True,
                "last_seen_at": now,
            })

            job_values.append(values)

        statement = insert(Job).values(job_values)

        statement = statement.on_conflict_do_update(
            index_elements=[
                Job.job_board_id,
                Job.external_id,
            ],
            set_={
                **{
                    column: getattr(statement.excluded, column)
                    for column in job_values[0]
                    if column not in {
                        "id",
                        "first_seen_at",
                        "created_at",
                    }
                },
                "first_seen_at": Job.first_seen_at,
                "created_at": Job.created_at,
            },
        )

        result = await self.session.execute(statement)

        return result