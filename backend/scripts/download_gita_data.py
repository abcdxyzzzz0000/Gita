"""
Download all Bhagavad Gita verses from the Vedic Scriptures API
and save to a JSON file. No database required.

Usage:
    python scripts/download_gita_data.py

Output:
    data/bhagavad_gita_complete.json
"""
import asyncio
import json
import os
import time

import httpx

API_BASE = "https://vedicscriptures.github.io"

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

THEME_KEYWORDS = [
    "soul", "duty", "action", "knowledge", "devotion", "meditation",
    "peace", "war", "dharma", "karma", "yoga", "wisdom", "mind",
    "death", "birth", "eternal", "divine", "faith", "surrender",
    "detachment", "desire", "anger", "fear", "courage", "truth",
    "compassion", "love", "equanimity", "renunciation", "liberation",
    "self", "God", "nature", "gunas", "senses", "intellect",
    "happiness", "sorrow", "attachment", "ego", "humility",
    "sacrifice", "austerity", "charity", "patience", "forgiveness",
]


def extract_english_translation(verse_data: dict) -> str:
    tej = verse_data.get("tej", {})
    for key in ["spiSp", "adi", "gambir", "purpiSp"]:
        if key in tej:
            author_data = tej[key]
            if isinstance(author_data, dict):
                et = author_data.get("et", "")
                if et:
                    return et.strip()
    for key, val in tej.items():
        if isinstance(val, dict) and "et" in val and val["et"]:
            return val["et"].strip()
    return "Translation not available."


def extract_themes(meaning: str) -> list[str]:
    meaning_lower = meaning.lower()
    return [t for t in THEME_KEYWORDS if t in meaning_lower][:6]


async def download_all():
    print("=" * 60)
    print("  Downloading Complete Bhagavad Gita Data")
    print("=" * 60)

    async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
        # Fetch chapters
        print("\nFetching chapters...")
        resp = await client.get(f"{API_BASE}/chapters")
        resp.raise_for_status()
        chapters_api = resp.json()

        all_data = {"chapters": [], "shlokas": []}
        total = 0

        for ch in chapters_api:
            ch_num = ch["chapter_number"]
            verse_count = ch["verses_count"]

            chapter_entry = {
                "id": ch_num,
                "title": ch["meaning"]["en"],
                "sanskrit_name": ch["transliteration"],
                "description": CHAPTER_DESCRIPTIONS.get(ch_num, ch["summary"]["en"]),
                "shloka_count": verse_count,
            }
            all_data["chapters"].append(chapter_entry)

            print(f"  Chapter {ch_num:2d} ({verse_count:2d} verses) ", end="", flush=True)

            for v_num in range(1, verse_count + 1):
                try:
                    vresp = await client.get(f"{API_BASE}/slok/{ch_num}/{v_num}")
                    if vresp.status_code == 200:
                        vdata = vresp.json()
                        meaning = extract_english_translation(vdata)
                        shloka_entry = {
                            "chapter": ch_num,
                            "shloka_number": v_num,
                            "sanskrit_text": vdata.get("slok", "").strip(),
                            "transliteration": vdata.get("transliteration", "").strip(),
                            "meaning": meaning,
                            "themes": extract_themes(meaning),
                        }
                        all_data["shlokas"].append(shloka_entry)
                        total += 1
                except Exception as e:
                    print(f"X", end="", flush=True)

                if v_num % 10 == 0:
                    print(".", end="", flush=True)

                await asyncio.sleep(0.08)

            print(f" OK")

    # Save to file
    out_dir = os.path.join(os.path.dirname(__file__), "..", "data")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "bhagavad_gita_complete.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)

    print(f"\n{'=' * 60}")
    print(f"  DONE! {total} verses saved to {out_path}")
    print(f"  Chapters: {len(all_data['chapters'])}")
    print(f"  Shlokas:  {len(all_data['shlokas'])}")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    start = time.time()
    asyncio.run(download_all())
    print(f"\n  Completed in {time.time() - start:.1f}s")
