from pydantic import BaseModel, Field


class CreateTaskRequest(BaseModel):
    content: str = Field(..., min_length=1)
    due_at: str
    priority: str = "medium"
    note: str = ""


class UpdateTaskRequest(BaseModel):
    content: str = Field(..., min_length=1)
    due_at: str
    priority: str = "medium"
    note: str = ""


class CompleteTaskResponse(BaseModel):
    job: dict
