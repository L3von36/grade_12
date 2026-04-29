#!/usr/bin/env python3
"""
Download Ethiopian Grade 12 exams from ethiobookreview.com
URL pattern: https://www.ethiobookreview.com/assets/exams/{subject}-{year}-{type}.pdf
"""

import os
import urllib.request
import urllib.error
import time

# Base URL
BASE_URL = "https://www.ethiobookreview.com/assets/exams/"

# Download directory
DOWNLOAD_DIR = "/workspace/downloads/ethiopian_grade12"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Natural Science subjects (Grade 12)
NATURAL_SCIENCE_SUBJECTS = [
    "english",
    "mathematics",
    "physics",
    "chemistry",
    "biology",
    "civics"
]

# Social Science subjects
SOCIAL_SCIENCE_SUBJECTS = [
    "geography",
    "history",
    "economics"
]

# Years to download (EC calendar)
YEARS = ["2005", "2006", "2007", "2008", "2009", "2010"]

# File types
TYPES = ["questions", "answers"]

def download_file(url, filepath):
    """Download a file with retry logic"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            urllib.request.urlretrieve(url, filepath)
            return True
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            time.sleep(2)
    return False

def download_subject_year(subject, year, download_dir):
    """Download all files for a subject-year combination"""
    results = []

    for file_type in TYPES:
        filename = f"{subject}-{year}-{file_type}.pdf"
        url = f"{BASE_URL}{filename}"
        filepath = os.path.join(download_dir, filename)

        if os.path.exists(filepath):
            print(f"  ✓ Already exists: {filename}")
            results.append((filename, "already_downloaded"))
            continue

        print(f"  Downloading: {filename}...", end=" ")

        if download_file(url, filepath):
            size = os.path.getsize(filepath)
            print(f"✓ ({size:,} bytes)")
            results.append((filename, "success"))
        else:
            print(f"✗ Failed")
            results.append((filename, "failed"))

        time.sleep(0.5)  # Be polite to the server

    return results

def main():
    print("=" * 60)
    print("Ethiopian Grade 12 Exam Downloader")
    print("=" * 60)

    # Download Natural Science subjects
    print("\n📚 NATURAL SCIENCE STREAM")
    print("-" * 40)

    natural_results = {}
    for subject in NATURAL_SCIENCE_SUBJECTS:
        print(f"\n{subject.upper()}:")
        subject_dir = os.path.join(DOWNLOAD_DIR, "natural_science", subject)
        os.makedirs(subject_dir, exist_ok=True)

        for year in YEARS:
            _, status = download_subject_year(subject, year, subject_dir)[0]
            if subject not in natural_results:
                natural_results[subject] = {"downloaded": 0, "failed": 0}
            if status == "success":
                natural_results[subject]["downloaded"] += 2
            elif status == "failed":
                natural_results[subject]["failed"] += 2

    # Download Social Science subjects
    print("\n\n📚 SOCIAL SCIENCE STREAM")
    print("-" * 40)

    social_results = {}
    for subject in SOCIAL_SCIENCE_SUBJECTS:
        print(f"\n{subject.upper()}:")
        subject_dir = os.path.join(DOWNLOAD_DIR, "social_science", subject)
        os.makedirs(subject_dir, exist_ok=True)

        for year in YEARS:
            _, status = download_subject_year(subject, year, subject_dir)[0]
            if subject not in social_results:
                social_results[subject] = {"downloaded": 0, "failed": 0}
            if status == "success":
                social_results[subject]["downloaded"] += 2
            elif status == "failed":
                social_results[subject]["failed"] += 2

    # Summary
    print("\n" + "=" * 60)
    print("DOWNLOAD SUMMARY")
    print("=" * 60)

    print("\n📗 Natural Science:")
    total_natural = 0
    for subject, stats in natural_results.items():
        total_natural += stats["downloaded"]
        print(f"  {subject}: {stats['downloaded']} files downloaded, {stats['failed']} failed")

    print("\n📕 Social Science:")
    total_social = 0
    for subject, stats in social_results.items():
        total_social += stats["downloaded"]
        print(f"  {subject}: {stats['downloaded']} files downloaded, {stats['failed']} failed")

    print(f"\nTotal: {total_natural + total_social} files downloaded")
    print(f"Saved to: {DOWNLOAD_DIR}")

if __name__ == "__main__":
    main()
