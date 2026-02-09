#!/usr/bin/env python3
"""
Create Corrected Final Version of On Attaining Buddhahood
Removes artifacts, preserves chapter markers, generates detailed report
"""

import re
import os
from datetime import datetime

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

def identify_artifacts_with_lines(text):
    """Identify all artifacts with their line numbers"""
    artifacts = []
    lines = text.split('\n')

    for i, line in enumerate(lines, 1):
        # Page markers
        if re.match(r'OAB_pp\.[^\n]+Page \w+', line):
            artifacts.append({
                "line": i,
                "type": "page_marker",
                "content": line.strip(),
                "action": "REMOVE"
            })
        # Standalone page numbers (at start or end of book sections)
        elif re.match(r'^\s*\d{1,2}\s*$', line) and 1 <= int(line.strip()) <= 70:
            artifacts.append({
                "line": i,
                "type": "standalone_page_number",
                "content": line.strip(),
                "action": "REVIEW"  # May be legitimate content
            })

    return artifacts

def create_corrected_text(text):
    """Create a corrected version removing artifacts"""
    lines = text.split('\n')
    corrected_lines = []
    removed_count = 0
    changes = []

    for i, line in enumerate(lines, 1):
        # Remove page markers
        if re.match(r'OAB_pp\.[^\n]+Page \w+', line):
            removed_count += 1
            changes.append(f"Line {i}: REMOVED page marker: {line[:60]}...")
            continue

        # Keep [Chapter X] markers
        if re.match(r'\[Chapter \d+\]', line.strip()):
            corrected_lines.append(line)
            continue

        # Clean up excessive blank lines (keep max 2)
        if line.strip() == '':
            if len(corrected_lines) >= 2:
                if corrected_lines[-1].strip() == '' and corrected_lines[-2].strip() == '':
                    continue  # Skip extra blank line

        corrected_lines.append(line)

    corrected_text = '\n'.join(corrected_lines)

    # Final cleanup - remove more than 2 consecutive blank lines
    corrected_text = re.sub(r'\n{4,}', '\n\n\n', corrected_text)

    return corrected_text, changes

def generate_report(original, corrected, artifacts, changes):
    """Generate detailed correction report"""
    report = []
    report.append("=" * 70)
    report.append("ON ATTAINING BUDDHAHOOD - TEXT CORRECTION REPORT")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report.append("=" * 70)

    report.append("\n## SUMMARY")
    report.append(f"- Original file size: {len(original):,} characters")
    report.append(f"- Corrected file size: {len(corrected):,} characters")
    report.append(f"- Characters removed: {len(original) - len(corrected):,}")
    report.append(f"- Original lines: {len(original.split(chr(10))):,}")
    report.append(f"- Corrected lines: {len(corrected.split(chr(10))):,}")

    report.append("\n## ARTIFACTS FOUND")
    report.append(f"Total artifacts identified: {len(artifacts)}")

    # Group by type
    by_type = {}
    for art in artifacts:
        t = art["type"]
        by_type[t] = by_type.get(t, 0) + 1

    for t, count in by_type.items():
        report.append(f"  - {t}: {count}")

    report.append("\n## ARTIFACT DETAILS (First 20)")
    for art in artifacts[:20]:
        report.append(f"  Line {art['line']}: [{art['type']}] {art['content'][:50]}...")

    report.append("\n## CHANGES MADE (First 20)")
    for change in changes[:20]:
        report.append(f"  {change}")

    if len(changes) > 20:
        report.append(f"  ... and {len(changes) - 20} more changes")

    report.append("\n## CHAPTER STRUCTURE")
    chapters = re.findall(r'\[Chapter (\d+)\]', corrected)
    report.append(f"Total chapters: {len(chapters)}")
    for ch in chapters:
        report.append(f"  - Chapter {ch}")

    report.append("\n## QUALITY CHECKS")

    # Check for remaining artifacts
    remaining_artifacts = re.findall(r'OAB_pp\.[^\n]+', corrected)
    if remaining_artifacts:
        report.append(f"WARNING: {len(remaining_artifacts)} page markers still present")
    else:
        report.append("OK: All page markers removed")

    # Check for Table of Contents
    if "Table of Contents" in corrected or "C o n t e n t s" in corrected:
        report.append("OK: Table of Contents present")
    else:
        report.append("INFO: No explicit Table of Contents found")

    # Check for Index
    if "Index" in corrected:
        report.append("OK: Index section present")
    else:
        report.append("INFO: No Index section found")

    report.append("\n## FILES CREATED")
    report.append(f"  - CORRECTED_SHANNON_BODIE.txt")
    report.append(f"  - correction_report.md")

    report.append("\n" + "=" * 70)

    return '\n'.join(report)

def main():
    print("Creating corrected version of On Attaining Buddhahood...")

    # Load original
    original_path = os.path.join(EBOOK_DIR, "OAB_pp.00i-00v_7x10 magazine - Shannon Bodie.txt")
    original = load_file(original_path)

    if not original:
        print("ERROR: Could not load original file")
        return

    print(f"Loaded original: {len(original):,} characters")

    # Identify artifacts
    artifacts = identify_artifacts_with_lines(original)
    print(f"Identified {len(artifacts)} artifacts")

    # Create corrected version
    corrected, changes = create_corrected_text(original)
    print(f"Created corrected version: {len(corrected):,} characters")
    print(f"Applied {len(changes)} changes")

    # Generate report
    report = generate_report(original, corrected, artifacts, changes)

    # Save files
    corrected_path = os.path.join(OUTPUT_DIR, "CORRECTED_SHANNON_BODIE.txt")
    with open(corrected_path, 'w', encoding='utf-8') as f:
        f.write(corrected)
    print(f"Saved: {corrected_path}")

    report_path = os.path.join(OUTPUT_DIR, "correction_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"Saved: {report_path}")

    # Print report
    print("\n" + report)

if __name__ == "__main__":
    main()
