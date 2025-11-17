from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
import re


# Base response schemas
class ResponseBase(BaseModel):
    success: bool
    message: Optional[str] = None


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None


class ErrorResponse(ResponseBase):
    success: bool = False
    error: ErrorDetail


# User schemas
class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)

    @validator('password')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v


class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    phone: Optional[str] = None
    timezone: Optional[str] = None


class UserResponse(BaseModel):
    id: str
    name: str
    email: str
    emailVerified: bool
    phone: Optional[str] = None
    avatar: Optional[str] = None
    timezone: str
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_model(cls, user):
        return cls(
            id=str(user.id),
            name=user.name,
            email=user.email,
            emailVerified=user.email_verified,
            phone=user.phone,
            avatar=user.avatar_url,
            timezone=user.timezone,
            createdAt=user.created_at,
            updatedAt=user.updated_at,
        )


# Token schemas
class TokenPair(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int


class TokenResponse(BaseModel):
    user: UserResponse
    tokens: TokenPair


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class RefreshTokenRequest(BaseModel):
    refreshToken: str


class ChangePasswordRequest(BaseModel):
    currentPassword: str
    newPassword: str = Field(..., min_length=8)

    @validator('newPassword')
    def validate_password(cls, v):
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        return v


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    newPassword: str = Field(..., min_length=8)


class VerifyEmailRequest(BaseModel):
    token: str


# Success responses
class SignupResponse(ResponseBase):
    success: bool = True
    data: TokenResponse
    message: str = "Account created successfully"


class LoginResponse(ResponseBase):
    success: bool = True
    data: TokenResponse
    message: str = "Login successful"


class RefreshTokenResponse(ResponseBase):
    success: bool = True
    data: Dict[str, Any]


class LogoutResponse(ResponseBase):
    success: bool = True
    message: str = "Logged out successfully"


class UserProfileResponse(ResponseBase):
    success: bool = True
    data: Dict[str, UserResponse]


class MessageResponse(ResponseBase):
    success: bool = True

