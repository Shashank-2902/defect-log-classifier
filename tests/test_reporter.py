# test_reporter.py
# Tests for the accuracy calculation -- the function behind every
# percentage we report, so it's worth checking carefully.

import pandas as pd
from src import reporter


def test_all_correct_is_100_percent():
    predicted = pd.Series(["A", "B", "C"])
    actual = pd.Series(["A", "B", "C"])
    assert reporter.accuracy(predicted, actual) == 1.0


def test_all_wrong_is_zero():
    predicted = pd.Series(["A", "A", "A"])
    actual = pd.Series(["B", "B", "B"])
    assert reporter.accuracy(predicted, actual) == 0.0


def test_half_correct_is_one_half():
    predicted = pd.Series(["A", "B", "X", "Y"])
    actual = pd.Series(["A", "B", "C", "D"])
    assert reporter.accuracy(predicted, actual) == 0.5