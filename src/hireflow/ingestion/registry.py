from arq.jobs import Job
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from hireflow.db.enums import ATSProvider
from hireflow.db.models import JobBoard

class JobBoardRegistry:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_active_boards(self,  provider: ATSProvider | None) -> list[JobBoard]:
        statement = (
            select(JobBoard).where(JobBoard.is_active.is_(True))
        )

        if provider is not None:
            statement = statement.where(JobBoard.provider == provider)

        statement = statement.order_by(JobBoard.created_at)
        result = await self.session.scalars(statement)
        return list(result.all())
        


