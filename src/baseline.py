"""Keyword baseline: the non-AI "before" that the classifier has to beat."""

from rapidfuzz import fuzz

KEYWORDS = {
    "Sensor Fault": ["sensor", "reading", "signal", "werte", "messwert", "output"],
    "Communication Error": ["can", "bus", "timeout", "communication", "kommunikation",
                            "ethernet", "uart", "spi", "i2c", "crc", "link"],
    "Power Supply Issue": ["spannung", "voltage", "power", "rail", "regler", "strom",
                           "netzteil", "supply", "5v", "3.3v", "3v"],
    "Calibration Drift": ["kalibrier", "calibration", "drift", "offset", "toleranz",
                          "genauigkeit"],
    "Mechanical Damage": ["gehaeuse", "gebrochen", "riss", "pin", "stecker", "connector",
                          "bruch", "verbogen", "schraube", "kante"],
}

EXACT_MATCH_SCORE = 2
FUZZY_MATCH_SCORE = 1
FUZZY_THRESHOLD = 88


def guess_category(text):
    """Return the category with the highest keyword score, or 'Unknown'.

    An exact keyword hit scores higher than a fuzzy hit, which tolerates typos.
    """
    text_lower = text.lower()
    best_category = "Unknown"
    best_score = 0

    for category, words in KEYWORDS.items():
        score = 0
        for word in words:
            if word in text_lower:
                score += EXACT_MATCH_SCORE
            elif fuzz.partial_ratio(word, text_lower) > FUZZY_THRESHOLD:
                score += FUZZY_MATCH_SCORE
        if score > best_score:
            best_score = score
            best_category = category

    return best_category


def run_baseline(df):
    """Return a copy of the table with a 'baseline_category' column."""
    df = df.copy()
    df["baseline_category"] = df["description"].apply(guess_category)
    return df
