"""
Seed the database from the downloaded JSON file.
Run download_gita_data.py first, then this script.

Usage:
    python scripts/seed_from_json.py
"""
import asyncio
import json
import os
import sys

# Add parent dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy import select, delete
from app.database import async_session, engine, Base
from app.models.chapter import Chapter
from app.models.shloka import Shloka

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bhagavad_gita_complete.json")


async def seed():
    if not os.path.exists(DATA_PATH):
        print(f"Data file not found: {DATA_PATH}")
        print("Run 'python scripts/download_gita_data.py' first.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"Loaded {len(data['chapters'])} chapters, {len(data['shlokas'])} shlokas from JSON.")

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Clear existing
    async with async_session() as db:
        await db.execute(delete(Shloka))
        await db.execute(delete(Chapter))
        await db.commit()

    # Seed chapters
    async with async_session() as db:
        for ch in data["chapters"]:
            db.add(Chapter(**ch))
        await db.commit()
        print(f"Seeded {len(data['chapters'])} chapters.")

    # Seed shlokas in batches
    async with async_session() as db:
        for idx, sh in enumerate(data["shlokas"]):
            db.add(Shloka(
                chapter=sh["chapter"],
                shloka_number=sh["shloka_number"],
                sanskrit_text=sh["sanskrit_text"],
                transliteration=sh["transliteration"],
                meaning=sh["meaning"],
                themes=sh.get("themes"),
                embedding_index=idx,
            ))

            if (idx + 1) % 100 == 0:
                await db.flush()
                print(f"  {idx + 1}/{len(data['shlokas'])} shlokas...")

        await db.commit()
        print(f"Seeded {len(data['shlokas'])} shlokas. Done!")


if __name__ == "__main__":
    asyncio.run(seed())
