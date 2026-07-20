# classifier.py
# The AI step. We send each messy log line to Groq and ask it to pick
# ONE category, ONE severity, and how confident it is. This is the thing
# a plain keyword script is bad at: understanding messy, mixed-language text.

import json
from src import config

def build_prompt(description):
    """Write the instruction (the 'prompt') we send to the model for one log line."""
    categories = ", ".join(config.CATEGORIES)
    severities = ", ".join(config.SEVERITIES)

    # We are strict about the output format (JSON only) so we can read the
    # answer back reliably in code instead of parsing messy free text.
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
    """Send one log line to Groq and return a dict with the model's answer."""
    prompt = build_prompt(description)

    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,  # 0 = as consistent/repeatable as possible
    )

     # The model's text answer lives here:
    raw = response.choices[0].message.content.strip()

    # Sometimes models wrap JSON in ```json ... ``` fences. Strip those off.
    if raw.startswith("```"):
        raw = raw.strip("`")
        raw = raw.replace("json", "", 1).strip()

    # Try to read the JSON. If anything is off, fail SAFE: mark it 'Unknown'
    # with low confidence so a human reviews it, instead of crashing.
    try:
        data = json.loads(raw)
        category = data.get("category", "Unknown")
        severity = data.get("severity", "Unknown")
        confidence = data.get("confidence", "low")
    except json.JSONDecodeError:
        category, severity, confidence = "Unknown", "Unknown", "low"

    # Guard against the model inventing a category that isn't on our list.
    if category not in config.CATEGORIES:
        category = "Unknown"
        confidence = "low"

    return {"category": category, "severity": severity, "confidence": confidence}

def run_classifier(client, df, model=config.MODEL):
    """Classify every row and add ai_category, ai_severity, ai_confidence,
    and needs_review columns."""
    df = df.copy()

    categories = []
    severities = []
    confidences = []

    # Go through each description one at a time and ask the model.
    for description in df["description"]:
        result = classify_one(client, description, model)
        categories.append(result["category"])
        severities.append(result["severity"])
        confidences.append(result["confidence"])

    df["ai_category"] = categories
    df["ai_severity"] = severities
    df["ai_confidence"] = confidences

    return df