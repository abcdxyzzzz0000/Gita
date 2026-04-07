"""Audio streaming endpoint for shloka chanting."""
import os

from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse

router = APIRouter(tags=["Content"])

AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "audio")


@router.get("/shlokas/{shloka_id}/audio")
async def stream_audio(shloka_id: str):
    """Stream audio file for a shloka. Returns 404 if no audio available."""
    # Check multiple possible file names
    for ext in ["mp3", "wav", "ogg"]:
        file_path = os.path.join(AUDIO_DIR, f"{shloka_id}.{ext}")
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
