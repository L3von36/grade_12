#!/usr/bin/env python3
"""
Extract text from Ethiopian Grade 12 exam PDFs using OCR
Steps:
1. Convert PDF pages to images
2. Run Tesseract OCR on each page
3. Combine results and create CSV
"""

import os
import csv
import re
import subprocess
import tempfile
from pathlib import Path

# Paths
DOWNLOAD_DIR = "/workspace/downloads/ethiopian_grade12"
OUTPUT_CSV = "/workspace/data/ethiopian_exams_extracted.csv"
EXTRACTED_DIR = "/workspace/data/extracted_text"

def pdf_to_images(pdf_path, output_dir, dpi=200):
    """Convert PDF pages to images using pdftoppm"""
    cmd = ['pdftoppm', '-r', str(dpi), '-png', pdf_path, os.path.join(output_dir, 'page')]
    subprocess.run(cmd, capture_output=True, check=False)

    # Get list of generated images
    images = sorted([f for f in os.listdir(output_dir) if f.startswith('page') and f.endswith('.png')])
    return [os.path.join(output_dir, img) for img in images]

def extract_text_from_image(image_path):
    """Run Tesseract OCR on a single image"""
    cmd = ['tesseract', image_path, 'stdout', '-l', 'eng', '--psm', '6']
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return result.stdout if result.returncode == 0 else ""
    except:
        return ""

def extract_text_from_pdf(pdf_path, temp_dir=None):
    """Extract text from all pages of a PDF"""
    if temp_dir is None:
        temp_dir = tempfile.mkdtemp()

    # Clean temp dir
    for f in os.listdir(temp_dir):
        os.remove(os.path.join(temp_dir, f))

    # Convert PDF to images
    images = pdf_to_images(pdf_path, temp_dir, dpi=200)

    # OCR each page
    all_text = []
    for img in images:
        text = extract_text_from_image(img)
        if text.strip():
            all_text.append(text)
        # Clean up image
        try:
            os.remove(img)
        except:
            pass

    return "\n\n".join(all_text)

def parse_filename(filename):
    """Parse filename to extract subject, year, and type"""
    name = filename.replace('.pdf', '')
    parts = name.split('-')

    if len(parts) >= 3:
        return parts[0], parts[1], parts[2]
    else:
        return parts[0] if len(parts) > 0 else "unknown", \
               parts[1] if len(parts) > 1 else "unknown", \
               parts[2] if len(parts) > 2 else "unknown"

def clean_text(text):
    """Clean extracted text"""
    if not text:
        return ""
    # Normalize whitespace
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def main():
    print("=" * 60)
    print("Ethiopian Grade 12 Exam Text Extractor (OCR)")
    print("=" * 60 + "\n")

    os.makedirs(EXTRACTED_DIR, exist_ok=True)
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)

    # Subject lists
    natural_subjects = ["english", "mathematics", "physics", "chemistry", "biology", "civics"]
    social_subjects = ["geography", "history", "economics"]

    # Count total files
    total_files = 0
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for f in files:
            if f.endswith('.pdf'):
                total_files += 1

    print(f"Found {total_files} PDF files to process\n")

    all_records = []
    processed = 0
    errors = 0

    # Create temp dir once
    temp_dir = tempfile.mkdtemp(prefix="pdf_ocr_")

    # Process all files
    for root, dirs, files in os.walk(DOWNLOAD_DIR):
        for filename in sorted(files):
            if not filename.endswith('.pdf'):
                continue

            processed += 1
            pdf_path = os.path.join(root, filename)

            print(f"[{processed}/{total_files}] {filename}...", end=" ", flush=True)

            # Parse filename
            subject, year, file_type = parse_filename(filename)

            # Determine stream
            if subject in natural_subjects:
                stream = "natural_science"
            elif subject in social_subjects:
                stream = "social_science"
            else:
                stream = "unknown"

            try:
                # Extract text
                raw_text = extract_text_from_pdf(pdf_path, temp_dir)
                clean_text_content = clean_text(raw_text)

                # Save individual text file
                subject_dir = os.path.join(EXTRACTED_DIR, stream, subject)
                os.makedirs(subject_dir, exist_ok=True)
                text_file = os.path.join(subject_dir, filename.replace('.pdf', '.txt'))
                with open(text_file, 'w', encoding='utf-8') as f:
                    f.write(clean_text_content)

                file_size = os.path.getsize(pdf_path)

                record = {
                    'subject': subject,
                    'year': year,
                    'type': file_type,
                    'stream': stream,
                    'filename': filename,
                    'file_size_bytes': file_size,
                    'text_length': len(clean_text_content),
                    'text_preview': clean_text_content[:500] if clean_text_content else "",
                    'text_full': clean_text_content
                }
                all_records.append(record)
                print(f"✓ ({len(clean_text_content):,} chars)")

            except Exception as e:
                print(f"✗ Error: {e}")
                errors += 1
                all_records.append({
                    'subject': subject,
                    'year': year,
                    'type': file_type,
                    'stream': stream,
                    'filename': filename,
                    'file_size_bytes': 0,
                    'text_length': 0,
                    'text_preview': "",
                    'text_full': ""
                })

    # Clean up temp dir
    try:
        for f in os.listdir(temp_dir):
            os.remove(os.path.join(temp_dir, f))
        os.rmdir(temp_dir)
    except:
        pass

    # Create CSV
    if all_records:
        fieldnames = ['subject', 'year', 'type', 'stream', 'filename', 'file_size_bytes', 'text_length', 'text_preview', 'text_full']
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_records)

    # Summary
    print("\n" + "=" * 60)
    print("EXTRACTION SUMMARY")
    print("=" * 60)

    subjects = {}
    for r in all_records:
        s = r['subject']
        if s not in subjects:
            subjects[s] = {'count': 0, 'chars': 0}
        subjects[s]['count'] += 1
        subjects[s]['chars'] += r['text_length']

    print("\nBy Subject:")
    for s, stats in sorted(subjects.items()):
        print(f"  {s}: {stats['count']} files, {stats['chars']:,} chars")

    print(f"\nTotal: {len(all_records)} files processed")
    print(f"Errors: {errors}")
    print(f"Total characters: {sum(r['text_length'] for r in all_records):,}")
    print(f"\nOutput:")
    print(f"  CSV: {OUTPUT_CSV}")
    print(f"  Text: {EXTRACTED_DIR}")

if __name__ == "__main__":
    main()