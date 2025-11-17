"""Service for authentication business logic."""
from datetime import datetime, timedelta
from typing import Optional, Tuple
from app.repository.auth_repository import AuthRepository
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.core.config import settings
from app.api.exceptions import (
    ConflictException,
    UnauthorizedException,
)
from app.models.models import User, RefreshToken


class AuthService:
    """Service for authentication operations."""
    
    def __init__(self, repository: AuthRepository):
        self.repository = repository
    
    async def signup(self, name: str, email: str, password: str) -> Tuple[User, str, str]:
        """Register a new user."""
        # Check if user already exists
        existing_user = await self.repository.get_user_by_email(email)
        if existing_user:
            raise ConflictException("Email already registered")
        
        # Create new user
        hashed_password = get_password_hash(password)
        user = await self.repository.create_user(name, email, hashed_password)
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token_str = create_refresh_token({"sub": str(user.id)})
        
        # Store refresh token
        await self.repository.create_refresh_token(str(user.id), refresh_token_str)
        
        return user, access_token, refresh_token_str
    
    async def login(self, email: str, password: str) -> Tuple[User, str, str]:
        """Login user."""
        # Find user by email
        user = await self.repository.get_user_by_email(email)
        
        if not user or not verify_password(password, user.password_hash):
            raise UnauthorizedException("Invalid email or password")
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token_str = create_refresh_token({"sub": str(user.id)})
        
        # Store refresh token
        await self.repository.create_refresh_token(str(user.id), refresh_token_str)
        
        return user, access_token, refresh_token_str
    
    async def refresh_access_token(self, refresh_token_str: str) -> str:
        """Refresh access token using refresh token."""
        # Find refresh token
        refresh_token = await self.repository.get_refresh_token(refresh_token_str)
        
        if not refresh_token:
            raise UnauthorizedException("Invalid refresh token")
        
        # Check if token is expired
        if refresh_token.expires_at < datetime.utcnow():
            await self.repository.delete_refresh_token_by_token(refresh_token_str)
            raise UnauthorizedException("Refresh token expired")
        
        # Generate new access token
        access_token = create_access_token({"sub": str(refresh_token.user_id)})
        
        return access_token
    
    async def logout(self, refresh_token_str: str, user_id: str) -> bool:
        """Logout user by invalidating refresh token."""
        return await self.repository.delete_refresh_token(refresh_token_str, user_id)
    
    async def forgot_password(self, email: str) -> bool:
        """Handle forgot password request."""
        # TODO: Implement email sending logic
        # For security, always return success even if email doesn't exist
        user = await self.repository.get_user_by_email(email)
        if user:
            # TODO: Generate reset token and send email
            pass
        return True
    
    async def reset_password(self, token: str, new_password: str) -> bool:
        """Reset password using token from email."""
        # TODO: Implement password reset logic with token verification
        return True
    
    async def verify_email(self, token: str) -> bool:
        """Verify email address using token."""
        # TODO: Implement email verification logic
        return True

