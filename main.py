"""Runs the full pipeline: load, baseline, AI classification, scoring, reports."""

import pandas as pd

from src import baseline, classifier, config, loader, reporter
from src.client import get_client


def main():
    client = get_client()

    print("Loading logs...")
    logs = loader.load_logs(config.RAW_LOGS_PATH)

    print("Running keyword baseline...")
    logs = baseline.run_baseline(logs)

    print(f"Running AI classifier with {config.MODEL}...")
    logs = classifier.run_classifier(client, logs)

    print("Scoring against ground truth...")
    truth = pd.read_csv(config.GROUND_TRUTH_PATH)
    baseline_acc, ai_acc, _ = reporter.score_methods(logs, truth)

    logs = reporter.flag_for_review(logs)
    reporter.write_clean_csv(logs)
    summary = reporter.write_summary(logs, baseline_acc, ai_acc)

    print()
    print(summary)


if __name__ == "__main__":
    main()
