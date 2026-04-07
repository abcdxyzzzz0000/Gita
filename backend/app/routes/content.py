from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.schemas.content import ChapterResponse, ShlokaResponse
from app.services.content_service import get_all_chapters, get_shlokas_by_chapter, get_chapter_by_id

router = APIRouter(tags=["Content"])


@router.get("/chapters", response_model=list[ChapterResponse])
async def list_chapters(db: AsyncSession = Depends(get_db)):
    chapters = await get_all_chapters(db)
    return chapters


@router.get("/chapters/{chapter_id}/shlokas", response_model=list[ShlokaResponse])
async def list_shlokas(chapter_id: int, db: AsyncSession = Depends(get_db)):
    if chapter_id < 1 or chapter_id > 18:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Chapter ID must be between 1 and 18",
        )

    chapter = await get_chapter_by_id(db, chapter_id)
    if not chapter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chapter {chapter_id} not found",
        )

    shlokas = await get_shlokas_by_chapter(db, chapter_id)
    return shlokas
