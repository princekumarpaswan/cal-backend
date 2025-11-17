"""Controller for authentication endpoints."""
from app.service.auth_service import AuthService
from app.repository.auth_repository import AuthRepository
from app.schemas.auth import (
    UserCreate,
    LoginRequest,
    RefreshTokenRequest,
    SignupResponse,
    LoginResponse,
    RefreshTokenResponse,
    LogoutResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    VerifyEmailRequest,
    MessageResponse,
    TokenPair,
    TokenResponse,
    UserResponse,
)
from app.core.config import settings
from app.models.models import User


class AuthController:
    """Controller for authentication operations."""
    
    def __init__(self, service: AuthService):
        self.service = service
    
    async def signup(self, user_data: UserCreate) -> SignupResponse:
        """Handle user signup."""
        user, access_token, refresh_token_str = await self.service.signup(
            user_data.name,
            user_data.email,
            user_data.password
        )
        
        return SignupResponse(
            success=True,
            data=TokenResponse(
                user=UserResponse.from_orm_model(user),
                tokens=TokenPair(
                    accessToken=access_token,
                    refreshToken=refresh_token_str,
                    expiresIn=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
            ),
            message="Account created successfully"
        )
    
    async def login(self, login_data: LoginRequest) -> LoginResponse:
        """Handle user login."""
        user, access_token, refresh_token_str = await self.service.login(
            login_data.email,
            login_data.password
        )
        
        return LoginResponse(
            success=True,
            data=TokenResponse(
                user=UserResponse.from_orm_model(user),
                tokens=TokenPair(
                    accessToken=access_token,
                    refreshToken=refresh_token_str,
                    expiresIn=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
                )
            ),
            message="Login successful"
        )
    
    async def refresh_token(self, token_data: RefreshTokenRequest) -> RefreshTokenResponse:
        """Handle token refresh."""
        access_token = await self.service.refresh_access_token(token_data.refreshToken)
        
        return RefreshTokenResponse(
            success=True,
            data={
                "accessToken": access_token,
                "expiresIn": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
            }
        )
    
    async def logout(self, token_data: RefreshTokenRequest, current_user: User) -> LogoutResponse:
        """Handle user logout."""
        await self.service.logout(token_data.refreshToken, str(current_user.id))
        
        return LogoutResponse(
            success=True,
            message="Logged out successfully"
        )
    
    async def forgot_password(self, request_data: ForgotPasswordRequest) -> MessageResponse:
        """Handle forgot password request."""
        await self.service.forgot_password(request_data.email)
        
        return MessageResponse(
            success=True,
            message="Password reset email sent"
        )
    
    async def reset_password(self, request_data: ResetPasswordRequest) -> MessageResponse:
        """Handle password reset."""
        await self.service.reset_password(request_data.token, request_data.newPassword)
        
        return MessageResponse(
            success=True,
            message="Password reset successful"
        )
    
    async def verify_email(self, request_data: VerifyEmailRequest) -> MessageResponse:
        """Handle email verification."""
        await self.service.verify_email(request_data.token)
        
        return MessageResponse(
            success=True,
            message="Email verified successfully"
        )

