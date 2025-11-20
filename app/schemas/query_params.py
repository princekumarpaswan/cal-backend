"""Query parameter validation schemas."""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class EventQueryParams(BaseModel):
    """Query parameters for event listing."""
    startDate: datetime = Field(
        ...,
        description="Start date for event range (ISO 8601 format)",
        examples=["2024-01-01T00:00:00Z"]
    )
    endDate: datetime = Field(
        ...,
        description="End date for event range (ISO 8601 format)",
        examples=["2024-12-31T23:59:59Z"]
    )
    familyGroupId: Optional[str] = Field(
        None,
        pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="Filter by family group UUID"
    )

    @field_validator('endDate')
    @classmethod
    def validate_date_range(cls, v: datetime, info) -> datetime:
        """Validate that end date is after start date."""
        if 'startDate' in info.data and v < info.data['startDate']:
            raise ValueError("End date must be after start date")
        
        # Validate date range (max 1 year)
        if 'startDate' in info.data:
            days_diff = (v - info.data['startDate']).days
            if days_diff > 365:
                raise ValueError("Date range cannot exceed 365 days")
        
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "startDate": "2024-01-01T00:00:00Z",
                "endDate": "2024-12-31T23:59:59Z",
                "familyGroupId": None
            }
        }


class TaskQueryParams(BaseModel):
    """Query parameters for task listing."""
    familyGroupId: Optional[str] = Field(
        None,
        pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="Filter by family group UUID"
    )
    status: Optional[str] = Field(
        None,
        pattern="^(pending|in_progress|completed|cancelled)$",
        description="Filter by task status"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "familyGroupId": None,
                "status": "pending"
            }
        }


class PaginationParams(BaseModel):
    """Pagination query parameters."""
    page: int = Field(
        default=1,
        ge=1,
        description="Page number (starts from 1)"
    )
    pageSize: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Number of items per page (max 100)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "pageSize": 20
            }
        }

