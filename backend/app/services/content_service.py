from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.chapter import Chapter
from app.models.shloka import Shloka


async def get_all_chapters(db: AsyncSession) -> list[Chapter]:
    result = await db.execute(
        select(Chapter).order_by(Chapter.id)
    )
    return list(result.scalars().all())


async def get_chapter_by_id(db: AsyncSession, chapter_id: int) -> Chapter | None:
    result = await db.execute(select(Chapter).where(Chapter.id == chapter_id))
    return result.scalar_one_or_none()


async def get_shlokas_by_chapter(db: AsyncSession, chapter_id: int) -> list[Shloka]:
    result = await db.execute(
        select(Shloka)
        .where(Shloka.chapter == chapter_id)
        .order_by(Shloka.shloka_number)
    )
    return list(result.scalars().all())


async def get_shloka_by_id(db: AsyncSession, shloka_id: str) -> Shloka | None:
    result = await db.execute(select(Shloka).where(Shloka.id == shloka_id))
    return result.scalar_one_or_none()
