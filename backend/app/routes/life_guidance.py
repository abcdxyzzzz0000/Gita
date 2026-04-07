"""Life guidance endpoints - recommend shlokas for life problems."""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.services.rag_service import retrieve_similar_shlokas

router = APIRouter(prefix="/life-guidance", tags=["Life Guidance"])

PROBLEM_CATEGORIES = [
    {"id": "stress", "title": "Stress & Anxiety", "description": "Finding inner peace and calm amidst chaos", "icon": "emoticon-sad-outline"},
    {"id": "fear", "title": "Fear & Worry", "description": "Overcoming fear and finding courage", "icon": "shield-alert-outline"},
    {"id": "confusion", "title": "Confusion & Doubt", "description": "Finding clarity when everything seems unclear", "icon": "help-circle-outline"},
    {"id": "anger", "title": "Anger & Frustration", "description": "Managing anger and finding patience", "icon": "fire"},
    {"id": "attachment", "title": "Attachment & Loss", "description": "Dealing with attachment and letting go", "icon": "heart-broken-outline"},
    {"id": "purpose", "title": "Finding Purpose", "description": "Discovering your path and life meaning", "icon": "compass-outline"},
    {"id": "motivation", "title": "Lack of Motivation", "description": "Rekindling your drive and determination", "icon": "lightning-bolt-outline"},
    {"id": "relationships", "title": "Relationship Struggles", "description": "Navigating bonds with compassion", "icon": "account-group-outline"},
]

PROBLEM_KEYWORDS = {
    "stress": "peace calm equanimity tranquility serenity stillness mind",
    "fear": "courage fearlessness strength confidence bravery warrior",
    "confusion": "clarity wisdom understanding knowledge discernment truth",
    "anger": "patience forgiveness compassion control self-discipline calm",
    "attachment": "detachment renunciation letting go impermanence acceptance",
    "purpose": "dharma duty purpose meaning path action calling",
    "motivation": "action effort perseverance determination energy work",
    "relationships": "love compassion understanding harmony devotion unity",
}


@router.get("/problems")
async def list_problems():
    """Get all life guidance problem categories."""
    return PROBLEM_CATEGORIES


@router.get("/recommendations")
async def get_recommendations(
    problem: str = Query(..., description="Problem category ID"),
    top_k: int = Query(5, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    """Get shloka recommendations for a life problem using RAG semantic search."""
    query = PROBLEM_KEYWORDS.get(problem)
    if not query:
        return {"error": f"Unknown problem category: {problem}", "available": [p["id"] for p in PROBLEM_CATEGORIES]}

    results = await retrieve_similar_shlokas(db, query=query, top_k=top_k, min_score=0.2)

    recommendations = []
    for r in results:
        shloka = r["shloka"]
        # Build a practical explanation focused on the problem
        problem_title = next((p["title"] for p in PROBLEM_CATEGORIES if p["id"] == problem), problem)

        explanation = (
            f"This verse from Chapter {shloka.chapter} offers guidance on {problem_title.lower()}. "
            f"{shloka.meaning}"
        )

        # Try to generate a richer explanation via RAG if available
        try:
            from app.services.rag_service import generate_explanation
            explanation = await generate_explanation(db, shloka)
        except Exception:
            pass

        recommendations.append({
            "shloka": {
                "id": str(shloka.id),
                "chapter": shloka.chapter,
                "shloka_number": shloka.shloka_number,
                "sanskrit_text": shloka.sanskrit_text,
                "transliteration": shloka.transliteration,
                "meaning": shloka.meaning,
                "themes": shloka.themes,
            },
            "explanation": explanation,
            "relevance_score": round(r["relevance_score"], 3),
        })

    return recommendations
