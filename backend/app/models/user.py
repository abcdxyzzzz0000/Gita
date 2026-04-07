import uuid
from datetime import datetime, time
from sqlalchemy import String, Boolean, DateTime, Time
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    hashed_password: Mapped[str | None] = mapped_column(String(255), nullable=True)
    oauth_provider: Mapped[str | None] = mapped_column(String(50), nullable=True)
    oauth_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    last_login: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    notification_enabled: Mapped[bool] = mapped_column(Boolean, default=True)
    notification_time: Mapped[time] = mapped_column(Time, default=time(8, 0))

    bookmarks = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    reading_progress = relationship("ReadingProgress", back_populates="user", cascade="all, delete-orphan")
