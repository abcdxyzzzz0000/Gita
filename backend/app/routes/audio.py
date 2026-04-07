"""Audio streaming endpoint for shloka chanting."""
import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.shloka import Shloka

router = APIRouter(tags=["Content"])

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "audio")


@router.get("/shlokas/{shloka_id}/audio")
async def stream_audio(shloka_id: str, db: AsyncSession = Depends(get_db)):
    """Stream audio file for a shloka. Returns 404 if no audio available."""
    # Look up shloka to get chapter/verse number for deterministic filename
    result = await db.execute(select(Shloka).where(Shloka.id == shloka_id))
    shloka = result.scalar_one_or_none()

    if not shloka:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Shloka not found",
        )

    # Try deterministic name (ch01_v001.mp3) and UUID-based name
    candidates = [
        f"ch{shloka.chapter:02d}_v{shloka.shloka_number:03d}",
        str(shloka.id),
    ]

    for name in candidates:
        for ext in ["mp3", "wav", "ogg"]:
            file_path = os.path.join(AUDIO_DIR, f"{name}.{ext}")
            if os.path.exists(file_path):
                media_type = {
                    "mp3": "audio/mpeg",
                    "wav": "audio/wav",
                    "ogg": "audio/ogg",
                }[ext]
                return FileResponse(file_path, media_type=media_type)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Audio file not available for this shloka",
    )
