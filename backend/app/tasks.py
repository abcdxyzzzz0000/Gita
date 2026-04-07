"""Celery tasks for daily wisdom generation and notifications."""
import asyncio
from datetime import datetime, timezone, time

from app.celery_app import celery_app
from app.database import async_session
from app.services.daily_wisdom_service import get_daily_wisdom

from sqlalchemy import select
from app.models.user import User


def _run_async(coro):
    """Run an async function from a sync Celery task."""
    loop = asyncio.new_event_loop()
    try:
        return loop.run_until_complete(coro)
    finally:
        loop.close()


@celery_app.task(name="app.tasks.generate_daily_wisdom_task")
def generate_daily_wisdom_task():
    """Generate daily wisdom for today. Runs at 00:05 UTC via Celery Beat."""

    async def _generate():
        async with async_session() as db:
            wisdom = await get_daily_wisdom(db)
            await db.commit()
            if wisdom:
                return f"Daily wisdom generated: Ch.{wisdom['chapter']} V.{wisdom['shloka_number']}"
            return "No shlokas available for daily wisdom"

    return _run_async(_generate())


@celery_app.task(name="app.tasks.send_daily_notifications_task")
def send_daily_notifications_task():
    """
    Check which users should receive notifications now and send them.
    Runs every 15 minutes. Matches users whose notification_time falls
    within the current 15-minute window.
    """

    async def _send():
        now = datetime.now(timezone.utc)
        current_hour = now.hour
        current_minute = (now.minute // 15) * 15  # Round to 15-min block

        async with async_session() as db:
            # Find users whose preferred notification time is in this window
            result = await db.execute(
                select(User).where(
                    User.notification_enabled == True,
                    User.notification_time >= time(current_hour, current_minute),
                    User.notification_time < time(
                        current_hour if current_minute < 45 else (current_hour + 1) % 24,
                        (current_minute + 15) % 60,
                    ),
                )
            )
            users = list(result.scalars().all())

            # Get today's wisdom
            wisdom = await get_daily_wisdom(db)
            await db.commit()

            if not wisdom:
                return "No daily wisdom available"

            # Phase 1: Log notifications (Phase 2 will use Firebase)
            for user in users:
                _log_notification(user, wisdom)

            return f"Processed {len(users)} notification(s)"

    return _run_async(_send())


def _log_notification(user: User, wisdom: dict):
    """Phase 1: Log the notification. Phase 2: Send via Firebase Cloud Messaging."""
    print(
        f"[NOTIFICATION] User {user.email}: "
        f"Daily Wisdom - Ch.{wisdom['chapter']} V.{wisdom['shloka_number']} - "
        f"{wisdom['shloka']['meaning'][:60]}..."
    )
