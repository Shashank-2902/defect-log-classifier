# main.py
# The conductor. It calls each module in order. Run THIS file to run the project.

import os
from dotenv import load_dotenv
from groq import Groq
import pandas as pd

from src import config
from src import loader
from src import baseline
from src import classifier
from src import reporter


def main():
    # 1. Load the secret API key from the .env file into the program.
    load_dotenv()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("No GROQ_API_KEY found. Put it in your .env file.")

    # The 'client' is our connection to Groq. Create it once, reuse it.
    client = Groq(api_key=api_key)

    # 2. Load the messy input logs.
    print("Loading logs...")
    logs = loader.load_logs(config.RAW_LOGS_PATH)

    # 3. Run the simple keyword baseline (the 'before').
    print("Running keyword baseline...")
    logs = baseline.run_baseline(logs)

    # 4. Run the AI classifier (the 'after'). Calls Groq once per row.
    print(f"Running AI classifier with {config.MODEL}...")
    logs = classifier.run_classifier(client, logs)

    # 5. Load the answer key and score both methods.
    print("Scoring against ground truth...")
    truth = pd.read_csv(config.GROUND_TRUTH_PATH)
    baseline_acc, ai_acc, _ = reporter.score_methods(logs, truth)

    # 5b. Decide which rows need review, based on baseline-vs-AI disagreement
    #     (a stronger, more honest signal than the model's own confidence).
    logs = reporter.flag_for_review(logs)

    # 6. Write the cleaned file and the plain-English summary.
    reporter.write_clean_csv(logs)
    summary = reporter.write_summary(logs, baseline_acc, ai_acc)

    # 7. Print the summary so you see the result immediately.
    print()
    print(summary)


if __name__ == "__main__":
    main()