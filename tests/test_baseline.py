"""Tests for the keyword baseline."""

from src import baseline

ALLOWED_LABELS = ["Sensor Fault", "Communication Error", "Power Supply Issue",
                  "Calibration Drift", "Mechanical Damage", "Unknown"]


def test_sensor_fault_is_detected():
    assert baseline.guess_category("sensor liefert falsche werte") == "Sensor Fault"


def test_communication_error_is_detected():
    assert baseline.guess_category("can bus timeout, ecu no response") == "Communication Error"


def test_no_keywords_returns_unknown():
    assert baseline.guess_category("irgendetwas stimmt hier nicht") == "Unknown"


def test_result_is_always_a_known_label():
    assert baseline.guess_category("random text with no meaning xyz") in ALLOWED_LABELS
