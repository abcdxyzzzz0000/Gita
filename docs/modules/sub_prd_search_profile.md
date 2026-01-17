# Search & Profile Module - Sub-PRD

## Module Overview & Purpose

The Search & Profile Module enables users to find specific content through keyword and semantic search, and manage their personalized learning journey through profile features including bookmarks, reading progress, and account settings.

## Functional Requirements

### User Stories & Acceptance Criteria

#### US-SEARCH-1: Keyword Search
**As a** user  
**I want** to search for shlokas by keyword, theme, or concept  
**So that** I can quickly find relevant verses

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

#### US-SEARCH-2: Semantic Search
**As a** user  
**I want** search results to understand meaning, not just keywords  
**So that** I find relevant verses even with different wording

**Acceptance Criteria:**
- Semantic similarity search using RAG embeddings
- Results include conceptually similar shlokas
- Combined ranking: keyword match + semantic similarity
- Works with natural language queries
- Example: "dealing with stress" finds shlokas about peace, calm, equanimity

#### US-PROFILE-1: View Profile
**As an** authenticated user  
**I want** to view my profile with learning statistics  
**So that** I can track my progress

**Acceptance Criteria:**
- Display user email and account creation date
- Show statistics: bookmarks count, shlokas read, chapters completed, days active
- Profile picture (from OAuth or default avatar)
- Last login timestamp
- Loading state while fetching
- Error handling with retry option

#### US-PROFILE-2: View Bookmarks
**As an** authenticated user  
**I want** to see all my bookmarked shlokas  
**So that** I can quickly access my favorite verses

**Acceptance Criteria:**
- Bookmarks displayed in reverse chronological order
- Each bookmark shows: chapter reference, shloka preview, bookmark date
- Swipe-to-delete gesture removes bookmark
- Confirmation dialog before deletion
- Empty state for no bookmarks with call-to-action
- Pull-to-refresh syncs latest bookmarks
- Navigate to shloka detail from bookmark
- Bookmark count badge

#### US-PROFILE-3: View Reading Progress
**As an** authenticated user  
**I want** to see which shlokas I've read  
**So that** I can track my learning journey

**Acceptance Criteria:**
- Chapter completion percentage displayed
- List of recently read shlokas (last 10)
- Visual progress indicators (progress bars)
- "Continue Reading" button to resume last shloka
- Reading streak counter (consecutive days)
- Total shlokas read count
- Chapters completed count

#### US-PROFILE-4: Manage Account Settings
**As an** authenticated user  
**I want** to manage my account settings  
**So that** I can customize my experience

**Acceptance Criteria:**
- View and edit notification preferences
- Change password (email/password users only)
- Logout functionality
- Account deletion option with confirmation
- Settings changes saved immediately
- Visual feedback for successful updates
- Error handling with clear messages

## Non-Functional Requirements

### Performance
- Search response time: < 1 second
- Profile load time: < 500ms
- Bookmarks load time: < 1 second
- Settings update: < 300ms

### Usability
- Search autocomplete/suggestions
- Clear search results layout
- Easy bookmark management
- Intuitive profile navigation
- Accessible settings

### Accuracy
- Search precision: > 80%
- Search recall: > 70%
- Semantic search relevance: > 75%

### Scalability
- Support 10,000 searches/hour
- Handle 1 million bookmarks
- Efficient pagination for large result sets

## API Contracts

### GET /api/search

**Query Parameters:**
- `q` (required): Search query (min 3 characters)
- `limit` (optional): Results limit (default 20, max 50)

**Response (200 OK):**
```json
{
  "results": [
    {
      "shloka": {
        "id": "uuid",
        "chapter": 2,
        "shlokaNumber": 47,
        "sanskritText": "कर्मण्येवाधिकारस्ते...",
        "transliteration": "karmaṇy-evādhikāras te...",
        "meaning": "You have a right to perform your duty..."
      },
      "matchedText": "...right to perform your <mark>duty</mark>...",
      "relevanceScore": 0.92,
      "matchType": "keyword"
    }
  ],
  "totalResults": 15,
  "query": "duty"
}
```

### GET /api/profile

**Headers:**
- `Authorization: Bearer <token>` (required)

**Response (200 OK):**
```json
{
  "user": {
    "id": "uuid",
    "email": "user@example.com",
    "oauthProvider": null,
    "createdAt": "2026-01-01T00:00:00Z",
    "lastLogin": "2026-01-17T10:00:00Z"
  },
  "stats": {
    "bookmarkCount": 12,
    "shlokasRead": 45,
    "chaptersCompleted": 2,
    "daysActive": 15,
    "readingStreak": 5
  }
}
```

### GET /api/progress

**Headers:**
- `Authorization: Bearer <token>` (required)

**Response (200 OK):**
```json
{
  "recentlyRead": [
    {
      "shloka": {
        "id": "uuid",
        "chapter": 2,
        "shlokaNumber": 47
      },
      "lastReadAt": "2026-01-17T09:30:00Z"
    }
  ],
  "chapterProgress": [
    {
      "chapter": 1,
      "totalShlokas": 47,
      "readShlokas": 47,
      "percentage": 100
    },
    {
      "chapter": 2,
      "totalShlokas": 72,
      "readShlokas": 35,
      "percentage": 49
    }
  ],
  "lastReadShloka": {
    "chapter": 2,
    "shlokaNumber": 47
  }
}
```

### POST /api/progress

**Headers:**
- `Authorization: Bearer <token>` (required)

**Request:**
```json
{
  "chapter": 2,
  "shlokaNumber": 47
}
```

**Response (201 Created)**

### PUT /api/profile/password

**Headers:**
- `Authorization: Bearer <token>` (required)

**Request:**
```json
{
  "currentPassword": "oldpassword",
  "newPassword": "newpassword123"
}
```

**Response (200 OK)**

### DELETE /api/profile

**Headers:**
- `Authorization: Bearer <token>` (required)

**Response (204 No Content)**

## Error Handling & Edge Cases

### Error Scenarios

1. **Search Query Too Short**
   - Error: 400 Bad Request
   - Message: "Search query must be at least 3 characters"

2. **No Search Results**
   - Display: Empty state with suggestions
   - Message: "No results found. Try different keywords"

3. **Search Service Unavailable**
   - Error: 503 Service Unavailable
   - Fallback: Basic keyword search only

4. **Profile Load Failure**
   - Error: 500 Internal Server Error
   - Action: Retry button, show cached data if available

5. **Password Change Failed**
   - Error: 401 Unauthorized (wrong current password)
   - Message: "Current password is incorrect"

6. **Account Deletion Confirmation**
   - Require: Re-enter password
   - Warning: "This action cannot be undone"

### Edge Cases

- Search with special characters: Sanitize input
- Very long search query: Truncate to 100 characters
- Concurrent bookmark deletions: Last action wins
- Reading progress for deleted shloka: Handle gracefully
- Profile stats calculation errors: Show partial data
- Empty bookmarks/progress: Show onboarding message

## Dependencies on Other Modules

### Internal Dependencies
- **Content Module**: Shloka data for search results
- **RAG Module**: Semantic search using embeddings
- **Authentication Module**: User authentication and profile data
- **Database Module**: User, Bookmark, ReadingProgress tables

### External Dependencies
- **PostgreSQL**: Full-text search, user data
- **FAISS**: Semantic search via RAG module
- **Redis**: Search result caching

## Assumptions & Constraints

### Assumptions
- Users understand search syntax (no advanced operators)
- Profile data fits in single response (no pagination)
- Reading progress tracked automatically on shloka view
- Bookmarks and progress synced across devices

### Constraints
- Search limited to English and Sanskrit
- No fuzzy matching for Sanskrit text
- Profile stats calculated on-demand (not pre-aggregated)
- No export functionality for bookmarks/progress
- Account deletion is permanent (no recovery)

## Success Metrics

### Functional Metrics
- Search success rate: > 90% (users find what they're looking for)
- Search result relevance: > 80%
- Profile load success rate: > 99%
- Settings update success rate: > 99%

### Engagement Metrics
- Search usage rate: > 30% of users
- Average searches per session: > 2
- Bookmark view rate: > 50% of authenticated users
- Profile view rate: > 40% of authenticated users
- Reading progress engagement: > 60%

### Performance Metrics
- Average search time: < 800ms
- Average profile load time: < 400ms
- Cache hit rate: > 60%

## Traceability to Master PRD

- **FR10**: Enable keyword search across chapters, themes, and verses
- **FR11**: Display user profile with bookmarked shlokas and reading progress
- **FR12**: Allow users to manage notification settings
- **Epic 5**: Search & User Profile implementation
- **Story 5.1**: Keyword Search Implementation
- **Story 5.2**: User Profile & Bookmarks View
- **Story 5.3**: Settings & Account Management
- **Story 5.4**: Reading Progress Tracking
