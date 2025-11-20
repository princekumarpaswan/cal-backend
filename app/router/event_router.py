"""Router for event endpoints."""
from fastapi import APIRouter, Depends, Query, Path, status
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
from app.schemas.query_params import EventQueryParams
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
    startDate: datetime = Query(..., description="Start date for event range (ISO 8601 format)"),
    endDate: datetime = Query(..., description="End date for event range (ISO 8601 format)"),
    familyGroupId: Optional[str] = Query(
        None,
        pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="Filter by family group UUID"
    ),
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Get events within a date range.
    
    - **startDate**: Start date for event range (ISO 8601 format)
    - **endDate**: End date for event range (ISO 8601 format, must be after startDate)
    - **familyGroupId**: Optional family group UUID to filter events
    """
    # Validate date range
    if endDate <= startDate:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be after start date"
        )
    
    # Validate date range doesn't exceed 365 days
    days_diff = (endDate - startDate).days
    if days_diff > 365:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date range cannot exceed 365 days"
        )
    
    return await controller.get_events(startDate, endDate, current_user, familyGroupId)


@router.get("/{event_id}")
async def get_event(
    event_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Event UUID"),
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Get a specific event by ID.
    
    - **event_id**: Event UUID
    """
    return await controller.get_event(event_id, current_user)


@router.put("/{event_id}")
async def update_event(
    event_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Event UUID"),
    event_data: EventUpdate = ...,
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Update an event.
    
    - **event_id**: Event UUID
    """
    return await controller.update_event(event_id, current_user, event_data)


@router.delete("/{event_id}")
async def delete_event(
    event_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Event UUID"),
    current_user: User = Depends(get_current_user),
    controller: EventController = Depends(get_event_controller)
):
    """Delete an event.
    
    - **event_id**: Event UUID
    """
    return await controller.delete_event(event_id, current_user)

