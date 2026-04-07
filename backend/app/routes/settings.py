"""User settings endpoints (notification preferences)."""
from datetime import time

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User

router = APIRouter(prefix="/settings", tags=["Settings"])


class SettingsResponse(BaseModel):
    notification_enabled: bool
    notification_time: str  # HH:MM


class SettingsUpdate(BaseModel):
    notification_enabled: bool | None = None
    notification_time: str | None = None  # HH:MM format


@router.get("", response_model=SettingsResponse)
async def get_settings(
    current_user: User = Depends(get_current_user),
):
    return SettingsResponse(
        notification_enabled=current_user.notification_enabled,
        notification_time=current_user.notification_time.strftime("%H:%M")
        if current_user.notification_time
        else "08:00",
    )


@router.put("", response_model=SettingsResponse)
async def update_settings(
    payload: SettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if payload.notification_enabled is not None:
        current_user.notification_enabled = payload.notification_enabled

    if payload.notification_time is not None:
        parts = payload.notification_time.split(":")
        current_user.notification_time = time(int(parts[0]), int(parts[1]))

    await db.flush()
    await db.refresh(current_user)

    return SettingsResponse(
        notification_enabled=current_user.notification_enabled,
        notification_time=current_user.notification_time.strftime("%H:%M")
        if current_user.notification_time
        else "08:00",
    )
