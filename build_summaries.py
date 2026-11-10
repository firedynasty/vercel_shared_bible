#!/usr/bin/env python3
"""
Split a combined chapter_summaries.json into one small file per book.

commentary.html loads only the book you are reading (summaries/<abbrev>.json),
so the page never pulls the whole Bible's summaries at once.

Usage:
    python build_summaries.py                      # uses the default source below
    python build_summaries.py /path/to/chapter_summaries.json
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_SOURCE = (
    HERE.parent / "vercel_bible_current" / "public" / "chapter_summaries.json"
)
OUT_DIR = HERE / "summaries"

# (display name, abbreviation) — abbreviations match the BOOKS table in commentary.html
BOOKS = [
    ("Genesis", "gn"), ("Exodus", "ex"), ("Leviticus", "lv"), ("Numbers", "nm"),
    ("Deuteronomy", "dt"), ("Joshua", "js"), ("Judges", "jud"), ("Ruth", "rt"),
    ("1 Samuel", "1sm"), ("2 Samuel", "2sm"), ("1 Kings", "1kgs"), ("2 Kings", "2kgs"),
    ("1 Chronicles", "1ch"), ("2 Chronicles", "2ch"), ("Ezra", "ezr"), ("Nehemiah", "ne"),
    ("Esther", "et"), ("Job", "job"), ("Psalms", "ps"), ("Proverbs", "prv"),
    ("Ecclesiastes", "ec"), ("Song of Solomon", "so"), ("Isaiah", "is"), ("Jeremiah", "jr"),
    ("Lamentations", "lm"), ("Ezekiel", "ez"), ("Daniel", "dn"), ("Hosea", "ho"),
    ("Joel", "jl"), ("Amos", "am"), ("Obadiah", "ob"), ("Jonah", "jn"),
    ("Micah", "mi"), ("Nahum", "na"), ("Habakkuk", "hk"), ("Zephaniah", "zp"),
    ("Haggai", "hg"), ("Zechariah", "zc"), ("Malachi", "ml"), ("Matthew", "mt"),
    ("Mark", "mk"), ("Luke", "lk"), ("John", "jo"), ("Acts", "act"),
    ("Romans", "rm"), ("1 Corinthians", "1co"), ("2 Corinthians", "2co"), ("Galatians", "gl"),
    ("Ephesians", "eph"), ("Philippians", "ph"), ("Colossians", "cl"),
    ("1 Thessalonians", "1ts"), ("2 Thessalonians", "2ts"), ("1 Timothy", "1tm"),
    ("2 Timothy", "2tm"), ("Titus", "tt"), ("Philemon", "phm"), ("Hebrews", "hb"),
    ("James", "jm"), ("1 Peter", "1pe"), ("2 Peter", "2pe"), ("1 John", "1jo"),
    ("2 John", "2jo"), ("3 John", "3jo"), ("Jude", "jd"), ("Revelation", "re"),
]


def main() -> None:
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_SOURCE
    if not source.is_file():
        sys.exit(f"ERROR: no combined summaries at {source}")

    combined = json.loads(source.read_text(encoding="utf-8"))
    OUT_DIR.mkdir(exist_ok=True)

    total = 0
    largest = ("", 0)
    for name, abbrev in BOOKS:
        prefix = name + " "
        per_chapter = {}
        for key, value in combined.items():
            if not key.startswith(prefix):
                continue
            tail = key[len(prefix):]
            if tail.isdigit():
                per_chapter[tail] = value
        if not per_chapter:
            print(f"  {name}: no summaries found, skipped")
            continue
        ordered = {k: per_chapter[k] for k in sorted(per_chapter, key=int)}
        path = OUT_DIR / f"{abbrev}.json"
        path.write_text(
            json.dumps(ordered, ensure_ascii=False, separators=(",", ":")) + "\n",
            encoding="utf-8",
        )
        kb = path.stat().st_size / 1024
        total += len(ordered)
        if kb > largest[1]:
            largest = (name, kb)
        print(f"  {name:<18} {len(ordered):>3} chapters  {kb:>6.1f} KB")

    print(f"\nWrote {total} chapters across {len(list(OUT_DIR.glob('*.json')))} files")
    print(f"Largest: {largest[0]} at {largest[1]:.1f} KB")


if __name__ == "__main__":
    main()
