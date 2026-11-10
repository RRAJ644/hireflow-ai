from datetime import datetime, timezone
from typing import Any

from hireflow.db.enums import EmploymentType, WorkplaceType

from hireflow.ingestion.schemas import NormalizedJob

def clean_text(value: Any) -> str | None:
    if value is None:
        return None

    if not isinstance(value, str):
        return None

    value = value.strip()

    return value or None


def normalize_workplace_type(
    value: Any,
) -> WorkplaceType | None:

    if not isinstance(value, str):
        return None

    value = value.strip().lower()

    mapping = {
        "remote": WorkplaceType.REMOTE,
        "hybrid": WorkplaceType.HYBRID,
        "onsite": WorkplaceType.ONSITE,
        "on-site": WorkplaceType.ONSITE,
        "on site": WorkplaceType.ONSITE,
        "office": WorkplaceType.ONSITE,
    }

    return mapping.get(value)


def normalize_employment_type(
    value: Any,
) -> EmploymentType | None:

    if not isinstance(value, str):
        return None

    value = value.strip().lower()

    mapping = {
        "fulltime": EmploymentType.FULL_TIME,
        "full-time": EmploymentType.FULL_TIME,
        "full time": EmploymentType.FULL_TIME,
        "parttime": EmploymentType.PART_TIME,
        "part-time": EmploymentType.PART_TIME,
        "part time": EmploymentType.PART_TIME,
        "intern": EmploymentType.INTERNSHIP,
        "internship": EmploymentType.INTERNSHIP,
        "contract": EmploymentType.CONTRACT,
        "contractor": EmploymentType.CONTRACT,
        "temporary": EmploymentType.TEMPORARY,
    }

    return mapping.get(value)


def parse_datetime(value: Any) -> datetime | None:

    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, (int, float)):
        # Lever timestamps are in milliseconds.
        return datetime.fromtimestamp(
            value / 1000,
            tz=timezone.utc,
        )

    if isinstance(value, str):
        value = value.strip()

        if not value:
            return None

        try:
            parsed = datetime.fromisoformat(
                value.replace("Z", "+00:00")
            )

            return parsed

        except ValueError:
            return None

    return None



def normalize_greenhouse_job(
    raw_job: dict[str, Any],
) -> NormalizedJob:

    location_data = raw_job.get("location")

    location = None
    if isinstance(location_data, dict):
        location = clean_text(location_data.get("name"))

    return NormalizedJob(
        external_id=str(raw_job["id"]),
        title=clean_text(raw_job.get("title")),
        description=clean_text(raw_job.get("content")),
        location=location,
        published_at=parse_datetime(
            raw_job.get("first_published")
        ),
        job_url=clean_text(raw_job.get("absolute_url")),
    )



def normalize_lever_job(
    raw_job: dict[str, Any],
) -> NormalizedJob:

    categories = raw_job.get("categories")

    if not isinstance(categories, dict):
        categories = {}

    return NormalizedJob(
        external_id=str(raw_job["id"]),
        title=clean_text(raw_job.get("text")),
        description=clean_text(
            raw_job.get("descriptionPlain")
        ),
        location=clean_text(
            categories.get("location")
        ),
        workplace_type=normalize_workplace_type(
            raw_job.get("workplaceType")
        ),
        employment_type=normalize_employment_type(
            categories.get("commitment")
        ),
        published_at=parse_datetime(
            raw_job.get("createdAt")
        ),
        job_url=clean_text(raw_job.get("hostedUrl")),
        apply_url=clean_text(raw_job.get("applyUrl")),
    )



def normalize_ashby_job(
    raw_job: dict[str, Any],
) -> NormalizedJob | None:

    # Exclude unlisted jobs from public job discovery.
    if raw_job.get("isListed") is False:
        return None

    # The public response may not contain a separate ID.
    # Use jobUrl as a stable fallback identifier.
    external_id = raw_job.get("id") or raw_job.get("jobUrl")

    if not external_id:
        raise ValueError(
            "Ashby job has neither an ID nor a job URL"
        )

    return NormalizedJob(
        external_id=str(external_id),
        title=clean_text(raw_job.get("title")),
        description=clean_text(
            raw_job.get("descriptionPlain")
        ),
        location=clean_text(raw_job.get("location")),
        workplace_type=normalize_workplace_type(
            raw_job.get("workplaceType")
        ),
        employment_type=normalize_employment_type(
            raw_job.get("employmentType")
        ),
        published_at=parse_datetime(
            raw_job.get("publishedAt")
        ),
        job_url=clean_text(raw_job.get("jobUrl")),
        apply_url=clean_text(raw_job.get("applyUrl")),
    )


