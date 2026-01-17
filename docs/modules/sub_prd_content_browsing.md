# Content Browsing Module - Sub-PRD

## Module Overview & Purpose

The Content Browsing Module enables users to explore and consume Bhagavad Gita content through an intuitive chapter-by-chapter and shloka-by-shloka navigation system. It provides access to Sanskrit text, transliterations, meanings, audio playback, and bookmark management, creating the core learning experience of the application.

## Functional Requirements

### User Stories & Acceptance Criteria

#### US-CONTENT-1: Browse Chapter List
**As a** user  
**I want** to see a list of all 18 Bhagavad Gita chapters  
**So that** I can choose which chapter to explore

**Acceptance Criteria:**
- Display all 18 chapters in sequential order
- Each chapter shows: number, title, Sanskrit name, brief description
- Chapter cards are tappable to navigate to shloka list
- Loading state displayed while fetching data
- Error state with retry option if fetch fails
- Offline mode displays cached chapter data
- Anonymous users can access chapter list

#### US-CONTENT-2: Browse Shloka List
**As a** user  
**I want** to see all shlokas within a selected chapter  
**So that** I can browse and select specific verses to study

**Acceptance Criteria:**
- Display all shlokas for selected chapter in sequential order
- Each shloka item shows: verse number, first line of Sanskrit text
- Bookmarked shlokas display visual indicator (bookmark icon)
- Shloka items are tappable to navigate to detail view
- Pull-to-refresh functionality updates shloka list
- Loading state displayed while fetching data
- Offline mode displays cached shloka data
- Bookmark status shown for authenticated users only

#### US-CONTENT-3: View Shloka Detail
**As a** user  
**I want** to view complete shloka details with AI explanation  
**So that** I can deeply understand the verse's wisdom

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

#### US-CONTENT-4: Play Shloka Audio
**As a** user  
**I want** to listen to audio chanting of shlokas  
**So that** I can experience the verses through sound

**Acceptance Criteria:**
- Audio player displays play/pause button
- Progress bar shows playback position
- Audio continues playing when screen is backgrounded
- Audio stops when navigating away from shloka
- Error message displayed if audio file unavailable
- Audio files cached for offline playback
- Loading indicator while audio buffers
- Playback speed control (1x, 1.5x, 2x) - optional

#### US-CONTENT-5: Bookmark Shlokas
**As an** authenticated user  
**I want** to bookmark shlokas for easy access later  
**So that** I can build a personal collection of meaningful verses

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

#### US-CONTENT-6: View Bookmarked Shlokas
**As an** authenticated user  
**I want** to see all my bookmarked shlokas in one place  
**So that** I can quickly access my favorite verses

**Acceptance Criteria:**
- Bookmarks displayed in reverse chronological order (newest first)
- Each bookmark shows: chapter reference, shloka preview, bookmark date
- Tapping bookmark navigates to shloka detail
- Swipe-to-delete gesture removes bookmark
- Empty state displayed for users with no bookmarks
- Pull-to-refresh syncs latest bookmarks
- Loading state while fetching bookmarks
- Bookmark count displayed in profile section

## Non-Functional Requirements

### Performance
- Chapter list load time: < 500ms
- Shloka list load time: < 1 second
- Shloka detail load time: < 2 seconds (including AI explanation)
- Audio playback start: < 1 second after tap
- Bookmark action response: < 300ms
- Offline content access: < 100ms (from cache)

### Usability
- Mobile-first responsive design
- Touch targets minimum 44x44 pixels
- Smooth scrolling and transitions
- Clear visual hierarchy
- Readable fonts (minimum 14px for body text)
- High contrast for Sanskrit text

### Accessibility
- WCAG AA compliance for text contrast
- Screen reader support for all content
- Semantic HTML/component structure
- Keyboard navigation support (web)
- Audio playback accessible via keyboard

### Reliability
- Offline-first architecture with local caching
- Graceful degradation when backend unavailable
- Automatic retry on network errors
- Data consistency between cache and server

### Scalability
- Support for 700+ shlokas across 18 chapters
- Efficient pagination for large shloka lists
- Lazy loading of audio files
- Optimized image/font loading

## API Contracts

### GET /api/chapters

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Arjuna's Dilemma",
    "sanskritName": "अर्जुनविषादयोग",
    "description": "Arjuna's moral crisis on the battlefield",
    "shlokaCount": 47
  },
  {
    "id": 2,
    "title": "The Yoga of Knowledge",
    "sanskritName": "सांख्ययोग",
    "description": "Krishna explains the nature of the soul",
    "shlokaCount": 72
  }
]
```

### GET /api/chapters/{chapterId}/shlokas

**Headers:**
- `Authorization: Bearer <token>` (optional)

**Response (200 OK):**
```json
[
  {
    "id": "uuid-1",
    "chapter": 1,
    "shlokaNumber": 1,
    "sanskritText": "धृतराष्ट्र उवाच...",
    "transliteration": "dhṛtarāṣṭra uvāca...",
    "meaning": "Dhritarashtra said...",
    "audioFilePath": "/audio/chapter1/shloka1.mp3",
    "themes": ["dharma", "duty", "war"],
    "isBookmarked": false
  }
]
```

### GET /api/shlokas/{shlokaId}

**Headers:**
- `Authorization: Bearer <token>` (optional)

**Response (200 OK):**
```json
{
  "id": "uuid-1",
  "chapter": 1,
  "shlokaNumber": 1,
  "sanskritText": "धृतराष्ट्र उवाच...",
  "transliteration": "dhṛtarāṣṭra uvāca...",
  "meaning": "Dhritarashtra said...",
  "audioFilePath": "/audio/chapter1/shloka1.mp3",
  "themes": ["dharma", "duty", "war"],
  "isBookmarked": false,
  "explanation": "This verse introduces the setting of the Bhagavad Gita. King Dhritarashtra asks his advisor Sanjaya about the events on the battlefield..."
}
```

### GET /api/shlokas/{shlokaId}/audio

**Response (200 OK):**
- Content-Type: audio/mpeg
- Body: Audio file stream

**Error Response (404 Not Found):**
```json
{
  "detail": "Audio file not available for this shloka"
}
```

### GET /api/bookmarks

**Headers:**
- `Authorization: Bearer <token>` (required)

**Response (200 OK):**
```json
[
  {
    "id": "bookmark-uuid-1",
    "userId": "user-uuid",
    "chapter": 2,
    "shlokaNumber": 47,
    "createdAt": "2026-01-17T10:30:00Z",
    "shloka": {
      "id": "shloka-uuid",
      "sanskritText": "कर्मण्येवाधिकारस्ते...",
      "transliteration": "karmaṇy-evādhikāras te...",
      "meaning": "You have a right to perform your duty..."
    }
  }
]
```

### POST /api/bookmarks

**Headers:**
- `Authorization: Bearer <token>` (required)

**Request:**
```json
{
  "chapter": 2,
  "shlokaNumber": 47
}
```

**Response (201 Created):**
```json
{
  "id": "bookmark-uuid-1",
  "userId": "user-uuid",
  "chapter": 2,
  "shlokaNumber": 47,
  "createdAt": "2026-01-17T10:30:00Z"
}
```

**Error Response (409 Conflict):**
```json
{
  "detail": "Shloka already bookmarked"
}
```

### DELETE /api/bookmarks/{bookmarkId}

**Headers:**
- `Authorization: Bearer <token>` (required)

**Response (204 No Content)**

## Error Handling & Edge Cases

### Error Scenarios

1. **Network Unavailable**
   - Action: Load from cache, show offline indicator
   - Message: "Viewing offline content"

2. **Chapter/Shloka Not Found**
   - Error: 404 Not Found
   - Message: "Content not found"
   - Action: Navigate back to previous screen

3. **Audio File Missing**
   - Error: 404 Not Found
   - Message: "Audio not available for this shloka"
   - Action: Hide audio player or show disabled state

4. **AI Explanation Generation Timeout**
   - Error: 504 Gateway Timeout
   - Message: "Explanation taking longer than expected"
   - Action: Show retry button or fallback explanation

5. **Bookmark Unauthorized**
   - Error: 401 Unauthorized
   - Message: "Please sign in to bookmark"
   - Action: Redirect to login

6. **Duplicate Bookmark**
   - Error: 409 Conflict
   - Message: "Already bookmarked"
   - Action: Update UI to show bookmarked state

### Edge Cases

- Empty chapter (no shlokas): Show message "Content coming soon"
- Very long Sanskrit text: Implement text wrapping and scrolling
- Slow network: Show loading indicators, implement timeouts
- Cache corruption: Clear cache and refetch from server
- Concurrent bookmark/unbookmark: Last action wins
- Audio playback during phone call: Pause audio automatically
- Background audio with screen lock: Continue playback

## Dependencies on Other Modules

### Internal Dependencies
- **Authentication Module**: User authentication for bookmarks
- **RAG Module**: AI explanation generation for shloka details
- **Database Module**: Chapter, Shloka, Bookmark tables
- **File Storage**: Audio file serving

### External Dependencies
- **PostgreSQL**: Content and bookmark data persistence
- **Redis**: Content caching for performance
- **File System**: Audio file storage
- **React Native**: Frontend UI components
- **AsyncStorage**: Offline content caching

## Assumptions & Constraints

### Assumptions
- All 18 chapters and ~700 shlokas pre-loaded in database
- Audio files available for most shlokas (not all)
- Users have stable internet for initial content download
- Mobile devices have sufficient storage for cached content
- Sanskrit fonts available on target devices

### Constraints
- Static content (chapters/shlokas) doesn't change frequently
- Audio files are pre-recorded (not generated)
- Bookmark limit: None (unlimited bookmarks per user)
- Cache size limit: 50MB for offline content
- No editing or user-generated content

## Success Metrics

### Functional Metrics
- Chapter list load success rate: > 99%
- Shloka detail view success rate: > 98%
- Audio playback success rate: > 95%
- Bookmark action success rate: > 99%
- Offline content access rate: > 90%

### Performance Metrics
- Average chapter list load time: < 300ms
- Average shloka detail load time: < 1.5 seconds
- Average bookmark action time: < 200ms
- Cache hit rate: > 80%

### Engagement Metrics
- Average shlokas viewed per session: > 5
- Average time on shloka detail: > 30 seconds
- Bookmark usage rate: > 30% of authenticated users
- Audio playback rate: > 40% of shloka views
- Return visit rate: > 60% within 7 days

## Traceability to Master PRD

- **FR2**: Display a browsable list of all 18 chapters
- **FR3**: Display a list of shlokas for each selected chapter
- **FR4**: Provide detailed shloka view with Sanskrit, transliteration, meaning, AI explanation
- **FR5**: Enable audio playback of shloka chanting
- **FR6**: Allow users to bookmark shlokas
- **FR14**: Support local caching of content for offline access
- **NFR2**: RAG-based AI responses within 2 seconds
- **NFR3**: Mobile-first responsive UI
- **Epic 3**: Core Content Browsing implementation
