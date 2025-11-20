from pydantic import BaseModel, Field, EmailStr, constr
from typing import Optional, List
from datetime import datetime


class FamilyMemberBase(BaseModel):
    userId: str = Field(..., description="User UUID")
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    role: str = Field(..., pattern="^(owner|admin|member)$")
    joinedAt: datetime


class FamilyGroupBase(BaseModel):
    name: constr(min_length=1, max_length=255, strip_whitespace=True) = Field(
        ...,
        description="Family group name",
        examples=["The Smith Family"]
    )
    description: Optional[constr(max_length=1000)] = Field(
        None,
        description="Family group description",
        max_length=1000
    )


class FamilyGroupCreate(FamilyGroupBase):
    pass


class FamilyGroupUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=255, strip_whitespace=True)] = Field(
        None,
        description="Family group name"
    )
    description: Optional[constr(max_length=1000)] = Field(
        None,
        description="Family group description"
    )


class FamilyGroupResponse(BaseModel):
    id: str = Field(..., description="Family group UUID")
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    ownerId: str = Field(..., description="Owner user UUID")
    members: List[FamilyMemberBase] = Field(default_factory=list)
    createdAt: datetime

    class Config:
        from_attributes = True


class InviteMemberRequest(BaseModel):
    email: EmailStr = Field(
        ...,
        description="Email address of the member to invite",
        examples=["member@example.com"]
    )
    role: constr(pattern="^(owner|admin|member)$") = Field(
        default="member",
        description="Role to assign to the member"
    )


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

