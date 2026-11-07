from sqlalchemy import Boolean, String 
from sqlalchemy.orm import Mapped, mapped_column, relationship

from hireflow.db.base import Base
from hireflow.db.mixins import IDMixin, TimestampMixin
from hireflow.db.models.job_board import JobBoard

class Company(Base, IDMixin, TimestampMixin):
    __tablename__ = "companies"

    name: Mapped[str]= mapped_column(
        String(length=255),
        nullable=False,
        index=True
    )

    website_url: Mapped[str | None] = mapped_column(
        String(length=255),
        nullable=True   
    )

    careers_url: Mapped[str | None] = mapped_column(
        String(length=255),
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean, 
        default=True,
        nullable=False
    )

    job_boards: Mapped[list["JobBoard"]] = relationship(
        "JobBoard",
        back_populates="company",
        cascade="all, delete-orphan",
    )
    
    jobs: Mapped[list["Job"]] = relationship(back_populates="company")

    