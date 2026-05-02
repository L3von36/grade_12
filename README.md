# grade_12

Ethiopian Grade 12 entrance-exam pattern analysis. **AI-powered study planner** that predicts which topics are most likely to appear on your exam, so you can focus study time wisely.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/L3von36/grade_12/blob/main/ethiopian_exam_pattern_colab.ipynb)

## For Students

👉 **[How to Use This (STUDENT_GUIDE.md)](STUDENT_GUIDE.md)**

1. Open the HTML study guide in your browser
2. Read the ranked topic list (study high-ranked topics first)
3. Download textbooks and practice exams
4. Print to PDF if you want a paper copy

## For Developers / Teachers

👉 **[Technical Details (DEVELOPER_GUIDE.md)](DEVELOPER_GUIDE.md)**

## How It Works

1. **Download** 6 years of past exam PDFs
2. **OCR** extract text (EasyOCR for accuracy)
3. **Parse** individual questions and build topic taxonomies
4. **Analyze** trends across years (cyclical patterns, rising/falling interest)
5. **Predict** next year's likely topics (ensemble model)
6. **Backtest** with leave-one-year-out validation
7. **Generate** personalized study guides (JSON + HTML)

## The Notebook

- `ethiopian_exam_pattern_colab.ipynb`: End-to-end workflow
  (download → OCR → extract questions → TF-IDF taxonomy → trend analysis
  → ensemble prediction → backtest → study guide generation)
  
  Run it in [Google Colab](https://colab.research.google.com) (click badge above) or locally in Jupyter.

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
- `prediction_model.py`: Ensemble next-year predictor (recent average,
  trend slope, cyclical phase, stability) plus leave-one-year-out
  backtesting that reports hit rate and rank correlation per subject.
- `student_output.py`: Generate study guides (JSON + HTML) from predictions.
  Each guide shows ranked topics, frequency, textbook links, confidence
  with explanations, and study time estimates.
- `validation.py`: Ground-truth loading + OCR/topic accuracy metrics
  (character error rate, word F1, topic precision/recall/F1).
- `validation/ground_truth.json`: Manually-transcribed reference text
  used to measure OCR and topic-detection quality.

## Scripts

- `download_ethiopian_exams.py`: CLI entry point for the downloader.
- `extract_exam_text_ocr.py`: CLI entry point for OCR extraction.
  Set `OCR_ENGINE=easyocr|tesseract|auto` (default: `auto`).

## Outputs

- `study_guides/`: Study guide JSON and HTML files (one per subject).
  Students open the HTML in a browser or download the JSON for use in apps.

## Roadmap

1. Phase 1 ✓: EasyOCR upgrade + validation harness + modular code.
2. Phase 2 ✓: Question extraction + hybrid TF-IDF topic taxonomy.
3. Phase 3 ✓: Backtested ensemble prediction model (cyclical patterns).
4. Phase 4 ✓: Student study guides (JSON + HTML).
5. Phase 5 ✓: Print-to-PDF, documentation, Colab badge, deployment ready.

## Status: Ready for Students ✅

The full pipeline is complete and working. Students can:
- Launch the notebook in Colab with one click
- Get personalized study guides in ~30 minutes
- Download HTML guides (print to PDF in any browser)
- See backtest metrics proving the model works
- Learn which topics to prioritize for their exam

## Next Steps

### For Students
- Follow [STUDENT_GUIDE.md](STUDENT_GUIDE.md)
- Download your subject's study guide
- Focus on high-ranked topics

### For Teachers / Developers
- See [DEVELOPER_GUIDE.md](DEVELOPER_GUIDE.md)
- Customize topics, add subjects, retrain the model
- Share the Colab link with students
- Contribute improvements
