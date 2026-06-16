from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, HTTPException

from .scheduler import (
    cancel_job,
    complete_job,
    create_job,
    delete_job,
    find_due_jobs,
    get_job,
    list_jobs,
    process_due_jobs,
    update_job,
)
from .schemas import CompleteTaskResponse, CreateTaskRequest, UpdateTaskRequest


router = APIRouter()


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.get("/api/tasks")
def api_list_tasks(status: Optional[str] = None) -> dict:
    return {"jobs": list_jobs(status=status)}


@router.post("/api/tasks")
def api_create_task(request: CreateTaskRequest) -> dict:
    try:
        job = create_job(
            content=request.content,
            due_at=request.due_at,
            priority=request.priority,
            note=request.note,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    return {"job": job}


@router.get("/api/tasks/due")
def api_due_tasks() -> dict:
    return {"jobs": find_due_jobs()}


@router.post("/api/tasks/process-due")
def api_process_due_tasks() -> dict:
    return process_due_jobs()


@router.get("/api/tasks/{job_id}")
def api_get_task(job_id: int) -> dict:
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return {"job": job}


@router.patch("/api/tasks/{job_id}")
def api_update_task(job_id: int, request: UpdateTaskRequest) -> dict:
    try:
        job = update_job(
            job_id=job_id,
            content=request.content,
            due_at=request.due_at,
            priority=request.priority,
            note=request.note,
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return {"job": job}


@router.delete("/api/tasks/{job_id}")
def api_delete_task(job_id: int) -> dict:
    deleted = delete_job(job_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="job not found")
    return {"status": "deleted", "id": job_id}


@router.post("/api/tasks/{job_id}/complete", response_model=CompleteTaskResponse)
def api_complete_task(job_id: int) -> CompleteTaskResponse:
    job = complete_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return CompleteTaskResponse(job=job)


@router.post("/api/tasks/{job_id}/cancel")
def api_cancel_task(job_id: int) -> dict:
    try:
        job = cancel_job(job_id)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return {"job": job}


@router.get("/api/summary")
def api_summary() -> dict:
    jobs = list_jobs()
    now = datetime.now(timezone.utc)
    pending = [job for job in jobs if job["status"] == "pending"]
    completed = [job for job in jobs if job["status"] == "completed"]
    due = find_due_jobs(now)
    upcoming = [
        job
        for job in pending
        if datetime.fromisoformat(job["due_at"]) > now
    ]
    return {
        "total": len(jobs),
        "pending": len(pending),
        "completed": len(completed),
        "due": len(due),
        "upcoming": len(upcoming),
    }
