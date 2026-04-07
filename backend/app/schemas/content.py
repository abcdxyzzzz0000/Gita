from uuid import UUID
from pydantic import BaseModel


class ChapterResponse(BaseModel):
    id: int
    title: str
    sanskrit_name: str
    description: str
    shloka_count: int

    model_config = {"from_attributes": True}


class ShlokaResponse(BaseModel):
    id: UUID
    chapter: int
    shloka_number: int
    sanskrit_text: str
    transliteration: str
    meaning: str
    audio_file_path: str | None = None
    themes: list[str] | None = None

    model_config = {"from_attributes": True}


class ShlokaDetailResponse(ShlokaResponse):
    explanation: str | None = None
    is_bookmarked: bool = False
