
from datetime import datetime
from decimal import Decimal
from uuid import UUID
from sqlalchemy import Enum as SQLAlchemyEnum
from hireflow.db.enums import EmploymentType, WorkplaceType

from sqlalchemy import (
    JSON,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hireflow.db.base import Base
from hireflow.db.mixins import IDMixin, TimestampMixin


class Job(Base, IDMixin, TimestampMixin):
    __tablename__ = "jobs"

    __table_args__ = (
        UniqueConstraint(
            "job_board_id",
            "external_id",
            name="uq_job_board_external_id",
        ),
    )

    # Relationships and ownership
    company_id: Mapped[UUID] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    job_board_id: Mapped[UUID] = mapped_column(
        ForeignKey("job_boards.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ATS identification
    external_id: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    # Job information
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    location: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    workplace_type: Mapped[WorkplaceType | None] = mapped_column(
        SQLAlchemyEnum(
            WorkplaceType,
            name="workplace_type_enum",
            values_callable=lambda enum: [item.value for item in enum],
        ),
        nullable=True,
    )

    employment_type: Mapped[EmploymentType | None] = mapped_column(
        SQLAlchemyEnum(
            EmploymentType,
            name="employment_type_enum",
            values_callable=lambda enum: [item.value for item in enum],
            ),
        nullable=True,
    )

    experience_min: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    experience_max: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    skills: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
    )

    # Compensation
    salary_min: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    salary_max: Mapped[Decimal | None] = mapped_column(
        Numeric(12, 2),
        nullable=True,
    )

    salary_currency: Mapped[str | None] = mapped_column(
        String(10),
        nullable=True,
    )

    # Tracking
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    first_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    last_seen_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False,
    )

    job_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    apply_url: Mapped[str | None] = mapped_column(
        String(1000),
        nullable=True,
    )

    # ORM relationships
    company: Mapped["Company"] = relationship(
        back_populates="jobs",
    )

    job_board: Mapped["JobBoard"] = relationship(
        back_populates="jobs",
    )
