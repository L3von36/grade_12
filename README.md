# grade_12

Ethiopian Grade 12 entrance-exam pattern analysis. Goal: turn historical
exam PDFs into a study guide for students by predicting which topics are
most likely to appear next.

## Notebook

- `ethiopian_exam_pattern_colab.ipynb`: End-to-end Colab workflow
  (download → OCR → clean → topic trend → next-year prediction →
  textbook alignment).

## Modules

- `config.py`: Shared paths, subject lists, years, URLs.
- `exam_downloader.py`: Download exam PDFs from ethiobookreview.com.
- `ocr_engine.py`: OCR with EasyOCR (primary) and Tesseract (fallback).
  Returns text + confidence per page.
- `topics.py`: Hand-curated `TOPIC_RULES` taxonomy (subject → topic → seed
  keywords) used as the seed for TF-IDF augmentation.
- `question_extractor.py`: Parse OCR text into individual questions with
  options. Filters out OCR noise too short to be a real question.
- `topic_classifier.py`: Hybrid TF-IDF taxonomy builder + classifier.
  Combines hand-curated seeds with corpus-learned terms.
- `validation.py`: Ground-truth loading + OCR/topic accuracy metrics
  (character error rate, word F1, topic precision/recall/F1).
- `validation/ground_truth.json`: Manually-transcribed reference text
  used to measure OCR and topic-detection quality.

## Scripts

- `download_ethiopian_exams.py`: CLI entry point for the downloader.
- `extract_exam_text_ocr.py`: CLI entry point for OCR extraction.
  Set `OCR_ENGINE=easyocr|tesseract|auto` (default: `auto`).

## Roadmap

1. Phase 1: EasyOCR upgrade + validation harness + modular code.
2. Phase 2 (current): Question extraction + hybrid TF-IDF topic taxonomy.
3. Phase 3: Backtested ensemble prediction model (cyclical patterns).
4. Phase 4: Per-subject student study guides (ranked topics, textbook
   chapters, confidence scores, practice questions).
5. Phase 5: End-to-end Colab pipeline + HTML/PDF student outputs.
