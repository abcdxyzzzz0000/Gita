# Story AUTH-4: Anonymous Read-Only Access

**Priority:** Medium  
**Dependencies:** Content browsing endpoints

**User Story:**  
As a visitor, I want to browse content without authentication, so that I can explore the app before registering.

**Acceptance Criteria:**
- Chapter and shloka endpoints accessible without token
- Bookmark and profile endpoints require authentication
- Anonymous users see "Sign in to bookmark" prompts
- No user-specific data returned for anonymous requests

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
