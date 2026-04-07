"""Daily wisdom endpoints."""
from datetime import date, datetime

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.daily_wisdom_service import get_daily_wisdom, get_wisdom_history

router = APIRouter(tags=["Daily Wisdom"])


@router.get("/daily-wisdom")
async def daily_wisdom(
    target_date: str | None = Query(None, alias="date", description="Date in YYYY-MM-DD format"),
    db: AsyncSession = Depends(get_db),
):
    """
    Get the daily wisdom shloka. Same shloka shown to all users for a given day.
    Defaults to today (UTC). Pass ?date=YYYY-MM-DD for a specific date.
    """
    parsed_date = None
    if target_date:
        parsed_date = date.fromisoformat(target_date)

    wisdom = await get_daily_wisdom(db, parsed_date)

    if wisdom is None:
        return {"message": "No daily wisdom available. Seed shloka data first."}

    return wisdom


@router.get("/daily-wisdom/history")
async def daily_wisdom_history(
    limit: int = Query(7, ge=1, le=30),
    db: AsyncSession = Depends(get_db),
):
    """Get recent daily wisdom entries."""
    return await get_wisdom_history(db, limit)
