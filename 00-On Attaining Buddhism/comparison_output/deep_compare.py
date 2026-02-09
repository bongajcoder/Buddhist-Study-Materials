#!/usr/bin/env python3
"""
Deep Text Comparison - Normalizes text for accurate comparison
"""

import re
import os
import json
from difflib import SequenceMatcher, unified_diff

BASE_DIR = "/Users/bonganimlambo/Documents/Code Development/Projects/Buddhist-Study-Materials/00-On Attaining Buddhism"
EBOOK_DIR = os.path.join(BASE_DIR, "ebook pdf")
OUTPUT_DIR = os.path.join(BASE_DIR, "comparison_output")

def load_file(filepath):
    encodings = ['utf-8', 'latin-1', 'cp1252']
    for enc in encodings:
        try:
            with open(filepath, 'r', encoding=enc) as f:
                return f.read()
        except:
            continue
    return None

def normalize_text(text):
    """Normalize text for comparison - removes formatting differences"""
    # Remove printer artifacts
    text = re.sub(r'OAB_pp\.[^\n]+Page \w+', '', text)
    text = re.sub(r'--- PAGE \d+ ---', '', text)
    text = re.sub(r'\[Chapter \d+\]', '', text)  # Remove chapter markers

    # Normalize whitespace
    text = re.sub(r'[ \t]+', ' ', text)  # Multiple spaces to single
    text = re.sub(r'\n+', '\n', text)  # Multiple newlines to single
    text = re.sub(r'^\s+', '', text, flags=re.MULTILINE)  # Leading whitespace
    text = re.sub(r'\s+$', '', text, flags=re.MULTILINE)  # Trailing whitespace

    # Normalize special characters
    text = text.replace(''', "'").replace(''', "'")
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace('—', '-').replace('–', '-')
    text = text.replace('…', '...')

    return text.strip().lower()

def extract_words(text):
    """Extract just words for word-level comparison"""
    words = re.findall(r'\b[a-z]+\b', text.lower())
    return words

def compare_word_lists(words1, words2):
    """Compare two word lists and find differences"""
    set1 = set(words1)
    set2 = set(words2)

    only_in_1 = set1 - set2
    only_in_2 = set2 - set1
    common = set1 & set2

    return {
        "only_in_first": len(only_in_1),
        "only_in_second": len(only_in_2),
        "common": len(common),
        "first_total": len(set1),
        "second_total": len(set2),
        "jaccard_similarity": len(common) / len(set1 | set2) if (set1 | set2) else 0,
        "sample_only_first": list(only_in_1)[:20],
        "sample_only_second": list(only_in_2)[:20]
    }

def find_content_differences(text1, text2, sample_size=10):
    """Find specific content differences between texts"""
    lines1 = [l.strip() for l in text1.split('\n') if l.strip()]
    lines2 = [l.strip() for l in text2.split('\n') if l.strip()]

    set1 = set(lines1)
    set2 = set(lines2)

    only_in_1 = list(set1 - set2)[:sample_size]
    only_in_2 = list(set2 - set1)[:sample_size]

    return {
        "lines_only_in_first": only_in_1,
        "lines_only_in_second": only_in_2,
        "total_lines_first": len(lines1),
        "total_lines_second": len(lines2)
    }

def main():
    # Load files
    shannon = load_file(os.path.join(EBOOK_DIR, "OAB_pp.00i-00v_7x10 magazine - Shannon Bodie.txt"))
    acrobat = load_file(os.path.join(EBOOK_DIR, "OAB_pp.00i-00v_7x10 magazine - Shannon Bodie-acrobat from pdf.txt"))
    pdf_ext = load_file(os.path.join(OUTPUT_DIR, "pdf_extracted_text.txt"))
    final = load_file(os.path.join(BASE_DIR, "FINAL_BOOK_TEXT.txt"))
    validated = load_file(os.path.join(BASE_DIR, "VALIDATED_COMPREHENSIVE_TEXT.txt"))

    print("=" * 70)
    print("DEEP TEXT COMPARISON - NORMALIZED ANALYSIS")
    print("=" * 70)

    # Normalize all texts
    norm_shannon = normalize_text(shannon)
    norm_acrobat = normalize_text(acrobat)
    norm_pdf = normalize_text(pdf_ext)
    norm_final = normalize_text(final)
    norm_validated = normalize_text(validated)

    print("\n=== NORMALIZED TEXT SIZES ===")
    print(f"  Shannon Bodie: {len(norm_shannon):,} chars")
    print(f"  Acrobat:       {len(norm_acrobat):,} chars")
    print(f"  PDF Extract:   {len(norm_pdf):,} chars")
    print(f"  Final:         {len(norm_final):,} chars")
    print(f"  Validated:     {len(norm_validated):,} chars")

    # Similarity after normalization
    print("\n=== NORMALIZED SIMILARITY WITH SHANNON BODIE ===")
    for name, text in [("Acrobat", norm_acrobat), ("PDF Extract", norm_pdf),
                       ("Final", norm_final), ("Validated", norm_validated)]:
        sim = SequenceMatcher(None, norm_shannon, text).ratio()
        print(f"  {name}: {sim:.2%}")

    # Word-level analysis
    print("\n=== WORD-LEVEL ANALYSIS ===")
    shannon_words = extract_words(shannon)
    print(f"  Shannon Bodie word count: {len(shannon_words):,}")

    for name, text in [("Acrobat", acrobat), ("PDF Extract", pdf_ext),
                       ("Final", final), ("Validated", validated)]:
        words = extract_words(text)
        print(f"  {name} word count: {len(words):,}")

        result = compare_word_lists(shannon_words, words)
        print(f"    Jaccard similarity: {result['jaccard_similarity']:.2%}")
        print(f"    Words only in Shannon: {result['only_in_first']}")
        print(f"    Words only in {name}: {result['only_in_second']}")

    # Find specific differences with Acrobat (closest source)
    print("\n=== CONTENT DIFFERENCES: SHANNON vs ACROBAT ===")
    diffs = find_content_differences(shannon, acrobat)
    print(f"  Lines in Shannon: {diffs['total_lines_first']}")
    print(f"  Lines in Acrobat: {diffs['total_lines_second']}")
    print("\n  Sample lines only in Shannon (might be additions):")
    for line in diffs['lines_only_in_first'][:5]:
        print(f"    - {line[:80]}...")
    print("\n  Sample lines only in Acrobat (might be missing from Shannon):")
    for line in diffs['lines_only_in_second'][:5]:
        print(f"    - {line[:80]}...")

    # Find printer artifacts specifically
    print("\n=== PRINTER ARTIFACT SAMPLES ===")
    artifacts = re.findall(r'OAB_pp\.[^\n]+', shannon)
    print(f"  Total page markers found: {len(artifacts)}")
    print("  Sample artifacts:")
    for art in artifacts[:5]:
        print(f"    - {art}")

    # Check for OCR-like errors
    print("\n=== POTENTIAL OCR ERRORS ===")
    # Look for unusual patterns that might be OCR errors
    unusual = re.findall(r'\b[A-Z][a-z]*[A-Z][a-z]*\b', shannon)  # Mixed case mid-word
    if unusual:
        print(f"  Unusual capitalization (potential OCR errors): {unusual[:10]}")
    else:
        print("  No unusual capitalization patterns found")

    # Save detailed comparison report
    report = {
        "normalized_sizes": {
            "shannon_bodie": len(norm_shannon),
            "acrobat": len(norm_acrobat),
            "pdf_extract": len(norm_pdf),
            "final": len(norm_final),
            "validated": len(norm_validated)
        },
        "word_counts": {
            "shannon_bodie": len(shannon_words)
        },
        "content_differences_acrobat": diffs,
        "artifact_count": len(artifacts)
    }

    with open(os.path.join(OUTPUT_DIR, "deep_analysis.json"), "w") as f:
        json.dump(report, f, indent=2)

    print("\n" + "=" * 70)
    print("ANALYSIS SAVED TO: deep_analysis.json")
    print("=" * 70)

if __name__ == "__main__":
    main()
