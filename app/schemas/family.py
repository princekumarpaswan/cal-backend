from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class FamilyMemberBase(BaseModel):
    userId: str
    name: str
    email: str
    role: str
    joinedAt: datetime


class FamilyGroupBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class FamilyGroupCreate(FamilyGroupBase):
    pass


class FamilyGroupUpdate(FamilyGroupBase):
    name: Optional[str] = Field(None, min_length=1, max_length=255)


class FamilyGroupResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    ownerId: str
    members: List[FamilyMemberBase]
    createdAt: datetime

    class Config:
        from_attributes = True


class InviteMemberRequest(BaseModel):
    email: str
    role: str = Field(default="member", pattern="^(owner|admin|member)$")


class InvitationResponse(BaseModel):
    id: str
    groupId: str
    email: str
    role: str
    status: str
    expiresAt: datetime


class FamilyGroupCreateResponse(BaseModel):
    success: bool = True
    data: dict


class InviteMemberResponse(BaseModel):
    success: bool = True
    data: dict
    message: str = "Invitation sent successfully"

