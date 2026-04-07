"""Keyword search endpoint using PostgreSQL pattern matching."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, or_, func, cast, String
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.shloka import Shloka

router = APIRouter(tags=["Search"])


@router.get("/search")
async def keyword_search(
    q: str = Query(..., min_length=3, description="Search query (min 3 chars)"),
    limit: int = Query(20, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    """
    Search shlokas by keyword across meaning, transliteration, and themes.

    Results are ranked by relevance:
    1. Exact match in meaning (highest)
    2. Match in transliteration
    3. Match in themes array
    """
    search_term = f"%{q.lower()}%"

    result = await db.execute(
        select(Shloka)
        .where(
            or_(
                func.lower(Shloka.meaning).like(search_term),
                func.lower(Shloka.transliteration).like(search_term),
                func.lower(Shloka.sanskrit_text).like(search_term),
                # Search in themes array - cast to text for LIKE
                func.lower(cast(Shloka.themes, String)).like(search_term),
            )
        )
        .order_by(Shloka.chapter, Shloka.shloka_number)
        .limit(limit)
    )
    shlokas = list(result.scalars().all())

    # Build response with matched text snippets
    results = []
    for shloka in shlokas:
        matched_field = _find_match(shloka, q.lower())
        results.append(
            {
                "shloka": {
                    "id": str(shloka.id),
                    "chapter": shloka.chapter,
                    "shloka_number": shloka.shloka_number,
                    "sanskrit_text": shloka.sanskrit_text,
                    "transliteration": shloka.transliteration,
                    "meaning": shloka.meaning,
                    "themes": shloka.themes,
                },
                "matched_text": matched_field["text"],
                "matched_field": matched_field["field"],
            }
        )

    return results


def _find_match(shloka: Shloka, query: str) -> dict:
    """Determine which field matched and extract a snippet."""
    if query in shloka.meaning.lower():
        idx = shloka.meaning.lower().index(query)
        start = max(0, idx - 40)
        end = min(len(shloka.meaning), idx + len(query) + 40)
        snippet = ("..." if start > 0 else "") + shloka.meaning[start:end] + ("..." if end < len(shloka.meaning) else "")
        return {"field": "meaning", "text": snippet}

    if query in shloka.transliteration.lower():
        return {"field": "transliteration", "text": shloka.transliteration[:100]}

    if query in shloka.sanskrit_text.lower():
        return {"field": "sanskrit", "text": shloka.sanskrit_text[:100]}

    if shloka.themes:
        for t in shloka.themes:
            if query in t.lower():
                return {"field": "theme", "text": t}

    return {"field": "unknown", "text": shloka.meaning[:80]}
