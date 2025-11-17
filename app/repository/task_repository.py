"""Repository for task-related database operations."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from datetime import datetime
from typing import List, Optional
from app.models.models import Task, FamilyGroup


class TaskRepository:
    """Repository for task operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_task(
        self,
        title: str,
        description: Optional[str],
        due_date: Optional[datetime],
        priority: str,
        status: str,
        assigned_to: Optional[str],
        linked_event_id: Optional[str],
        family_group_id: Optional[str],
        created_by: str
    ) -> Task:
        """Create a new task."""
        new_task = Task(
            title=title,
            description=description,
            due_date=due_date,
            priority=priority,
            status=status,
            assigned_to=assigned_to,
            linked_event_id=linked_event_id,
            family_group_id=family_group_id,
            created_by=created_by,
        )
        self.db.add(new_task)
        await self.db.commit()
        await self.db.refresh(new_task)
        return new_task
    
    async def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """Get task by ID."""
        result = await self.db.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()
    
    async def get_tasks(
        self,
        user_id: str,
        family_group_id: Optional[str] = None,
        status: Optional[str] = None
    ) -> List[Task]:
        """Get tasks for a user."""
        query = select(Task).where(
            or_(
                Task.created_by == user_id,
                Task.assigned_to == user_id
            )
        )
        
        if family_group_id:
            query = query.where(Task.family_group_id == family_group_id)
        
        if status:
            query = query.where(Task.status == status)
        
        result = await self.db.execute(query)
        return list(result.scalars().all())
    
    async def update_task(self, task: Task) -> Task:
        """Update task."""
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def delete_task(self, task: Task) -> bool:
        """Delete task."""
        await self.db.delete(task)
        await self.db.commit()
        return True
    
    async def get_family_group_by_id(self, group_id: str) -> Optional[FamilyGroup]:
        """Get family group by ID."""
        result = await self.db.execute(select(FamilyGroup).where(FamilyGroup.id == group_id))
        return result.scalar_one_or_none()

