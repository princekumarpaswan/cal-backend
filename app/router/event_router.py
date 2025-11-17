"""Router for event endpoints."""
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.models import User
from app.schemas.event import (
    EventCreate,
    EventUpdate,
    EventCreateResponse,
    EventListResponse,
)
from app.repository.event_repository import EventRepository
from app.service.event_service import EventService
from app.controller.event_controller import EventController

router = APIRouter()


def get_event_controller(db: AsyncSession = Depends(get_db)) -> EventController:
    """Dependency to get event controller."""
    repository = EventRepository(db)
    service = EventService(repository)
    return EventController(service)


@router.post("", response_model=EventCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    event_data: EventCreate,
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Create a new calendar event."""
    return await controller.create_event(current_user, event_data)


@router.get("", response_model=EventListResponse)
async def get_events(
    startDate: datetime = Query(...),
    endDate: datetime = Query(...),
    familyGroupId: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Get events within a date range."""
    return await controller.get_events(startDate, endDate, current_user, familyGroupId)


@router.get("/{event_id}")
async def get_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Get a specific event by ID."""
    return await controller.get_event(event_id, current_user)


@router.put("/{event_id}")
async def update_event(
    event_id: str,
    event_data: EventUpdate,
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Update an event."""
    return await controller.update_event(event_id, current_user, event_data)


@router.delete("/{event_id}")
async def delete_event(
    event_id: str,
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Delete an event."""
    return await controller.delete_event(event_id, current_user)

