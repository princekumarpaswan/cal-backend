"""Router for user endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.api.dependencies import get_current_user
from app.models.models import User
from app.schemas.auth import (
    UserUpdate,
    UserProfileResponse,
    ChangePasswordRequest,
    MessageResponse,
)
from app.repository.user_repository import UserRepository
from app.service.user_service import UserService
from app.controller.user_controller import UserController

router = APIRouter()


def get_user_controller(db: AsyncSession = Depends(get_db)) -> UserController:
    """Dependency to get user controller."""
    repository = UserRepository(db)
    service = UserService(repository)
    return UserController(service)


@router.get("/profile", response_model=UserProfileResponse)
async def get_profile(
    current_user: User = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller)
):
    """Get current user profile."""
    return await controller.get_profile(current_user)


@router.put("/profile", response_model=UserProfileResponse)
async def update_profile(
    user_data: UserUpdate,
    current_user: User = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller)
):
    """Update current user profile."""
    return await controller.update_profile(current_user, user_data)


@router.post("/change-password", response_model=MessageResponse)
async def change_password(
    password_data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    controller: UserController = Depends(get_user_controller)
):
    """Change user password."""
    return await controller.change_password(current_user, password_data)

