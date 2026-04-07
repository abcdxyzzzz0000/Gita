import uuid
from sqlalchemy import Integer, Text, String, ForeignKey, ARRAY
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class Shloka(Base):
    __tablename__ = "shlokas"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    chapter: Mapped[int] = mapped_column(Integer, ForeignKey("chapters.id"), nullable=False)
    shloka_number: Mapped[int] = mapped_column(Integer, nullable=False)
    sanskrit_text: Mapped[str] = mapped_column(Text, nullable=False)
    transliteration: Mapped[str] = mapped_column(Text, nullable=False)
    meaning: Mapped[str] = mapped_column(Text, nullable=False)
    audio_file_path: Mapped[str | None] = mapped_column(String(500), nullable=True)
    themes: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    embedding_index: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    chapter_rel = relationship("Chapter", back_populates="shlokas")

    __table_args__ = (
        {"schema": None},
    )
