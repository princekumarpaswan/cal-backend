"""Repository for family-related database operations."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from sqlalchemy.orm import selectinload
from datetime import datetime
from typing import List, Optional
from app.models.models import User, FamilyGroup, FamilyInvitation, family_members


class FamilyRepository:
    """Repository for family operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_family_group(self, name: str, description: Optional[str], owner_id: str) -> FamilyGroup:
        """Create a new family group."""
        new_group = FamilyGroup(
            name=name,
            description=description,
            owner_id=owner_id,
        )
        self.db.add(new_group)
        await self.db.flush()
        
        # Add creator as owner member
        stmt = family_members.insert().values(
            family_group_id=new_group.id,
            user_id=owner_id,
            role="owner",
            joined_at=datetime.utcnow()
        )
        await self.db.execute(stmt)
        await self.db.commit()
        await self.db.refresh(new_group)
        return new_group
    
    async def get_family_group_by_id(self, group_id: str, load_members: bool = False) -> Optional[FamilyGroup]:
        """Get family group by ID."""
        query = select(FamilyGroup).where(FamilyGroup.id == group_id)
        if load_members:
            query = query.options(selectinload(FamilyGroup.members))
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def get_user_family_groups(self, user_id: str) -> List[FamilyGroup]:
        """Get all family groups for a user."""
        result = await self.db.execute(
            select(FamilyGroup)
            .join(family_members, FamilyGroup.id == family_members.c.family_group_id)
            .where(family_members.c.user_id == user_id)
            .options(selectinload(FamilyGroup.members))
        )
        return list(result.scalars().all())
    
    async def get_family_members(self, group_id: str) -> List[tuple]:
        """Get family group members with roles."""
        result = await self.db.execute(
            select(User, family_members.c.role, family_members.c.joined_at)
            .join(family_members, User.id == family_members.c.user_id)
            .where(family_members.c.family_group_id == group_id)
        )
        return result.all()
    
    async def check_membership(self, group_id: str, user_id: str) -> Optional[dict]:
        """Check if user is a member of the group and get role."""
        result = await self.db.execute(
            select(family_members).where(
                and_(
                    family_members.c.family_group_id == group_id,
                    family_members.c.user_id == user_id
                )
            )
        )
        membership = result.first()
        return dict(membership._mapping) if membership else None
    
    async def create_invitation(self, family_group_id: str, email: str, role: str, token: str, expires_at: datetime) -> FamilyInvitation:
        """Create a family invitation."""
        invitation = FamilyInvitation(
            family_group_id=family_group_id,
            email=email,
            role=role,
            status="pending",
            token=token,
            expires_at=expires_at
        )
        self.db.add(invitation)
        await self.db.commit()
        await self.db.refresh(invitation)
        return invitation

