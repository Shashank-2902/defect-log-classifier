# defect-log-classifier

An AI-assisted tool that reads messy, free-text defect logs and sorts each one
into a fixed category and severity level, flagging uncertain cases for a human
to review. Built as a small, honest demonstration of using an AI model to add
measurable value to a real business process.

> **Note on data:** The dataset is fully synthetic. It is modelled to resemble
> messy automotive-semiconductor quality logs (mixed German/English, typos,
> inconsistent wording) but contains no real company data.

## The problem

Quality and defect logs are often written as short, inconsistent free text.
Sorting them by hand is slow and subjective. The goal here: automatically
standardise each log into a known category and severity, so the important
issues can be found and prioritised quickly.

## What it does

1. Reads raw, messy defect logs.
2. Classifies each one with a simple keyword baseline (the "before").
3. Classifies each one with an AI model via the Groq API (the "after").
4. Flags rows for human review where the two methods disagree.
5. Scores both methods against a hand-labelled answer key.
6. Writes a cleaned file and a plain-English summary.

## Results

On 82 synthetic logs, scored against a hand-labelled answer key:

| Method                  | Accuracy |
| ----------------------- | -------- |
| Simple keyword baseline | 76%      |
| AI classifier           | 98%      |

- **62 of 82** logs were auto-classified with confidence.
- **20 of 82** were flagged for human review (where baseline and AI disagreed).

### Model cost-benefit

The same logs were run through two models to test whether the larger, pricier
model is worth it for this task:

| Model               | Accuracy | Price / 1M input tokens |
| ------------------- | -------- | ----------------------- |
| openai/gpt-oss-20b  | 98%      | $0.075                  |
| openai/gpt-oss-120b | 99%      | $0.15                   |

**Conclusion:** The larger model gained only ~1 point of accuracy at twice the
price. For this workload the smaller model is the better choice. The larger
model would only be justified if the cost of a misclassification were high
enough to warrant paying double for that last point.

## How the human-in-the-loop works

An earlier version flagged rows using the model's own self-reported confidence.
That did not work: the model reported high confidence on nearly every row,
including ones it got wrong. The review trigger was changed to flag rows where
the keyword baseline and the AI **disagree** — a genuine conflict between two
independent methods, which is a more reliable signal that a row is hard.

## Agent Skill

This project includes an Agent Skill (`.claude/skills/defect-log-classifier/SKILL.md`)
so an AI assistant such as Claude Code can run the whole workflow from a plain-English
request. The skill wraps the pipeline into ordered steps and enforces the human-review
step: the assistant runs the classifier, then stops and presents the flagged rows for a
person to confirm before the results are treated as final. The scripts are unchanged —
the skill is a plain-English instruction file layered on top.

## Limitations (honest)

- The data is synthetic and fairly clean; real logs would be messier.
- The 1-point gap between the two models is within noise on 82 rows; the honest
  reading is that the models are roughly equal in accuracy here.
- "Cost" uses input-token price as a simple proxy; a full costing would include
  output tokens and throughput.
- Disagreement-based flagging over-flags, because the weak baseline is often the
  one that is wrong. It is a cheap proxy for "hard," chosen because over-flagging
  is the safe direction for a review queue.

## How to run

```bash
# 1. Set up
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 2. Add your Groq API key to a file named .env
#    GROQ_API_KEY=your_key_here

# 3. Generate the synthetic data
python generate_data.py

# 4. Run the pipeline
python main.py

# 5. (Optional) Compare the two models
python compare_models.py

# 6. Run the tests
pytest
```

## Tech

Python, pandas, Groq API (openai/gpt-oss-20b), rapidfuzz, pytest.
Plain functions in separate modules; no framework.
