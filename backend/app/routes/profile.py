"""Profile and statistics endpoints."""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.models.bookmark import Bookmark
from app.models.reading_progress import ReadingProgress
from app.schemas.auth import UserResponse

router = APIRouter(tags=["Profile"])


@router.get("/profile")
async def get_profile(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user profile with learning statistics."""
    # Bookmark count
    bm_result = await db.execute(
        select(func.count()).where(Bookmark.user_id == current_user.id)
    )
    bookmark_count = bm_result.scalar() or 0

    # Shlokas read
    read_result = await db.execute(
        select(func.count()).where(ReadingProgress.user_id == current_user.id)
    )
    shlokas_read = read_result.scalar() or 0

    # Chapters completed (all shlokas in a chapter read)
    chapters_result = await db.execute(
        select(func.count(distinct(ReadingProgress.chapter))).where(
            ReadingProgress.user_id == current_user.id
        )
    )
    chapters_started = chapters_result.scalar() or 0

    # Days active (distinct dates of reading)
    days_result = await db.execute(
        select(
            func.count(distinct(func.date(ReadingProgress.last_read_at)))
        ).where(ReadingProgress.user_id == current_user.id)
    )
    days_active = days_result.scalar() or 0

    return {
        "user": UserResponse.from_orm_user(current_user),
        "stats": {
            "bookmark_count": bookmark_count,
            "shlokas_read": shlokas_read,
            "chapters_completed": chapters_started,
            "days_active": days_active,
        },
    }
