#!/usr/bin/env python3
"""
Advanced OCR Script for Buddhist Study Materials
Handles mixed single-column and two-column page layouts.

Uses Surya OCR (best for complex layouts) with Tesseract as fallback.
"""

import os
import sys
import argparse
from pathlib import Path
from datetime import datetime

# PDF processing
import fitz  # PyMuPDF
from PIL import Image
import io

# OCR engines
import pytesseract

# Surya OCR (v0.17+ API)
SURYA_AVAILABLE = False
try:
    from surya.recognition import RecognitionPredictor
    from surya.detection import DetectionPredictor
    from surya.foundation import FoundationPredictor
    SURYA_AVAILABLE = True
except ImportError:
    print("Note: Surya OCR not fully available, will use Tesseract")


def pdf_to_images(pdf_path: str, dpi: int = 300) -> list:
    """Convert PDF pages to PIL Images using PyMuPDF."""
    doc = fitz.open(pdf_path)
    images = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        # Create high-res image matrix
        mat = fitz.Matrix(dpi / 72, dpi / 72)
        pix = page.get_pixmap(matrix=mat)

        # Convert to PIL Image
        img_data = pix.tobytes("png")
        img = Image.open(io.BytesIO(img_data))

        # Convert to RGB if necessary (Surya needs RGB)
        if img.mode != 'RGB':
            img = img.convert('RGB')

        images.append(img)

        print(f"  Converted page {page_num + 1}/{len(doc)}", end='\r')

    print()
    doc.close()
    return images


def ocr_with_surya(images: list) -> list:
    """Run Surya OCR on images - best for complex layouts (v0.17+ API)."""
    if not SURYA_AVAILABLE:
        raise RuntimeError("Surya OCR not available")

    print("Loading Surya models (first run downloads ~2GB)...")

    # Initialize predictors with the new API
    foundation_predictor = FoundationPredictor()
    recognition_predictor = RecognitionPredictor(foundation_predictor)
    detection_predictor = DetectionPredictor()

    print("Running Surya OCR...")
    texts = []

    # Process in batches for memory efficiency
    batch_size = 4
    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]

        # Run OCR on batch (Surya v0.17 API - no language param needed)
        predictions = recognition_predictor(
            batch,
            det_predictor=detection_predictor,
            sort_lines=True  # Helps with reading order
        )

        # Extract text from predictions
        for pred in predictions:
            if hasattr(pred, 'text'):
                texts.append(pred.text)
            elif isinstance(pred, dict) and 'text' in pred:
                texts.append(pred['text'])
            else:
                # Try to extract from text_lines
                page_text = []
                if hasattr(pred, 'text_lines'):
                    for line in pred.text_lines:
                        if hasattr(line, 'text'):
                            page_text.append(line.text)
                texts.append('\n'.join(page_text))

        print(f"  OCR'd page {min(i+batch_size, len(images))}/{len(images)}", end='\r')

    print()
    return texts


def ocr_with_tesseract(images: list, psm: int = 3, oem: int = 3,
                        preprocess: bool = True, lang: str = 'eng') -> list:
    """
    Run Tesseract OCR on images with optimized settings.

    PSM modes for layout:
    - 1: Automatic page segmentation with OSD
    - 3: Fully automatic page segmentation (default)
    - 4: Assume single column of text of variable sizes
    - 6: Assume uniform block of text
    - 11: Sparse text - find as much text as possible in no particular order
    - 12: Sparse text with OSD

    OEM modes:
    - 0: Legacy engine only
    - 1: Neural nets LSTM engine only
    - 2: Legacy + LSTM engines
    - 3: Default, based on what is available
    """
    print(f"Running Tesseract OCR (PSM={psm}, OEM={oem}, lang={lang})...")

    texts = []
    custom_config = f'--psm {psm} --oem {oem} -l {lang}'

    for i, img in enumerate(images):
        # Optional preprocessing for better accuracy
        if preprocess:
            # Convert to grayscale
            if img.mode != 'L':
                img_processed = img.convert('L')
            else:
                img_processed = img
        else:
            img_processed = img

        text = pytesseract.image_to_string(img_processed, config=custom_config)
        texts.append(text)
        print(f"  OCR'd page {i + 1}/{len(images)}", end='\r')

    print()
    return texts


def detect_layout(image: Image.Image) -> str:
    """
    Detect if page is single or two-column layout.
    Returns 'single', 'double', or 'mixed'.
    """
    width, height = image.size
    gray = image.convert('L')

    # Sample the middle 10% of the image width
    middle_start = int(width * 0.45)
    middle_end = int(width * 0.55)

    # Count dark pixels (text) in middle strip
    middle_region = gray.crop((middle_start, int(height * 0.1), middle_end, int(height * 0.9)))
    pixels = list(middle_region.getdata())
    dark_pixels = sum(1 for p in pixels if p < 128)
    total_pixels = len(pixels)

    dark_ratio = dark_pixels / total_pixels if total_pixels > 0 else 0

    if dark_ratio < 0.05:
        return 'double'
    else:
        return 'single'


def process_pdf(pdf_path: str, output_dir: str, engine: str = 'surya',
                dpi: int = 300, psm: int = 3):
    """
    Process PDF with OCR and save results.
    """
    pdf_path = Path(pdf_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n{'='*60}")
    print(f"OCR Processing: {pdf_path.name}")
    print(f"Engine: {engine.upper()}")
    print(f"DPI: {dpi}")
    if engine in ['tesseract', 'both']:
        print(f"Tesseract PSM: {psm}")
    print(f"{'='*60}\n")

    # Convert PDF to images
    print("Step 1: Converting PDF to images...")
    images = pdf_to_images(str(pdf_path), dpi=dpi)
    print(f"  Total pages: {len(images)}")

    # Detect layouts
    print("\nStep 2: Analyzing page layouts...")
    layouts = []
    for i, img in enumerate(images):
        layout = detect_layout(img)
        layouts.append(layout)

    single_count = layouts.count('single')
    double_count = layouts.count('double')
    print(f"  Single-column pages: {single_count}")
    print(f"  Two-column pages: {double_count}")

    # Run OCR
    results = {}

    if engine in ['surya', 'both']:
        print("\nStep 3a: Running Surya OCR (optimized for layouts)...")
        try:
            surya_texts = ocr_with_surya(images)
            results['surya'] = surya_texts
        except Exception as e:
            print(f"  Surya OCR failed: {e}")
            if engine == 'surya':
                print("  Falling back to Tesseract...")
                engine = 'tesseract'

    if engine in ['tesseract', 'both']:
        print(f"\nStep 3b: Running Tesseract OCR (PSM={psm})...")
        tesseract_texts = ocr_with_tesseract(images, psm=psm, preprocess=True)
        results['tesseract'] = tesseract_texts

    # Save results
    print("\nStep 4: Saving results...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for eng_name, texts in results.items():
        # Full document
        output_file = output_dir / f"ocr_{eng_name}_{timestamp}.txt"

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"# OCR Output: {pdf_path.name}\n")
            f.write(f"# Engine: {eng_name.upper()}\n")
            f.write(f"# Date: {datetime.now().isoformat()}\n")
            f.write(f"# Pages: {len(texts)}\n")
            f.write(f"# DPI: {dpi}\n")
            if eng_name == 'tesseract':
                f.write(f"# PSM: {psm}\n")
            f.write("=" * 60 + "\n\n")

            for i, text in enumerate(texts):
                layout = layouts[i] if i < len(layouts) else 'unknown'
                f.write(f"\n{'='*60}\n")
                f.write(f"PAGE {i + 1} (Layout: {layout})\n")
                f.write(f"{'='*60}\n\n")
                f.write(text)
                f.write("\n")

        print(f"  Saved: {output_file}")

        # Also save per-page files for review
        pages_dir = output_dir / f"{eng_name}_pages"
        pages_dir.mkdir(exist_ok=True)

        for i, text in enumerate(texts):
            page_file = pages_dir / f"page_{i+1:03d}.txt"
            with open(page_file, 'w', encoding='utf-8') as f:
                f.write(text)

    # Summary
    print(f"\n{'='*60}")
    print("OCR Complete!")
    print(f"{'='*60}")
    print(f"Output directory: {output_dir}")

    for eng_name in results:
        total_chars = sum(len(t) for t in results[eng_name])
        print(f"  {eng_name.upper()}: {total_chars:,} characters extracted")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="OCR a PDF book with support for two-column layouts",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python ocr_book.py book.pdf                    # Use Surya (best)
  python ocr_book.py book.pdf --engine tesseract # Use Tesseract
  python ocr_book.py book.pdf --engine both      # Compare both
  python ocr_book.py book.pdf --dpi 400          # Higher quality
  python ocr_book.py book.pdf --psm 4            # Single column mode
  python ocr_book.py book.pdf --psm 1            # Auto with OSD
        """
    )

    parser.add_argument('pdf_path', help='Path to the PDF file')
    parser.add_argument('--output', '-o', help='Output directory (default: same as PDF)')
    parser.add_argument('--engine', '-e', choices=['surya', 'tesseract', 'both'],
                        default='surya', help='OCR engine to use (default: surya)')
    parser.add_argument('--dpi', '-d', type=int, default=300,
                        help='DPI for PDF rendering (default: 300)')
    parser.add_argument('--psm', type=int, default=3,
                        help='Tesseract PSM mode (default: 3)')

    args = parser.parse_args()

    pdf_path = Path(args.pdf_path)
    if not pdf_path.exists():
        print(f"Error: PDF file not found: {pdf_path}")
        sys.exit(1)

    output_dir = args.output or pdf_path.parent / "ocr_output"

    process_pdf(str(pdf_path), str(output_dir), engine=args.engine,
                dpi=args.dpi, psm=args.psm)


if __name__ == '__main__':
    main()
