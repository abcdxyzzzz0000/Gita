"""RAG service for AI-powered shloka explanations using FAISS + Ollama."""
import json
import os
from typing import Any

import numpy as np
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.models.shloka import Shloka

settings = get_settings()

# Lazy-loaded globals to avoid import-time heavy lifting
_embedding_model = None
_faiss_index = None
_index_mapping = None


def _get_embedding_model():
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        _embedding_model = SentenceTransformer(settings.embedding_model)
    return _embedding_model


def _get_faiss_index():
    global _faiss_index
    if _faiss_index is None:
        import faiss
        if os.path.exists(settings.faiss_index_path):
            _faiss_index = faiss.read_index(settings.faiss_index_path)
    return _faiss_index


def _get_index_mapping() -> dict[int, str]:
    global _index_mapping
    if _index_mapping is None:
        if os.path.exists(settings.faiss_mapping_path):
            with open(settings.faiss_mapping_path, "r") as f:
                raw = json.load(f)
                _index_mapping = {int(k): v for k, v in raw.items()}
        else:
            _index_mapping = {}
    return _index_mapping


def reload_index():
    """Reload FAISS index and mapping after ingestion."""
    global _faiss_index, _index_mapping
    _faiss_index = None
    _index_mapping = None
    _get_faiss_index()
    _get_index_mapping()


def generate_embedding(text: str) -> np.ndarray:
    model = _get_embedding_model()
    return model.encode([text])[0].astype("float32")


async def retrieve_similar_shlokas(
    db: AsyncSession,
    query: str,
    top_k: int = 5,
    exclude_id: str | None = None,
    min_score: float = 0.0,
) -> list[dict[str, Any]]:
    """
    Retrieve semantically similar shlokas using FAISS vector search.

    Returns list of {"shloka": Shloka, "relevance_score": float}.
    """
    index = _get_faiss_index()
    mapping = _get_index_mapping()

    if index is None or not mapping:
        return []

    query_vec = generate_embedding(query)
    query_vec = np.array([query_vec]).astype("float32")

    distances, indices = index.search(query_vec, top_k + 5)

    results: list[dict[str, Any]] = []
    for idx, distance in zip(indices[0], distances[0]):
        if int(idx) == -1:
            continue
        shloka_id = mapping.get(int(idx))
        if not shloka_id or shloka_id == exclude_id:
            continue
        score = float(1 / (1 + distance))
        if score < min_score:
            continue

        result = await db.execute(select(Shloka).where(Shloka.id == shloka_id))
        shloka = result.scalar_one_or_none()
        if shloka:
            results.append({"shloka": shloka, "relevance_score": score})
        if len(results) >= top_k:
            break

    return results


def _build_explanation_prompt(shloka: Shloka, related: list[dict]) -> str:
    context_text = "\n\n".join(
        f"Related Verse {i+1}:\n"
        f"Sanskrit: {s['shloka'].sanskrit_text}\n"
        f"Meaning: {s['shloka'].meaning}"
        for i, s in enumerate(related)
    )

    return f"""You are a wise teacher explaining the Bhagavad Gita to students aged 12-22.

CRITICAL RULES:
1. Base your explanation ONLY on the verse provided and related verses below
2. Do NOT add information not present in these verses
3. Use simple, student-friendly language
4. Keep explanation between 150-300 words
5. Focus on practical wisdom applicable to daily life
6. Do NOT mention that you are an AI

TARGET VERSE:
Chapter {shloka.chapter}, Verse {shloka.shloka_number}
Sanskrit: {shloka.sanskrit_text}
Transliteration: {shloka.transliteration}
Meaning: {shloka.meaning}

RELATED VERSES FOR CONTEXT:
{context_text if context_text else "No additional context available."}

Provide a clear, simple explanation of what this verse teaches, using only the information from the verses above. Make it relatable to a student's life.

Explanation:"""


def _fallback_explanation(shloka: Shloka) -> str:
    return (
        f"This verse from Chapter {shloka.chapter}, Verse {shloka.shloka_number} teaches: "
        f"{shloka.meaning}\n\n"
        "This is a core teaching of the Bhagavad Gita that encourages us to reflect "
        "on our actions and their deeper meaning in everyday life."
    )


async def generate_explanation(
    db: AsyncSession,
    shloka: Shloka,
    use_cache: bool = True,
) -> str:
    """
    Generate an AI explanation for a shloka using RAG pipeline.

    1. Retrieve related shlokas via FAISS
    2. Build constrained prompt
    3. Generate via Ollama LLM
    4. Fallback to basic explanation on failure
    """
    # Check Redis cache first
    if use_cache:
        cached = await _get_cached_explanation(str(shloka.id))
        if cached:
            return cached

    # Step 1: Retrieve context
    related = await retrieve_similar_shlokas(
        db,
        query=f"{shloka.sanskrit_text} {shloka.meaning}",
        top_k=settings.rag_context_size,
        exclude_id=str(shloka.id),
    )

    # Step 2: Build prompt
    prompt = _build_explanation_prompt(shloka, related)

    # Step 3: Generate with Ollama
    try:
        import ollama as ollama_client

        response = ollama_client.generate(
            model=settings.ollama_model,
            prompt=prompt,
            options={
                "temperature": settings.rag_temperature,
                "top_p": 0.9,
                "num_predict": settings.rag_max_tokens,
            },
        )
        explanation = response["response"].strip()
    except Exception:
        explanation = _fallback_explanation(shloka)

    # Cache result
    await _cache_explanation(str(shloka.id), explanation)

    return explanation


async def _get_cached_explanation(shloka_id: str) -> str | None:
    try:
        import redis.asyncio as aioredis

        r = aioredis.from_url(settings.redis_url)
        cached = await r.get(f"explanation:{shloka_id}")
        await r.aclose()
        if cached:
            return cached.decode("utf-8")
    except Exception:
        pass
    return None


async def _cache_explanation(shloka_id: str, explanation: str) -> None:
    try:
        import redis.asyncio as aioredis

        r = aioredis.from_url(settings.redis_url)
        await r.set(f"explanation:{shloka_id}", explanation, ex=86400)  # 24h cache
        await r.aclose()
    except Exception:
        pass
