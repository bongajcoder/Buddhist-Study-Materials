#!/usr/bin/env python3
"""
Comprehensive Text Comparison Script for On Attaining Buddhahood
Compares all text versions, identifies artifacts, and generates detailed report
"""

import re
import os
import json
from difflib import SequenceMatcher, unified_diff
from collections import defaultdict

# Base paths
BASE_DIR = "/Users/bonganimlambo/Documents/Code Development/Projects/Buddhist-Study-Materials/00-On Attaining Buddhism"
EBOOK_DIR = os.path.join(BASE_DIR, "ebook pdf")
OUTPUT_DIR = os.path.join(BASE_DIR, "comparison_output")

# Files to compare
FILES = {
    "shannon_bodie": os.path.join(EBOOK_DIR, "OAB_pp.00i-00v_7x10 magazine - Shannon Bodie.txt"),
    "acrobat": os.path.join(EBOOK_DIR, "OAB_pp.00i-00v_7x10 magazine - Shannon Bodie-acrobat from pdf.txt"),
    "pdf_extracted": os.path.join(OUTPUT_DIR, "pdf_extracted_text.txt"),
    "final": os.path.join(BASE_DIR, "FINAL_BOOK_TEXT.txt"),
    "validated": os.path.join(BASE_DIR, "VALIDATED_COMPREHENSIVE_TEXT.txt"),
}

# Printer artifact patterns
ARTIFACT_PATTERNS = [
    r'OAB_pp\.[^\n]+Page \w+',  # OAB_pp.00i-00v_7x10 magazine 11/28/11 9:50 AM Page i
    r'--- PAGE \d+ ---',  # Page markers from PDF extraction
    r'^\s*\d+\s*$',  # Standalone page numbers
]

def load_file(filepath):
    """Load file content with encoding fallback"""
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                return content
        except (FileNotFoundError, UnicodeDecodeError):
            continue
    return None

def remove_artifacts(text):
    """Remove printer artifacts from text"""
    cleaned = text
    for pattern in ARTIFACT_PATTERNS:
        cleaned = re.sub(pattern, '', cleaned, flags=re.MULTILINE)
    # Remove excessive blank lines
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    return cleaned.strip()

def split_by_chapters(text):
    """Split text by chapter markers"""
    # Look for [Chapter X] markers
    chapters = {}
    parts = re.split(r'(\[Chapter \d+\])', text)

    current_chapter = "front_matter"
    current_content = []

    for part in parts:
        if re.match(r'\[Chapter \d+\]', part):
            # Save previous chapter
            chapters[current_chapter] = '\n'.join(current_content).strip()
            # Start new chapter
            match = re.search(r'\[Chapter (\d+)\]', part)
            current_chapter = f"chapter_{match.group(1)}"
            current_content = []
        else:
            current_content.append(part)

    # Save last chapter
    chapters[current_chapter] = '\n'.join(current_content).strip()

    return chapters

def calculate_similarity(text1, text2):
    """Calculate similarity ratio between two texts"""
    return SequenceMatcher(None, text1, text2).ratio()

def find_differences(text1, text2, context=3):
    """Find specific differences between texts"""
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()

    diff = list(unified_diff(lines1, lines2, lineterm='', n=context))
    return diff

def count_artifacts(text):
    """Count printer artifacts in text"""
    counts = {}
    for pattern in ARTIFACT_PATTERNS:
        matches = re.findall(pattern, text, flags=re.MULTILINE)
        if matches:
            counts[pattern] = len(matches)
    return counts

def analyze_all_files():
    """Main analysis function"""
    results = {
        "files_loaded": {},
        "file_stats": {},
        "artifact_counts": {},
        "chapter_analysis": {},
        "similarity_matrix": {},
        "recommendations": []
    }

    # Load all files
    texts = {}
    for name, path in FILES.items():
        content = load_file(path)
        if content:
            texts[name] = content
            results["files_loaded"][name] = True
            results["file_stats"][name] = {
                "characters": len(content),
                "lines": len(content.splitlines()),
                "words": len(content.split())
            }
            results["artifact_counts"][name] = count_artifacts(content)
        else:
            results["files_loaded"][name] = False
            print(f"Warning: Could not load {name}")

    print(f"\n=== FILES LOADED ===")
    for name, loaded in results["files_loaded"].items():
        status = "OK" if loaded else "MISSING"
        print(f"  {name}: {status}")

    # Analyze chapters in Shannon Bodie text
    if "shannon_bodie" in texts:
        chapters = split_by_chapters(texts["shannon_bodie"])
        results["chapter_analysis"]["shannon_bodie"] = {
            name: {
                "characters": len(content),
                "lines": len(content.splitlines()),
                "preview": content[:200].replace('\n', ' ')[:100] + "..."
            }
            for name, content in chapters.items()
        }
        print(f"\n=== CHAPTERS FOUND IN SHANNON BODIE ===")
        for ch_name, ch_data in results["chapter_analysis"]["shannon_bodie"].items():
            print(f"  {ch_name}: {ch_data['characters']} chars, {ch_data['lines']} lines")

    # Calculate similarity matrix
    print(f"\n=== SIMILARITY MATRIX ===")
    for name1 in texts:
        for name2 in texts:
            if name1 < name2:  # Only compare each pair once
                # Clean texts before comparison
                clean1 = remove_artifacts(texts[name1])
                clean2 = remove_artifacts(texts[name2])

                similarity = calculate_similarity(clean1, clean2)
                key = f"{name1}_vs_{name2}"
                results["similarity_matrix"][key] = round(similarity, 4)
                print(f"  {name1} vs {name2}: {similarity:.2%}")

    # Find best match for Shannon Bodie
    if "shannon_bodie" in texts:
        clean_shannon = remove_artifacts(texts["shannon_bodie"])

        print(f"\n=== DETAILED COMPARISON WITH SHANNON BODIE ===")
        for name, content in texts.items():
            if name != "shannon_bodie":
                clean_other = remove_artifacts(content)
                sim = calculate_similarity(clean_shannon, clean_other)
                print(f"\n{name}:")
                print(f"  Similarity: {sim:.2%}")
                print(f"  Shannon Bodie: {len(clean_shannon)} chars")
                print(f"  {name}: {len(clean_other)} chars")
                print(f"  Difference: {abs(len(clean_shannon) - len(clean_other))} chars")

    # Artifact analysis
    print(f"\n=== ARTIFACT ANALYSIS ===")
    for name, artifacts in results["artifact_counts"].items():
        if artifacts:
            total = sum(artifacts.values())
            print(f"  {name}: {total} artifacts found")
            for pattern, count in artifacts.items():
                print(f"    - {pattern[:50]}...: {count}")
        else:
            print(f"  {name}: No artifacts detected")

    # Generate recommendations
    if "shannon_bodie" in texts:
        artifact_count = sum(results["artifact_counts"].get("shannon_bodie", {}).values())
        if artifact_count > 0:
            results["recommendations"].append(
                f"Remove {artifact_count} printer artifacts from shannon_bodie"
            )

    # Save results
    with open(os.path.join(OUTPUT_DIR, "analysis_results.json"), "w") as f:
        json.dump(results, f, indent=2)

    return results

def generate_cleaned_version():
    """Generate a cleaned version of Shannon Bodie text"""
    shannon_path = FILES["shannon_bodie"]
    content = load_file(shannon_path)

    if not content:
        print("Error: Could not load Shannon Bodie text")
        return

    cleaned = remove_artifacts(content)

    # Save cleaned version
    output_path = os.path.join(OUTPUT_DIR, "shannon_bodie_cleaned.txt")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned)

    print(f"\n=== CLEANED VERSION CREATED ===")
    print(f"  Original: {len(content)} chars")
    print(f"  Cleaned: {len(cleaned)} chars")
    print(f"  Removed: {len(content) - len(cleaned)} chars")
    print(f"  Saved to: {output_path}")

    return cleaned

def chunk_and_compare_chapters():
    """Create chapter-by-chapter comparison files"""
    shannon = load_file(FILES["shannon_bodie"])
    pdf = load_file(FILES["pdf_extracted"])

    if not shannon:
        print("Error: Could not load Shannon Bodie text")
        return

    chapters = split_by_chapters(shannon)
    chapter_dir = os.path.join(OUTPUT_DIR, "chunked_chapters")
    os.makedirs(chapter_dir, exist_ok=True)

    for ch_name, ch_content in chapters.items():
        # Save chapter
        chapter_path = os.path.join(chapter_dir, f"{ch_name}.txt")
        with open(chapter_path, "w", encoding="utf-8") as f:
            f.write(ch_content)

        # Save cleaned version
        cleaned = remove_artifacts(ch_content)
        cleaned_path = os.path.join(chapter_dir, f"{ch_name}_cleaned.txt")
        with open(cleaned_path, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"  {ch_name}: {len(ch_content)} chars -> {len(cleaned)} chars (cleaned)")

if __name__ == "__main__":
    print("=" * 60)
    print("ON ATTAINING BUDDHAHOOD - TEXT COMPARISON ANALYSIS")
    print("=" * 60)

    # Run main analysis
    results = analyze_all_files()

    # Generate cleaned version
    generate_cleaned_version()

    # Chunk chapters
    print(f"\n=== CHUNKING CHAPTERS ===")
    chunk_and_compare_chapters()

    print("\n" + "=" * 60)
    print("ANALYSIS COMPLETE")
    print(f"Results saved to: {OUTPUT_DIR}")
    print("=" * 60)
