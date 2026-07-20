# compare_models.py
# Runs the SAME logs through two different models and compares them on
# accuracy and (rough) cost. This is the "cost vs benefit" evidence:
# is the bigger, pricier model actually worth it for this task?

import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd

from src import config
from src import loader
from src import baseline
from src import classifier
from src import reporter

# The two models we compare, with their price per 1 million INPUT tokens
# (from Groq's pricing page). We use input price as a simple stand-in for
# "how expensive is this model" -- good enough for a rough comparison.
MODELS = {
    "openai/gpt-oss-20b": 0.075,   # cheaper, faster
    "openai/gpt-oss-120b": 0.15,   # bigger, pricier
}


def evaluate_model(client, logs, truth, model_name):
    """Run one model over all logs and return its accuracy."""
    print(f"Running {model_name} ...")

    # Classify every row with THIS model.
    results = classifier.run_classifier(client, logs, model_name)

    # Score it against the answer key, reusing our existing scorer.
    _, ai_acc, _ = reporter.score_methods(results, truth)

    return ai_acc


def main():
    # Set up the Groq connection (same as main.py).
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("No GROQ_API_KEY found. Put it in your .env file.")
    client = Groq(api_key=api_key)

    # Load the logs and run the baseline once (same input for both models).
    logs = loader.load_logs(config.RAW_LOGS_PATH)
    logs = baseline.run_baseline(logs)
    truth = pd.read_csv(config.GROUND_TRUTH_PATH)

    # Run each model and collect its accuracy.
    scores = {}
    for model_name, price in MODELS.items():
        accuracy = evaluate_model(client, logs, truth, model_name)
        scores[model_name] = (accuracy, price)

    # Print a small comparison table.
    print()
    print("MODEL COMPARISON")
    print("=" * 55)
    print(f"{'Model':<28}{'Accuracy':<12}{'Price/1M in':<12}")
    print("-" * 55)
    for model_name, (accuracy, price) in scores.items():
        print(f"{model_name:<28}{accuracy:<12.0%}${price:<11}")


if __name__ == "__main__":
    main()