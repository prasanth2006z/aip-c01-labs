# Skill 1.3.4 lab: Clean and enrich input for better answers

Take three messy customer messages and improve them before they reach the model: normalise them in plain Python (the kind of code that runs in a Lambda function), detect language, entities and PII with Amazon Comprehend, rewrite them into a clean summary with Amazon Bedrock, then compare answers for raw and enhanced input.

- **Time:** about 30 minutes
- **Cost:** under US$0.05 (Comprehend charges per 100 characters, with a minimum per request)
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; `comprehend:DetectDominantLanguage`, `comprehend:DetectEntities`, `comprehend:DetectPiiEntities`; `bedrock:InvokeModel` on Amazon Nova 2 Lite through the US inference profile

## Files

| File | What it is |
| --- | --- |
| `tickets.json` | Three customer messages: shouting, emoji, inconsistent order IDs and dates, contact details |
| `enhance_input.py` | The four lab steps |

## Run it

```bash
pip install boto3
python enhance_input.py normalize    # no AWS calls
python enhance_input.py comprehend
python enhance_input.py reformat
python enhance_input.py compare
```

| Step | What it shows |
| --- | --- |
| `normalize` | Deterministic clean-up: emoji, repeated punctuation, spacing, `#B 2096` → `B-2096`, `3rd oct 2026` → `2026-10-03`, shouting → sentence case |
| `comprehend` | Dominant language, entities (dates, quantities, commercial items) and PII; PII is replaced with `[PHONE]`, `[EMAIL]` and so on |
| `reformat` | Bedrock rewrites each message into fixed lines: Item, Order, Purchase date, Problem, Customer wants |
| `compare` | Same policy question three times on raw and on enhanced input. The raw `10/05/2026` can be read as 5 October or 10 May; normalised ISO dates remove the guess |

The `10/05/2026` → `2026-10-05` rule assumes US month/day order. In a real system the format comes from the source (form locale, country), not a guess.

## Clean up

Nothing to delete: Comprehend and Bedrock are called on demand.
