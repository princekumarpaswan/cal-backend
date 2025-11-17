"""Router layer for FastAPI route definitions."""

from fastapi import FastAPI
from app.router import auth_router, user_router, family_router, event_router, task_router
from app.core.config import settings


def include_routers(app: FastAPI) -> None:
    """Include all application routers with their configurations."""
    
    app.include_router(
        auth_router.router,
        prefix=f"{settings.API_V1_PREFIX}/auth",
        tags=["Authentication"]
    )

    app.include_router(
        user_router.router,
        prefix=f"{settings.API_V1_PREFIX}/user",
        tags=["User Profile"]
    )

    app.include_router(
        family_router.router,
        prefix=f"{settings.API_V1_PREFIX}/family",
        tags=["Family Groups"]
    )

    app.include_router(
        event_router.router,
        prefix=f"{settings.API_V1_PREFIX}/events",
        tags=["Events"]
    )

    app.include_router(
        task_router.router,
        prefix=f"{settings.API_V1_PREFIX}/tasks",
        tags=["Tasks"]
    )
