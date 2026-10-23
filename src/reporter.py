"""Scores the classifiers against the answer key and writes the output files."""

from src import config


def accuracy(predicted, actual):
    """Fraction of predictions that match the correct answer (0.0 to 1.0)."""
    correct = (predicted.values == actual.values).sum()
    total = len(actual)
    return correct / total if total else 0.0


def score_methods(results_df, truth_df):
    """Return baseline accuracy, AI accuracy and the merged table."""
    merged = results_df.merge(truth_df, on="id")
    baseline_acc = accuracy(merged["baseline_category"], merged["true_category"])
    ai_acc = accuracy(merged["ai_category"], merged["true_category"])
    return baseline_acc, ai_acc, merged


def flag_for_review(results_df):
    """Add a 'needs_review' column.

    A row is flagged when the baseline and the AI disagree, or the AI could not
    decide. The model's self-reported confidence is not used: it said 'high' on
    nearly every row, including wrong ones.
    """
    results_df = results_df.copy()
    results_df["needs_review"] = (
        (results_df["ai_category"] != results_df["baseline_category"])
        | (results_df["ai_category"] == "Unknown")
    )
    return results_df


def write_clean_csv(results_df):
    """Save the id, original text, the AI's answers and the review flag."""
    columns = ["id", "description", "ai_category", "ai_severity",
               "ai_confidence", "needs_review"]
    results_df[columns].to_csv(config.CLEAN_OUTPUT_PATH, index=False)


def write_summary(results_df, baseline_acc, ai_acc):
    """Write a short plain-text summary and return it."""
    total = len(results_df)
    flagged = int(results_df["needs_review"].sum())
    high_severity = int((results_df["ai_severity"] == "High").sum())

    lines = [
        "DEFECT LOG CLASSIFICATION - SUMMARY",
        "=" * 40,
        f"Total logs processed: {total}",
        f"Auto-classified (trusted): {total - flagged}",
        f"Flagged for human review: {flagged}",
        f"High-severity items to prioritize: {high_severity}",
        "",
        "Accuracy against the answer key:",
        f"  Simple keyword baseline: {baseline_acc:.0%}",
        f"  AI classifier:           {ai_acc:.0%}",
        "",
        "Category breakdown:",
    ]
    for category, count in results_df["ai_category"].value_counts().items():
        lines.append(f"  {category}: {count}")

    text = "\n".join(lines)
    with open(config.SUMMARY_OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write(text)
    return text
