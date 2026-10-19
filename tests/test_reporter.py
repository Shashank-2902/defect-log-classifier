"""Tests for the accuracy calculation behind every reported percentage."""

import pandas as pd

from src import reporter


def test_all_correct_is_100_percent():
    predicted = pd.Series(["A", "B", "C"])
    assert reporter.accuracy(predicted, predicted) == 1.0


def test_all_wrong_is_zero():
    predicted = pd.Series(["A", "A", "A"])
    actual = pd.Series(["B", "B", "B"])
    assert reporter.accuracy(predicted, actual) == 0.0


def test_half_correct_is_one_half():
    predicted = pd.Series(["A", "B", "X", "Y"])
    actual = pd.Series(["A", "B", "C", "D"])
    assert reporter.accuracy(predicted, actual) == 0.5
