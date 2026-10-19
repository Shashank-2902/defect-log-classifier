"""AI classifier: asks a Groq model for a category, severity and confidence per log."""

import json

from src import config


def build_prompt(description):
    categories = ", ".join(config.CATEGORIES)
    severities = ", ".join(config.SEVERITIES)

    return f"""You are classifying automotive-semiconductor defect logs.
The text may mix German and English and contain typos.

Choose exactly ONE category from this list: {categories}
Choose exactly ONE severity from this list: {severities}
Also state your confidence as one of: high, medium, low.

Reply with ONLY a JSON object, nothing else, in this exact form:
{{"category": "...", "severity": "...", "confidence": "..."}}

Log text: "{description}"
"""


def classify_one(client, description, model=config.MODEL):
    """Classify one log line and return a dict with category, severity, confidence."""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": build_prompt(description)}],
        temperature=0,
    )
    raw = response.choices[0].message.content.strip()

    # Models sometimes wrap the JSON in ```json fences.
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    # An unreadable answer becomes 'Unknown' so it gets flagged for review.
    try:
        data = json.loads(raw)
        category = data.get("category", "Unknown")
        severity = data.get("severity", "Unknown")
        confidence = data.get("confidence", "low")
    except json.JSONDecodeError:
        category, severity, confidence = "Unknown", "Unknown", "low"

    if category not in config.CATEGORIES:
        category = "Unknown"
        confidence = "low"

    return {"category": category, "severity": severity, "confidence": confidence}


def run_classifier(client, df, model=config.MODEL):
    """Return a copy of the table with ai_category, ai_severity and ai_confidence."""
    df = df.copy()
    results = [classify_one(client, description, model) for description in df["description"]]

    df["ai_category"] = [r["category"] for r in results]
    df["ai_severity"] = [r["severity"] for r in results]
    df["ai_confidence"] = [r["confidence"] for r in results]
    return df
