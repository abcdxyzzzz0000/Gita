"""
Full Bhagavad Gita data ingestion script.

Fetches all ~700 verses from the public Vedic Scriptures API
(https://vedicscriptures.github.io) and seeds the database.

Usage:
    python -m app.seed_full
"""
import asyncio
import httpx
import time
import sys

from sqlalchemy import select, delete
from app.database import async_session, engine, Base
from app.models.chapter import Chapter
from app.models.shloka import Shloka

API_BASE = "https://vedicscriptures.github.io"

# Chapter metadata with English descriptions
CHAPTER_DESCRIPTIONS = {
    1: "Arjuna's moral crisis on the battlefield of Kurukshetra, where he sees his relatives and teachers arrayed against him and is overwhelmed with grief and doubt.",
    2: "Krishna teaches Arjuna about the eternal nature of the soul, the importance of duty, and introduces the paths of knowledge and selfless action.",
    3: "Krishna explains the importance of selfless action (Karma Yoga) - performing one's duty without attachment to results as the path to spiritual liberation.",
    4: "Krishna reveals the divine nature of his incarnations, the ancient tradition of spiritual knowledge, and how knowledge of the self burns away all karmic reactions.",
    5: "Krishna compares the paths of renunciation of action and selfless action, explaining that both lead to liberation when performed with the right understanding.",
    6: "Krishna describes the practice of meditation, self-discipline, and the qualities of a true yogi who has mastered the mind and senses.",
    7: "Krishna reveals both theoretical knowledge and experiential wisdom about the nature of reality, his divine energy, and why few truly know him.",
    8: "Krishna explains the imperishable Brahman, the process of attaining the supreme goal at the time of death, and the paths of light and darkness.",
    9: "Krishna shares the most confidential knowledge about his supreme nature, universal presence, and how simple devotion with love is the highest path.",
    10: "Krishna describes his divine manifestations throughout the universe, showing how he is the source and essence of everything magnificent in creation.",
    11: "Arjuna is granted divine vision to see Krishna's cosmic universal form containing the entire universe, all beings, and the flow of time itself.",
    12: "Krishna explains devotion (Bhakti) as the supreme path and describes the qualities that make a devotee most dear to him.",
    13: "Krishna explains the body as the field and the soul as the knower, distinguishing between matter, spirit, and the Supreme Spirit.",
    14: "Krishna describes the three qualities (gunas) of material nature - goodness, passion, and ignorance - and how they bind the soul to the material world.",
    15: "Krishna explains the metaphor of the sacred fig tree representing the material world, and reveals himself as the Supreme Person beyond both the perishable and imperishable.",
    16: "Krishna distinguishes between divine qualities that lead to liberation and demonic qualities that lead to bondage, urging Arjuna to cultivate divine nature.",
    17: "Krishna classifies faith, food, worship, charity, and austerity according to the three gunas, and explains the meaning of 'Om Tat Sat'.",
    18: "Krishna gives his final and most comprehensive teaching on renunciation, duty, the three gunas in all aspects of life, and ultimate surrender to the Divine.",
}


async def fetch_chapters() -> list[dict]:
    """Fetch all chapter metadata from the API."""
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{API_BASE}/chapters")
        resp.raise_for_status()
        return resp.json()


async def fetch_verse(chapter: int, verse: int, client: httpx.AsyncClient) -> dict | None:
    """Fetch a single verse from the API."""
    try:
        resp = await client.get(f"{API_BASE}/slok/{chapter}/{verse}")
        if resp.status_code == 200:
            return resp.json()
        return None
    except Exception as e:
        print(f"  Error fetching {chapter}:{verse} - {e}")
        return None


def extract_english_translation(verse_data: dict) -> str:
    """Extract the best English translation from the verse data."""
    tej = verse_data.get("tej", {})

    # Priority order for English translations
    for key in ["spiSp", "adi", "gambir", "purpiSp"]:
        if key in tej:
            author_data = tej[key]
            if isinstance(author_data, dict):
                et = author_data.get("et", "")
                if et:
                    return et.strip()

    # Fallback: try any key with 'et' field
    for key, val in tej.items():
        if isinstance(val, dict) and "et" in val and val["et"]:
            return val["et"].strip()

    return verse_data.get("transliteration", "Translation not available.")


def extract_themes(meaning: str) -> list[str]:
    """Extract theme keywords from the verse meaning."""
    theme_keywords = [
        "soul", "duty", "action", "knowledge", "devotion", "meditation",
        "peace", "war", "dharma", "karma", "yoga", "wisdom", "mind",
        "death", "birth", "eternal", "divine", "faith", "surrender",
        "detachment", "desire", "anger", "fear", "courage", "truth",
        "compassion", "love", "equanimity", "renunciation", "liberation",
        "self", "God", "nature", "gunas", "senses", "intellect",
        "happiness", "sorrow", "attachment", "ego", "humility",
        "sacrifice", "austerity", "charity", "patience", "forgiveness",
    ]
    meaning_lower = meaning.lower()
    return [t for t in theme_keywords if t in meaning_lower][:6]


async def seed_full_gita():
    """Main function to seed all Bhagavad Gita data."""
    print("=" * 60)
    print("  Bhagavad Gita Full Data Ingestion")
    print("=" * 60)

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Clear existing data
    async with async_session() as db:
        await db.execute(delete(Shloka))
        await db.execute(delete(Chapter))
        await db.commit()
        print("\nCleared existing data.")

    # Fetch chapter metadata
    print("\nFetching chapter metadata...")
    chapters_data = await fetch_chapters()
    print(f"  Found {len(chapters_data)} chapters.")

    # Seed chapters
    async with async_session() as db:
        for ch in chapters_data:
            ch_num = ch["chapter_number"]
            chapter = Chapter(
                id=ch_num,
                title=ch["meaning"]["en"],
                sanskrit_name=ch["transliteration"],
                description=CHAPTER_DESCRIPTIONS.get(ch_num, ch["summary"]["en"]),
                shloka_count=ch["verses_count"],
            )
            db.add(chapter)
        await db.commit()
        print(f"  Seeded {len(chapters_data)} chapters.\n")

    # Fetch and seed all verses
    total_verses = 0
    failed_verses = 0
    embedding_idx = 0

    async with httpx.AsyncClient(timeout=30) as client:
        for ch in chapters_data:
            ch_num = ch["chapter_number"]
            verse_count = ch["verses_count"]
            print(f"Chapter {ch_num:2d} ({ch['transliteration']:30s}) - {verse_count} verses ", end="", flush=True)

            chapter_shlokas = []

            for v_num in range(1, verse_count + 1):
                verse = await fetch_verse(ch_num, v_num, client)

                if verse:
                    sanskrit = verse.get("slok", "").strip()
                    transliteration = verse.get("transliteration", "").strip()
                    meaning = extract_english_translation(verse)
                    themes = extract_themes(meaning)

                    chapter_shlokas.append(
                        Shloka(
                            chapter=ch_num,
                            shloka_number=v_num,
                            sanskrit_text=sanskrit,
                            transliteration=transliteration,
                            meaning=meaning,
                            themes=themes if themes else None,
                            embedding_index=embedding_idx,
                        )
                    )
                    embedding_idx += 1
                    total_verses += 1
                else:
                    failed_verses += 1

                # Print progress dot every 10 verses
                if v_num % 10 == 0:
                    print(".", end="", flush=True)

                # Rate limit: small delay to be respectful to the API
                await asyncio.sleep(0.1)

            # Batch insert chapter's shlokas
            async with async_session() as db:
                for s in chapter_shlokas:
                    db.add(s)
                await db.commit()

            print(f" [{len(chapter_shlokas)}/{verse_count}]")

    print(f"\n{'=' * 60}")
    print(f"  DONE!")
    print(f"  Total verses seeded: {total_verses}")
    if failed_verses:
        print(f"  Failed verses:       {failed_verses}")
    print(f"{'=' * 60}")

    # Verify
    async with async_session() as db:
        ch_count = (await db.execute(select(Chapter))).scalars().all()
        sh_count = (await db.execute(select(Shloka))).scalars().all()
        print(f"\n  Database now has: {len(ch_count)} chapters, {len(sh_count)} shlokas")

    return total_verses


if __name__ == "__main__":
    start = time.time()
    count = asyncio.run(seed_full_gita())
    elapsed = time.time() - start
    print(f"\n  Completed in {elapsed:.1f} seconds.")
