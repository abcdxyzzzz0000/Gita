# Story SEARCH-2: Semantic Search

**Priority:** Medium  
**Dependencies:** SEARCH-1, RAG-2 (FAISS embeddings)

**User Story:**  
As a user, I want search results to understand meaning, not just keywords, so that I find relevant verses even with different wording.

**Acceptance Criteria:**
- Semantic similarity search using RAG embeddings
- Results include conceptually similar shlokas
- Combined ranking: keyword match + semantic similarity
- Works with natural language queries
- Example: "dealing with stress" finds shlokas about peace, calm, equanimity

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
