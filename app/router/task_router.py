"""Router for task endpoints."""
from fastapi import APIRouter, Depends, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.models import User
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskCreateResponse,
    TaskUpdateResponse,
    TaskListResponse,
)
from app.schemas.query_params import TaskQueryParams
from app.repository.task_repository import TaskRepository
from app.service.task_service import TaskService
from app.controller.task_controller import TaskController

router = APIRouter()


def get_task_controller(db: AsyncSession = Depends(get_db)) -> TaskController:
    """Dependency to get task controller."""
    repository = TaskRepository(db)
    service = TaskService(repository)
    return TaskController(service)


@router.post("", response_model=TaskCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    """Create a new task."""
    return await controller.create_task(current_user, task_data)


@router.get("", response_model=TaskListResponse)
async def get_tasks(
    familyGroupId: Optional[str] = Query(
        None,
        pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="Filter by family group UUID"
    ),
    status: Optional[str] = Query(
        None,
        pattern="^(pending|in_progress|completed|cancelled)$",
        description="Filter by task status"
    ),
    current_user: User = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    """Get tasks for the current user.
    
    - **familyGroupId**: Optional family group UUID to filter tasks
    - **status**: Optional task status filter (pending, in_progress, completed, cancelled)
    """
    return await controller.get_tasks(current_user, familyGroupId, status)


@router.get("/{task_id}")
async def get_task(
    task_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Task UUID"),
    current_user: User = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    """Get a specific task by ID.
    
    - **task_id**: Task UUID
    """
    return await controller.get_task(task_id, current_user)


@router.put("/{task_id}")
async def update_task(
    task_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Task UUID"),
    task_data: TaskUpdate = ...,
    current_user: User = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    """Update a task.
    
    - **task_id**: Task UUID
    """
    return await controller.update_task(task_id, current_user, task_data)


@router.patch("/{task_id}/status")
async def update_task_status(
    task_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Task UUID"),
    status_data: TaskStatusUpdate = ...,
    current_user: User = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    """Update task status.
    
    - **task_id**: Task UUID
    """
    return await controller.update_task_status(task_id, current_user, status_data)


@router.delete("/{task_id}")
async def delete_task(
    task_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Task UUID"),
    current_user: User = Depends(get_current_user),
    controller: TaskController = Depends(get_task_controller)
):
    """Delete a task.
    
    - **task_id**: Task UUID
    """
    return await controller.delete_task(task_id, current_user)

