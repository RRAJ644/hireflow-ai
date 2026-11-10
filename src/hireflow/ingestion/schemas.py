from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from hireflow.db.enums import EmploymentType, WorkplaceType

class NormalizedJob(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    external_id: str = Field(min_length=1)

    title: str = Field(min_length=1)
    description: str | None = None
    location: str | None = None 

    workplace_type: WorkplaceType | None = None 
    employment_type: EmploymentType | None = None 

    experience_min: int | None = None
    experience_max: int | None = None

    skills: list[str] | None = None

    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    salary_currency: str | None = None

    published_at: datetime | None = None

    job_url: str | None = None
    apply_url: str | None = None





