"""Router for authentication endpoints."""
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.models import User
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
)
from app.repository.auth_repository import AuthRepository
from app.service.auth_service import AuthService
from app.controller.auth_controller import AuthController

router = APIRouter()


def get_auth_controller(db: AsyncSession = Depends(get_db)) -> AuthController:
    """Dependency to get auth controller."""
    repository = AuthRepository(db)
    service = AuthService(repository)
    return AuthController(service)


@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserCreate,
    controller: AuthController = Depends(get_auth_controller)
):
    """Register a new user with email and password."""
    return await controller.signup(user_data)


@router.post("/login", response_model=LoginResponse)
async def login(
    login_data: LoginRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Login with email and password."""
    return await controller.login(login_data)


@router.post("/refresh", response_model=RefreshTokenResponse)
async def refresh_token(
    token_data: RefreshTokenRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Refresh access token using refresh token."""
    return await controller.refresh_token(token_data)


@router.post("/logout", response_model=LogoutResponse)
async def logout(
    token_data: RefreshTokenRequest,
    current_user: User = Depends(get_current_user),
    controller: AuthController = Depends(get_auth_controller)
):
    """Logout user by invalidating refresh token."""
    return await controller.logout(token_data, current_user)


@router.post("/forgot-password", response_model=MessageResponse)
async def forgot_password(
    request_data: ForgotPasswordRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Send password reset email."""
    return await controller.forgot_password(request_data)


@router.post("/reset-password", response_model=MessageResponse)
async def reset_password(
    request_data: ResetPasswordRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Reset password using token from email."""
    return await controller.reset_password(request_data)


@router.post("/verify-email", response_model=MessageResponse)
async def verify_email(
    request_data: VerifyEmailRequest,
    controller: AuthController = Depends(get_auth_controller)
):
    """Verify email address using token."""
    return await controller.verify_email(request_data)

