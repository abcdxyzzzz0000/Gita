# Daily Wisdom & Notifications Module - Sub-Architecture

## Module-Level Architecture Overview

The Daily Wisdom & Notifications Module uses Celery for scheduled task execution, with Redis as the message broker. It implements a two-phase approach: daily wisdom selection (scheduled task) and notification delivery (batch processing).

```
┌────────────────────────────────────────────────────────┐
│                   API Layer                            │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │ Daily Wisdom │  │   Settings   │                   │
│  │  Endpoints   │  │  Endpoints   │                   │
│  └──────────────┘  └──────────────┘                   │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                 Service Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │Daily Wisdom  │  │ Notification │  │  Settings   │ │
│  │   Service    │  │   Service    │  │  Service    │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│              Background Tasks (Celery)                 │
│  ┌──────────────┐  ┌──────────────┐                   │
│  │Select Daily  │  │Send Batch    │                   │
│  │   Wisdom     │  │Notifications │                   │
│  └──────────────┘  └──────────────┘                   │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                  Data Layer                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │PostgreSQL│  │  Redis   │  │   FCM    │           │
│  │ Database │  │  Broker  │  │(Future)  │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└────────────────────────────────────────────────────────┘
```

## Internal Components & Responsibilities

### 1. Daily Wisdom Router (`daily_wisdom_router.py`)
**Endpoints**:
- `GET /api/daily-wisdom` - Get today's or historical wisdom
- `GET /api/daily-wisdom/calendar` - Get available dates

### 2. Settings Router (`settings_router.py`)
**Endpoints**:
- `GET /api/settings` - Get user settings
- `PUT /api/settings` - Update notification preferences

### 3. Daily Wisdom Service (`daily_wisdom_service.py`)
**Functions**:
- `get_daily_wisdom(date)` - Retrieve wisdom for date
- `select_next_shloka()` - Choose next shloka (sequential/curated)
- `generate_wisdom_explanation(shloka)` - Create daily explanation

### 4. Notification Service (`notification_service.py`)
**Functions**:
- `send_notification(user_id, shloka)` - Send single notification
- `batch_send_notifications(users, shloka)` - Batch processing
- `register_device_token(user_id, token)` - Store FCM token

### 5. Settings Service (`settings_service.py`)
**Functions**:
- `get_user_settings(user_id)` - Retrieve settings
- `update_notification_settings(user_id, enabled, time)` - Update preferences

### 6. Celery Tasks (`celery_tasks.py`)
**Tasks**:
- `select_daily_wisdom_task()` - Scheduled at 3 AM UTC daily
- `send_daily_notifications_task()` - Scheduled hourly, processes users by timezone

### 7. Daily Wisdom Repository (`daily_wisdom_repository.py`)
**Functions**:
- `get_wisdom_by_date(date)` - SELECT daily wisdom
- `create_wisdom(date, chapter, shloka_number, explanation)` - INSERT
- `get_last_selected_shloka()` - For sequential selection

## Data Flow

### Daily Wisdom Selection (Scheduled Task)

```
1. Celery Beat → schedule_daily_wisdom_task() at 3:00 AM UTC
2. DailyWisdomService.select_next_shloka()
   - Get last selected shloka from database
   - Increment to next shloka (sequential)
   - If end of chapter, move to next chapter
   - If end of Gita, restart from Chapter 1
3. RAGService.generate_daily_wisdom_explanation(shloka)
   - Generate 100-150 word explanation
   - Focus on daily practical application
4. DailyWisdomRepository.create_wisdom(today, chapter, shloka_number, explanation)
   - INSERT into daily_wisdom table
5. Cache in Redis: SET daily_wisdom:today
6. Task complete
```

### Notification Delivery (Hourly Batch)

```
1. Celery Beat → send_daily_notifications_task() every hour
2. Calculate current hour in each timezone (0-23)
3. UserRepository.get_users_for_notification(hour)
   - SELECT users WHERE notification_enabled=true 
     AND notification_time BETWEEN hour:00 AND hour:59
4. DailyWisdomService.get_daily_wisdom(today)
5. For each batch of 1000 users:
   a. NotificationService.batch_send_notifications(users, shloka)
   b. For each user:
      - Build notification payload
      - Send via FCM (Phase 2) or local notification (Phase 1)
      - Log delivery status
6. Update last_notification_sent timestamp
7. Task complete
```

### User Settings Update

```
1. Client → PUT /api/settings {notificationEnabled: true, notificationTime: "09:30"}
2. SettingsRouter → AuthMiddleware (validate token)
3. SettingsRouter → SettingsService.update_notification_settings(user_id, true, "09:30")
4. SettingsService → UserRepository.update_user(user_id, {notification_enabled, notification_time})
5. UserRepository → PostgreSQL UPDATE
6. SettingsService → CacheService.invalidate_cache('user_settings:{user_id}')
7. Return updated settings
```

## Database Schema / Tables Involved

### Daily Wisdom Table

```sql
CREATE TABLE daily_wisdom (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE UNIQUE NOT NULL,
    chapter INTEGER NOT NULL,
    shloka_number INTEGER NOT NULL,
    explanation TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_daily_wisdom_date ON daily_wisdom(date DESC);
```

### Users Table (Notification Fields)

```sql
-- Relevant columns from users table
notification_enabled BOOLEAN DEFAULT true,
notification_time TIME DEFAULT '08:00:00',
notification_token VARCHAR(500), -- FCM token (Phase 2)
last_notification_sent TIMESTAMP WITH TIME ZONE
```

## External Services Used

### Celery + Redis

**Purpose**: Task scheduling and execution

**Configuration**:
```python
# celery_config.py
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'
timezone = 'UTC'
beat_schedule = {
    'select-daily-wisdom': {
        'task': 'tasks.select_daily_wisdom_task',
        'schedule': crontab(hour=3, minute=0),  # 3 AM UTC daily
    },
    'send-notifications': {
        'task': 'tasks.send_daily_notifications_task',
        'schedule': crontab(minute=0),  # Every hour
    },
}
```

**Monitoring**:
- Task success/failure rates
- Task execution duration
- Queue length

### Firebase Cloud Messaging (Phase 2)

**Purpose**: Push notifications to mobile devices

**API Endpoint**:
```
POST https://fcm.googleapis.com/v1/projects/{project-id}/messages:send
Authorization: Bearer {access-token}
```

**Payload**:
```json
{
  "message": {
    "token": "device-token",
    "notification": {
      "title": "Daily Gita Wisdom",
      "body": "कर्मण्येवाधिकारस्ते... (Tap to read more)"
    },
    "data": {
      "type": "daily_wisdom",
      "date": "2026-01-17",
      "shloka_id": "uuid"
    }
  }
}
```

## Security Considerations

- Notification tokens encrypted in database
- Rate limiting on settings updates
- Validate notification time format
- Prevent notification spam (max 1 per day per user)
- Secure FCM credentials in environment variables

## Scalability & Failure Handling

### Scalability
- Batch notification processing: 10,000 users/minute
- Celery workers: 4 concurrent workers
- Redis queue capacity: 100,000 tasks
- Database connection pooling

### Failure Handling
- Daily wisdom generation failure: Use fallback shloka
- Notification delivery failure: Retry 3 times, then skip
- Celery worker crash: Task automatically retried
- Redis unavailable: Tasks queued in memory temporarily

## Deployment Considerations

### Environment Variables
```bash
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
FCM_PROJECT_ID=bhagavad-gita-app
FCM_CREDENTIALS_PATH=/app/config/fcm-credentials.json
DAILY_WISDOM_GENERATION_HOUR=3
```

### Docker Configuration
```yaml
services:
  celery_worker:
    command: celery -A app.celery worker --loglevel=info
    depends_on:
      - redis
      - postgres
  
  celery_beat:
    command: celery -A app.celery beat --loglevel=info
    depends_on:
      - redis
```

### Monitoring
```python
metrics = {
    "daily_wisdom_generation_duration": Histogram,
    "notification_delivery_rate": Gauge,
    "notification_failures": Counter,
    "celery_task_duration": Histogram
}
```
