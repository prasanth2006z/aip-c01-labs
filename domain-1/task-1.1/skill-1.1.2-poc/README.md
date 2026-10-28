# Skill 1.1.2 lab: Prove it works with a GenAI proof of concept

Runs a golden set of questions against two candidate models on Amazon Bedrock, measures accuracy,
p90 latency, tokens and cost, and prints GO or NO-GO against exit criteria agreed up front.

- **Time:** about 35 minutes
- **Cost:** under US$0.05 (16 short model calls); creates no AWS resources
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`, AWS credentials, Amazon Nova 2 Lite and Nova Micro available through the US inference profiles

## Files

| File | What it is |
| --- | --- |
| `returns-policy.md` | The policy the assistant answers from |
| `golden_set.json` | 8 questions, each with the phrases a correct answer must contain |
| `poc_harness.py` | The harness: exit criteria, candidates, prices, evaluation and report |

## Run it

1. Open `poc_harness.py` and read `EXIT_CRITERIA` before running anything.
2. Optional: fill in `PRICES` (USD per 1,000 tokens) from the [Amazon Bedrock pricing page](https://aws.amazon.com/bedrock/pricing/) to enable the cost check.
3. Run:

```bash
pip install boto3
python poc_harness.py
```

## Troubleshooting

- `AccessDeniedException`: allow `bedrock:InvokeModel` on the inference profiles and the underlying models.
- `ValidationException` on the model ID: Nova 2 Lite is only available through an inference profile; keep the `us.` prefix.
