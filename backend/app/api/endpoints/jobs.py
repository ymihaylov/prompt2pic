import logging

from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_job_repository
from app.repositories.job_repository import JobRepository

router = APIRouter(
    prefix="/jobs",
    tags=["jobs"],
    responses={404: {"description": "Not found"}},
)

logger = logging.getLogger(__name__)


@router.get("/status/{job_id}")
async def get_job_status(
    job_id: str, job_status_service: JobRepository = Depends(get_job_repository)
):
    try:
        return job_status_service.get_job_dict(job_id)
    except ValueError as e:
        logger.info("Job not found", extra={"job_id": job_id})
        raise HTTPException(status_code=404, detail=str(e))
