from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ReminderSchema(BaseModel):
    type: str = Field(..., pattern="^(notification|email)$")
    minutesBefore: int = Field(..., ge=0)


class RecurrenceSchema(BaseModel):
    frequency: str = Field(..., pattern="^(daily|weekly|monthly|yearly|none)$")
    interval: int = Field(default=1, ge=1)
    endDate: Optional[datetime] = None


class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    startTime: datetime
    endTime: datetime
    location: Optional[str] = None
    color: Optional[str] = Field(default="#3B82F6", pattern="^#[0-9A-Fa-f]{6}$")
    recurrence: Optional[RecurrenceSchema] = None
    reminders: Optional[List[ReminderSchema]] = None
    familyGroupId: Optional[str] = None


class EventCreate(EventBase):
    attendees: Optional[List[str]] = []


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    startTime: Optional[datetime] = None
    endTime: Optional[datetime] = None
    location: Optional[str] = None
    color: Optional[str] = Field(None, pattern="^#[0-9A-Fa-f]{6}$")
    recurrence: Optional[RecurrenceSchema] = None
    reminders: Optional[List[ReminderSchema]] = None
    attendees: Optional[List[str]] = None


class EventResponse(BaseModel):
    id: str
    title: str
    description: Optional[str]
    startTime: datetime
    endTime: datetime
    location: Optional[str]
    color: str
    recurrence: Optional[Dict[str, Any]]
    reminders: Optional[List[Dict[str, Any]]]
    attendees: List[Dict[str, str]]
    createdBy: str
    createdAt: datetime

    class Config:
        from_attributes = True


class EventListResponse(BaseModel):
    success: bool = True
    data: Dict[str, Any]


class EventCreateResponse(BaseModel):
    success: bool = True
    data: Dict[str, EventResponse]

