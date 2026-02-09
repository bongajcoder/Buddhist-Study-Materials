#!/usr/bin/env python3
"""
PDF Text Extraction Script for On Attaining Buddhahood
Extracts text from PDF and saves page-by-page for analysis
"""

import fitz
import os
import json

# Paths
PDF_PATH = "/Users/bonganimlambo/Documents/Code Development/Projects/Buddhist-Study-Materials/00-On Attaining Buddhism/ebook pdf/OAB_pp.00i-00v_7x10 magazine - Shannon Bodie.pdf"
OUTPUT_DIR = "/Users/bonganimlambo/Documents/Code Development/Projects/Buddhist-Study-Materials/00-On Attaining Buddhism/comparison_output"

def extract_pdf_text():
    """Extract text from PDF, page by page"""
    doc = fitz.open(PDF_PATH)

    all_text = []
    page_texts = {}

    print(f"Processing PDF with {len(doc)} pages...")

    for page_num, page in enumerate(doc):
        text = page.get_text()
        page_texts[page_num + 1] = text
        all_text.append(f"\n--- PAGE {page_num + 1} ---\n{text}")
        print(f"  Page {page_num + 1}: {len(text)} characters")

    # Save full extracted text
    full_text = "\n".join(all_text)
    with open(os.path.join(OUTPUT_DIR, "pdf_extracted_text.txt"), "w", encoding="utf-8") as f:
        f.write(full_text)

    # Save page metadata
    metadata = {
        "total_pages": len(doc),
        "page_char_counts": {k: len(v) for k, v in page_texts.items()},
        "total_characters": sum(len(v) for v in page_texts.values())
    }

    with open(os.path.join(OUTPUT_DIR, "pdf_metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\nTotal characters extracted: {metadata['total_characters']}")
    print(f"Saved to: {OUTPUT_DIR}/pdf_extracted_text.txt")

    doc.close()
    return full_text, metadata

if __name__ == "__main__":
    text, meta = extract_pdf_text()
    print("\n=== PDF EXTRACTION COMPLETE ===")
    print(json.dumps(meta, indent=2))
