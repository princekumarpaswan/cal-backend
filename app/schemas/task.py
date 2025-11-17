from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime


class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    dueDate: Optional[datetime] = None
    priority: str = Field(default="medium", pattern="^(low|medium|high)$")
    assignedTo: Optional[str] = None
    linkedEventId: Optional[str] = None
    familyGroupId: Optional[str] = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    dueDate: Optional[datetime] = None
    priority: Optional[str] = Field(None, pattern="^(low|medium|high)$")
    assignedTo: Optional[str] = None
    linkedEventId: Optional[str] = None


class TaskStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(pending|in_progress|completed|cancelled)$")


class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    dueDate: Optional[datetime]
    priority: str
    status: str
    assignedTo: Optional[str]
    createdBy: str
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

