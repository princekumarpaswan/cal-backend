"""Service for event business logic."""
from datetime import datetime
from typing import List, Dict, Optional
from app.repository.event_repository import EventRepository
from app.api.exceptions import NotFoundException, ForbiddenException
from app.models.models import User, Event
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    """Service for event operations."""
    
    def __init__(self, repository: EventRepository):
        self.repository = repository
    
    async def create_event(self, user: User, event_data: EventCreate) -> Event:
        """Create a new event."""
        # Validate family group if provided
        if event_data.familyGroupId:
            family_group = await self.repository.get_family_group_by_id(event_data.familyGroupId)
            if not family_group:
                raise NotFoundException("Family group not found")
        
        return await self.repository.create_event(
            title=event_data.title,
            description=event_data.description,
            start_time=event_data.startTime,
            end_time=event_data.endTime,
            location=event_data.location,
            color=event_data.color,
            recurrence=event_data.recurrence.dict() if event_data.recurrence else None,
            reminders=[r.dict() for r in event_data.reminders] if event_data.reminders else None,
            family_group_id=event_data.familyGroupId,
            created_by=str(user.id),
            attendee_ids=event_data.attendees
        )
    
    async def get_events(
        self,
        start_date: datetime,
        end_date: datetime,
        user: User,
        family_group_id: Optional[str] = None
    ) -> List[Event]:
        """Get events within a date range."""
        return await self.repository.get_events(
            start_date,
            end_date,
            str(user.id),
            family_group_id
        )
    
    async def get_event(self, event_id: str, user: User) -> Event:
        """Get a specific event."""
        event = await self.repository.get_event_by_id(event_id, load_attendees=True)
        
        if not event:
            raise NotFoundException("Event not found")
        
        # Check if user has access
        is_creator = event.created_by == user.id
        is_attendee = any(a.id == user.id for a in event.attendees)
        
        if not is_creator and not is_attendee:
            raise ForbiddenException("You don't have access to this event")
        
        return event
    
    async def update_event(self, event_id: str, user: User, event_data: EventUpdate) -> Event:
        """Update an event."""
        event = await self.repository.get_event_by_id(event_id)
        
        if not event:
            raise NotFoundException("Event not found")
        
        # Only creator can update
        if event.created_by != user.id:
            raise ForbiddenException("Only the event creator can update the event")
        
        # Update fields
        if event_data.title is not None:
            event.title = event_data.title
        if event_data.description is not None:
            event.description = event_data.description
        if event_data.startTime is not None:
            event.start_time = event_data.startTime
        if event_data.endTime is not None:
            event.end_time = event_data.endTime
        if event_data.location is not None:
            event.location = event_data.location
        if event_data.color is not None:
            event.color = event_data.color
        if event_data.recurrence is not None:
            event.recurrence = event_data.recurrence.dict()
        if event_data.reminders is not None:
            event.reminders = [r.dict() for r in event_data.reminders]
        
        # Update attendees if provided
        if event_data.attendees is not None:
            await self.repository.update_event_attendees(str(event.id), event_data.attendees)
        
        return await self.repository.update_event(event)
    
    async def delete_event(self, event_id: str, user: User) -> bool:
        """Delete an event."""
        event = await self.repository.get_event_by_id(event_id)
        
        if not event:
            raise NotFoundException("Event not found")
        
        # Only creator can delete
        if event.created_by != user.id:
            raise ForbiddenException("Only the event creator can delete the event")
        
        return await self.repository.delete_event(event)

