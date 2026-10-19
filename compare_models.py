"""Runs the same logs through two models and compares accuracy and price."""

import pandas as pd

from src import baseline, classifier, config, loader, reporter
from src.client import get_client

# Price per 1 million input tokens (Groq pricing page). Input price is only a
# rough stand-in for overall cost.
MODELS = {
    "openai/gpt-oss-20b": 0.075,
    "openai/gpt-oss-120b": 0.15,
}


def evaluate_model(client, logs, truth, model_name):
    """Classify every log with one model and return its accuracy."""
    print(f"Running {model_name} ...")
    results = classifier.run_classifier(client, logs, model_name)
    _, ai_acc, _ = reporter.score_methods(results, truth)
    return ai_acc


def main():
    client = get_client()

    logs = loader.load_logs(config.RAW_LOGS_PATH)
    logs = baseline.run_baseline(logs)
    truth = pd.read_csv(config.GROUND_TRUTH_PATH)

    scores = {name: (evaluate_model(client, logs, truth, name), price)
              for name, price in MODELS.items()}

    print()
    print("MODEL COMPARISON")
    print("=" * 55)
    print(f"{'Model':<28}{'Accuracy':<12}{'Price/1M in':<12}")
    print("-" * 55)
    for name, (accuracy, price) in scores.items():
        print(f"{name:<28}{accuracy:<12.0%}${price:<11}")


if __name__ == "__main__":
    main()
