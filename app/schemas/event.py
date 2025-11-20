from pydantic import BaseModel, Field, field_validator, model_validator, constr
from typing import Optional, List, Dict, Any
from datetime import datetime
from uuid import UUID


class ReminderSchema(BaseModel):
    type: constr(pattern="^(notification|email)$") = Field(
        ...,
        description="Reminder type (notification or email)"
    )
    minutesBefore: int = Field(
        ...,
        ge=0,
        le=10080,  # Max 7 days in minutes
        description="Minutes before event to send reminder"
    )


class RecurrenceSchema(BaseModel):
    frequency: constr(pattern="^(daily|weekly|monthly|yearly|none)$") = Field(
        ...,
        description="Recurrence frequency"
    )
    interval: int = Field(
        default=1,
        ge=1,
        le=365,
        description="Interval between recurrences (e.g., every 2 weeks)"
    )
    endDate: Optional[datetime] = Field(
        None,
        description="End date for recurrence (optional)"
    )

    @model_validator(mode='after')
    def validate_recurrence(self):
        """Validate recurrence settings."""
        if self.frequency == "none" and self.interval != 1:
            raise ValueError("Interval must be 1 when frequency is 'none'")
        return self


class EventBase(BaseModel):
    title: constr(min_length=1, max_length=255, strip_whitespace=True) = Field(
        ...,
        description="Event title",
        examples=["Team Meeting"]
    )
    description: Optional[constr(max_length=5000)] = Field(
        None,
        description="Event description",
        max_length=5000
    )
    startTime: datetime = Field(
        ...,
        description="Event start time (ISO 8601 format)"
    )
    endTime: datetime = Field(
        ...,
        description="Event end time (ISO 8601 format)"
    )
    location: Optional[constr(max_length=500)] = Field(
        None,
        description="Event location",
        max_length=500
    )
    color: Optional[constr(pattern="^#[0-9A-Fa-f]{6}$")] = Field(
        default="#3B82F6",
        description="Event color in hex format",
        examples=["#3B82F6"]
    )
    recurrence: Optional[RecurrenceSchema] = Field(
        None,
        description="Recurrence settings"
    )
    reminders: Optional[List[ReminderSchema]] = Field(
        None,
        description="List of reminders",
        max_length=10  # Limit number of reminders
    )
    familyGroupId: Optional[constr(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")] = Field(
        None,
        description="Family group UUID (optional)"
    )

    @model_validator(mode='after')
    def validate_time_range(self):
        """Validate that end time is after start time."""
        if self.endTime <= self.startTime:
            raise ValueError("End time must be after start time")
        
        # Validate event duration (max 30 days)
        duration = (self.endTime - self.startTime).total_seconds() / 3600
        if duration > 720:  # 30 days in hours
            raise ValueError("Event duration cannot exceed 30 days")
        
        return self


class EventCreate(EventBase):
    attendees: Optional[List[constr(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")]] = Field(
        default=[],
        description="List of attendee user UUIDs",
        max_length=100  # Limit number of attendees
    )


class EventUpdate(BaseModel):
    title: Optional[constr(min_length=1, max_length=255, strip_whitespace=True)] = Field(
        None,
        description="Event title"
    )
    description: Optional[constr(max_length=5000)] = Field(
        None,
        description="Event description"
    )
    startTime: Optional[datetime] = Field(
        None,
        description="Event start time"
    )
    endTime: Optional[datetime] = Field(
        None,
        description="Event end time"
    )
    location: Optional[constr(max_length=500)] = Field(
        None,
        description="Event location"
    )
    color: Optional[constr(pattern="^#[0-9A-Fa-f]{6}$")] = Field(
        None,
        description="Event color in hex format"
    )
    recurrence: Optional[RecurrenceSchema] = None
    reminders: Optional[List[ReminderSchema]] = Field(
        None,
        max_length=10
    )
    attendees: Optional[List[constr(pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$")]] = Field(
        None,
        max_length=100
    )

    @model_validator(mode='after')
    def validate_time_range(self):
        """Validate that end time is after start time if both are provided."""
        if self.startTime and self.endTime:
            if self.endTime <= self.startTime:
                raise ValueError("End time must be after start time")
            
            duration = (self.endTime - self.startTime).total_seconds() / 3600
            if duration > 720:
                raise ValueError("Event duration cannot exceed 30 days")
        
        return self


class EventResponse(BaseModel):
    id: str = Field(..., description="Event UUID")
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    startTime: datetime
    endTime: datetime
    location: Optional[str] = None
    color: str = Field(..., pattern="^#[0-9A-Fa-f]{6}$")
    recurrence: Optional[Dict[str, Any]] = None
    reminders: Optional[List[Dict[str, Any]]] = None
    attendees: List[Dict[str, str]] = Field(default_factory=list)
    createdBy: str = Field(..., description="Creator user UUID")
    createdAt: datetime

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    success: bool = True
    data: Dict[str, Any]


class EventCreateResponse(BaseModel):
    success: bool = True
    data: Dict[str, EventResponse]

