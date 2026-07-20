# baseline.py
# A simple, NON-AI classifier. It just checks whether certain keywords
# appear in the text. It is deliberately basic: its job is to be the
# "before" number that the AI has to beat. If the AI only ties this,
# the AI wasn't worth the cost.

from rapidfuzz import fuzz

# A DICTIONARY: each key is a category, each value is a list of keywords
# (German + English) we'd expect to see for that category.
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


def guess_category(text):
    """Return the category whose keywords best match the text.

    We score each category by how many of its keywords appear in the text,
    with a little fuzzy matching so small typos still count. The highest
    scoring category wins. If nothing matches, we return 'Unknown'.
    """
    text_lower = text.lower()
    best_category = "Unknown"
    best_score = 0

    for category, words in KEYWORDS.items():
        score = 0
        for word in words:
            # exact match is the strong signal
            if word in text_lower:
                score += 2
            # fuzzy match catches close-but-not-exact spellings (typos)
            elif fuzz.partial_ratio(word, text_lower) > 88:
                score += 1
        if score > best_score:
            best_score = score
            best_category = category

    return best_category


def run_baseline(df):
    """Add a 'baseline_category' column to the table using guess_category."""
    df = df.copy()  # work on a copy so we never change the original by accident
    df["baseline_category"] = df["description"].apply(guess_category)
    return df