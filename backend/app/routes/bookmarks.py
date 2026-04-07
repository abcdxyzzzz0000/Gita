"""Bookmark CRUD endpoints."""
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.middleware.auth import get_current_user
from app.models.bookmark import Bookmark
from app.models.shloka import Shloka
from app.models.user import User

router = APIRouter(prefix="/bookmarks", tags=["Bookmarks"])


class BookmarkResponse:
    pass


from pydantic import BaseModel
from datetime import datetime


class BookmarkOut(BaseModel):
    id: UUID
    user_id: UUID
    chapter: int
    shloka_number: int
    created_at: datetime
    shloka: dict | None = None

    model_config = {"from_attributes": True}


class BookmarkCreate(BaseModel):
    chapter: int
    shloka_number: int


@router.get("", response_model=list[BookmarkOut])
async def list_bookmarks(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get all bookmarks for the current user, newest first."""
    result = await db.execute(
        select(Bookmark)
        .where(Bookmark.user_id == current_user.id)
        .order_by(Bookmark.created_at.desc())
    )
    bookmarks = list(result.scalars().all())

    # Enrich with shloka data
    response = []
    for bm in bookmarks:
        shloka_result = await db.execute(
            select(Shloka).where(
                Shloka.chapter == bm.chapter,
                Shloka.shloka_number == bm.shloka_number,
            )
        )
        shloka = shloka_result.scalar_one_or_none()
        shloka_data = None
        if shloka:
            shloka_data = {
                "id": str(shloka.id),
                "chapter": shloka.chapter,
                "shloka_number": shloka.shloka_number,
                "sanskrit_text": shloka.sanskrit_text,
                "transliteration": shloka.transliteration,
                "meaning": shloka.meaning,
            }
        response.append(
            BookmarkOut(
                id=bm.id,
                user_id=bm.user_id,
                chapter=bm.chapter,
                shloka_number=bm.shloka_number,
                created_at=bm.created_at,
                shloka=shloka_data,
            )
        )

    return response


@router.post("", response_model=BookmarkOut, status_code=status.HTTP_201_CREATED)
async def create_bookmark(
    payload: BookmarkCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a bookmark. Duplicate bookmarks are prevented."""
    # Check for duplicate
    existing = await db.execute(
        select(Bookmark).where(
            Bookmark.user_id == current_user.id,
            Bookmark.chapter == payload.chapter,
            Bookmark.shloka_number == payload.shloka_number,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Bookmark already exists",
        )

    bookmark = Bookmark(
        user_id=current_user.id,
        chapter=payload.chapter,
        shloka_number=payload.shloka_number,
    )
    db.add(bookmark)
    await db.flush()
    await db.refresh(bookmark)

    return BookmarkOut(
        id=bookmark.id,
        user_id=bookmark.user_id,
        chapter=bookmark.chapter,
        shloka_number=bookmark.shloka_number,
        created_at=bookmark.created_at,
    )


@router.delete("/{bookmark_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_bookmark(
    bookmark_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a bookmark by ID. Only the owner can delete."""
    result = await db.execute(
        select(Bookmark).where(
            Bookmark.id == bookmark_id,
            Bookmark.user_id == current_user.id,
        )
    )
    bookmark = result.scalar_one_or_none()
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found",
        )

    await db.delete(bookmark)


@router.delete(
    "/by-shloka/{chapter}/{shloka_number}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_bookmark_by_shloka(
    chapter: int,
    shloka_number: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a bookmark by chapter and shloka number (for toggle UI)."""
    result = await db.execute(
        select(Bookmark).where(
            Bookmark.user_id == current_user.id,
            Bookmark.chapter == chapter,
            Bookmark.shloka_number == shloka_number,
        )
    )
    bookmark = result.scalar_one_or_none()
    if not bookmark:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Bookmark not found",
        )

    await db.delete(bookmark)
