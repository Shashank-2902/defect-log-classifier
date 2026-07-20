# loader.py
# One job: read the raw logs CSV into a table (DataFrame) we can work with.

import pandas as pd

def load_logs(path):
    """Read the raw logs CSV and return it as a pandas DataFrame (a table)."""
    df = pd.read_csv(path)

    # A tiny safety check: make sure the columns we expect are actually there.
    # If someone hands us the wrong file, we stop early with a clear message
    # instead of a confusing crash somewhere deeper in the code.
    expected = {"id", "description"}
    missing = expected - set(df.columns)
    if missing:
        raise ValueError(f"raw logs file is missing columns: {missing}")

    return df