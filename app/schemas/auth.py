from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, HttpUrl, constr
from typing import Optional, List, Dict, Any
from datetime import datetime
import re
from uuid import UUID


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
    name: constr(min_length=2, max_length=50, strip_whitespace=True) = Field(
        ...,
        description="User's full name",
        examples=["John Doe"]
    )
    email: EmailStr = Field(
        ...,
        description="User's email address",
        examples=["user@example.com"]
    )


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=128) = Field(
        ...,
        description="User password (min 8 chars, must contain uppercase, lowercase, and number)",
        examples=["SecurePass123"]
    )

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate password strength."""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class UserUpdate(BaseModel):
    name: Optional[constr(min_length=2, max_length=50, strip_whitespace=True)] = Field(
        None,
        description="User's full name",
        examples=["John Doe"]
    )
    phone: Optional[constr(pattern=r'^\+?[1-9]\d{1,14}$')] = Field(
        None,
        description="Phone number in E.164 format",
        examples=["+1234567890"]
    )
    timezone: Optional[constr(pattern=r'^[A-Za-z_/]+$')] = Field(
        None,
        description="Timezone identifier (e.g., America/New_York, UTC)",
        examples=["America/New_York", "UTC"]
    )
    avatar: Optional[HttpUrl] = Field(
        None,
        description="Avatar image URL",
        examples=["https://example.com/avatar.jpg"]
    )


class UserResponse(BaseModel):
    id: str = Field(..., description="User UUID")
    name: str = Field(..., min_length=2, max_length=50)
    email: EmailStr
    emailVerified: bool = Field(..., description="Whether email is verified")
    phone: Optional[str] = Field(None, pattern=r'^\+?[1-9]\d{1,14}$')
    avatar: Optional[str] = Field(None, description="Avatar URL")
    timezone: str = Field(..., pattern=r'^[A-Za-z_/]+$')
    authProvider: str = Field(default="email", pattern="^(email|google|apple)$")
    createdAt: datetime
    updatedAt: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "John Doe",
                "email": "john@example.com",
                "emailVerified": True,
                "phone": "+1234567890",
                "avatar": "https://example.com/avatar.jpg",
                "timezone": "America/New_York",
                "authProvider": "email",
                "createdAt": "2024-01-01T00:00:00Z",
                "updatedAt": "2024-01-01T00:00:00Z"
            }
        }

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
            authProvider=user.auth_provider,
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
    currentPassword: str = Field(..., description="Current password")
    newPassword: constr(min_length=8, max_length=128) = Field(
        ...,
        description="New password (min 8 chars, must contain uppercase, lowercase, number, and special char)"
    )

    @field_validator('newPassword')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate new password strength."""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    @model_validator(mode='after')
    def validate_passwords_different(self):
        """Ensure new password is different from current password."""
        if self.currentPassword == self.newPassword:
            raise ValueError('New password must be different from current password')
        return self


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str = Field(..., min_length=1, description="Password reset token")
    newPassword: constr(min_length=8, max_length=128) = Field(
        ...,
        description="New password (min 8 chars, must contain uppercase, lowercase, number, and special char)"
    )

    @field_validator('newPassword')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """Validate new password strength."""
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


class VerifyEmailRequest(BaseModel):
    token: str = Field(..., min_length=1, description="Email verification token")


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


# OAuth schemas
class OAuthLoginRequest(BaseModel):
    provider: constr(pattern="^(google|apple)$") = Field(
        ...,
        description="OAuth provider (google or apple)"
    )
    idToken: constr(min_length=1) = Field(
        ...,
        description="ID token from OAuth provider"
    )


class OAuthSignupRequest(BaseModel):
    provider: constr(pattern="^(google|apple)$") = Field(
        ...,
        description="OAuth provider (google or apple)"
    )
    idToken: constr(min_length=1) = Field(
        ...,
        description="ID token from OAuth provider"
    )
    name: Optional[constr(min_length=2, max_length=50, strip_whitespace=True)] = Field(
        None,
        description="User's name (required for Apple, optional for Google)"
    )
    timezone: Optional[constr(pattern=r'^[A-Za-z_/]+$')] = Field(
        default="UTC",
        description="Timezone identifier",
        examples=["America/New_York", "UTC"]
    )

