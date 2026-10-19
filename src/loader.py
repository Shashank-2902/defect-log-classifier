"""Reads the raw defect logs from CSV."""

import pandas as pd

REQUIRED_COLUMNS = {"id", "description"}


def load_logs(path):
    """Return the raw logs as a DataFrame, failing early if columns are missing."""
    df = pd.read_csv(path)
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"raw logs file is missing columns: {missing}")
    return df
