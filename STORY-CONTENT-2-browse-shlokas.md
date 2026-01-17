# Story CONTENT-2: Browse Shloka List

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

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
