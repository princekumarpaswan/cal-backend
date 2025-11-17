"""Controller for family endpoints."""
from app.service.family_service import FamilyService
from app.repository.family_repository import FamilyRepository
from app.schemas.family import (
    FamilyGroupCreate,
    FamilyGroupCreateResponse,
    InviteMemberRequest,
    InviteMemberResponse,
    FamilyMemberBase,
)
from app.models.models import User, FamilyGroup
from datetime import datetime


class FamilyController:
    """Controller for family operations."""
    
    def __init__(self, service: FamilyService):
        self.service = service
    
    async def create_family_group(self, current_user: User, group_data: FamilyGroupCreate) -> FamilyGroupCreateResponse:
        """Handle create family group request."""
        group = await self.service.create_family_group(current_user, group_data)
        
        # Format members
        members = [
            FamilyMemberBase(
                userId=str(current_user.id),
                name=current_user.name,
                email=current_user.email,
                role="owner",
                joinedAt=datetime.utcnow()
            )
        ]
        
        return FamilyGroupCreateResponse(
            success=True,
            data={
                "group": {
                    "id": str(group.id),
                    "name": group.name,
                    "description": group.description,
                    "ownerId": str(group.owner_id),
                    "members": members,
                    "createdAt": group.created_at,
                }
            }
        )
    
    async def get_family_group(self, group_id: str, current_user: User) -> dict:
        """Handle get family group request."""
        group, members = await self.service.get_family_group(group_id, current_user)
        
        return {
            "success": True,
            "data": {
                "group": {
                    "id": str(group.id),
                    "name": group.name,
                    "description": group.description,
                    "ownerId": str(group.owner_id),
                    "members": members,
                    "createdAt": group.created_at,
                }
            }
        }
    
    async def get_user_family_groups(self, current_user: User) -> dict:
        """Handle get user family groups request."""
        groups_data = await self.service.get_user_family_groups(current_user)
        
        return {
            "success": True,
            "data": {
                "groups": groups_data
            }
        }
    
    async def invite_member(self, group_id: str, current_user: User, invite_data: InviteMemberRequest) -> InviteMemberResponse:
        """Handle invite member request."""
        invitation = await self.service.invite_member(group_id, current_user, invite_data)
        
        return InviteMemberResponse(
            success=True,
            data={"invitation": invitation},
            message="Invitation sent successfully"
        )

