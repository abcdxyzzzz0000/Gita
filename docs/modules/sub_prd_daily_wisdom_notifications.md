# Daily Wisdom & Notifications Module - Sub-PRD

## Module Overview & Purpose

The Daily Wisdom & Notifications Module delivers proactive engagement by providing users with one meaningful shloka each day along with a practical explanation. It manages notification scheduling, user preferences, and ensures consistent daily content delivery to build learning habits.

## Functional Requirements

### User Stories & Acceptance Criteria

#### US-DAILY-1: View Daily Wisdom
**As a** user  
**I want** to see one meaningful shloka each day with explanation  
**So that** I can reflect on Gita wisdom as part of my daily routine

**Acceptance Criteria:**
- Same shloka displayed to all users on a given day
- Shloka changes daily at midnight UTC
- Explanation optimized for daily reflection (100-150 words)
- Displayed prominently on home screen
- "Read More" button navigates to full shloka detail
- Historical daily wisdom accessible by date
- Loading state while fetching
- Offline mode shows cached daily wisdom

#### US-DAILY-2: Enable/Disable Notifications
**As a** user  
**I want** to enable or disable daily wisdom notifications  
**So that** I can control when I receive reminders

**Acceptance Criteria:**
- Notification toggle in settings screen
- Default state: enabled
- Changes saved immediately to backend
- Visual feedback on toggle
- Notification permission requested on first enable
- Works for both authenticated and anonymous users (local notifications)
- Setting synced across devices for authenticated users

#### US-DAILY-3: Set Notification Time
**As a** user  
**I want** to choose what time I receive daily notifications  
**So that** I can align reminders with my schedule

**Acceptance Criteria:**
- Time picker in settings screen
- Default time: 8:00 AM local time
- Time saved in user's timezone
- Changes applied from next day
- 24-hour and 12-hour format support
- Visual confirmation of time change
- Authenticated users only (anonymous users use default)

#### US-DAILY-4: Receive Daily Notification
**As a** user with notifications enabled  
**I want** to receive a push notification with daily wisdom  
**So that** I'm reminded to engage with the app

**Acceptance Criteria:**
- Notification sent at user's preferred time
- Notification includes shloka preview (first line)
- Tapping notification opens app to daily wisdom
- Notification respects device Do Not Disturb settings
- No duplicate notifications on same day
- Notification includes app icon and title
- Deep link to daily wisdom screen

#### US-DAILY-5: Access Historical Daily Wisdom
**As a** user  
**I want** to view past daily wisdom shlokas  
**So that** I can revisit previous teachings

**Acceptance Criteria:**
- Calendar view or date picker to select past dates
- Display shloka and explanation for selected date
- Navigate between dates (previous/next buttons)
- Limited to past 30 days
- Loading state while fetching
- Error message if date not available

## Non-Functional Requirements

### Performance
- Daily wisdom fetch time: < 500ms
- Notification delivery: Within 5 minutes of scheduled time
- Settings update: < 300ms
- Historical wisdom fetch: < 1 second

### Reliability
- Notification delivery rate: > 95%
- Daily wisdom selection: 100% consistent (same for all users)
- No missed days (wisdom selected for every date)
- Graceful handling of notification permission denial

### Scalability
- Support 1 million users with notifications enabled
- Notification batch processing: 10,000 users/minute
- Daily wisdom pre-generated during off-peak hours
- Efficient database queries for user notification settings

### Usability
- Clear notification permission request
- Easy-to-find settings
- Intuitive time picker
- Notification preview before enabling

## API Contracts

### GET /api/daily-wisdom

**Query Parameters:**
- `date` (optional): YYYY-MM-DD format, defaults to today

**Response (200 OK):**
```json
{
  "date": "2026-01-17",
  "shloka": {
    "id": "uuid",
    "chapter": 2,
    "shlokaNumber": 47,
    "sanskritText": "कर्मण्येवाधिकारस्ते...",
    "transliteration": "karmaṇy-evādhikāras te...",
    "meaning": "You have a right to perform your duty..."
  },
  "explanation": "Today's wisdom reminds us to focus on our efforts rather than worrying about results. Whether you're studying for exams or working on a project, give your best without stressing about the outcome. This mindset brings peace and better performance."
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "Daily wisdom not available for this date"
}
```

### GET /api/settings

**Headers:**
- `Authorization: Bearer <token>` (required)

**Response (200 OK):**
```json
{
  "notificationEnabled": true,
  "notificationTime": "08:00"
}
```

### PUT /api/settings

**Headers:**
- `Authorization: Bearer <token>` (required)

**Request:**
```json
{
  "notificationEnabled": true,
  "notificationTime": "09:30"
}
```

**Response (200 OK):**
```json
{
  "notificationEnabled": true,
  "notificationTime": "09:30"
}
```

## Error Handling & Edge Cases

### Error Scenarios

1. **Daily Wisdom Not Generated**
   - Error: 404 Not Found
   - Action: Generate on-demand or use fallback shloka
   - Log: Critical error logged
   - Alert: Notify ops team

2. **Notification Permission Denied**
   - Action: Show message explaining benefits
   - Fallback: In-app reminders only
   - No error thrown

3. **Invalid Time Format**
   - Error: 400 Bad Request
   - Message: "Time must be in HH:MM format"
   - Action: Client-side validation prevents

4. **Notification Delivery Failure**
   - Action: Retry up to 3 times
   - Log: Failure logged with user_id
   - No user-facing error (silent failure)

5. **Timezone Conversion Error**
   - Action: Use UTC as fallback
   - Log: Error logged
   - Notification may be off by hours

### Edge Cases

- User changes timezone: Notification time adjusted automatically
- User disables then re-enables: Notification scheduled for next day
- Multiple devices: Notification sent to all registered devices
- App uninstalled: Notification token invalidated automatically
- Notification during app usage: Show in-app banner instead
- Leap year dates: Handled correctly
- Daylight saving time: Timezone library handles automatically

## Dependencies on Other Modules

### Internal Dependencies
- **Content Module**: Shloka data for daily wisdom
- **RAG Module**: Generate daily wisdom explanations
- **Authentication Module**: User settings and preferences
- **Database Module**: DailyWisdom and User tables

### External Dependencies
- **Celery**: Task scheduling for daily wisdom selection and notifications
- **Redis**: Celery broker and result backend
- **Firebase Cloud Messaging**: Push notifications (Phase 2)
- **PostgreSQL**: Store daily wisdom and user settings
- **React Native**: Local notifications (Phase 1)

## Assumptions & Constraints

### Assumptions
- Users have granted notification permissions
- Device supports push notifications
- Users understand timezone implications
- Daily wisdom generated before first user wakes up (e.g., 3 AM UTC)
- Notification tokens stored securely

### Constraints
- One daily wisdom per day (global, not per-user)
- Notification time granularity: 1 minute
- Historical wisdom limited to 30 days
- No custom notification messages (Phase 1)
- Local notifications only in Phase 1 (no FCM)
- Notification scheduling requires app to be installed

## Success Metrics

### Functional Metrics
- Daily wisdom availability: 100% (no missed days)
- Notification delivery rate: > 95%
- Settings update success rate: > 99%
- Notification open rate: > 20%

### Engagement Metrics
- Users with notifications enabled: > 60%
- Daily wisdom view rate: > 40% of active users
- Notification click-through rate: > 15%
- Average time on daily wisdom: > 20 seconds

### Performance Metrics
- Daily wisdom generation time: < 5 seconds
- Notification batch processing: 10,000 users/minute
- Settings update latency: < 200ms

## Traceability to Master PRD

- **FR7**: Deliver one "Daily Gita Wisdom" shloka per day
- **FR8**: Send optional daily notifications
- **FR12**: Allow users to manage notification settings
- **Epic 4**: Daily Wisdom & Life Guidance implementation
- **Story 4.1**: Daily Wisdom Selection & API
- **Story 4.2**: Notification System
