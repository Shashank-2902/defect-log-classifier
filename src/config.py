# config.py
# One place for all the settings the rest of the project reads.
# If you want to change categories, the model, or file paths, change them HERE.

# The 5 fixed categories every log gets sorted into.
# We keep this list short on purpose: a small, clear set is easier to
# measure and easier to explain than a huge messy one.
CATEGORIES = [
    "Sensor Fault",
    "Communication Error",
    "Power Supply Issue",
    "Calibration Drift",
    "Mechanical Damage",
]

# How urgent an issue is. This is the "prioritization" part:
# it lets us push the High items to the top later.
SEVERITIES = ["High", "Medium", "Low"]

# Which Groq model to use for the main run.
# gpt-oss-20b is fast and cheap.
MODEL = "openai/gpt-oss-20b"

# File locations, kept in one place so no file path is hard-coded elsewhere.
RAW_LOGS_PATH = "data/raw_logs.csv"
GROUND_TRUTH_PATH = "data/ground_truth.csv"
CLEAN_OUTPUT_PATH = "data/cleaned_logs.csv"
SUMMARY_OUTPUT_PATH = "data/summary.txt"