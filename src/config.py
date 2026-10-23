"""Settings shared across the project: labels, model and file paths."""

CATEGORIES = [
    "Sensor Fault",
    "Communication Error",
    "Power Supply Issue",
    "Calibration Drift",
    "Mechanical Damage",
]

SEVERITIES = ["High", "Medium", "Low"]

MODEL = "openai/gpt-oss-20b"

RAW_LOGS_PATH = "data/raw_logs.csv"
GROUND_TRUTH_PATH = "data/ground_truth.csv"
CLEAN_OUTPUT_PATH = "data/cleaned_logs.csv"
SUMMARY_OUTPUT_PATH = "data/summary.txt"
