# RAG Engine Module - Sub-Architecture

## Module-Level Architecture Overview

The RAG Engine implements a retrieval-augmented generation pipeline combining FAISS vector search with Ollama LLM inference. The architecture ensures sub-2-second response times through aggressive caching and optimized retrieval strategies.

```
┌────────────────────────────────────────────────────────┐
│                   RAG Service Layer                    │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │ Explanation  │  │  Retrieval   │  │   Life      │ │
│  │  Generator   │  │   Engine     │  │  Guidance   │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                  Core Components                       │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │   Embedding  │  │    Prompt    │  │    Cache    │ │
│  │   Generator  │  │   Builder    │  │   Manager   │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────────┘
                          │
┌────────────────────────────────────────────────────────┐
│                  External Services                     │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────┐ │
│  │    FAISS     │  │    Ollama    │  │    Redis    │ │
│  │ Vector Store │  │  (Mistral)   │  │    Cache    │ │
│  └──────────────┘  └──────────────┘  └─────────────┘ │
└────────────────────────────────────────────────────────┘
```

## Internal Components & Responsibilities

### 1. RAG Service (`rag_service.py`)
**Responsibility**: Orchestrate RAG pipeline and expose high-level API

**Functions**:
- `generate_explanation(shloka, context_type, problem_context)` - Main explanation generation
- `get_life_guidance_recommendations(problem_id)` - Life guidance feature
- `generate_daily_wisdom_explanation(shloka)` - Daily wisdom specific

**Dependencies**: RetrievalEngine, PromptBuilder, OllamaClient, CacheManager

### 2. Retrieval Engine (`retrieval_engine.py`)
**Responsibility**: Semantic search using FAISS vector store

**Functions**:
- `retrieve_similar_shlokas(query, top_k, chapter_filter)` - Semantic search
- `retrieve_by_themes(themes, top_k)` - Theme-based retrieval
- `get_shloka_embedding(shloka_id)` - Get pre-computed embedding

**Dependencies**: FAISSIndex, EmbeddingGenerator, ShlokaRepository

### 3. Embedding Generator (`embedding_generator.py`)
**Responsibility**: Generate embeddings using Sentence-Transformers

**Functions**:
- `generate_query_embedding(text)` - Embed user query
- `generate_shloka_embedding(shloka)` - Embed shloka content
- `batch_generate_embeddings(texts)` - Batch processing for efficiency

**Dependencies**: Sentence-Transformers (all-MiniLM-L6-v2 model)

### 4. FAISS Index Manager (`faiss_index.py`)
**Responsibility**: Manage FAISS vector store operations

**Functions**:
- `load_index(index_path)` - Load pre-built FAISS index
- `search(query_embedding, top_k)` - Similarity search
- `get_metadata(index_id)` - Retrieve shloka metadata
- `rebuild_index(shlokas)` - Rebuild index from scratch

**Dependencies**: FAISS library, NumPy

### 5. Prompt Builder (`prompt_builder.py`)
**Responsibility**: Construct prompts for LLM with retrieved context

**Functions**:
- `build_explanation_prompt(shloka, context_shlokas, context_type)` - General explanation
- `build_life_guidance_prompt(shloka, problem, context_shlokas)` - Problem-specific
- `build_daily_wisdom_prompt(shloka, context_shlokas)` - Daily wisdom

**Dependencies**: Jinja2 templates

### 6. Ollama Client (`ollama_client.py`)
**Responsibility**: Interface with Ollama LLM service

**Functions**:
- `generate(prompt, max_tokens, temperature)` - Generate text
- `generate_streaming(prompt)` - Stream generation (future)
- `health_check()` - Check Ollama availability

**Dependencies**: httpx library, Ollama service

### 7. Cache Manager (`cache_manager.py`)
**Responsibility**: Cache explanations and embeddings

**Functions**:
- `get_cached_explanation(shloka_id, context_type)` - Retrieve cached
- `cache_explanation(shloka_id, context_type, explanation, ttl)` - Store
- `get_cached_embedding(text_hash)` - Retrieve cached embedding
- `invalidate_cache(pattern)` - Clear cache entries

**Dependencies**: Redis

## Data Flow

### Explanation Generation Flow

```
1. RAGService.generate_explanation(shloka, "general", None)
2. CacheManager.get_cached_explanation(shloka.id, "general")
3. If cache hit → return cached explanation (< 50ms)
4. If cache miss:
   a. EmbeddingGenerator.generate_shloka_embedding(shloka)
      - Combine sanskrit_text + transliteration + meaning
      - model.encode(combined_text) → embedding vector (384 dims)
      - Time: ~50ms
   
   b. RetrievalEngine.retrieve_similar_shlokas(shloka, top_k=3)
      - FAISSIndex.search(embedding, k=3)
      - FAISS similarity search → top 3 indices + scores
      - Time: ~100ms
      - Get full shloka details from metadata
   
   c. PromptBuilder.build_explanation_prompt(shloka, context_shlokas, "general")
      - Load template: explanation_template.jinja2
      - Inject target shloka and context shlokas
      - Add constraints: "Use only the provided verses", "Student-friendly language"
      - Add instructions: "150-300 words", "Practical application"
      - Time: ~10ms
   
   d. OllamaClient.generate(prompt, max_tokens=400, temperature=0.7)
      - POST to http://localhost:11434/api/generate
      - Request: {model: "mistral:7b", prompt: "...", options: {...}}
      - Ollama inference with Mistral 7B
      - Time: ~1000-1500ms (depends on CPU/GPU)
      - Response: generated explanation text
   
   e. Post-processing:
      - Trim to 300 words if exceeded
      - Remove any external references
      - Validate no hallucinations (basic checks)
   
   f. CacheManager.cache_explanation(shloka.id, "general", explanation, ttl=86400)
      - Redis SET with 24-hour expiration
   
5. Return explanation
6. Total time: ~1.5-2 seconds (first request), < 50ms (cached)
```

### Life Guidance Recommendations Flow

```
1. RAGService.get_life_guidance_recommendations("stress")
2. Map problem to keywords:
   - "stress" → ["peace", "calm", "equanimity", "tranquility", "mental stability"]
3. EmbeddingGenerator.generate_query_embedding(keywords_text)
   - Combine keywords into query string
   - Generate embedding
4. RetrievalEngine.retrieve_similar_shlokas(query, top_k=5)
   - FAISS search returns top 5 relevant shlokas
5. For each retrieved shloka:
   a. Check cache: CacheManager.get_cached_explanation(shloka.id, "life_guidance_stress")
   b. If cache miss:
      - PromptBuilder.build_life_guidance_prompt(shloka, "stress", context_shlokas)
      - Add problem-specific instructions: "Focus on practical stress management"
      - OllamaClient.generate(prompt)
   c. Combine shloka + explanation + relevance_score
6. Return list of recommendations
7. Total time: ~3 seconds (5 shlokas, some cached)
```

### FAISS Index Building (One-time Setup)

```
1. ShlokaRepository.get_all_shlokas() → 700 shlokas
2. For each shloka:
   a. Combine sanskrit_text + transliteration + meaning
   b. EmbeddingGenerator.generate_shloka_embedding(shloka)
   c. Store embedding in array
3. Create FAISS index:
   - faiss.IndexFlatL2(384) → L2 distance metric
   - index.add(embeddings_array)
4. Save metadata mapping:
   - {index_id: shloka_id} for lookup
5. Persist index to disk:
   - faiss.write_index(index, "faiss_index.bin")
6. Total time: ~5 minutes for 700 shlokas
```

## Database Schema / Tables Involved

### Shlokas Table (Read-Only)

```sql
SELECT 
    id, 
    chapter, 
    shloka_number, 
    sanskrit_text, 
    transliteration, 
    meaning, 
    themes,
    embedding_index
FROM shlokas
WHERE id = ?;
```

**Usage**: Retrieve full shloka details after FAISS search returns indices

### Life Guidance Problems (Configuration)

```python
# Stored in code or config file, not database
PROBLEM_KEYWORDS = {
    "stress": ["peace", "calm", "equanimity", "tranquility"],
    "fear": ["courage", "fearlessness", "strength", "confidence"],
    "confusion": ["clarity", "wisdom", "knowledge", "understanding"],
    "anger": ["patience", "forgiveness", "self-control", "peace"],
    "sadness": ["joy", "contentment", "acceptance", "hope"],
    "purpose": ["dharma", "duty", "purpose", "meaning"],
    "relationships": ["love", "compassion", "understanding", "harmony"],
    "decision-making": ["wisdom", "discernment", "clarity", "judgment"]
}
```

## External Services Used

### FAISS (Facebook AI Similarity Search)

**Purpose**: Fast vector similarity search

**Configuration**:
- Index type: IndexFlatL2 (exact search, no approximation)
- Dimension: 384 (all-MiniLM-L6-v2 embedding size)
- Distance metric: L2 (Euclidean distance)
- Index size: ~2MB for 700 vectors

**Operations**:
- `index.search(query_embedding, k)` - Find k nearest neighbors
- Time complexity: O(n) for exact search (acceptable for 700 vectors)
- Memory: Loaded into RAM on startup

**Scaling Considerations**:
- For > 10,000 vectors: Use IndexIVFFlat (approximate search)
- For > 100,000 vectors: Use IndexIVFPQ (product quantization)

### Sentence-Transformers (all-MiniLM-L6-v2)

**Purpose**: Generate text embeddings

**Model Details**:
- Model: sentence-transformers/all-MiniLM-L6-v2
- Embedding dimension: 384
- Max sequence length: 256 tokens
- Model size: ~80MB
- Inference time: ~50ms per text (CPU)

**Usage**:
```python
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')
embedding = model.encode(text, convert_to_numpy=True)
```

**Advantages**:
- Fast inference on CPU
- Good semantic understanding
- Multilingual support (limited)
- Open-source, no API costs

### Ollama (Mistral 7B)

**Purpose**: LLM inference for text generation

**Configuration**:
- Model: mistral:7b (7 billion parameters)
- Quantization: Q4_K_M (4-bit quantization)
- Memory: ~4GB RAM
- Context window: 4096 tokens
- Temperature: 0.7 (balanced creativity/consistency)

**API Endpoint**:
```
POST http://localhost:11434/api/generate
{
  "model": "mistral:7b",
  "prompt": "...",
  "options": {
    "temperature": 0.7,
    "top_p": 0.9,
    "max_tokens": 400
  }
}
```

**Response Time**:
- CPU inference: 1-2 seconds
- GPU inference: 500-800ms (if available)

**Error Handling**:
- Connection timeout: 5 seconds
- Generation timeout: 3 seconds
- Retry: 2 attempts with exponential backoff

### Redis Cache

**Purpose**: Cache explanations and embeddings

**Cache Keys**:
- `explanation:{shloka_id}:{context_type}` - Cached explanations
- `embedding:{text_hash}` - Cached embeddings
- `life_guidance:{problem_id}` - Cached recommendations

**TTL (Time To Live)**:
- Explanations: 24 hours (86400 seconds)
- Embeddings: 7 days (604800 seconds)
- Life guidance: 1 hour (3600 seconds)

**Memory Usage**:
- Average explanation: ~500 bytes
- Average embedding: ~1.5KB (384 floats)
- Expected cache size: ~50MB for 10,000 cached items

## Security Considerations

### Input Validation
- Query text sanitized (remove special characters)
- Maximum query length: 500 characters
- Shloka ID validated (UUID format)
- Problem ID validated (whitelist of allowed values)

### Prompt Injection Prevention
- User input not directly inserted into prompts
- Prompts use templates with escaped variables
- LLM output validated for unexpected content

### Resource Protection
- Rate limiting: 100 RAG requests/minute per user
- Queue requests during high load
- Timeout enforcement (2 seconds max)
- Memory limits for FAISS and Ollama

### Data Privacy
- No user data in prompts (only shloka content)
- Explanations not personalized (same for all users)
- No logging of generated explanations (only metadata)

## Scalability & Failure Handling

### Scalability Strategies

**Caching**:
- 70%+ cache hit rate reduces LLM load
- Explanations cached for 24 hours
- Embeddings cached for 7 days
- Pre-generate explanations for popular shlokas

**Request Queuing**:
- Ollama limited to 5 concurrent requests
- Queue additional requests with timeout
- Priority queue: daily wisdom > life guidance > general

**Horizontal Scaling**:
- FAISS index replicated across instances
- Ollama instances load-balanced (future)
- Redis cache shared across instances

**Performance Optimization**:
- Batch embedding generation where possible
- FAISS index loaded once on startup
- Connection pooling for Ollama requests

### Failure Handling

**Ollama Unavailable**:
- Health check every 30 seconds
- Circuit breaker: Stop requests after 5 failures
- Fallback: Return cached explanation or generic message
- Alert: Notify ops team

**FAISS Index Corruption**:
- Validate index on startup
- Rebuild from database if corrupted
- Downtime: ~5 minutes
- Backup index stored for quick recovery

**Embedding Generation Failure**:
- Retry once with exponential backoff
- Fallback: Use pre-computed embedding if available
- Log error for monitoring

**Generation Timeout**:
- Cancel request after 2 seconds
- Return cached explanation if available
- Log timeout for analysis
- Alert if timeout rate > 10%

**Redis Cache Failure**:
- Degrade gracefully (no caching)
- All requests go to LLM (slower)
- Monitor LLM load increase
- Alert ops team

## Deployment Considerations

### Environment Variables

```bash
# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b
OLLAMA_TIMEOUT=3
OLLAMA_MAX_TOKENS=400
OLLAMA_TEMPERATURE=0.7

# FAISS Configuration
FAISS_INDEX_PATH=/app/data/faiss_index.bin
FAISS_METADATA_PATH=/app/data/faiss_metadata.json

# Sentence-Transformers
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
EMBEDDING_CACHE_DIR=/app/models

# Redis Cache
REDIS_URL=redis://localhost:6379/1
CACHE_TTL_EXPLANATIONS=86400
CACHE_TTL_EMBEDDINGS=604800

# Performance
RAG_TIMEOUT=2
RAG_MAX_CONCURRENT=5
```

### Docker Configuration

```yaml
# docker-compose.yml
services:
  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    command: serve
    
  backend:
    depends_on:
      - ollama
    volumes:
      - ./data:/app/data  # FAISS index
      - ./models:/app/models  # Sentence-Transformers cache
    environment:
      - OLLAMA_BASE_URL=http://ollama:11434
```

### Model Setup

```bash
# Download Ollama model
docker exec ollama ollama pull mistral:7b

# Download Sentence-Transformers model
python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Build FAISS index
python scripts/build_faiss_index.py --source data/shlokas.json --output data/faiss_index.bin
```

### Monitoring

```python
# Metrics to track
metrics = {
    "rag_explanation_duration": Histogram,
    "rag_retrieval_duration": Histogram,
    "rag_generation_duration": Histogram,
    "rag_cache_hit_rate": Gauge,
    "ollama_availability": Gauge,
    "faiss_search_duration": Histogram,
    "rag_timeout_rate": Counter
}
```

### Testing Strategy

**Unit Tests**:
- Embedding generation
- Prompt building
- Cache operations
- FAISS search logic

**Integration Tests**:
- End-to-end RAG pipeline
- Ollama integration (mocked)
- FAISS retrieval accuracy
- Cache integration

**Performance Tests**:
- 100 concurrent explanation requests
- Cache performance under load
- Ollama throughput
- FAISS search latency

**Quality Tests**:
- Manual evaluation of explanations
- Hallucination detection
- Relevance scoring
- Student-friendliness assessment
