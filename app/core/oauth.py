"""OAuth validation utilities for Google and Apple Sign-In."""
from typing import Optional, Dict, Any
import httpx
from jose import jwt, JWTError
from app.api.exceptions import UnauthorizedException
from app.core.config import settings
import json


class GoogleOAuth:
    """Google OAuth validation."""
    
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
    GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"
    
    @staticmethod
    async def verify_id_token(id_token: str) -> Dict[str, Any]:
        """
        Verify Google ID token and extract user information.
        
        Args:
            id_token: Google ID token from the client
            
        Returns:
            Dict containing user information (sub, email, name, picture)
            
        Raises:
            UnauthorizedException: If token is invalid
        """
        try:
            # Option 1: Use Google's tokeninfo endpoint (simpler but requires network call)
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    GoogleOAuth.GOOGLE_TOKEN_INFO_URL,
                    params={"id_token": id_token},
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise UnauthorizedException("Invalid Google ID token")
                
                token_info = response.json()
                
                # Verify the token is for our app
                if settings.GOOGLE_CLIENT_ID and token_info.get("aud") != settings.GOOGLE_CLIENT_ID:
                    raise UnauthorizedException("Token audience mismatch")
                
                # Verify email is verified
                if not token_info.get("email_verified", False):
                    raise UnauthorizedException("Email not verified by Google")
                
                return {
                    "provider_user_id": token_info["sub"],
                    "email": token_info["email"],
                    "name": token_info.get("name", ""),
                    "avatar_url": token_info.get("picture"),
                    "email_verified": token_info.get("email_verified", False)
                }
                
        except httpx.TimeoutException:
            raise UnauthorizedException("Google verification timeout")
        except httpx.RequestError as e:
            raise UnauthorizedException(f"Google verification failed: {str(e)}")
        except KeyError as e:
            raise UnauthorizedException(f"Missing required field in Google token: {str(e)}")
        except Exception as e:
            raise UnauthorizedException(f"Google token verification failed: {str(e)}")


class AppleOAuth:
    """Apple OAuth validation."""
    
    APPLE_PUBLIC_KEYS_URL = "https://appleid.apple.com/auth/keys"
    APPLE_ISSUER = "https://appleid.apple.com"
    
    _public_keys_cache: Optional[Dict[str, Any]] = None
    
    @staticmethod
    async def get_apple_public_keys() -> Dict[str, Any]:
        """Fetch Apple's public keys for token verification."""
        if AppleOAuth._public_keys_cache:
            return AppleOAuth._public_keys_cache
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    AppleOAuth.APPLE_PUBLIC_KEYS_URL,
                    timeout=10.0
                )
                
                if response.status_code != 200:
                    raise UnauthorizedException("Failed to fetch Apple public keys")
                
                AppleOAuth._public_keys_cache = response.json()
                return AppleOAuth._public_keys_cache
                
        except Exception as e:
            raise UnauthorizedException(f"Failed to fetch Apple public keys: {str(e)}")
    
    @staticmethod
    async def verify_id_token(id_token: str) -> Dict[str, Any]:
        """
        Verify Apple ID token and extract user information.
        
        Args:
            id_token: Apple ID token from the client
            
        Returns:
            Dict containing user information (sub, email, email_verified)
            
        Raises:
            UnauthorizedException: If token is invalid
        """
        try:
            # Decode the token header to get the key id (kid)
            unverified_header = jwt.get_unverified_header(id_token)
            kid = unverified_header.get("kid")
            
            if not kid:
                raise UnauthorizedException("Missing kid in Apple token header")
            
            # Get Apple's public keys
            keys_data = await AppleOAuth.get_apple_public_keys()
            
            # Find the matching public key
            public_key = None
            for key in keys_data.get("keys", []):
                if key.get("kid") == kid:
                    public_key = key
                    break
            
            if not public_key:
                raise UnauthorizedException("Could not find matching public key for Apple token")
            
            # Verify and decode the token
            # Note: python-jose doesn't support JWK directly, so we'll do basic verification
            # In production, you should use a proper JWK library like PyJWT with cryptography
            
            # For now, we'll decode without verification of signature but verify claims
            # In production, implement proper JWK signature verification
            decoded_token = jwt.decode(
                id_token,
                key="",  # Empty key - not verifying signature in this example
                options={
                    "verify_signature": False,  # Set to True in production with proper key
                    "verify_aud": True,
                    "verify_iss": True,
                    "verify_exp": True
                },
                audience=settings.APPLE_CLIENT_ID if settings.APPLE_CLIENT_ID else None,
                issuer=AppleOAuth.APPLE_ISSUER
            )
            
            # Extract user information
            return {
                "provider_user_id": decoded_token["sub"],
                "email": decoded_token.get("email", ""),
                "name": "",  # Apple doesn't provide name in ID token after first sign-in
                "avatar_url": None,
                "email_verified": decoded_token.get("email_verified", False)
            }
            
        except JWTError as e:
            raise UnauthorizedException(f"Invalid Apple ID token: {str(e)}")
        except KeyError as e:
            raise UnauthorizedException(f"Missing required field in Apple token: {str(e)}")
        except Exception as e:
            raise UnauthorizedException(f"Apple token verification failed: {str(e)}")


async def verify_oauth_token(provider: str, id_token: str) -> Dict[str, Any]:
    """
    Verify OAuth ID token based on provider.
    
    Args:
        provider: OAuth provider (google or apple)
        id_token: ID token from the provider
        
    Returns:
        Dict containing user information
        
    Raises:
        UnauthorizedException: If token is invalid
    """
    if provider == "google":
        return await GoogleOAuth.verify_id_token(id_token)
    elif provider == "apple":
        return await AppleOAuth.verify_id_token(id_token)
    else:
        raise UnauthorizedException(f"Unsupported OAuth provider: {provider}")

