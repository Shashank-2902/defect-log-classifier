# test_baseline.py
# Tests for the keyword baseline. We check that guess_category returns the
# category we expect for clear, obvious inputs.

from src import baseline


def test_sensor_fault_is_detected():
    text = "sensor liefert falsche werte"
    result = baseline.guess_category(text)
    assert result == "Sensor Fault"

def test_communication_error_is_detected():
    text = "can bus timeout, ecu no response"
    result = baseline.guess_category(text)
    assert result == "Communication Error"


def test_no_keywords_returns_unknown():
    # This text has none of our keywords, so the baseline SHOULD give up
    # and return "Unknown" rather than guessing wrongly. Testing this
    # honest failure is as important as testing the successes.
    text = "irgendetwas stimmt hier nicht"
    result = baseline.guess_category(text)
    assert result == "Unknown"


def test_result_is_always_a_known_label():
    # Whatever the input, the baseline must return one of our categories
    # or "Unknown" -- never something random. This guards the contract
    # that downstream code relies on.
    allowed = ["Sensor Fault", "Communication Error", "Power Supply Issue",
               "Calibration Drift", "Mechanical Damage", "Unknown"]
    result = baseline.guess_category("random text with no meaning xyz")
    assert result in allowed