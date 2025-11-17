"""Controller for user endpoints."""
from app.service.user_service import UserService
from app.repository.user_repository import UserRepository
from app.schemas.auth import (
    UserUpdate,
    UserProfileResponse,
    ChangePasswordRequest,
    MessageResponse,
    UserResponse,
)
from app.models.models import User


class UserController:
    """Controller for user operations."""
    
    def __init__(self, service: UserService):
        self.service = service
    
    async def get_profile(self, current_user: User) -> UserProfileResponse:
        """Handle get profile request."""
        user = await self.service.get_profile(current_user)
        
        return UserProfileResponse(
            success=True,
            data={"user": UserResponse.from_orm_model(user)}
        )
    
    async def update_profile(self, current_user: User, user_data: UserUpdate) -> UserProfileResponse:
        """Handle update profile request."""
        user = await self.service.update_profile(current_user, user_data)
        
        return UserProfileResponse(
            success=True,
            data={"user": UserResponse.from_orm_model(user)}
        )
    
    async def change_password(self, current_user: User, password_data: ChangePasswordRequest) -> MessageResponse:
        """Handle change password request."""
        await self.service.change_password(current_user, password_data)
        
        return MessageResponse(
            success=True,
            message="Password changed successfully"
        )

