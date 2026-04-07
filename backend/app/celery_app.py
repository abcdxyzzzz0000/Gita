"""Celery application for background tasks (daily wisdom, notifications)."""
from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

settings = get_settings()

celery_app = Celery(
    "gita",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

# Beat schedule - runs daily wisdom generation at midnight UTC
celery_app.conf.beat_schedule = {
    "generate-daily-wisdom": {
        "task": "app.tasks.generate_daily_wisdom_task",
        "schedule": crontab(hour=0, minute=5),  # 00:05 UTC daily
    },
    "send-daily-notifications": {
        "task": "app.tasks.send_daily_notifications_task",
        "schedule": crontab(minute="*/15"),  # Every 15 min, checks user prefs
    },
}
