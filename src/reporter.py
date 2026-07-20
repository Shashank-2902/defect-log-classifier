# reporter.py
# Two jobs: (1) measure how accurate each method is against our answer key,
# and (2) write the cleaned file plus a plain-English summary.

import pandas as pd
from src import config


def accuracy(predicted, actual):
    """What fraction of predictions match the correct answer? Returns 0.0 to 1.0."""
    correct = (predicted.values == actual.values).sum()
    total = len(actual)
    return correct / total if total else 0.0


def score_methods(results_df, truth_df):
    """Compare baseline vs AI category predictions against ground truth."""
    merged = results_df.merge(truth_df, on="id")

    baseline_acc = accuracy(merged["baseline_category"], merged["true_category"])
    ai_acc = accuracy(merged["ai_category"], merged["true_category"])

    return baseline_acc, ai_acc, merged

def flag_for_review(results_df):
    """Flag rows where the baseline and the AI disagree, or the AI couldn't decide.

    We do NOT trust the model's self-reported confidence: it reported 'high'
    on nearly every row, including ones it got wrong. That is not a usable
    signal. Instead we flag rows where two independent methods -- the simple
    keyword baseline and the AI -- give different answers. A genuine conflict
    between two methods is a much stronger sign that a row is hard and deserves
    a human look before we trust it.
    """
    results_df = results_df.copy()
    results_df["needs_review"] = (
        (results_df["ai_category"] != results_df["baseline_category"])
        | (results_df["ai_category"] == "Unknown")
    )
    return results_df

def write_clean_csv(results_df):
    """Save the tidied-up table: id, original text, and the AI's answers."""
    columns = ["id", "description", "ai_category", "ai_severity",
               "ai_confidence", "needs_review"]
    results_df[columns].to_csv(config.CLEAN_OUTPUT_PATH, index=False)


def write_summary(results_df, baseline_acc, ai_acc):
    """Write a short, plain-English summary a non-technical person can read."""
    total = len(results_df)
    flagged = int(results_df["needs_review"].sum())
    auto = total - flagged

    category_counts = results_df["ai_category"].value_counts()
    high_severity = int((results_df["ai_severity"] == "High").sum())

    lines = []
    lines.append("DEFECT LOG CLASSIFICATION - SUMMARY")
    lines.append("=" * 40)
    lines.append(f"Total logs processed: {total}")
    lines.append(f"Auto-classified (trusted): {auto}")
    lines.append(f"Flagged for human review: {flagged}")
    lines.append(f"High-severity items to prioritize: {high_severity}")
    lines.append("")
    lines.append("Accuracy against the answer key:")
    lines.append(f"  Simple keyword baseline: {baseline_acc:.0%}")
    lines.append(f"  AI classifier:           {ai_acc:.0%}")
    lines.append("")
    lines.append("Category breakdown:")
    for category, count in category_counts.items():
        lines.append(f"  {category}: {count}")

    text = "\n".join(lines)

    with open(config.SUMMARY_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)

    return text