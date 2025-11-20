"""Router for family endpoints."""
from fastapi import APIRouter, Depends, Path, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.models import User
from app.schemas.family import (
    FamilyGroupCreate,
    FamilyGroupCreateResponse,
    InviteMemberRequest,
    InviteMemberResponse,
)
from app.repository.family_repository import FamilyRepository
from app.service.family_service import FamilyService
from app.controller.family_controller import FamilyController

router = APIRouter()


def get_family_controller(db: AsyncSession = Depends(get_db)) -> FamilyController:
    """Dependency to get family controller."""
    repository = FamilyRepository(db)
    service = FamilyService(repository)
    return FamilyController(service)


@router.post("/groups", response_model=FamilyGroupCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_family_group(
    group_data: FamilyGroupCreate,
    current_user: User = Depends(get_current_user),
    controller: FamilyController = Depends(get_family_controller)
):
    """Create a new family group."""
    return await controller.create_family_group(current_user, group_data)


@router.get("/groups/{group_id}")
async def get_family_group(
    group_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Family group UUID"),
    current_user: User = Depends(get_current_user),
    controller: FamilyController = Depends(get_family_controller)
):
    """Get family group details.
    
    - **group_id**: Family group UUID
    """
    return await controller.get_family_group(group_id, current_user)


@router.get("/groups")
async def get_user_family_groups(
    current_user: User = Depends(get_current_user),
    controller: FamilyController = Depends(get_family_controller)
):
    """Get all family groups for current user."""
    return await controller.get_user_family_groups(current_user)


@router.post("/groups/{group_id}/invite", response_model=InviteMemberResponse)
async def invite_family_member(
    group_id: str = Path(..., pattern="^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", description="Family group UUID"),
    invite_data: InviteMemberRequest = ...,
    current_user: User = Depends(get_current_user),
    controller: FamilyController = Depends(get_family_controller)
):
    """Invite a member to a family group.
    
    - **group_id**: Family group UUID
    """
    return await controller.invite_member(group_id, current_user, invite_data)

