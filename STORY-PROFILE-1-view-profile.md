# Story PROFILE-1: View Profile

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

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
