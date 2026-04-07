"""One-time ingestion pipeline: generate embeddings for all shlokas and build FAISS index."""
import json
import os

import numpy as np
from sqlalchemy import select

from app.database import async_session
from app.models.shloka import Shloka
from app.services.rag_service import _get_embedding_model, reload_index
from app.config import get_settings

settings = get_settings()


async def build_faiss_index() -> int:
    """
    Build FAISS index from all shlokas in the database.

    Steps:
    1. Load all shlokas from PostgreSQL
    2. Generate embeddings for each shloka (combining meaning + themes)
    3. Build FAISS flat L2 index
    4. Save index and ID mapping to disk

    Returns the number of shlokas indexed.
    """
    import faiss

    model = _get_embedding_model()

    async with async_session() as db:
        result = await db.execute(
            select(Shloka).order_by(Shloka.chapter, Shloka.shloka_number)
        )
        shlokas = list(result.scalars().all())

    if not shlokas:
        print("No shlokas found in database. Seed data first.")
        return 0

    # Generate embeddings
    texts = []
    for s in shlokas:
        # Combine meaning + themes for richer embedding
        themes = " ".join(s.themes) if s.themes else ""
        text = f"{s.meaning} {themes} {s.transliteration}"
        texts.append(text)

    print(f"Generating embeddings for {len(shlokas)} shlokas...")
    embeddings = model.encode(texts, show_progress_bar=True)
    embeddings = np.array(embeddings).astype("float32")

    # Build FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    # Ensure data directory exists
    os.makedirs(os.path.dirname(settings.faiss_index_path) or "data", exist_ok=True)

    # Save index
    faiss.write_index(index, settings.faiss_index_path)

    # Save mapping: FAISS index position -> shloka UUID
    mapping = {i: str(s.id) for i, s in enumerate(shlokas)}
    with open(settings.faiss_mapping_path, "w") as f:
        json.dump(mapping, f)

    # Update embedding_index on each shloka
    async with async_session() as db:
        for i, shloka in enumerate(shlokas):
            result = await db.execute(select(Shloka).where(Shloka.id == shloka.id))
            s = result.scalar_one()
            s.embedding_index = i
        await db.commit()

    reload_index()

    print(f"FAISS index built with {len(shlokas)} vectors (dimension={dimension}).")
    print(f"Saved to {settings.faiss_index_path}")
    return len(shlokas)


if __name__ == "__main__":
    import asyncio
    asyncio.run(build_faiss_index())
