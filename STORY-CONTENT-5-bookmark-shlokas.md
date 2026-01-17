# Story CONTENT-5: Bookmark Shlokas

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

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
