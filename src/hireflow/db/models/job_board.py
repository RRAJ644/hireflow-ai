from ast import For
from uuid import UUID

from sqlalchemy import (
    Boolean,
    ForeignKey,
    String,
    UniqueConstraint
)

from sqlalchemy.orm import Mapped, mapped_column, relationship

from hireflow.db.base import Base
from hireflow.db.mixins import IDMixin, TimestampMixin

class JobBoard(Base, IDMixin, TimestampMixin):
    __tablename__ = "job_boards"

    __table_args__ = (
    UniqueConstraint(
        "provider",
        "board_token",
        name="uq_job_board_provider_token"
    ),
)

    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    provider: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
    )

    board_token: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False,
        index=True
    )

    board_url: Mapped[str] = mapped_column(
        String(length=255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    company: Mapped["Company"] = relationship(
        "Company",
        back_populates="job_boards",
        lazy="joined"
    )
    ingestion_runs: Mapped[list["IngestionRun"]] = relationship(
    back_populates="job_board",
)