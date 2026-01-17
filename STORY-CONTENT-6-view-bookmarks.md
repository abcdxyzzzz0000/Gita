# Story CONTENT-6: View Bookmarked Shlokas

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

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
