"""Daily wisdom selection and generation service."""
import random
from datetime import date, datetime, timezone

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.daily_wisdom import DailyWisdom
from app.models.shloka import Shloka


async def get_daily_wisdom(db: AsyncSession, target_date: date | None = None) -> dict | None:
    """Get the daily wisdom for a given date (defaults to today UTC)."""
    if target_date is None:
        target_date = datetime.now(timezone.utc).date()

    result = await db.execute(
        select(DailyWisdom).where(DailyWisdom.date == target_date)
    )
    wisdom = result.scalar_one_or_none()

    if wisdom is None:
        # Auto-generate if not exists
        wisdom = await _generate_daily_wisdom(db, target_date)

    if wisdom is None:
        return None

    # Fetch the full shloka
    shloka_result = await db.execute(
        select(Shloka).where(
            Shloka.chapter == wisdom.chapter,
            Shloka.shloka_number == wisdom.shloka_number,
        )
    )
    shloka = shloka_result.scalar_one_or_none()

    return {
        "id": str(wisdom.id),
        "date": str(wisdom.date),
        "chapter": wisdom.chapter,
        "shloka_number": wisdom.shloka_number,
        "explanation": wisdom.explanation,
        "shloka": {
            "id": str(shloka.id) if shloka else None,
            "chapter": wisdom.chapter,
            "shloka_number": wisdom.shloka_number,
            "sanskrit_text": shloka.sanskrit_text if shloka else "",
            "transliteration": shloka.transliteration if shloka else "",
            "meaning": shloka.meaning if shloka else "",
            "themes": shloka.themes if shloka else [],
        },
    }


async def _generate_daily_wisdom(db: AsyncSession, target_date: date) -> DailyWisdom | None:
    """Select a shloka for daily wisdom and generate an explanation."""
    # Get total shloka count
    count_result = await db.execute(select(func.count()).select_from(Shloka))
    total = count_result.scalar() or 0
    if total == 0:
        return None

    # Deterministic selection based on date (so all users see the same one)
    day_seed = target_date.toordinal()
    random.seed(day_seed)

    # Get all shlokas and pick one
    all_result = await db.execute(
        select(Shloka).order_by(Shloka.chapter, Shloka.shloka_number)
    )
    all_shlokas = list(all_result.scalars().all())
    selected = all_shlokas[day_seed % len(all_shlokas)]

    # Generate a daily-focused explanation
    explanation = await _generate_daily_explanation(db, selected)

    wisdom = DailyWisdom(
        date=target_date,
        chapter=selected.chapter,
        shloka_number=selected.shloka_number,
        explanation=explanation,
    )
    db.add(wisdom)
    await db.flush()
    await db.refresh(wisdom)
    return wisdom


async def _generate_daily_explanation(db: AsyncSession, shloka: Shloka) -> str:
    """Generate a daily-focused explanation (100-150 words, inspirational tone)."""
    try:
        from app.services.rag_service import generate_explanation
        explanation = await generate_explanation(db, shloka, use_cache=False)
        return explanation
    except Exception:
        return (
            f"Today's wisdom comes from Chapter {shloka.chapter}, Verse {shloka.shloka_number}: "
            f"{shloka.meaning}\n\n"
            "Take a moment today to reflect on how this teaching applies to your life. "
            "The Gita reminds us that true wisdom comes through daily practice and reflection."
        )


async def get_wisdom_history(db: AsyncSession, limit: int = 7) -> list[dict]:
    """Get recent daily wisdom entries."""
    result = await db.execute(
        select(DailyWisdom).order_by(DailyWisdom.date.desc()).limit(limit)
    )
    entries = list(result.scalars().all())

    history = []
    for w in entries:
        shloka_result = await db.execute(
            select(Shloka).where(
                Shloka.chapter == w.chapter,
                Shloka.shloka_number == w.shloka_number,
            )
        )
        shloka = shloka_result.scalar_one_or_none()
        history.append({
            "id": str(w.id),
            "date": str(w.date),
            "chapter": w.chapter,
            "shloka_number": w.shloka_number,
            "explanation": w.explanation[:100] + "..." if len(w.explanation) > 100 else w.explanation,
            "shloka_meaning": shloka.meaning[:80] + "..." if shloka and len(shloka.meaning) > 80 else (shloka.meaning if shloka else ""),
        })

    return history
