"""
Generate TTS audio files for all Bhagavad Gita verses using Google Text-to-Speech.
Reads directly from JSON data - no database required.

Usage:
    python scripts/generate_audio.py [--delay 1.5] [--force]
"""
import argparse
import json
import os
import sys
import time

from gtts import gTTS

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "bhagavad_gita_complete.json")
AUDIO_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "audio")


def generate_all(delay: float, force: bool):
    os.makedirs(AUDIO_DIR, exist_ok=True)

    if not os.path.exists(DATA_PATH):
        print(f"Data file not found: {DATA_PATH}")
        print("Run 'python scripts/download_gita_data.py' first.")
        return

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    shlokas = data["shlokas"]
    total = len(shlokas)
    generated = 0
    skipped = 0
    failures = []

    print(f"Generating audio for {total} shlokas...")
    print(f"Output directory: {os.path.abspath(AUDIO_DIR)}")
    print(f"Delay between requests: {delay}s")
    print()

    for idx, shloka in enumerate(shlokas, 1):
        ch = shloka["chapter"]
        v = shloka["shloka_number"]
        file_name = f"ch{ch:02d}_v{v:03d}.mp3"
        file_path = os.path.join(AUDIO_DIR, file_name)

        # Skip if already exists (resume support)
        if os.path.exists(file_path) and not force:
            skipped += 1
            continue

        try:
            # Generate TTS from Sanskrit text using Hindi pronunciation
            tts = gTTS(text=shloka["sanskrit_text"], lang="hi")
            tts.save(file_path)

            generated += 1
            print(f"[{idx}/{total}] Ch.{ch} V.{v} - OK")

            # Rate limiting
            time.sleep(delay)

        except Exception as e:
            failures.append((ch, v, str(e)))
            print(f"[{idx}/{total}] Ch.{ch} V.{v} - FAILED: {e}")

    # Summary
    print()
    print(f"Done! Generated: {generated}, Skipped (existing): {skipped}, Failed: {len(failures)}")

    if failures:
        print("\nFailed verses:")
        for ch, v, err in failures:
            print(f"  Ch.{ch} V.{v}: {err}")


def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio for Bhagavad Gita verses")
    parser.add_argument("--delay", type=float, default=1.5, help="Delay between requests in seconds (default: 1.5)")
    parser.add_argument("--force", action="store_true", help="Regenerate existing audio files")
    args = parser.parse_args()

    generate_all(delay=args.delay, force=args.force)


if __name__ == "__main__":
    main()
