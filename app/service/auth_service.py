"""Service for authentication business logic."""
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any
from app.repository.auth_repository import AuthRepository
from app.core.security import (
    get_password_hash,
    verify_password,
    create_access_token,
    create_refresh_token,
)
from app.core.oauth import verify_oauth_token
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
    
    async def oauth_login(
        self,
        provider: str,
        id_token: str,
        name: Optional[str] = None,
        timezone: str = "UTC"
    ) -> Tuple[User, str, str]:
        """
        Login or create user via OAuth (Google/Apple).
        
        Args:
            provider: OAuth provider (google or apple)
            id_token: ID token from the provider
            name: User's name (optional, for first-time Apple users)
            timezone: User's timezone
            
        Returns:
            Tuple of (User, access_token, refresh_token)
        """
        # Verify the ID token with the provider
        user_info = await verify_oauth_token(provider, id_token)
        
        # Check if user exists by OAuth provider ID
        user = await self.repository.get_user_by_oauth_provider(
            provider,
            user_info["provider_user_id"]
        )
        
        if user:
            # Existing user - just login
            # Update avatar if it changed (for Google users)
            if user_info.get("avatar_url") and user_info["avatar_url"] != user.avatar_url:
                user.avatar_url = user_info["avatar_url"]
                await self.repository.db.commit()
                await self.repository.db.refresh(user)
        else:
            # Check if user exists with same email but different auth provider
            existing_user = await self.repository.get_user_by_email(user_info["email"])
            
            if existing_user:
                # Email exists with different auth method
                raise ConflictException(
                    f"An account with email {user_info['email']} already exists. "
                    f"Please login with {existing_user.auth_provider}."
                )
            
            # New user - create account
            user_name = name or user_info.get("name") or user_info["email"].split("@")[0]
            
            user = await self.repository.create_oauth_user(
                name=user_name,
                email=user_info["email"],
                provider=provider,
                provider_user_id=user_info["provider_user_id"],
                email_verified=user_info.get("email_verified", True),  # OAuth emails are typically verified
                avatar_url=user_info.get("avatar_url"),
                timezone=timezone
            )
        
        # Generate tokens
        access_token = create_access_token({"sub": str(user.id)})
        refresh_token_str = create_refresh_token({"sub": str(user.id)})
        
        # Store refresh token
        await self.repository.create_refresh_token(str(user.id), refresh_token_str)
        
        return user, access_token, refresh_token_str

