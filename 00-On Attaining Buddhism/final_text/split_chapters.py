#!/usr/bin/env python3
"""
Split On Attaining Buddhahood into individual chapter files
"""

import re
import os

BASE_DIR = "/Users/bonganimlambo/Documents/Code Development/Projects/Buddhist-Study-Materials/00-On Attaining Buddhism/final_text"

# Chapter titles from the Table of Contents
CHAPTER_TITLES = {
    "front_matter": "Front Matter - Title Page, Copyright, Contents, Editor's Note",
    "chapter_1": "Chapter 1 - Attaining Buddhahood in This Lifetime—The Fundamental Purpose of Life and a Source of Hope for Humankind",
    "chapter_2": "Chapter 2 - The Significance of Chanting Nam-myoho-renge-kyo—Achieving a Life of Supreme Victory Through Correct Buddhist Practice",
    "chapter_3": "Chapter 3 - If You Think the Law Is Outside Yourself, You Are Not Embracing the Mystic Law",
    "chapter_4": "Chapter 4 - Transforming Our Fundamental Attitude—Refusing To Live an Endless, Painful Austerity",
    "chapter_5": "Chapter 5 - Chanting Nam-myoho-renge-kyo With a Brave and Vigorous Spirit—Polishing Our Lives Through Daily Challenge",
    "chapter_6": "Chapter 6 - The Mystic Nature of Our Lives—Become the Master of Your Mind Rather Than Let Your Mind Master You",
    "chapter_7": "Chapter 7 - Faith for Attaining Buddhahood in This Lifetime—Advance Unerringly Along the Great Path of the Oneness of Mentor and Disciple",
}

def load_file(filepath):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except:
            continue
    return None

def split_into_chapters(text):
    """Split text by [Chapter X] markers"""
    chapters = {}

    # Split by chapter markers, keeping the markers
    parts = re.split(r'(\[Chapter \d+\])', text)

    current_chapter = "front_matter"
    current_content = []

    for part in parts:
        match = re.match(r'\[Chapter (\d+)\]', part)
        if match:
            # Save previous chapter
            chapters[current_chapter] = '\n'.join(current_content).strip()
            # Start new chapter
            chapter_num = match.group(1)
            current_chapter = f"chapter_{chapter_num}"
            current_content = []
        else:
            current_content.append(part)

    # Save last chapter
    chapters[current_chapter] = '\n'.join(current_content).strip()

    return chapters

def main():
    # Load the final corrected text
    text_path = os.path.join(BASE_DIR, "FINAL_CORRECTED_TEXT.txt")
    text = load_file(text_path)

    if not text:
        print("ERROR: Could not load final text")
        return

    print(f"Loaded: {len(text):,} characters")

    # Split into chapters
    chapters = split_into_chapters(text)

    print(f"\nFound {len(chapters)} sections")
    print("\nCreating individual chapter files...")

    # Create chapters directory
    chapters_dir = os.path.join(BASE_DIR, "chapters")
    os.makedirs(chapters_dir, exist_ok=True)

    for chapter_key, content in chapters.items():
        # Get title
        title = CHAPTER_TITLES.get(chapter_key, chapter_key)

        # Create filename (sanitize title)
        if chapter_key == "front_matter":
            filename = "00_Front_Matter.txt"
        else:
            # Extract chapter number
            num = chapter_key.split('_')[1]
            filename = f"{num.zfill(2)}_{chapter_key.replace('chapter_', 'Chapter_')}.txt"

        filepath = os.path.join(chapters_dir, filename)

        # Add header to content
        header = f"{'=' * 70}\n{title}\n{'=' * 70}\n\n"
        full_content = header + content

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        word_count = len(content.split())
        print(f"  {filename}: {len(content):,} chars, {word_count:,} words")

    # Create a README
    readme_path = os.path.join(BASE_DIR, "README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("""ON ATTAINING BUDDHAHOOD IN THIS LIFETIME
by Daisaku Ikeda

=========================================

This folder contains the cleaned, corrected text of the book.

FILES:
------
- FINAL_CORRECTED_TEXT.txt  - Complete book in one file
- chapters/                  - Individual chapter files

CHAPTERS:
---------
00_Front_Matter.txt  - Title, Copyright, Contents, Editor's Note
01_Chapter_1.txt     - Attaining Buddhahood in This Lifetime
02_Chapter_2.txt     - The Significance of Chanting Nam-myoho-renge-kyo
03_Chapter_3.txt     - If You Think the Law Is Outside Yourself
04_Chapter_4.txt     - Transforming Our Fundamental Attitude
05_Chapter_5.txt     - Chanting With a Brave and Vigorous Spirit
06_Chapter_6.txt     - The Mystic Nature of Our Lives
07_Chapter_7.txt     - Faith for Attaining Buddhahood in This Lifetime

SOURCE:
-------
Extracted from: OAB_pp.00i-00v_7x10 magazine - Shannon Bodie.pdf
Cleaned: November 29, 2025
Artifacts removed: 72 printer page markers

""")

    print(f"\nCreated README.txt")
    print(f"\nAll files saved to: {BASE_DIR}")

if __name__ == "__main__":
    main()
