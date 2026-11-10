from fastapi import APIRouter, Request, status

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/run", status_code=status.HTTP_202_ACCEPTED)
async def trigger_ingestion(request: Request):
    job = await request.app.state.redis.enqueue_job("run_ingestion")

    if job is None:
        return {
            "message": "An ingestion job is already queued.",
        }

    return {
        "message": "Ingestion job queued successfully.",
        "job_id": job.job_id,
    }
