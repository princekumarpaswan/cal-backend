"""Service for family business logic."""
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
import secrets
from app.repository.family_repository import FamilyRepository
from app.api.exceptions import NotFoundException, ForbiddenException
from app.models.models import User, FamilyGroup
from app.schemas.family import FamilyGroupCreate, InviteMemberRequest, FamilyMemberBase


class FamilyService:
    """Service for family operations."""
    
    def __init__(self, repository: FamilyRepository):
        self.repository = repository
    
    async def create_family_group(self, user: User, group_data: FamilyGroupCreate) -> FamilyGroup:
        """Create a new family group."""
        return await self.repository.create_family_group(
            group_data.name,
            group_data.description,
            str(user.id)
        )
    
    async def get_family_group(self, group_id: str, user: User) -> Tuple[FamilyGroup, List[Dict]]:
        """Get family group details."""
        group = await self.repository.get_family_group_by_id(group_id, load_members=True)
        
        if not group:
            raise NotFoundException("Family group not found")
        
        # Check if user is a member
        is_member = any(member.id == user.id for member in group.members)
        if not is_member:
            raise ForbiddenException("You are not a member of this group")
        
        # Get member details with roles
        members_data = await self.repository.get_family_members(group_id)
        
        members = [
            {
                "userId": str(member.id),
                "name": member.name,
                "email": member.email,
                "role": role,
                "joinedAt": joined_at
            }
            for member, role, joined_at in members_data
        ]
        
        return group, members
    
    async def get_user_family_groups(self, user: User) -> List[Dict]:
        """Get all family groups for a user."""
        groups = await self.repository.get_user_family_groups(str(user.id))
        
        groups_data = []
        for group in groups:
            member_count = len(group.members)
            groups_data.append({
                "id": str(group.id),
                "name": group.name,
                "description": group.description,
                "ownerId": str(group.owner_id),
                "memberCount": member_count,
                "createdAt": group.created_at,
            })
        
        return groups_data
    
    async def invite_member(self, group_id: str, user: User, invite_data: InviteMemberRequest) -> Dict:
        """Invite a member to a family group."""
        # Get the group
        group = await self.repository.get_family_group_by_id(group_id)
        
        if not group:
            raise NotFoundException("Family group not found")
        
        # Check if user is owner or admin
        membership = await self.repository.check_membership(group_id, str(user.id))
        
        if not membership or membership.get("role") not in ["owner", "admin"]:
            raise ForbiddenException("Only owners and admins can invite members")
        
        # Generate invitation token
        token = secrets.token_urlsafe(32)
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        # Create invitation
        invitation = await self.repository.create_invitation(
            group.id,
            invite_data.email,
            invite_data.role,
            token,
            expires_at
        )
        
        # TODO: Send invitation email
        
        return {
            "id": str(invitation.id),
            "groupId": str(invitation.family_group_id),
            "email": invitation.email,
            "role": invitation.role,
            "status": invitation.status,
            "expiresAt": invitation.expires_at,
        }

