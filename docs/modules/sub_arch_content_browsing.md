# Content Browsing Module - Sub-Architecture

## Module-Level Architecture Overview

The Content Browsing Module implements a three-tier architecture with API endpoints, business logic services, and data access layers. It integrates with the RAG module for AI explanations and implements aggressive caching for offline-first mobile experience.

```
┌──────────────────────────────────────────────────────────┐
│                     API Layer                            │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  │
│  │Chapters │  │ Shlokas │  │  Audio  │  │Bookmarks │  │
│  │Endpoints│  │Endpoints│  │Endpoint │  │Endpoints │  │
│  └─────────┘  └─────────┘  └─────────┘  └──────────┘  │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│                  Service Layer                           │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Content   │  │   Bookmark   │  │     Audio     │  │
│  │   Service   │  │   Service    │  │   Service     │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│                Repository Layer                          │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │   Chapter   │  │    Shloka    │  │   Bookmark    │  │
│  │ Repository  │  │  Repository  │  │  Repository   │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
└──────────────────────────────────────────────────────────┘
                          │
┌──────────────────────────────────────────────────────────┐
│                   Data Layer                             │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐│
│  │PostgreSQL│  │  Redis   │  │   File   │  │   RAG   ││
│  │ Database │  │  Cache   │  │  System  │  │ Module  ││
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘│
└──────────────────────────────────────────────────────────┘
```

## Internal Components & Responsibilities

### 1. Content Router (`content_router.py`)
**Responsibility**: Define content-related API endpoints

**Endpoints**:
- `GET /api/chapters` - List all chapters
- `GET /api/chapters/{id}/shlokas` - List shlokas in chapter
- `GET /api/shlokas/{id}` - Get shloka detail with explanation
- `GET /api/shlokas/{id}/audio` - Stream audio file

**Dependencies**: ContentService, AuthMiddleware (optional)

### 2. Bookmark Router (`bookmark_router.py`)
**Responsibility**: Define bookmark-related API endpoints

**Endpoints**:
- `GET /api/bookmarks` - List user bookmarks
- `POST /api/bookmarks` - Create bookmark
- `DELETE /api/bookmarks/{id}` - Delete bookmark

**Dependencies**: BookmarkService, AuthMiddleware (required)

### 3. Content Service (`content_service.py`)
**Responsibility**: Business logic for content operations

**Functions**:
- `get_all_chapters()` - Retrieve chapter list with caching
- `get_shlokas_by_chapter(chapter_id, user_id)` - Get shlokas with bookmark status
- `get_shloka_detail(shloka_id, user_id)` - Get shloka with AI explanation
- `get_audio_file_path(shloka_id)` - Resolve audio file location

**Dependencies**: ChapterRepository, ShlokaRepository, RAGService, CacheService

### 4. Bookmark Service (`bookmark_service.py`)
**Responsibility**: Business logic for bookmark operations

**Functions**:
- `get_user_bookmarks(user_id)` - Retrieve all user bookmarks
- `create_bookmark(user_id, chapter, shloka_number)` - Add bookmark
- `delete_bookmark(bookmark_id, user_id)` - Remove bookmark
- `is_bookmarked(user_id, chapter, shloka_number)` - Check bookmark status

**Dependencies**: BookmarkRepository, ShlokaRepository

### 5. Audio Service (`audio_service.py`)
**Responsibility**: Handle audio file streaming

**Functions**:
- `stream_audio(file_path)` - Stream audio file with range support
- `validate_audio_exists(shloka_id)` - Check audio availability

**Dependencies**: File system

### 6. Chapter Repository (`chapter_repository.py`)
**Responsibility**: Database operations for chapters

**Functions**:
- `get_all_chapters()` - SELECT all chapters
- `get_chapter_by_id(chapter_id)` - SELECT single chapter

**Dependencies**: SQLAlchemy, PostgreSQL

### 7. Shloka Repository (`shloka_repository.py`)
**Responsibility**: Database operations for shlokas

**Functions**:
- `get_shlokas_by_chapter(chapter_id)` - SELECT shlokas for chapter
- `get_shloka_by_id(shloka_id)` - SELECT single shloka
- `get_shloka_by_reference(chapter, shloka_number)` - SELECT by chapter/verse

**Dependencies**: SQLAlchemy, PostgreSQL

### 8. Bookmark Repository (`bookmark_repository.py`)
**Responsibility**: Database operations for bookmarks

**Functions**:
- `get_bookmarks_by_user(user_id)` - SELECT user bookmarks with JOIN
- `create_bookmark(user_id, chapter, shloka_number)` - INSERT bookmark
- `delete_bookmark(bookmark_id, user_id)` - DELETE bookmark
- `check_bookmark_exists(user_id, chapter, shloka_number)` - Check existence

**Dependencies**: SQLAlchemy, PostgreSQL

### 9. Cache Service (`cache_service.py`)
**Responsibility**: Redis caching operations

**Functions**:
- `get_cached(key)` - Retrieve from cache
- `set_cached(key, value, ttl)` - Store in cache
- `invalidate_cache(pattern)` - Clear cache entries

**Dependencies**: Redis

## Data Flow

### Chapter List Flow

```
1. Client → GET /api/chapters
2. ContentRouter → ContentService.get_all_chapters()
3. ContentService → CacheService.get_cached('chapters')
4. If cache hit → return cached data
5. If cache miss:
   - ContentService → ChapterRepository.get_all_chapters()
   - ChapterRepository → PostgreSQL SELECT
   - PostgreSQL → return 18 chapter records
   - ContentService → CacheService.set_cached('chapters', data, ttl=3600)
6. ContentService → return chapters
7. ContentRouter → return 200 OK with chapters
8. Client ← chapter list
```

### Shloka List Flow (Authenticated User)

```
1. Client → GET /api/chapters/1/shlokas (with auth token)
2. ContentRouter → AuthMiddleware.optional_auth()
3. AuthMiddleware → extract user_id from token
4. ContentRouter → ContentService.get_shlokas_by_chapter(1, user_id)
5. ContentService → CacheService.get_cached('shlokas_chapter_1')
6. If cache miss:
   - ContentService → ShlokaRepository.get_shlokas_by_chapter(1)
   - ShlokaRepository → PostgreSQL SELECT
   - PostgreSQL → return shloka records
   - ContentService → CacheService.set_cached('shlokas_chapter_1', data)
7. ContentService → BookmarkRepository.get_user_bookmark_map(user_id, chapter=1)
8. BookmarkRepository → PostgreSQL SELECT bookmarks
9. ContentService → merge bookmark status into shloka data
10. ContentService → return shlokas with isBookmarked flags
11. ContentRouter → return 200 OK
12. Client ← shloka list with bookmark status
```

### Shloka Detail with AI Explanation Flow

```
1. Client → GET /api/shlokas/{id}
2. ContentRouter → ContentService.get_shloka_detail(id, user_id)
3. ContentService → CacheService.get_cached('shloka_detail_{id}')
4. If cache miss:
   - ContentService → ShlokaRepository.get_shloka_by_id(id)
   - ShlokaRepository → PostgreSQL SELECT
   - PostgreSQL → return shloka record
5. ContentService → RAGService.generate_explanation(shloka)
6. RAGService → (see RAG module flow)
7. RAGService → return AI explanation
8. ContentService → merge explanation with shloka data
9. ContentService → CacheService.set_cached('shloka_detail_{id}', data, ttl=86400)
10. If user authenticated:
    - ContentService → BookmarkRepository.check_bookmark_exists(user_id, chapter, shloka_number)
    - BookmarkRepository → PostgreSQL SELECT
    - Add isBookmarked flag to response
11. ContentService → return complete shloka data
12. ContentRouter → return 200 OK
13. Client ← shloka with explanation
```

### Audio Streaming Flow

```
1. Client → GET /api/shlokas/{id}/audio
2. ContentRouter → AudioService.stream_audio(shloka_id)
3. AudioService → ShlokaRepository.get_shloka_by_id(id)
4. ShlokaRepository → PostgreSQL SELECT audio_file_path
5. AudioService → validate file exists on file system
6. If file not found → return 404 Not Found
7. AudioService → open file stream
8. AudioService → set Content-Type: audio/mpeg
9. AudioService → set Accept-Ranges: bytes (for seeking)
10. AudioService → stream file chunks
11. ContentRouter → return 200 OK with audio stream
12. Client ← audio file stream
```

### Bookmark Creation Flow

```
1. Client → POST /api/bookmarks {chapter: 2, shlokaNumber: 47}
2. BookmarkRouter → AuthMiddleware.require_auth()
3. AuthMiddleware → validate token, extract user_id
4. BookmarkRouter → BookmarkService.create_bookmark(user_id, 2, 47)
5. BookmarkService → BookmarkRepository.check_bookmark_exists(user_id, 2, 47)
6. BookmarkRepository → PostgreSQL SELECT
7. If exists → return 409 Conflict
8. BookmarkService → ShlokaRepository.get_shloka_by_reference(2, 47)
9. ShlokaRepository → PostgreSQL SELECT (validate shloka exists)
10. If not found → return 404 Not Found
11. BookmarkService → BookmarkRepository.create_bookmark(user_id, 2, 47)
12. BookmarkRepository → PostgreSQL INSERT
13. PostgreSQL → return bookmark record
14. BookmarkService → CacheService.invalidate_cache('bookmarks_user_{user_id}')
15. BookmarkService → return bookmark
16. BookmarkRouter → return 201 Created
17. Client ← bookmark record
```

## Database Schema / Tables Involved

### Chapters Table

```sql
CREATE TABLE chapters (
    id INTEGER PRIMARY KEY CHECK (id BETWEEN 1 AND 18),
    title VARCHAR(255) NOT NULL,
    sanskrit_name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    shloka_count INTEGER NOT NULL
);
```

**Usage**: Static reference data, rarely changes, heavily cached

### Shlokas Table

```sql
CREATE TABLE shlokas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chapter INTEGER NOT NULL REFERENCES chapters(id),
    shloka_number INTEGER NOT NULL,
    sanskrit_text TEXT NOT NULL,
    transliteration TEXT NOT NULL,
    meaning TEXT NOT NULL,
    audio_file_path VARCHAR(500),
    themes TEXT[],
    embedding_index INTEGER NOT NULL,
    CONSTRAINT unique_shloka UNIQUE (chapter, shloka_number)
);

CREATE INDEX idx_shlokas_chapter ON shlokas(chapter);
CREATE INDEX idx_shlokas_themes ON shlokas USING GIN(themes);
```

**Usage**: Core content data, ~700 records, cached per chapter

### Bookmarks Table

```sql
CREATE TABLE bookmarks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter INTEGER NOT NULL,
    shloka_number INTEGER NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_bookmark UNIQUE (user_id, chapter, shloka_number)
);

CREATE INDEX idx_bookmarks_user ON bookmarks(user_id);
CREATE INDEX idx_bookmarks_created ON bookmarks(created_at DESC);
```

**Usage**: User-generated data, grows with user base, indexed by user_id

## External Services Used

### RAG Module (Internal)
**Purpose**: Generate AI explanations for shlokas

**Interface**:
- `generate_explanation(shloka: Shloka) -> str`
- Input: Shloka object with all fields
- Output: Student-friendly explanation text
- Timeout: 2 seconds
- Caching: Explanations cached for 24 hours

### File System
**Purpose**: Store and serve audio files

**Structure**:
```
/audio/
  chapter1/
    shloka1.mp3
    shloka2.mp3
  chapter2/
    shloka1.mp3
```

**File Format**: MP3, 128kbps, mono
**Average Size**: 500KB per file
**Total Storage**: ~350MB for all audio files

## Security Considerations

### Access Control
- Chapter and shloka endpoints: Public (no auth required)
- Bookmark endpoints: Authenticated users only
- Audio streaming: Public (no auth required)
- User can only access/modify their own bookmarks

### Data Validation
- Chapter ID validated (1-18 range)
- Shloka ID validated (UUID format)
- Bookmark creation validates shloka exists
- SQL injection prevented by parameterized queries

### Rate Limiting
- Content endpoints: 100 requests/minute per IP
- Bookmark endpoints: 20 requests/minute per user
- Audio streaming: 50 requests/minute per IP

### Caching Security
- Cache keys include user_id for user-specific data
- No sensitive data in cache (only content and bookmarks)
- Cache invalidation on bookmark changes

## Scalability & Failure Handling

### Scalability Strategies

**Caching**:
- Chapters cached for 1 hour (rarely changes)
- Shlokas cached per chapter for 1 hour
- Shloka details with explanations cached for 24 hours
- User bookmarks cached for 5 minutes
- Cache hit rate target: > 80%

**Database Optimization**:
- Indexes on frequently queried columns
- Connection pooling (10 connections per instance)
- Read replicas for content queries (future)
- Bookmark queries use composite index

**Content Delivery**:
- Audio files served with CDN (future)
- Static content (chapters/shlokas) pre-loaded
- Lazy loading of audio files
- Progressive audio streaming with range requests

**Load Handling**:
- Expected load: 10,000 shloka views/hour
- Bookmark operations: 1,000/hour
- Audio streams: 5,000/hour
- Database capacity: 1 million bookmarks

### Failure Handling

**Database Failures**:
- Connection timeout: 5 seconds
- Retry logic: 3 attempts with exponential backoff
- Fallback to cache if database unavailable
- Return 503 if both database and cache fail

**Cache Failures**:
- Redis unavailable: Skip cache, query database directly
- Cache corruption: Clear and rebuild from database
- No impact on functionality, only performance

**Audio File Failures**:
- File not found: Return 404 with clear message
- File corruption: Log error, return 500
- Streaming error: Client handles partial download

**RAG Module Failures**:
- Timeout (>2s): Return cached explanation or generic message
- Generation error: Return fallback explanation
- Log error for monitoring

**Monitoring & Alerts**:
- Cache hit rate < 70% triggers alert
- Database query time > 1s triggers alert
- Audio streaming errors > 5% triggers alert
- RAG timeout rate > 10% triggers alert

## Deployment Considerations

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/bhagavad_gita

# Redis Cache
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_CHAPTERS=3600
CACHE_TTL_SHLOKAS=3600
CACHE_TTL_EXPLANATIONS=86400

# Audio Files
AUDIO_BASE_PATH=/app/audio
AUDIO_CDN_URL=https://cdn.bhagavadgita.app/audio

# Performance
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20
```

### Docker Configuration

```yaml
# docker-compose.yml
services:
  backend:
    volumes:
      - ./audio:/app/audio:ro  # Mount audio files read-only
    environment:
      - AUDIO_BASE_PATH=/app/audio
```

### Data Seeding

```bash
# Seed chapters and shlokas from JSON
python scripts/seed_content.py --source data/bhagavad_gita.json

# Verify audio files
python scripts/verify_audio.py --audio-dir audio/
```

### Monitoring

```python
# Metrics to track
metrics = {
    "content_api_requests": Counter,
    "cache_hit_rate": Gauge,
    "database_query_duration": Histogram,
    "audio_stream_errors": Counter,
    "rag_explanation_duration": Histogram
}
```

### Testing Strategy

**Unit Tests**:
- Content service logic
- Bookmark service logic
- Repository CRUD operations
- Cache service operations

**Integration Tests**:
- Chapter list endpoint
- Shloka list with bookmark status
- Shloka detail with AI explanation
- Bookmark CRUD operations
- Audio streaming

**Performance Tests**:
- 1000 concurrent shloka detail requests
- Cache performance under load
- Database query optimization
- Audio streaming bandwidth

**End-to-End Tests**:
- Complete user journey: browse → view → bookmark
- Offline mode functionality
- Audio playback across devices
