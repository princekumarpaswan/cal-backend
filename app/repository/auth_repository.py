"""Repository for authentication-related database operations."""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
from typing import Optional
from app.models.models import User, RefreshToken
from app.core.config import settings


class AuthRepository:
    """Repository for authentication operations."""
    
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email."""
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()
    
    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get user by ID."""
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()
    
    async def get_user_by_oauth_provider(self, provider: str, provider_user_id: str) -> Optional[User]:
        """Get user by OAuth provider and provider user ID."""
        result = await self.db.execute(
            select(User).where(
                User.auth_provider == provider,
                User.oauth_provider_id == provider_user_id
            )
        )
        return result.scalar_one_or_none()
    
    async def create_user(self, name: str, email: str, password_hash: str) -> User:
        """Create a new user."""
        new_user = User(
            name=name,
            email=email,
            password_hash=password_hash,
            email_verified=False,
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def create_oauth_user(
        self,
        name: str,
        email: str,
        provider: str,
        provider_user_id: str,
        email_verified: bool = False,
        avatar_url: Optional[str] = None,
        timezone: str = "UTC"
    ) -> User:
        """Create a new user from OAuth provider."""
        new_user = User(
            name=name,
            email=email,
            password_hash=None,  # No password for OAuth users
            email_verified=email_verified,
            auth_provider=provider,
            oauth_provider_id=provider_user_id,
            avatar_url=avatar_url,
            timezone=timezone
        )
        self.db.add(new_user)
        await self.db.commit()
        await self.db.refresh(new_user)
        return new_user
    
    async def get_refresh_token(self, token: str) -> Optional[RefreshToken]:
        """Get refresh token by token string."""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        return result.scalar_one_or_none()
    
    async def create_refresh_token(self, user_id: str, token: str) -> RefreshToken:
        """Create a new refresh token."""
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        )
        self.db.add(refresh_token)
        await self.db.commit()
        await self.db.refresh(refresh_token)
        return refresh_token
    
    async def delete_refresh_token(self, token: str, user_id: str) -> bool:
        """Delete a refresh token."""
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token == token,
                RefreshToken.user_id == user_id
            )
        )
        refresh_token = result.scalar_one_or_none()
        
        if refresh_token:
            await self.db.delete(refresh_token)
            await self.db.commit()
            return True
        return False
    
    async def delete_refresh_token_by_token(self, token: str) -> bool:
        """Delete a refresh token by token string."""
        result = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token == token)
        )
        refresh_token = result.scalar_one_or_none()
        
        if refresh_token:
            await self.db.delete(refresh_token)
            await self.db.commit()
            return True
        return False

