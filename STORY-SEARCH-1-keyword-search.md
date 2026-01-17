# Story SEARCH-1: Keyword Search

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

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
