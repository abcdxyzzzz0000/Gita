"""Reading progress tracking endpoints."""
from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import select, func, distinct
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.reading_progress import ReadingProgress
from app.models.user import User

router = APIRouter(tags=["Progress"])


class ProgressRecord(BaseModel):
    chapter: int
    shloka_number: int


@router.post("/progress", status_code=201)
async def record_progress(
    payload: ProgressRecord,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Record that a user has read a shloka. Upserts on (user, chapter, shloka)."""
    result = await db.execute(
        select(ReadingProgress).where(
            ReadingProgress.user_id == current_user.id,
            ReadingProgress.chapter == payload.chapter,
            ReadingProgress.shloka_number == payload.shloka_number,
        )
    )
    existing = result.scalar_one_or_none()

    if existing:
        existing.last_read_at = datetime.now(timezone.utc)
    else:
        db.add(
            ReadingProgress(
                user_id=current_user.id,
                chapter=payload.chapter,
                shloka_number=payload.shloka_number,
            )
        )

    await db.flush()
    return {"status": "recorded"}


@router.get("/progress")
async def get_progress(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get user's reading progress summary."""
    # Recent reads
    recent_result = await db.execute(
        select(ReadingProgress)
        .where(ReadingProgress.user_id == current_user.id)
        .order_by(ReadingProgress.last_read_at.desc())
        .limit(10)
    )
    recent = [
        {
            "chapter": r.chapter,
            "shloka_number": r.shloka_number,
            "last_read_at": r.last_read_at.isoformat(),
        }
        for r in recent_result.scalars().all()
    ]

    # Per-chapter progress
    chapter_counts = {}
    all_result = await db.execute(
        select(ReadingProgress.chapter, func.count())
        .where(ReadingProgress.user_id == current_user.id)
        .group_by(ReadingProgress.chapter)
    )
    for chapter, count in all_result.all():
        chapter_counts[chapter] = count

    # Total shlokas per chapter (from architecture: known counts)
    chapter_totals = {
        1: 47, 2: 72, 3: 43, 4: 42, 5: 29, 6: 47, 7: 30, 8: 28, 9: 34,
        10: 42, 11: 55, 12: 20, 13: 35, 14: 27, 15: 20, 16: 24, 17: 28, 18: 78,
    }

    chapter_progress = []
    for ch_id in range(1, 19):
        read = chapter_counts.get(ch_id, 0)
        total = chapter_totals.get(ch_id, 0)
        chapter_progress.append({
            "chapter": ch_id,
            "read": read,
            "total": total,
            "percentage": round((read / total * 100) if total > 0 else 0, 1),
        })

    # Streak (consecutive days)
    days_result = await db.execute(
        select(distinct(func.date(ReadingProgress.last_read_at)))
        .where(ReadingProgress.user_id == current_user.id)
        .order_by(func.date(ReadingProgress.last_read_at).desc())
    )
    dates = [row[0] for row in days_result.all()]

    streak = 0
    if dates:
        from datetime import timedelta
        today = datetime.now(timezone.utc).date()
        expected = today
        for d in dates:
            if d == expected:
                streak += 1
                expected -= timedelta(days=1)
            elif d < expected:
                break

    total_read = sum(chapter_counts.values())

    return {
        "recent": recent,
        "chapter_progress": chapter_progress,
        "total_read": total_read,
        "streak": streak,
        "last_read": recent[0] if recent else None,
    }
