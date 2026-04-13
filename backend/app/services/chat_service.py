"""Chat service using ChromaDB RAG from the chatbot module."""
import os
from typing import Optional

import chromadb
from app.config import get_settings

settings = get_settings()

# Path to the chatbot's ChromaDB data
CHROMADB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "..", "chatbot", "gita_chromadb")

_chroma_client = None
_collection = None


def _get_collection():
    """Lazy-load ChromaDB collection from the chatbot's persisted data."""
    global _chroma_client, _collection
    if _collection is None:
        path = os.path.abspath(CHROMADB_PATH)
        if not os.path.exists(path):
            return None
        _chroma_client = chromadb.PersistentClient(path=path)
        try:
            _collection = _chroma_client.get_collection("bhagavad_gita")
        except Exception:
            # Collection doesn't exist yet
            return None
    return _collection


def search_passages(query: str, n_results: int = 3) -> list[dict]:
    """Search ChromaDB for relevant Gita passages."""
    collection = _get_collection()
    if collection is None or collection.count() == 0:
        return []

    results = collection.query(query_texts=[query], n_results=n_results)

    passages = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        passages.append({
            "text": doc,
            "metadata": meta,
            "relevance_score": round(1 - dist, 3) if dist < 1 else 0.0,
        })
    return passages


def _build_chat_prompt(query: str, passages: list[dict]) -> str:
    """Build the LLM prompt with retrieved context."""
    context = "\n\n".join(
        f"Passage {i+1}: {p['text']}" for i, p in enumerate(passages)
    )
    return f"""You are a wise and knowledgeable assistant specializing in the Bhagavad Gita.
Answer the user's question based on the following passages from the Bhagavad Gita.
Be respectful, insightful, and provide wisdom from the text.
If the passages don't contain relevant information, say so politely.
Keep your response concise (under 300 words).

CONTEXT FROM BHAGAVAD GITA:
{context}

USER'S QUESTION: {query}

ANSWER:"""


async def generate_chat_response(query: str) -> dict:
    """
    Full RAG pipeline: retrieve passages + generate LLM response.

    Tries Groq first, then Ollama, then falls back to showing passages.
    """
    passages = search_passages(query, n_results=3)

    if not passages:
        return {
            "response": "I don't have Bhagavad Gita data loaded yet. Please load the PDF first using the chatbot setup.",
            "passages": [],
        }

    prompt = _build_chat_prompt(query, passages)
    response_text = None

    # Try Groq (free, fast)
    groq_key = settings.groq_api_key or os.getenv("GROQ_API_KEY")
    if groq_key:
        try:
            from groq import Groq
            client = Groq(api_key=groq_key)
            completion = client.chat.completions.create(
                model=settings.groq_model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=1000,
                temperature=0.7,
            )
            response_text = completion.choices[0].message.content
        except Exception as e:
            print(f"[chat] Groq call failed: {e}")

    # Try Ollama
    if response_text is None:
        try:
            import ollama as ollama_client
            result = ollama_client.generate(
                model=settings.ollama_model,
                prompt=prompt,
                options={"temperature": 0.7, "num_predict": 500},
            )
            response_text = result["response"].strip()
        except Exception:
            pass

    # Fallback: return passages directly
    if response_text is None:
        passage_text = "\n\n".join(
            f"**Passage {i+1}:** {p['text']}" for i, p in enumerate(passages)
        )
        response_text = f"Here are relevant passages from the Bhagavad Gita:\n\n{passage_text}"

    return {
        "response": response_text,
        "passages": [
            {"text": p["text"], "relevance_score": p["relevance_score"]}
            for p in passages
        ],
    }
