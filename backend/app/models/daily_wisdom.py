import uuid
from datetime import datetime, date
from sqlalchemy import Integer, Text, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base


class DailyWisdom(Base):
    __tablename__ = "daily_wisdom"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    date: Mapped[date] = mapped_column(Date, unique=True, nullable=False, index=True)
    chapter: Mapped[int] = mapped_column(Integer, nullable=False)
    shloka_number: Mapped[int] = mapped_column(Integer, nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
