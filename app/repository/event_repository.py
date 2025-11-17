"""Repository for event-related database operations."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from sqlalchemy.orm import selectinload
from datetime import datetime
from typing import List, Optional
from app.models.models import Event, FamilyGroup, User, event_attendees


class EventRepository:
    """Repository for event operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_event(
        self,
        title: str,
        description: Optional[str],
        start_time: datetime,
        end_time: datetime,
        location: Optional[str],
        color: str,
        recurrence: Optional[dict],
        reminders: Optional[List[dict]],
        family_group_id: Optional[str],
        created_by: str,
        attendee_ids: Optional[List[str]] = None
    ) -> Event:
        """Create a new event."""
        new_event = Event(
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
            location=location,
            color=color,
            recurrence=recurrence,
            reminders=reminders,
            family_group_id=family_group_id,
            created_by=created_by,
        )
        self.db.add(new_event)
        await self.db.flush()
        
        # Add attendees
        if attendee_ids:
            for attendee_id in attendee_ids:
                stmt = event_attendees.insert().values(
                    event_id=new_event.id,
                    user_id=attendee_id,
                    status="pending"
                )
                await self.db.execute(stmt)
        
        await self.db.commit()
        await self.db.refresh(new_event)
        return new_event
    
    async def get_event_by_id(self, event_id: str, load_attendees: bool = False) -> Optional[Event]:
        """Get event by ID."""
        query = select(Event).where(Event.id == event_id)
        if load_attendees:
            query = query.options(selectinload(Event.attendees))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_events(
        self,
        start_date: datetime,
        end_date: datetime,
        user_id: str,
        family_group_id: Optional[str] = None
    ) -> List[Event]:
        """Get events within a date range."""
        query = select(Event).where(
            and_(
                Event.start_time >= start_date,
                Event.end_time <= end_date,
                or_(
                    Event.created_by == user_id,
                    Event.id.in_(
                        select(event_attendees.c.event_id).where(
                            event_attendees.c.user_id == user_id
                        )
                    )
                )
            )
        )
        
        if family_group_id:
            query = query.where(Event.family_group_id == family_group_id)
        
        result = await self.db.execute(query.options(selectinload(Event.attendees)))
        return list(result.scalars().all())
    
    async def update_event(self, event: Event) -> Event:
        """Update event."""
        await self.db.commit()
        await self.db.refresh(event)
        return event
    
    async def delete_event(self, event: Event) -> bool:
        """Delete event."""
        await self.db.delete(event)
        await self.db.commit()
        return True
    
    async def update_event_attendees(self, event_id: str, attendee_ids: List[str]) -> None:
        """Update event attendees."""
        # Remove existing attendees
        await self.db.execute(
            event_attendees.delete().where(event_attendees.c.event_id == event_id)
        )
        # Add new attendees
        for attendee_id in attendee_ids:
            stmt = event_attendees.insert().values(
                event_id=event_id,
                user_id=attendee_id,
                status="pending"
            )
            await self.db.execute(stmt)
        await self.db.commit()
    
    async def get_event_attendees(self, event_id: str) -> List[User]:
        """Get event attendees."""
        result = await self.db.execute(
            select(User)
            .join(event_attendees, User.id == event_attendees.c.user_id)
            .where(event_attendees.c.event_id == event_id)
        )
        return list(result.scalars().all())
    
    async def get_family_group_by_id(self, group_id: str) -> Optional[FamilyGroup]:
        """Get family group by ID."""
        result = await self.db.execute(select(FamilyGroup).where(FamilyGroup.id == group_id))
        return result.scalar_one_or_none()

