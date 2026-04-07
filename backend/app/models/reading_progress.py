import uuid
from datetime import datetime
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class ReadingProgress(Base):
    __tablename__ = "reading_progress"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    chapter: Mapped[int] = mapped_column(Integer, nullable=False)
    shloka_number: Mapped[int] = mapped_column(Integer, nullable=False)
    last_read_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user = relationship("User", back_populates="reading_progress")

    __table_args__ = (
        UniqueConstraint("user_id", "chapter", "shloka_number", name="unique_user_progress"),
    )
