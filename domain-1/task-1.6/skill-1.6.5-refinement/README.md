# Skill 1.6.5 lab: Improve prompts step by step

Take a one-line prompt that decides whether a return is eligible, and improve it in four measured steps: structured input, an output format specification, chain-of-thought instructions, and a feedback loop where code checks the answer and sends problems back to the model.

- **Time:** about 25 minutes
- **Cost:** under US$0.05
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; Amazon Nova 2 Lite (US inference profile)

## Files

| File | What it is |
| --- | --- |
| `tickets.json` | Six customer tickets with dates in different formats, each labelled with the right decision and day count |
| `refine_lab.py` | Five prompt versions (v0-v4), the parser, the feedback checks and the scoreboard |

## Run it

```bash
pip install boto3
python refine_lab.py show v0
python refine_lab.py run v0
python refine_lab.py show v3
python refine_lab.py run v3
python refine_lab.py compare
```

| Version | Adds |
| --- | --- |
| v0 | "Is this return eligible?" and the ticket |
| v1 | Policy, today's date and the ticket in labelled XML-style tags |
| v2 | A JSON output specification with category, purchase date, day count, limit and decision |
| v3 | Step-by-step reasoning in `<thinking>` tags before the JSON answer in `<answer>` tags |
| v4 | v3 plus a feedback loop: code recomputes the day count and the decision, and asks the model to fix any mismatch (up to 2 rounds) |

Free-text answers from v0 and v1 are scored with a simple keyword parser, so treat their scores as approximate. The point is the trend, not the exact numbers.

## Clean up

Nothing to delete.
