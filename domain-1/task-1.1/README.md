# Domain 1, Task 1.1: Analyze requirements and design GenAI solutions

Lab files for the four Medium posts covering Task 1.1. Region: **us-west-2**.

| Post | Skill | Format | Folder |
| --- | --- | --- | --- |
| 1 | 1.1.1 Turning requirements into an architecture | Notes | — |
| 2 | 1.1.2 Proving it works: a GenAI proof of concept | Lab, ~35 min | [`skill-1.1.2-poc`](skill-1.1.2-poc) |
| 3 | 1.1.3 Reviewing designs with the Generative AI Lens | Lab, ~30 min | [`skill-1.1.3-wa-lens`](skill-1.1.3-wa-lens) |
| 4 | Task 1.1 exam notes | Notes | — |

## Skill 1.1.2 files

- `returns-policy.md`: the policy the assistant answers from (same document as the chunking lab)
- `golden_set.json`: 8 questions, each with the phrases a correct answer must contain
- `poc_harness.py`: runs the golden set against two candidate models and checks accuracy, p90 latency and cost against exit criteria. Fill in `PRICES` from the Amazon Bedrock pricing page to enable the cost check.

```bash
python poc_harness.py
```

## Skill 1.1.3 files

- `README.md`: step-by-step for importing the Generative AI Lens into the AWS Well-Architected Tool and reviewing the PoC with it
