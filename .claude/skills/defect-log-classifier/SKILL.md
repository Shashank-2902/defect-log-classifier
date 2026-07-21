---
name: defect-log-classifier
description: Classifies messy, free-text defect or quality logs into fixed categories and severity levels using an AI model, then flags uncertain rows for human review. Use this whenever the user has a batch of short, inconsistent defect notes, error logs, or quality records (especially mixed-language or typo-heavy text) and wants them standardized, categorized, prioritized by severity, or cleaned up. Also use when the user asks to sort, triage, or route logs, or to turn raw defect text into a structured summary.
---

# Defect Log Classifier

This skill classifies messy, free-text defect logs into fixed categories and
severity levels, and flags uncertain rows for a human to review before the
results are trusted.

## What this skill does

It takes short, inconsistent defect or quality notes (often mixed German/English
with typos) and turns them into a clean, structured table: each log gets one
category, one severity level, and a flag showing whether a human should check it.

## Categories

Every log is sorted into exactly one of these five categories:
- Sensor Fault
- Communication Error
- Power Supply Issue
- Calibration Drift
- Mechanical Damage

Severity is one of: High, Medium, Low.

## Workflow

Follow these steps in order.

1. **Prepare the input.** Make sure the defect logs are in `data/raw_logs.csv`
   with two columns: `id` and `description`. If the user provides logs in another
   form, convert them to this format first.

2. **Run the classifier.** Run `python main.py` from the project root. This runs
   a keyword baseline, then the AI classifier, scores both against the answer key
   in `data/ground_truth.csv`, and writes the outputs.

3. **Review the flagged rows before trusting the results.** Open
   `data/cleaned_logs.csv` and look at every row where `needs_review` is `True`.
   These are rows where the baseline and the AI disagreed, which means they are
   likely hard cases. Present these flagged rows to the user and let a human
   confirm or correct them. Do not treat the classification as final until this
   review step has happened.

4. **Summarize the results.** Read `data/summary.txt` and explain it to the user
   in plain language: how many logs were processed, how many were auto-classified,
   how many need review, how many are high severity, and the accuracy numbers.

5. **(Optional) Compare models.** If the user wants to weigh accuracy against
   cost, run `python compare_models.py` and explain the trade-off between the
   cheaper and the more expensive model.

## Guidelines

- The review step in the workflow is not optional. The value of this tool comes
  from combining automatic classification with human judgement on the hard cases,
  not from replacing the human.
- When explaining results, lead with what matters to a non-technical reader: how
  many issues are high severity and need attention, and how many need review.
  Keep the accuracy numbers brief.
- Keep the category list fixed. If a log does not fit any category well, it is
  better to flag it for review than to force it into a category.
- The severity level is a prioritization aid, not a guarantee. Treat High-severity
  items as "look at these first," not as a final verdict.

## Limitations

- The classifier was built and measured on synthetic data that is cleaner than
  real production logs. On messier real-world data, expect lower accuracy and more
  rows needing review.
- The review flag is based on the baseline and the AI disagreeing. Because the
  keyword baseline is weak, this tends to over-flag. Over-flagging is the safe
  direction, but the user should know some flagged rows will be easy ones the AI
  actually got right.
- This skill classifies and prioritizes logs. It does not diagnose root causes or
  recommend fixes.