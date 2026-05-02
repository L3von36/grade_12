# Student Study Guide

## What is This?

This is an **AI-powered study planner** for Ethiopian Grade 12 entrance exams. It analyzes 6 years of past exams to predict which topics are most likely to appear on your upcoming exam, so you can focus your study time wisely.

## How to Use It (5 minutes)

### 1. Open the Study Guide
- Your teachers/school will give you an **HTML file** like `mathematics_2011_study_guide.html`
- Open it in any web browser (Chrome, Firefox, Safari, Edge)
- No internet needed after download

### 2. Read the Table
The table shows:
- **Rank**: Topic priority (1 = study first)
- **Score**: Likelihood of appearing (0–1, higher is more likely)
- **Confidence**: How sure the model is (0–1, higher is more sure)
- **History**: How many past exams (e.g., "5/6" = appeared in 5 of 6 exams)
- **Trend**: Is interest rising or falling? 
- **Study**: Estimated hours to master

### 3. Make a Study Plan

**Example (Mathematics):**
```
Rank 1: Calculus (Score 0.85, Confidence 0.90, 12 hrs)
  → Study most: this topic is very likely AND the model is confident

Rank 2: Algebra (Score 0.78, Confidence 0.85, 10 hrs)
  → Study next: likely and confident

Rank 5: Geometry (Score 0.42, Confidence 0.60, 6 hrs)
  → Study last: less likely, model is less confident
```

### 4. Download the Textbook
- Click the **Grade 11** or **Grade 12** link in the guide
- Download the textbook PDF for your subject
- Find the chapters that cover the top-ranked topics
- Study those chapters first

### 5. Practice Past Exams
- Get past exam papers from your school
- Focus practice on the top-ranked topics
- Check your answers against the answer key

### 6. Print the Guide (Optional)
- Click **Print** (Ctrl+P or Cmd+P)
- Choose "Save as PDF"
- Print or email to yourself

## Understanding Confidence

**Confidence = how sure the model is about a prediction**

- **≥0.8** (high): "This topic will definitely appear. Study hard."
- **0.6–0.8** (medium): "This topic might appear. It's a good bet."
- **<0.6** (low): "The model is unsure. Use this as one hint, not the only hint."

Confidence is low when:
- Very few past exams mentioned this topic
- The trend is unpredictable
- The model signals are mixed (some say "study this," others say "don't")

## What If I Disagree?

The model is **not perfect**. It's based on 6 years of exams, but:
- Your exam might have new topics not in the past 6 years
- The exam board might change priorities
- Your teacher might emphasize topics differently

**Use the guide as a starting point, not the only guide.** If your teacher emphasizes a topic, study it even if the model ranks it low.

## Questions?

### Why is Topic X ranked so low?
- It appeared in fewer past exams
- There's no clear trend (some years yes, some no)
- Or the model's confidence is low for this topic

### Why does the confidence differ across subjects?
- Some subjects are more predictable (e.g., math, chemistry with strong trends)
- Others are less predictable (e.g., history, civics where topics vary more)
- More data = higher confidence

### Can I see how the model works?
- Yes! Ask your teacher or developer for the "Developer Guide" (`DEVELOPER_GUIDE.md`)
- The model combines:
  - Recent trends (rising/falling interest)
  - Cyclical patterns (even/odd year topics)
  - Historical frequency (how many exams)
  - Stability (predictability)

## Good luck! 📚

Study smart, not just hard. Use this guide to focus on what's likely. Good luck on your exam!
