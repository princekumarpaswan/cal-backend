"""Controller for task endpoints."""
from typing import List, Dict
from app.service.task_service import TaskService
from app.repository.task_repository import TaskRepository
from app.schemas.task import (
    TaskCreate,
    TaskUpdate,
    TaskStatusUpdate,
    TaskCreateResponse,
    TaskUpdateResponse,
    TaskListResponse,
    TaskResponse,
)
from app.models.models import User, Task


class TaskController:
    """Controller for task operations."""
    
    def __init__(self, service: TaskService):
        self.service = service
    
    def _format_task(self, task: Task) -> Dict:
        """Format task for response."""
        return {
            "id": str(task.id),
            "title": task.title,
            "description": task.description,
            "dueDate": task.due_date,
            "priority": task.priority,
            "status": task.status,
            "assignedTo": str(task.assigned_to) if task.assigned_to else None,
            "linkedEventId": str(task.linked_event_id) if task.linked_event_id else None,
            "createdBy": str(task.created_by),
            "createdAt": task.created_at,
            "completedAt": task.completed_at,
        }
    
    async def create_task(self, current_user: User, task_data: TaskCreate) -> TaskCreateResponse:
        """Handle create task request."""
        task = await self.service.create_task(current_user, task_data)
        
        return TaskCreateResponse(
            success=True,
            data={
                "task": TaskResponse(
                    id=str(task.id),
                    title=task.title,
                    description=task.description,
                    dueDate=task.due_date,
                    priority=task.priority,
                    status=task.status,
                    assignedTo=str(task.assigned_to) if task.assigned_to else None,
                    createdBy=str(task.created_by),
                    createdAt=task.created_at,
                )
            }
        )
    
    async def get_tasks(
        self,
        current_user: User,
        family_group_id: str = None,
        status: str = None
    ) -> TaskListResponse:
        """Handle get tasks request."""
        tasks = await self.service.get_tasks(current_user, family_group_id, status)
        
        tasks_list = [self._format_task(task) for task in tasks]
        
        return TaskListResponse(
            success=True,
            data={
                "tasks": tasks_list,
                "pagination": {
                    "total": len(tasks_list),
                    "page": 1,
                    "pageSize": len(tasks_list)
                }
            }
        )
    
    async def get_task(self, task_id: str, current_user: User) -> Dict:
        """Handle get task request."""
        task = await self.service.get_task(task_id, current_user)
        
        return {
            "success": True,
            "data": {
                "task": self._format_task(task)
            }
        }
    
    async def update_task(self, task_id: str, current_user: User, task_data: TaskUpdate) -> TaskUpdateResponse:
        """Handle update task request."""
        task = await self.service.update_task(task_id, current_user, task_data)
        
        return TaskUpdateResponse(
            success=True,
            data={
                "task": TaskResponse(
                    id=str(task.id),
                    title=task.title,
                    description=task.description,
                    dueDate=task.due_date,
                    priority=task.priority,
                    status=task.status,
                    assignedTo=str(task.assigned_to) if task.assigned_to else None,
                    createdBy=str(task.created_by),
                    createdAt=task.created_at,
                )
            }
        )
    
    async def update_task_status(self, task_id: str, current_user: User, status_data: TaskStatusUpdate) -> TaskUpdateResponse:
        """Handle update task status request."""
        task = await self.service.update_task_status(task_id, current_user, status_data)
        
        return TaskUpdateResponse(
            success=True,
            data={
                "task": TaskResponse(
                    id=str(task.id),
                    title=task.title,
                    description=task.description,
                    dueDate=task.due_date,
                    priority=task.priority,
                    status=task.status,
                    assignedTo=str(task.assigned_to) if task.assigned_to else None,
                    createdBy=str(task.created_by),
                    createdAt=task.created_at,
                )
            }
        )
    
    async def delete_task(self, task_id: str, current_user: User) -> Dict:
        """Handle delete task request."""
        await self.service.delete_task(task_id, current_user)
        
        return {
            "success": True,
            "message": "Task deleted successfully"
        }

