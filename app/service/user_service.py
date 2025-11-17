"""Service for user business logic."""
from app.repository.user_repository import UserRepository
from app.core.security import get_password_hash, verify_password
from app.api.exceptions import ValidationException
from app.models.models import User
from app.schemas.auth import UserUpdate, ChangePasswordRequest


class UserService:
    """Service for user operations."""
    
    def __init__(self, repository: UserRepository):
        self.repository = repository
    
    async def get_profile(self, user: User) -> User:
        """Get user profile."""
        return user
    
    async def update_profile(self, user: User, user_data: UserUpdate) -> User:
        """Update user profile."""
        # Update fields if provided
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.phone is not None:
            user.phone = user_data.phone
        if user_data.timezone is not None:
            user.timezone = user_data.timezone
        
        return await self.repository.update_user(user)
    
    async def change_password(self, user: User, password_data: ChangePasswordRequest) -> bool:
        """Change user password."""
        # Verify current password
        if not verify_password(password_data.currentPassword, user.password_hash):
            raise ValidationException("Current password is incorrect")
        
        # Update password
        user.password_hash = get_password_hash(password_data.newPassword)
        await self.repository.update_user(user)
        return True

