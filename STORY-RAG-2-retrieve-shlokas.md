# Story RAG-2: Retrieve Relevant Shlokas

**Priority:** High  
**Dependencies:** FAISS index setup, Embedding model

**User Story:**  
As a system, I want to find semantically similar shlokas for context, so that AI explanations are grounded in related verses.

**Acceptance Criteria:**
- Semantic search returns top 3-5 most relevant shlokas
- Retrieval completes within 500ms
- Similarity scores above 0.6 threshold
- Results include full shloka details (Sanskrit, transliteration, meaning)
- Query embedding uses same model as shloka embeddings
- Results cached for identical queries

**Definition of Done:**
- All stories follow the format: "As a [user type], I want [goal], so that [benefit]"
- Acceptance criteria are clear, testable, and specific
- Dependencies are explicitly stated to guide sprint planning
- Priorities align with MVP requirements and user value
- Stories are sized to be completable within a sprint
- Technical debt and infrastructure setup are considered in dependencies
