# Bhagavad Gita Learning App - User Stories

## Overview
This document contains all Agile user stories derived from the module Sub-PRDs. Stories are organized by module, prioritized, and include acceptance criteria and dependencies.

---

## Module 1: Authentication

### Story AUTH-1: User Registration with Email/Password
**Priority:** High  
**Dependencies:** Database setup, User table schema

**User Story:**  
As a new user, I want to register using my email and password, so that I can create a personalized account.

**Acceptance Criteria:**
- Email validation enforces valid email format
- Password must be minimum 8 characters
- Password is hashed using bcrypt before storage
- Duplicate email registration returns appropriate error
- Successful registration returns user object and JWT access token
- User record created in PostgreSQL with timestamp
- Token expiration set to 7 days by default

---

### Story AUTH-2: User Login with Email/Password
**Priority:** High  
**Dependencies:** AUTH-1 (User Registration)

**User Story:**  
As a registered user, I want to login with my email and password, so that I can access my personalized content.

**Acceptance Criteria:**
- Email and password validated against database
- Invalid credentials return 401 Unauthorized error
- Successful login returns user object and JWT access token
- Last login timestamp updated in database
- Token includes user ID and email in payload
- Token can be validated on subsequent requests

---

### Story AUTH-3: Google OAuth Authentication
**Priority:** High  
**Dependencies:** AUTH-1 (User Registration), OAuth configuration

**User Story:**  
As a user, I want to login using my Google account, so that I can access the app without creating a new password.

**Acceptance Criteria:**
- OAuth flow initiated via `/api/auth/google` endpoint
- User redirected to Google consent screen
- Authorization code exchanged for access token
- User profile retrieved from Google API
- New user created if email doesn't exist
- Existing user matched by email or oauth_id
- JWT token generated and returned to client
- OAuth provider and oauth_id stored in user record

---

### Story AUTH-4: Anonymous Read-Only Access
**Priority:** Medium  
**Dependencies:** Content browsing endpoints

**User Story:**  
As a visitor, I want to browse content without authentication, so that I can explore the app before registering.

**Acceptance Criteria:**
- Chapter and shloka endpoints accessible without token
- Bookmark and profile endpoints require authentication
- Anonymous users see "Sign in to bookmark" prompts
- No user-specific data returned for anonymous requests

---

### Story AUTH-5: Token Validation Middleware
**Priority:** High  
**Dependencies:** AUTH-1, AUTH-2, AUTH-3

**User Story:**  
As a system, I want to validate JWT tokens on protected endpoints, so that only authenticated users access personalized features.

**Acceptance Criteria:**
- Protected endpoints check for Authorization header
- Token signature validated using secret key
- Expired tokens return 401 Unauthorized
- Invalid tokens return 401 Unauthorized
- Valid tokens extract user ID for request context
- Token validation middleware reusable across endpoints

---

## Module 2: Content Browsing

### Story CONTENT-1: Browse Chapter List
**Priority:** High  
**Dependencies:** Database with chapter data

**User Story:**  
As a user, I want to see a list of all 18 Bhagavad Gita chapters, so that I can choose which chapter to explore.

**Acceptance Criteria:**
- Display all 18 chapters in sequential order
- Each chapter shows: number, title, Sanskrit name, brief description
- Chapter cards are tappable to navigate to shloka list
- Loading state displayed while fetching data
- Error state with retry option if fetch fails
- Offline mode displays cached chapter data
- Anonymous users can access chapter list

---

### Story CONTENT-2: Browse Shloka List
**Priority:** High  
**Dependencies:** CONTENT-1, Database with shloka data

**User Story:**  
As a user, I want to see all shlokas within a selected chapter, so that I can browse and select specific verses to study.

**Acceptance Criteria:**
- Display all shlokas for selected chapter in sequential order
- Each shloka item shows: verse number, first line of Sanskrit text
- Bookmarked shlokas display visual indicator (bookmark icon)
- Shloka items are tappable to navigate to detail view
- Pull-to-refresh functionality updates shloka list
- Loading state displayed while fetching data
- Offline mode displays cached shloka data
- Bookmark status shown for authenticated users only

---

### Story CONTENT-3: View Shloka Detail with AI Explanation
**Priority:** High  
**Dependencies:** CONTENT-2, RAG-1 (AI explanation generation)

**User Story:**  
As a user, I want to view complete shloka details with AI explanation, so that I can deeply understand the verse's wisdom.

**Acceptance Criteria:**
- Display Sanskrit text in appropriate font
- Display transliteration in readable Latin script
- Display English meaning/translation
- Display AI-generated explanation with "AI-generated" label
- Show loading state while explanation generates
- Explanation loads within 2 seconds (NFR requirement)
- Bookmark button visible and functional
- Audio player controls visible if audio available
- Navigation to previous/next shloka available
- Offline mode shows cached explanation or "offline" message
- Anonymous users can view all content except bookmark

---

### Story CONTENT-4: Play Shloka Audio
**Priority:** Medium  
**Dependencies:** CONTENT-3, Audio file storage setup

**User Story:**  
As a user, I want to listen to audio chanting of shlokas, so that I can experience the verses through sound.

**Acceptance Criteria:**
- Audio player displays play/pause button
- Progress bar shows playback position
- Audio continues playing when screen is backgrounded
- Audio stops when navigating away from shloka
- Error message displayed if audio file unavailable
- Audio files cached for offline playback
- Loading indicator while audio buffers
- Playback speed control (1x, 1.5x, 2x) - optional

---

### Story CONTENT-5: Bookmark Shlokas
**Priority:** High  
**Dependencies:** AUTH-5 (Token validation), CONTENT-3

**User Story:**  
As an authenticated user, I want to bookmark shlokas for easy access later, so that I can build a personal collection of meaningful verses.

**Acceptance Criteria:**
- Bookmark button visible on shloka detail screen
- Tapping bookmark toggles saved state
- Visual feedback shows bookmark status (filled/unfilled icon)
- Optimistic UI update (immediate visual feedback)
- Bookmark synced to backend after UI update
- Rollback on API failure with error message
- Bookmark status reflected across all views (list, detail, profile)
- Anonymous users see "Sign in to bookmark" prompt
- Duplicate bookmarks prevented by backend

---

### Story CONTENT-6: View Bookmarked Shlokas
**Priority:** Medium  
**Dependencies:** CONTENT-5, AUTH-5

**User Story:**  
As an authenticated user, I want to see all my bookmarked shlokas in one place, so that I can quickly access my favorite verses.

**Acceptance Criteria:**
- Bookmarks displayed in reverse chronological order (newest first)
- Each bookmark shows: chapter reference, shloka preview, bookmark date
- Tapping bookmark navigates to shloka detail
- Swipe-to-delete gesture removes bookmark
- Empty state displayed for users with no bookmarks
- Pull-to-refresh syncs latest bookmarks
- Loading state while fetching bookmarks
- Bookmark count displayed in profile section

---

## Module 3: RAG Engine

### Story RAG-1: Generate Shloka Explanation
**Priority:** High  
**Dependencies:** Ollama setup, FAISS index, Embedding model

**User Story:**  
As a user, I want to receive AI-generated simple explanations for shlokas, so that I can understand the wisdom in student-friendly language.

**Acceptance Criteria:**
- Explanation generated within 2 seconds
- Language appropriate for 12-22 age group
- Explanation grounded strictly in retrieved Gita context
- No hallucinated information or external references
- Explanation includes practical application when relevant
- Clear "AI-generated" label displayed
- Fallback to cached or generic explanation on failure
- Explanation length: 150-300 words

---

### Story RAG-2: Retrieve Relevant Shlokas
**Priority:** High  
**Dependencies:** FAISS index setup, Embedding model

**User Story:**  
As a system, I want to find semantically similar shlokas for context, so that AI explanations are grounded in related verses.

**Acceptance Criteria:**
- Semantic search returns top 3-5 most relevant shlokas
- Retrieval completes within 500ms
- Similarity scores above 0.6 threshold
- Results include full shloka details (Sanskrit, transliteration, meaning)
- Query embedding uses same model as shloka embeddings
- Results cached for identical queries

---

### Story RAG-3: Life Guidance Recommendations
**Priority:** Medium  
**Dependencies:** RAG-1, RAG-2

**User Story:**  
As a user, I want to receive relevant shlokas for my life problems, so that I can find practical wisdom for my current situation.

**Acceptance Criteria:**
- Problem categories mapped to relevant query keywords
- Top 3-5 most relevant shlokas returned
- Each recommendation includes practical explanation
- Relevance score displayed for each recommendation
- Recommendations generated within 3 seconds
- Explanations focus on practical application to the problem
- No generic or irrelevant recommendations

---

### Story RAG-4: Daily Wisdom Explanation Generation
**Priority:** Medium  
**Dependencies:** RAG-1, DAILY-1

**User Story:**  
As a system, I want to generate explanations for daily wisdom shlokas, so that users receive meaningful daily content.

**Acceptance Criteria:**
- Explanation emphasizes daily practical application
- Tone is inspirational and motivational
- Length optimized for mobile notification (100-150 words)
- Generated during off-peak hours (scheduled task)
- Cached for the entire day
- Fallback to pre-written explanation if generation fails

---

## Module 4: Daily Wisdom & Notifications

### Story DAILY-1: View Daily Wisdom
**Priority:** High  
**Dependencies:** RAG-4, Content data

**User Story:**  
As a user, I want to see one meaningful shloka each day with explanation, so that I can reflect on Gita wisdom as part of my daily routine.

**Acceptance Criteria:**
- Same shloka displayed to all users on a given day
- Shloka changes daily at midnight UTC
- Explanation optimized for daily reflection (100-150 words)
- Displayed prominently on home screen
- "Read More" button navigates to full shloka detail
- Historical daily wisdom accessible by date
- Loading state while fetching
- Offline mode shows cached daily wisdom

---

### Story DAILY-2: Enable/Disable Notifications
**Priority:** Medium  
**Dependencies:** AUTH-5 (for authenticated users)

**User Story:**  
As a user, I want to enable or disable daily wisdom notifications, so that I can control when I receive reminders.

**Acceptance Criteria:**
- Notification toggle in settings screen
- Default state: enabled
- Changes saved immediately to backend
- Visual feedback on toggle
- Notification permission requested on first enable
- Works for both authenticated and anonymous users (local notifications)
- Setting synced across devices for authenticated users

---

### Story DAILY-3: Set Notification Time
**Priority:** Medium  
**Dependencies:** DAILY-2, AUTH-5

**User Story:**  
As a user, I want to choose what time I receive daily notifications, so that I can align reminders with my schedule.

**Acceptance Criteria:**
- Time picker in settings screen
- Default time: 8:00 AM local time
- Time saved in user's timezone
- Changes applied from next day
- 24-hour and 12-hour format support
- Visual confirmation of time change
- Authenticated users only (anonymous users use default)

---

### Story DAILY-4: Receive Daily Notification
**Priority:** Medium  
**Dependencies:** DAILY-2, DAILY-3, Celery setup

**User Story:**  
As a user with notifications enabled, I want to receive a push notification with daily wisdom, so that I'm reminded to engage with the app.

**Acceptance Criteria:**
- Notification sent at user's preferred time
- Notification includes shloka preview (first line)
- Tapping notification opens app to daily wisdom
- Notification respects device Do Not Disturb settings
- No duplicate notifications on same day
- Notification includes app icon and title
- Deep link to daily wisdom screen

---

### Story DAILY-5: Access Historical Daily Wisdom
**Priority:** Low  
**Dependencies:** DAILY-1

**User Story:**  
As a user, I want to view past daily wisdom shlokas, so that I can revisit previous teachings.

**Acceptance Criteria:**
- Calendar view or date picker to select past dates
- Display shloka and explanation for selected date
- Navigate between dates (previous/next buttons)
- Limited to past 30 days
- Loading state while fetching
- Error message if date not available

---

## Module 5: Search & Profile

### Story SEARCH-1: Keyword Search
**Priority:** High  
**Dependencies:** Content data, PostgreSQL full-text search

**User Story:**  
As a user, I want to search for shlokas by keyword, theme, or concept, so that I can quickly find relevant verses.

**Acceptance Criteria:**
- Search input with minimum 3 characters
- Search across Sanskrit, transliteration, English meaning, and themes
- Results ranked by relevance
- Each result shows: chapter/verse reference, matched text snippet, relevance indicator
- Highlighted matching text in results
- Empty state for no results with suggestions
- Recent searches stored locally (last 5)
- Search debouncing (300ms delay)
- Loading state while searching
- Navigate to shloka detail from results

---

### Story SEARCH-2: Semantic Search
**Priority:** Medium  
**Dependencies:** SEARCH-1, RAG-2 (FAISS embeddings)

**User Story:**  
As a user, I want search results to understand meaning, not just keywords, so that I find relevant verses even with different wording.

**Acceptance Criteria:**
- Semantic similarity search using RAG embeddings
- Results include conceptually similar shlokas
- Combined ranking: keyword match + semantic similarity
- Works with natural language queries
- Example: "dealing with stress" finds shlokas about peace, calm, equanimity

---

### Story PROFILE-1: View Profile
**Priority:** Medium  
**Dependencies:** AUTH-5

**User Story:**  
As an authenticated user, I want to view my profile with learning statistics, so that I can track my progress.

**Acceptance Criteria:**
- Display user email and account creation date
- Show statistics: bookmarks count, shlokas read, chapters completed, days active
- Profile picture (from OAuth or default avatar)
- Last login timestamp
- Loading state while fetching
- Error handling with retry option

---

### Story PROFILE-2: View Bookmarks in Profile
**Priority:** Medium  
**Dependencies:** CONTENT-6, PROFILE-1

**User Story:**  
As an authenticated user, I want to see all my bookmarked shlokas, so that I can quickly access my favorite verses.

**Acceptance Criteria:**
- Bookmarks displayed in reverse chronological order
- Each bookmark shows: chapter reference, shloka preview, bookmark date
- Swipe-to-delete gesture removes bookmark
- Confirmation dialog before deletion
- Empty state for no bookmarks with call-to-action
- Pull-to-refresh syncs latest bookmarks
- Navigate to shloka detail from bookmark
- Bookmark count badge

---

### Story PROFILE-3: View Reading Progress
**Priority:** Low  
**Dependencies:** PROFILE-1, Progress tracking implementation

**User Story:**  
As an authenticated user, I want to see which shlokas I've read, so that I can track my learning journey.

**Acceptance Criteria:**
- Chapter completion percentage displayed
- List of recently read shlokas (last 10)
- Visual progress indicators (progress bars)
- "Continue Reading" button to resume last shloka
- Reading streak counter (consecutive days)
- Total shlokas read count
- Chapters completed count

---

### Story PROFILE-4: Manage Account Settings
**Priority:** Medium  
**Dependencies:** AUTH-5, DAILY-2

**User Story:**  
As an authenticated user, I want to manage my account settings, so that I can customize my experience.

**Acceptance Criteria:**
- View and edit notification preferences
- Change password (email/password users only)
- Logout functionality
- Account deletion option with confirmation
- Settings changes saved immediately
- Visual feedback for successful updates
- Error handling with clear messages

---

## Story Priority Summary

### High Priority (MVP - Phase 1)
- AUTH-1: User Registration
- AUTH-2: User Login
- AUTH-3: Google OAuth
- AUTH-5: Token Validation
- CONTENT-1: Browse Chapters
- CONTENT-2: Browse Shlokas
- CONTENT-3: View Shloka Detail
- CONTENT-5: Bookmark Shlokas
- RAG-1: Generate Explanation
- RAG-2: Retrieve Relevant Shlokas
- DAILY-1: View Daily Wisdom
- SEARCH-1: Keyword Search

### Medium Priority (Phase 1 Enhancement)
- AUTH-4: Anonymous Access
- CONTENT-4: Audio Playback
- CONTENT-6: View Bookmarks
- RAG-3: Life Guidance
- RAG-4: Daily Wisdom Generation
- DAILY-2: Enable/Disable Notifications
- DAILY-3: Set Notification Time
- DAILY-4: Receive Notifications
- SEARCH-2: Semantic Search
- PROFILE-1: View Profile
- PROFILE-2: View Bookmarks in Profile
- PROFILE-4: Account Settings

### Low Priority (Phase 2)
- DAILY-5: Historical Daily Wisdom
- PROFILE-3: Reading Progress

---

## Dependencies Graph

```
Database Setup
├── AUTH-1 (Registration)
│   ├── AUTH-2 (Login)
│   ├── AUTH-3 (OAuth)
│   └── AUTH-5 (Token Validation)
│       ├── CONTENT-5 (Bookmarks)
│       │   └── CONTENT-6 (View Bookmarks)
│       ├── PROFILE-1 (View Profile)
│       │   ├── PROFILE-2 (Bookmarks in Profile)
│       │   ├── PROFILE-3 (Reading Progress)
│       │   └── PROFILE-4 (Account Settings)
│       └── DAILY-2 (Notification Settings)
│           └── DAILY-3 (Notification Time)
│               └── DAILY-4 (Send Notifications)
│
├── CONTENT-1 (Chapter List)
│   └── CONTENT-2 (Shloka List)
│       └── CONTENT-3 (Shloka Detail)
│           └── CONTENT-4 (Audio Playback)
│
├── RAG Setup (FAISS + Ollama)
│   ├── RAG-2 (Retrieve Shlokas)
│   │   ├── RAG-1 (Generate Explanation)
│   │   │   ├── RAG-3 (Life Guidance)
│   │   │   └── RAG-4 (Daily Wisdom Generation)
│   │   │       └── DAILY-1 (View Daily Wisdom)
│   │   │           └── DAILY-5 (Historical Wisdom)
│   │   └── SEARCH-2 (Semantic Search)
│   │
│   └── SEARCH-1 (Keyword Search)
```

---

## Sprint Recommendations

### Sprint 1: Foundation (2 weeks)
- Database setup and schema
- AUTH-1, AUTH-2, AUTH-5
- CONTENT-1, CONTENT-2

### Sprint 2: Core Content (2 weeks)
- RAG setup (FAISS, Ollama)
- RAG-1, RAG-2
- CONTENT-3
- AUTH-3

### Sprint 3: Personalization (2 weeks)
- CONTENT-5, CONTENT-6
- PROFILE-1, PROFILE-2
- SEARCH-1

### Sprint 4: Engagement (2 weeks)
- DAILY-1, RAG-4
- DAILY-2, DAILY-3, DAILY-4
- CONTENT-4

### Sprint 5: Enhancement (1-2 weeks)
- SEARCH-2
- RAG-3
- PROFILE-3, PROFILE-4
- AUTH-4
- DAILY-5

---

## Notes

- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies

