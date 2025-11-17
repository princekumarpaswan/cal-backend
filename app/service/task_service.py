"""Service for task business logic."""
from datetime import datetime
from typing import List, Optional
from app.repository.task_repository import TaskRepository
from app.api.exceptions import NotFoundException, ForbiddenException
from app.models.models import User, Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate


class TaskService:
    """Service for task operations."""
    
    def __init__(self, repository: TaskRepository):
        self.repository = repository
    
    async def create_task(self, user: User, task_data: TaskCreate) -> Task:
        """Create a new task."""
        # Validate family group if provided
        if task_data.familyGroupId:
            family_group = await self.repository.get_family_group_by_id(task_data.familyGroupId)
            if not family_group:
                raise NotFoundException("Family group not found")
        
        return await self.repository.create_task(
            title=task_data.title,
            description=task_data.description,
            due_date=task_data.dueDate,
            priority=task_data.priority,
            status="pending",
            assigned_to=task_data.assignedTo,
            linked_event_id=task_data.linkedEventId,
            family_group_id=task_data.familyGroupId,
            created_by=str(user.id)
        )
    
    async def get_tasks(
        self,
        user: User,
        family_group_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Task]:
        """Get tasks for a user."""
        return await self.repository.get_tasks(str(user.id), family_group_id, status)
    
    async def get_task(self, task_id: str, user: User) -> Task:
        """Get a specific task."""
        task = await self.repository.get_task_by_id(task_id)
        
        if not task:
            raise NotFoundException("Task not found")
        
        # Check if user has access
        is_creator = task.created_by == user.id
        is_assignee = task.assigned_to == user.id
        
        if not is_creator and not is_assignee:
            raise ForbiddenException("You don't have access to this task")
        
        return task
    
    async def update_task(self, task_id: str, user: User, task_data: TaskUpdate) -> Task:
        """Update a task."""
        task = await self.repository.get_task_by_id(task_id)
        
        if not task:
            raise NotFoundException("Task not found")
        
        # Only creator can update task details
        if task.created_by != user.id:
            raise ForbiddenException("Only the task creator can update the task")
        
        # Update fields
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description
        if task_data.dueDate is not None:
            task.due_date = task_data.dueDate
        if task_data.priority is not None:
            task.priority = task_data.priority
        if task_data.assignedTo is not None:
            task.assigned_to = task_data.assignedTo
        if task_data.linkedEventId is not None:
            task.linked_event_id = task_data.linkedEventId
        
        return await self.repository.update_task(task)
    
    async def update_task_status(self, task_id: str, user: User, status_data: TaskStatusUpdate) -> Task:
        """Update task status."""
        task = await self.repository.get_task_by_id(task_id)
        
        if not task:
            raise NotFoundException("Task not found")
        
        # Creator or assignee can update status
        is_creator = task.created_by == user.id
        is_assignee = task.assigned_to == user.id
        
        if not is_creator and not is_assignee:
            raise ForbiddenException("You don't have permission to update this task")
        
        # Update status
        task.status = status_data.status
        
        # Set completed_at if status is completed
        if status_data.status == "completed":
            task.completed_at = datetime.utcnow()
        elif task.completed_at:
            task.completed_at = None
        
        return await self.repository.update_task(task)
    
    async def delete_task(self, task_id: str, user: User) -> bool:
        """Delete a task."""
        task = await self.repository.get_task_by_id(task_id)
        
        if not task:
            raise NotFoundException("Task not found")
        
        # Only creator can delete
        if task.created_by != user.id:
            raise ForbiddenException("Only the task creator can delete the task")
        
        return await self.repository.delete_task(task)

