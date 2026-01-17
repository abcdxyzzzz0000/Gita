# Search & Profile Module - Sub-Architecture

## Module-Level Architecture Overview

The Search & Profile Module combines PostgreSQL full-text search with RAG semantic search for comprehensive search capabilities, and provides user profile management with statistics calculation and settings management.

```
┌────────────────────────────────────────────────────────┐
│                   API Layer                            │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │    Search    │  │   Profile    │  │  Settings   │ │
│  │  Endpoints   │  │  Endpoints   │  │  Endpoints  │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                 Service Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │    Search    │  │   Profile    │  │  Progress   │ │
│  │   Service    │  │   Service    │  │  Service    │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│              Repository Layer                          │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │    Search    │  │     User     │  │  Progress   │ │
│  │  Repository  │  │  Repository  │  │ Repository  │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                  Data Layer                            │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │PostgreSQL│  │  Redis   │  │   RAG    │           │
│  │(FTS+Data)│  │  Cache   │  │  Module  │           │
│  └──────────┘  └──────────┘  └──────────┘           │
└────────────────────────────────────────────────────────┘
```

## Internal Components & Responsibilities

### 1. Search Router (`search_router.py`)
**Endpoints**:
- `GET /api/search` - Keyword and semantic search

### 2. Profile Router (`profile_router.py`)
**Endpoints**:
- `GET /api/profile` - Get user profile with stats
- `PUT /api/profile/password` - Change password
- `DELETE /api/profile` - Delete account

### 3. Progress Router (`progress_router.py`)
**Endpoints**:
- `GET /api/progress` - Get reading progress
- `POST /api/progress` - Record shloka view

### 4. Search Service (`search_service.py`)
**Functions**:
- `search(query, limit)` - Combined keyword + semantic search
- `keyword_search(query)` - PostgreSQL full-text search
- `semantic_search(query)` - RAG-based similarity search
- `merge_and_rank_results(keyword_results, semantic_results)` - Combine results

### 5. Profile Service (`profile_service.py`)
**Functions**:
- `get_user_profile(user_id)` - Get profile with stats
- `calculate_statistics(user_id)` - Compute reading stats
- `change_password(user_id, current, new)` - Update password
- `delete_account(user_id)` - Remove user and data

### 6. Progress Service (`progress_service.py`)
**Functions**:
- `record_progress(user_id, chapter, shloka_number)` - Track reading
- `get_reading_progress(user_id)` - Get progress summary
- `calculate_chapter_progress(user_id)` - Chapter completion percentages
- `get_reading_streak(user_id)` - Calculate consecutive days

### 7. Search Repository (`search_repository.py`)
**Functions**:
- `full_text_search(query)` - PostgreSQL FTS query
- `search_by_themes(themes)` - Theme-based search

### 8. Progress Repository (`progress_repository.py`)
**Functions**:
- `create_or_update_progress(user_id, chapter, shloka_number)` - UPSERT
- `get_user_progress(user_id)` - Get all progress records
- `get_recently_read(user_id, limit)` - Recent shlokas
- `count_shlokas_read(user_id)` - Total count

## Data Flow

### Search Flow (Combined Keyword + Semantic)

```
1. Client → GET /api/search?q=dealing with stress
2. SearchRouter → SearchService.search("dealing with stress", limit=20)
3. SearchService → parallel execution:
   
   a. Keyword Search Path:
      - SearchRepository.full_text_search("dealing with stress")
      - PostgreSQL: SELECT * FROM shlokas 
        WHERE to_tsvector('english', meaning || ' ' || transliteration) 
        @@ to_tsquery('dealing & stress')
      - Returns: 5 results with text match scores
   
   b. Semantic Search Path:
      - RAGService.retrieve_relevant_shlokas("dealing with stress", top_k=10)
      - Generate query embedding
      - FAISS similarity search
      - Returns: 10 results with similarity scores
   
4. SearchService.merge_and_rank_results(keyword_results, semantic_results)
   - Combine results, remove duplicates
   - Calculate combined score: 0.6 * keyword_score + 0.4 * semantic_score
   - Sort by combined score descending
   - Take top 20 results
   
5. SearchService → highlight matched text in results
6. SearchService → CacheService.set_cached('search:{query_hash}', results, ttl=3600)
7. Return search results
```

### Profile with Statistics Flow

```
1. Client → GET /api/profile
2. ProfileRouter → AuthMiddleware (extract user_id)
3. ProfileRouter → ProfileService.get_user_profile(user_id)
4. ProfileService → parallel execution:
   
   a. User Data:
      - UserRepository.get_user_by_id(user_id)
      - PostgreSQL: SELECT * FROM users WHERE id=?
   
   b. Statistics:
      - ProfileService.calculate_statistics(user_id)
      - BookmarkRepository.count_bookmarks(user_id)
        → SELECT COUNT(*) FROM bookmarks WHERE user_id=?
      - ProgressRepository.count_shlokas_read(user_id)
        → SELECT COUNT(DISTINCT chapter, shloka_number) FROM reading_progress WHERE user_id=?
      - ProgressRepository.count_chapters_completed(user_id)
        → Complex query checking if all shlokas in chapter are read
      - ProgressRepository.count_active_days(user_id)
        → SELECT COUNT(DISTINCT DATE(last_read_at)) FROM reading_progress WHERE user_id=?
      - ProgressRepository.get_reading_streak(user_id)
        → Calculate consecutive days with activity
   
5. ProfileService → merge user data + statistics
6. ProfileService → CacheService.set_cached('profile:{user_id}', data, ttl=300)
7. Return profile data
```

### Reading Progress Recording Flow

```
1. Client → POST /api/progress {chapter: 2, shloka_number: 47}
2. ProgressRouter → AuthMiddleware (extract user_id)
3. ProgressRouter → ProgressService.record_progress(user_id, 2, 47)
4. ProgressService → ProgressRepository.create_or_update_progress(user_id, 2, 47)
5. ProgressRepository → PostgreSQL:
   INSERT INTO reading_progress (user_id, chapter, shloka_number, last_read_at)
   VALUES (?, ?, ?, NOW())
   ON CONFLICT (user_id, chapter, shloka_number)
   DO UPDATE SET last_read_at = NOW()
6. ProgressService → CacheService.invalidate_cache('profile:{user_id}')
7. ProgressService → CacheService.invalidate_cache('progress:{user_id}')
8. Return 201 Created
```

### Password Change Flow

```
1. Client → PUT /api/profile/password {currentPassword, newPassword}
2. ProfileRouter → AuthMiddleware (extract user_id)
3. ProfileRouter → ProfileService.change_password(user_id, current, new)
4. ProfileService → UserRepository.get_user_by_id(user_id)
5. ProfileService → PasswordHasher.verify_password(current, user.hashed_password)
6. If invalid → return 401 Unauthorized
7. ProfileService → PasswordHasher.hash_password(new)
8. ProfileService → UserRepository.update_user(user_id, {hashed_password: new_hash})
9. ProfileService → log password change event
10. Return 200 OK
```

## Database Schema / Tables Involved

### Full-Text Search Configuration

```sql
-- Add full-text search index to shlokas table
ALTER TABLE shlokas ADD COLUMN search_vector tsvector;

-- Create index for fast full-text search
CREATE INDEX idx_shlokas_search ON shlokas USING GIN(search_vector);

-- Update search vector on insert/update
CREATE TRIGGER shlokas_search_vector_update BEFORE INSERT OR UPDATE
ON shlokas FOR EACH ROW EXECUTE FUNCTION
tsvector_update_trigger(search_vector, 'pg_catalog.english', 
  sanskrit_text, transliteration, meaning);

-- Full-text search query
SELECT 
  id, chapter, shloka_number, sanskrit_text, transliteration, meaning,
  ts_rank(search_vector, query) AS rank
FROM shlokas, to_tsquery('english', 'duty & karma') query
WHERE search_vector @@ query
ORDER BY rank DESC
LIMIT 20;
```

### Reading Progress Table

```sql
CREATE TABLE reading_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    chapter INTEGER NOT NULL,
    shloka_number INTEGER NOT NULL,
    last_read_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_user_progress UNIQUE (user_id, chapter, shloka_number)
);

CREATE INDEX idx_progress_user ON reading_progress(user_id);
CREATE INDEX idx_progress_last_read ON reading_progress(last_read_at DESC);
CREATE INDEX idx_progress_user_date ON reading_progress(user_id, DATE(last_read_at));
```

### Statistics Queries

```sql
-- Bookmark count
SELECT COUNT(*) FROM bookmarks WHERE user_id = ?;

-- Shlokas read count
SELECT COUNT(DISTINCT (chapter, shloka_number)) 
FROM reading_progress 
WHERE user_id = ?;

-- Chapters completed
SELECT chapter 
FROM (
  SELECT chapter, COUNT(*) as read_count
  FROM reading_progress
  WHERE user_id = ?
  GROUP BY chapter
) progress
JOIN chapters ON progress.chapter = chapters.id
WHERE progress.read_count = chapters.shloka_count;

-- Days active
SELECT COUNT(DISTINCT DATE(last_read_at))
FROM reading_progress
WHERE user_id = ?;

-- Reading streak (consecutive days)
WITH daily_activity AS (
  SELECT DISTINCT DATE(last_read_at) as activity_date
  FROM reading_progress
  WHERE user_id = ?
  ORDER BY activity_date DESC
)
SELECT COUNT(*) as streak
FROM daily_activity
WHERE activity_date >= CURRENT_DATE - INTERVAL '1 day' * ROW_NUMBER() OVER (ORDER BY activity_date DESC);
```

## External Services Used

### PostgreSQL Full-Text Search

**Purpose**: Keyword-based search with ranking

**Features Used**:
- `tsvector` data type for indexed text
- `to_tsquery()` for query parsing
- `ts_rank()` for relevance scoring
- GIN index for fast search

**Performance**:
- Search time: < 100ms for 700 shlokas
- Index size: ~5MB
- Supports English stemming and stop words

### RAG Module (Semantic Search)

**Purpose**: Meaning-based search using embeddings

**Interface**:
- `retrieve_relevant_shlokas(query, top_k)` - Returns similar shlokas
- Uses FAISS vector similarity search
- Returns results with similarity scores (0-1)

**Integration**:
- Called in parallel with keyword search
- Results merged and re-ranked
- Adds semantic understanding to search

## Security Considerations

### Search Security
- Input sanitization to prevent SQL injection
- Query length limit (100 characters)
- Rate limiting: 100 searches/minute per user
- No sensitive data in search logs

### Profile Security
- User can only access their own profile
- Password change requires current password
- Account deletion requires re-authentication
- Audit log for profile changes

### Data Privacy
- Reading progress is private (not shared)
- Bookmarks are private
- Statistics aggregated, no raw data exposed
- GDPR compliance: account deletion removes all data

## Scalability & Failure Handling

### Scalability Strategies

**Search Optimization**:
- Full-text search index for fast keyword search
- Search result caching (1 hour TTL)
- Pagination for large result sets
- Parallel execution of keyword + semantic search

**Profile Optimization**:
- Statistics caching (5 minute TTL)
- Lazy calculation of expensive stats
- Database indexes on frequently queried columns
- Connection pooling

**Progress Tracking**:
- UPSERT for efficient progress updates
- Batch progress recording (future)
- Indexes on user_id and date columns

### Failure Handling

**Search Failures**:
- Semantic search timeout: Fall back to keyword search only
- Database error: Return cached results if available
- Empty results: Show helpful suggestions

**Profile Failures**:
- Statistics calculation error: Show partial data
- Database timeout: Retry with exponential backoff
- Cache unavailable: Query database directly

**Progress Recording Failures**:
- Database error: Queue for retry
- Duplicate progress: Handled by UPSERT
- Invalid shloka reference: Validate before insert

## Deployment Considerations

### Environment Variables

```bash
# Search Configuration
SEARCH_RESULT_LIMIT=20
SEARCH_CACHE_TTL=3600
SEARCH_TIMEOUT=1

# Profile Configuration
PROFILE_CACHE_TTL=300
STATS_CALCULATION_TIMEOUT=2

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/bhagavad_gita
DB_POOL_SIZE=10
```

### Database Migrations

```bash
# Create full-text search index
alembic revision -m "add_fulltext_search_index"

# Create reading progress table
alembic revision -m "create_reading_progress_table"

# Add statistics indexes
alembic revision -m "add_statistics_indexes"
```

### Monitoring

```python
metrics = {
    "search_duration": Histogram,
    "search_result_count": Histogram,
    "profile_load_duration": Histogram,
    "stats_calculation_duration": Histogram,
    "progress_recording_duration": Histogram,
    "search_cache_hit_rate": Gauge
}
```

### Testing Strategy

**Unit Tests**:
- Search result merging and ranking
- Statistics calculation logic
- Progress recording logic
- Password change validation

**Integration Tests**:
- Full-text search with database
- Semantic search with RAG module
- Profile endpoint with statistics
- Progress recording with database

**Performance Tests**:
- 1000 concurrent searches
- Statistics calculation under load
- Progress recording throughput
- Cache performance

**End-to-End Tests**:
- Complete search journey
- Profile view and update
- Reading progress tracking
- Account deletion
