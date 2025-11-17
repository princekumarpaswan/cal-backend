"""Controller for event endpoints."""
from datetime import datetime
from typing import List, Dict
from app.service.event_service import EventService
from app.repository.event_repository import EventRepository
from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventCreateResponse,
    EventListResponse,
    EventResponse,
)
from app.models.models import User, Event


class EventController:
    """Controller for event operations."""
    
    def __init__(self, service: EventService):
        self.service = service
    
    def _format_event(self, event: Event) -> Dict:
        """Format event for response."""
        attendees_list = [
            {"id": str(a.id), "name": a.name, "email": a.email}
            for a in event.attendees
        ]
        
        return {
            "id": str(event.id),
            "title": event.title,
            "description": event.description,
            "startTime": event.start_time,
            "endTime": event.end_time,
            "location": event.location,
            "color": event.color,
            "recurrence": event.recurrence,
            "reminders": event.reminders,
            "attendees": attendees_list,
            "createdBy": str(event.created_by),
            "createdAt": event.created_at,
        }
    
    async def create_event(self, current_user: User, event_data: EventCreate) -> EventCreateResponse:
        """Handle create event request."""
        event = await self.service.create_event(current_user, event_data)
        
        # Get attendees
        attendees = await self.service.repository.get_event_attendees(str(event.id))
        attendees_list = [
            {"id": str(a.id), "name": a.name, "email": a.email}
            for a in attendees
        ]
        
        return EventCreateResponse(
            success=True,
            data={
                "event": EventResponse(
                    id=str(event.id),
                    title=event.title,
                    description=event.description,
                    startTime=event.start_time,
                    endTime=event.end_time,
                    location=event.location,
                    color=event.color,
                    recurrence=event.recurrence,
                    reminders=event.reminders,
                    attendees=attendees_list,
                    createdBy=str(event.created_by),
                    createdAt=event.created_at,
                )
            }
        )
    
    async def get_events(
        self,
        start_date: datetime,
        end_date: datetime,
        current_user: User,
        family_group_id: str = None
    ) -> EventListResponse:
        """Handle get events request."""
        events = await self.service.get_events(start_date, end_date, current_user, family_group_id)
        
        events_list = [self._format_event(event) for event in events]
        
        return EventListResponse(
            success=True,
            data={
                "events": events_list,
                "pagination": {
                    "total": len(events_list),
                    "page": 1,
                    "pageSize": len(events_list)
                }
            }
        )
    
    async def get_event(self, event_id: str, current_user: User) -> Dict:
        """Handle get event request."""
        event = await self.service.get_event(event_id, current_user)
        
        return {
            "success": True,
            "data": {
                "event": self._format_event(event)
            }
        }
    
    async def update_event(self, event_id: str, current_user: User, event_data: EventUpdate) -> Dict:
        """Handle update event request."""
        event = await self.service.update_event(event_id, current_user, event_data)
        
        # Reload attendees
        event = await self.service.repository.get_event_by_id(event_id, load_attendees=True)
        
        return {
            "success": True,
            "data": {
                "event": self._format_event(event)
            },
            "message": "Event updated successfully"
        }
    
    async def delete_event(self, event_id: str, current_user: User) -> Dict:
        """Handle delete event request."""
        await self.service.delete_event(event_id, current_user)
        
        return {
            "success": True,
            "message": "Event deleted successfully"
        }

