# Developer Guide

## Overview

This is an **educational data pipeline** that:
1. Downloads Ethiopian Grade 12 exam PDFs
2. Extracts text via OCR (EasyOCR + Tesseract fallback)
3. Extracts individual questions from the text
4. Builds a hybrid TF-IDF topic taxonomy per subject
5. Analyzes topic trends across years
6. Uses an ensemble prediction model to forecast next-year topics
7. Backtests the model and generates student study guides

All code is modular and reusable. Each phase can be run independently.

## Architecture

```
config.py
  ├─ Shared configuration (paths, subjects, years)
  
exam_downloader.py
  └─ Downloads PDFs from ethiobookreview.com
  
ocr_engine.py
  ├─ EasyOCR (primary) + Tesseract (fallback)
  └─ Returns text + confidence per page
  
question_extractor.py
  └─ Parses OCR text → individual question objects
  
topics.py
  └─ TOPIC_RULES: hand-curated seed keywords per topic
  
topic_classifier.py
  ├─ Builds hybrid TF-IDF taxonomy
  ├─ Combines seed keywords + corpus-learned terms
  └─ Scores text against topics
  
validation.py
  ├─ Ground-truth loading
  └─ OCR + topic accuracy metrics (CER, F1)
  
prediction_model.py
  ├─ Ensemble model: recent_avg + trend + cyclical + stability
  ├─ Leave-one-year-out backtesting
  └─ Confidence calibration
  
student_output.py
  ├─ Generate StudyGuide JSON/HTML
  └─ Print-to-PDF support (browser native)
  
ethiopian_exam_pattern_colab.ipynb
  └─ End-to-end notebook orchestration
```

## Running the Pipeline

### Local (Python)
```bash
# Download exams
python exam_downloader.py

# Extract text
OCR_ENGINE=easyocr python extract_exam_text_ocr.py

# (Everything else is in the notebook)
```

### Colab
1. Click the **Open in Colab** badge (in README)
2. Run cells top-to-bottom
3. Download study guides from `study_guides/` folder

## Key Modules

### `ocr_engine.py`
**Purpose**: Convert PDF to text.

**Key functions**:
- `extract_text_from_pdf(pdf_path, engine='easyocr')` → `OCRResult` with per-page text + confidence

**Engine choice**:
- `'easyocr'`: Better accuracy (~90%), slower, needs torch
- `'tesseract'`: Fast, lower accuracy (~70%), no dependencies
- `'auto'`: Tries EasyOCR, falls back to Tesseract

### `question_extractor.py`
**Purpose**: Split OCR text into individual questions.

**Key functions**:
- `extract_questions(text)` → `List[Question]` (number, text, options dict)
- `extract_question_texts(text)` → `List[str]` (just the stems, for downstream analysis)

**Note**: Uses regex heuristics; ~80% accuracy on cleanly-scanned exams. Improves with better OCR.

### `topic_classifier.py`
**Purpose**: Build a hybrid topic taxonomy and classify text.

**Key functions**:
- `build_taxonomy(subject, question_texts)` → `TopicTaxonomy` (subject → topic → {term: weight})
- `score_text(text, taxonomy)` → `Dict[topic, score]` (topic scores for a given text)

**Hybrid approach**:
1. Start with seed keywords from `topics.TOPIC_RULES`
2. Compute TF-IDF over the question corpus
3. For each topic, find corpus terms that co-occur with seeds
4. Add top-N learned terms to the taxonomy, weighted by TF-IDF

**Why hybrid**: Pure keyword matching is brittle; pure unsupervised models need more data. Seeds + TF-IDF is Goldilocks.

### `prediction_model.py`
**Purpose**: Predict next-year topics and backtest.

**Key functions**:
- `predict_subject(trend_df, subject, target_year)` → `List[TopicPrediction]` (ranked topics)
- `backtest_subject(trend_df, subject)` → `List[BacktestResult]` (leave-one-year-out CV results)

**Ensemble model**:
```
likely_score = weighted_combination([
  recent_avg (last N years),
  trend (slope, normalized),
  cyclical (even/odd parity match),
  stability (inverse of variance)
])
```

All components normalized 0..1 across topics. Weights: 0.40/0.20/0.20/0.20.

**Cyclical detection**: Uses Cohen's d to measure even/odd-year separation. Example: if a topic's even-year mean is much higher than odd-year mean, it's a "even-year topic."

### `validation.py`
**Purpose**: Measure OCR and topic-detection accuracy.

**Key functions**:
- `load_ground_truth(path)` → `List[ExamGroundTruth]`
- `evaluate_ocr(extracted_by_exam, ground_truth)` → accuracy metrics

**Ground truth format** (`validation/ground_truth.json`):
```json
{
  "exams": [
    {
      "exam_id": "mathematics-2008-questions",
      "subject": "mathematics",
      "year": "2008",
      "type": "questions",
      "expected_topics": ["calculus", "algebra"],
      "questions": [
        {"page": 1, "id": "q1", "text": "..."}
      ]
    }
  ]
}
```

To enable OCR validation:
1. Manually transcribe 10–15 questions from 2–3 exams (one per subject)
2. Add to `validation/ground_truth.json`
3. Run `evaluate_ocr()` to measure improvement from Tesseract → EasyOCR

## Extending the System

### Add a New Subject

1. **Update `config.py`**:
   ```python
   NATURAL_SCIENCE_SUBJECTS = [..., 'new_subject']
   ```

2. **Add topic rules in `topics.py`**:
   ```python
   'new_subject': {
     'topic_1': ['keyword_a', 'keyword_b'],
     'topic_2': ['keyword_c', 'keyword_d'],
   }
   ```

3. **Download exams**:
   ```bash
   python exam_downloader.py
   ```

4. **Run notebook**: The pipeline automatically picks up the new subject.

### Improve Topic Detection

1. **Refine seed keywords** in `topics.py` — add domain-specific terms
2. **Fill `validation/ground_truth.json`** with real exam questions
3. **Run validation** to measure OCR + topic detection F1
4. **Adjust TF-IDF parameters** in `topic_classifier.build_taxonomy()` (top_n_per_topic, seed_weight)

### Retrain the Model

1. **Run the notebook** end-to-end
2. Check **backtest hit rate** — if <0.5, diagnose:
   - Is OCR quality low? (Switch to EasyOCR, fill ground_truth.json)
   - Is topic detection weak? (Refine TOPIC_RULES, increase top_n_per_topic)
   - Is data too sparse? (More exam years, or aggregate topics)

### Add Custom Predictions

Modify the ensemble weights in the notebook:
```python
weights = EnsembleWeights(recent=0.5, trend=0.3, cyclical=0.1, stability=0.1)
predictions = predict_all(trend_df, target_year=2011, weights=weights)
```

## Testing & Validation

### Unit Tests
```bash
python -m pytest test_*.py -v
```

(Currently no tests; contributions welcome!)

### Smoke Test
```bash
python -c "from prediction_model import *; from question_extractor import *; print('OK')"
```

### Backtest
- The notebook automatically runs leave-one-year-out CV
- Check the **backtest summary**: if hit_rate > 0.7, model is good
- If hit_rate < 0.5, debug with validation.py

## Deployment

### Colab (Easiest)
- Share the notebook link + a markdown file with instructions
- Students run all cells, download study guides

### Local Jupyter
- Clone repo, install dependencies (`pip install pandas scikit-learn matplotlib seaborn easyocr`)
- Run notebook locally
- Serve study guides via a simple web server

### Web App (Future)
- Wrap the pipeline in a Flask/FastAPI backend
- Serve study guide HTML + JSON via API
- Create a frontend for students to select subject + year

## Troubleshooting

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| OCR accuracy low (~60%) | Tesseract, or bad PDF quality | Switch to EasyOCR, improve PDF scans |
| Backtest hit rate <0.5 | Topic detection or prediction weak | Refine TOPIC_RULES, fill ground_truth.json |
| Cyclical detection fails | Not enough data or no real pattern | Aggregate topics, use more years |
| Study guides not generated | Missing predictions | Check trend_df is non-empty, pred_df has rows |

## Contributing

1. Fork the repo (or create a branch)
2. Make changes in a feature branch
3. Test with smoke tests + manual validation
4. Submit a PR with a clear description

## Resources

- **OCR**: [EasyOCR docs](https://github.com/JaidedAI/EasyOCR)
- **NLP**: [scikit-learn TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html)
- **Statistics**: Kendall tau correlation, Cohen's d
- **Data**: Ethiopian Learning textbooks (links in code)

## License

MIT (or specify your license)
