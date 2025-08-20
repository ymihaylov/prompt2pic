# Create router instance
from fastapi import APIRouter, Depends

from app.core.dependencies import get_job_status_service
from app.services.job_status_service import JobStatusService

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)


@router.get("/status/{job_id}")
async def get_job_status(
    job_id: str, job_status_service: JobStatusService = Depends(get_job_status_service)
):
    """Get the status of a job by ID."""
    return job_status_service.get_job_dict(
        job_id
    )  # TODO: Check if this job is existing
