# RAG Engine Module - Sub-PRD

## Module Overview & Purpose

The RAG (Retrieval-Augmented Generation) Engine Module provides AI-powered explanations for Bhagavad Gita shlokas that are strictly grounded in the actual text to prevent hallucinations. It combines semantic search using FAISS vector store with LLM generation via Ollama (Mistral 7B) to deliver student-friendly explanations and contextual recommendations.

## Functional Requirements

### User Stories & Acceptance Criteria

#### US-RAG-1: Generate Shloka Explanation
**As a** user  
**I want** to receive AI-generated simple explanations for shlokas  
**So that** I can understand the wisdom in student-friendly language

**Acceptance Criteria:**
- Explanation generated within 2 seconds
- Language appropriate for 12-22 age group
- Explanation grounded strictly in retrieved Gita context
- No hallucinated information or external references
- Explanation includes practical application when relevant
- Clear "AI-generated" label displayed
- Fallback to cached or generic explanation on failure
- Explanation length: 150-300 words

#### US-RAG-2: Retrieve Relevant Shlokas
**As a** system  
**I want** to find semantically similar shlokas for context  
**So that** AI explanations are grounded in related verses

**Acceptance Criteria:**
- Semantic search returns top 3-5 most relevant shlokas
- Retrieval completes within 500ms
- Similarity scores above 0.6 threshold
- Results include full shloka details (Sanskrit, transliteration, meaning)
- Query embedding uses same model as shloka embeddings
- Results cached for identical queries

#### US-RAG-3: Life Guidance Recommendations
**As a** user  
**I want** to receive relevant shlokas for my life problems  
**So that** I can find practical wisdom for my current situation

**Acceptance Criteria:**
- Problem categories mapped to relevant query keywords
- Top 3-5 most relevant shlokas returned
- Each recommendation includes practical explanation
- Relevance score displayed for each recommendation
- Recommendations generated within 3 seconds
- Explanations focus on practical application to the problem
- No generic or irrelevant recommendations

#### US-RAG-4: Daily Wisdom Explanation
**As a** system  
**I want** to generate explanations for daily wisdom shlokas  
**So that** users receive meaningful daily content

**Acceptance Criteria:**
- Explanation emphasizes daily practical application
- Tone is inspirational and motivational
- Length optimized for mobile notification (100-150 words)
- Generated during off-peak hours (scheduled task)
- Cached for the entire day
- Fallback to pre-written explanation if generation fails

## Non-Functional Requirements

### Performance
- Total RAG response time: < 2 seconds (retrieval + generation)
- Retrieval time: < 500ms
- Generation time: < 1.5 seconds
- Embedding generation: < 100ms per query
- Cache hit rate: > 70%

### Accuracy
- Explanation relevance: > 90% (manual evaluation)
- No hallucinations: 100% (grounded in retrieved context)
- Semantic search precision: > 85%
- Life guidance relevance: > 80%

### Scalability
- Support 1000 explanation requests/hour
- FAISS index size: ~700 embeddings (all shlokas)
- Ollama concurrent requests: 5 (limited by GPU/CPU)
- Queue requests during high load

### Reliability
- Ollama availability: > 99%
- Fallback to cached explanations on failure
- Graceful degradation if LLM unavailable
- Automatic retry on transient failures

### Resource Usage
- FAISS index memory: < 100MB
- Ollama model memory: ~4GB (Mistral 7B)
- CPU usage: < 50% average
- GPU usage: Optional (CPU inference acceptable)

## API Contracts

### Internal API: generate_explanation()

**Function Signature:**
```python
def generate_explanation(
    shloka: Shloka,
    context_type: str = "general",  # "general", "daily_wisdom", "life_guidance"
    problem_context: Optional[str] = None
) -> str
```

**Input:**
```python
{
    "shloka": {
        "id": "uuid",
        "chapter": 2,
        "shlokaNumber": 47,
        "sanskritText": "कर्मण्येवाधिकारस्ते...",
        "transliteration": "karmaṇy-evādhikāras te...",
        "meaning": "You have a right to perform your duty..."
    },
    "context_type": "general",
    "problem_context": null
}
```

**Output:**
```python
"This verse teaches us about detachment from results. Krishna tells Arjuna that we should focus on doing our duty well, without worrying about success or failure. For students, this means studying sincerely without stressing about grades. The key is to give your best effort and let go of anxiety about outcomes."
```

### Internal API: retrieve_relevant_shlokas()

**Function Signature:**
```python
def retrieve_relevant_shlokas(
    query: str,
    top_k: int = 5,
    chapter_filter: Optional[int] = None
) -> List[Tuple[Shloka, float]]
```

**Input:**
```python
{
    "query": "dealing with stress and anxiety",
    "top_k": 5,
    "chapter_filter": null
}
```

**Output:**
```python
[
    (Shloka(chapter=2, shlokaNumber=47, ...), 0.85),
    (Shloka(chapter=6, shlokaNumber=35, ...), 0.78),
    (Shloka(chapter=2, shlokaNumber=14, ...), 0.72)
]
```

### Internal API: get_life_guidance_recommendations()

**Function Signature:**
```python
def get_life_guidance_recommendations(
    problem_id: str
) -> List[Dict[str, Any]]
```

**Input:**
```python
{
    "problem_id": "stress"
}
```

**Output:**
```python
[
    {
        "shloka": Shloka(...),
        "explanation": "When facing stress, this verse reminds us...",
        "relevanceScore": 0.85
    },
    {
        "shloka": Shloka(...),
        "explanation": "Krishna teaches that stress comes from...",
        "relevanceScore": 0.78
    }
]
```

## Error Handling & Edge Cases

### Error Scenarios

1. **Ollama Service Unavailable**
   - Error: Connection refused or timeout
   - Action: Return cached explanation or generic fallback
   - Log: Error logged for monitoring
   - Retry: Exponential backoff (3 attempts)

2. **Generation Timeout (>2s)**
   - Error: LLM generation exceeds time limit
   - Action: Cancel generation, return cached or fallback
   - Log: Timeout logged with shloka ID
   - Alert: Alert if timeout rate > 10%

3. **FAISS Index Corruption**
   - Error: Index file corrupted or missing
   - Action: Rebuild index from database
   - Log: Critical error logged
   - Downtime: ~5 minutes to rebuild

4. **Low Relevance Scores**
   - Scenario: All retrieved shlokas have score < 0.6
   - Action: Return top results anyway with disclaimer
   - Message: "These verses may be loosely related"

5. **Empty Query**
   - Error: Query string is empty or whitespace
   - Action: Return 400 Bad Request
   - Message: "Query cannot be empty"

6. **Embedding Generation Failure**
   - Error: Sentence-Transformers model error
   - Action: Retry once, then fail gracefully
   - Log: Error logged with query text

### Edge Cases

- Very long shloka text: Truncate to 500 characters for embedding
- Non-English query: Model handles multilingual (limited support)
- Duplicate queries: Serve from cache
- Concurrent requests for same shloka: Queue and deduplicate
- Model loading delay: Warm up model on startup
- Out of memory: Reduce batch size, queue requests

## Dependencies on Other Modules

### Internal Dependencies
- **Content Module**: Shloka data for retrieval and explanation
- **Database Module**: Shloka table for full text retrieval
- **Cache Module**: Redis for caching explanations and embeddings

### External Dependencies
- **FAISS**: Vector similarity search
- **Sentence-Transformers**: Embedding generation (all-MiniLM-L6-v2)
- **Ollama**: LLM inference (Mistral 7B)
- **PostgreSQL**: Shloka metadata and themes
- **Redis**: Explanation caching

## Assumptions & Constraints

### Assumptions
- Ollama service running locally or on same network
- FAISS index pre-built during setup
- All shlokas have embeddings in FAISS
- Mistral 7B model downloaded and available
- Sufficient CPU/RAM for inference (4GB+ RAM)
- Explanations in English only (Phase 1)

### Constraints
- LLM cannot be fine-tuned (using pre-trained Mistral)
- Embedding model fixed (all-MiniLM-L6-v2)
- Context window limited to 4096 tokens
- No real-time model updates
- Single Ollama instance (no load balancing in Phase 1)
- Explanations not editable by users

## Success Metrics

### Functional Metrics
- Explanation generation success rate: > 98%
- Retrieval accuracy (manual evaluation): > 85%
- Life guidance relevance (user feedback): > 80%
- Zero hallucination rate: 100%

### Performance Metrics
- Average explanation generation time: < 1.5 seconds
- Average retrieval time: < 300ms
- Cache hit rate: > 70%
- Ollama uptime: > 99%

### Quality Metrics
- Explanation readability (Flesch-Kincaid): Grade 8-10
- User satisfaction (ratings): > 4.0/5.0
- Explanation length compliance: > 95% within 150-300 words
- Practical applicability (user feedback): > 75%

## Traceability to Master PRD

- **FR4**: AI-powered simple explanation for shlokas
- **FR9**: Life Guidance feature with relevant shlokas and practical explanations
- **FR13**: RAG strictly constrained to retrieved Gita context
- **NFR2**: RAG responses within 2 seconds
- **NFR6**: Low infrastructure costs through open-source models
- **NFR7**: AI content grounded in actual Gita text, no hallucinations
- **Epic 2**: Content Ingestion & RAG Pipeline implementation
- **Epic 4**: Daily Wisdom & Life Guidance features
