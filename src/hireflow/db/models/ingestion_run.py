
from datetime import datetime
from uuid import UUID

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hireflow.db.base import Base
from hireflow.db.mixins import IDMixin, TimestampMixin, TimestampMixin


class IngestionRun(IDMixin, TimestampMixin, Base):
    __tablename__ = "ingestion_runs"

    job_board_id: Mapped[UUID] = mapped_column(
        ForeignKey("job_boards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="running",
        nullable=False,
        index=True,
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    finished_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    jobs_fetched: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    jobs_created: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    jobs_updated: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    jobs_deactivated: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    error_message: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    job_board: Mapped["JobBoard"] = relationship(
        back_populates="ingestion_runs",
    )

