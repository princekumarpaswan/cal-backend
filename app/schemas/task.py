from pydantic import BaseModel, Field, constr
from typing import Optional, Dict, Any
from datetime import datetime


class TaskBase(BaseModel):
    title: constr(min_length=1, max_length=255, strip_whitespace=True) = Field(
        ...,
        description="Task title",
        examples=["Complete project documentation"]
    )
    description: Optional[constr(max_length=5000)] = Field(
        None,
        description="Task description",
        max_length=5000
    )
    dueDate: Optional[datetime] = Field(
        None,
        description="Task due date (ISO 8601 format)"
    )
    priority: constr(pattern="^(low|medium|high)$") = Field(
        default="medium",
        description="Task priority level"
    )
    assignedTo: Optional[constr(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")] = Field(
        None,
        description="Assigned user UUID"
    )
    linkedEventId: Optional[constr(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")] = Field(
        None,
        description="Linked event UUID"
    )
    familyGroupId: Optional[constr(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")] = Field(
        None,
        description="Family group UUID"
    )


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=255, strip_whitespace=True)] = Field(
        None,
        description="Task title"
    )
    description: Optional[constr(max_length=5000)] = Field(
        None,
        description="Task description"
    )
    dueDate: Optional[datetime] = Field(
        None,
        description="Task due date"
    )
    priority: Optional[constr(pattern="^(low|medium|high)$")] = Field(
        None,
        description="Task priority level"
    )
    assignedTo: Optional[constr(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")] = Field(
        None,
        description="Assigned user UUID"
    )
    linkedEventId: Optional[constr(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")] = Field(
        None,
        description="Linked event UUID"
    )


class TaskStatusUpdate(BaseModel):
    status: constr(pattern="^(pending|in_progress|completed|cancelled)$") = Field(
        ...,
        description="Task status"
    )


class TaskResponse(BaseModel):
    id: str = Field(..., description="Task UUID")
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    dueDate: Optional[datetime] = None
    priority: str = Field(..., pattern="^(low|medium|high)$")
    status: str = Field(..., pattern="^(pending|in_progress|completed|cancelled)$")
    assignedTo: Optional[str] = Field(None, description="Assigned user UUID")
    createdBy: str = Field(..., description="Creator user UUID")
    createdAt: datetime

    class Config:
        from_attributes = True


class TaskListResponse(BaseModel):
    success: bool = True
    data: Dict[str, Any]


class TaskCreateResponse(BaseModel):
    success: bool = True
    data: Dict[str, TaskResponse]


class TaskUpdateResponse(BaseModel):
    success: bool = True
    data: Dict[str, TaskResponse]

