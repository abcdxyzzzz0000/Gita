from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_optional_user
from app.models.user import User
from app.schemas.content import ShlokaDetailResponse
from app.services.content_service import get_shloka_by_id
from app.services.rag_service import generate_explanation, retrieve_similar_shlokas

router = APIRouter(tags=["Content", "RAG"])


@router.get("/shlokas/{shloka_id}", response_model=ShlokaDetailResponse)
async def get_shloka_detail(
    shloka_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User | None = Depends(get_optional_user),
):
    """Get detailed shloka view with AI-generated explanation."""
    shloka = await get_shloka_by_id(db, shloka_id)
    if not shloka:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shloka not found",
        )

    explanation = await generate_explanation(db, shloka)

    # Check bookmark status if authenticated
    is_bookmarked = False
    if current_user:
        from sqlalchemy import select
        from app.models.bookmark import Bookmark

        result = await db.execute(
            select(Bookmark).where(
                Bookmark.user_id == current_user.id,
                Bookmark.chapter == shloka.chapter,
                Bookmark.shloka_number == shloka.shloka_number,
            )
        )
        is_bookmarked = result.scalar_one_or_none() is not None

    return ShlokaDetailResponse(
        id=shloka.id,
        chapter=shloka.chapter,
        shloka_number=shloka.shloka_number,
        sanskrit_text=shloka.sanskrit_text,
        transliteration=shloka.transliteration,
        meaning=shloka.meaning,
        audio_file_path=shloka.audio_file_path,
        themes=shloka.themes,
        explanation=explanation,
        is_bookmarked=is_bookmarked,
    )


@router.get("/search/semantic")
async def semantic_search(
    q: str = Query(..., min_length=3, description="Search query"),
    top_k: int = Query(5, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """Semantic search for shlokas using FAISS vector similarity."""
    results = await retrieve_similar_shlokas(db, query=q, top_k=top_k, min_score=0.3)

    return [
        {
            "shloka": {
                "id": str(r["shloka"].id),
                "chapter": r["shloka"].chapter,
                "shloka_number": r["shloka"].shloka_number,
                "sanskrit_text": r["shloka"].sanskrit_text,
                "transliteration": r["shloka"].transliteration,
                "meaning": r["shloka"].meaning,
                "themes": r["shloka"].themes,
            },
            "relevance_score": r["relevance_score"],
        }
        for r in results
    ]
