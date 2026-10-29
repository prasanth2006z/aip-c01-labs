# Skill 1.6.4 lab: Test prompts like code

Run eight test cases, including edge cases (a false premise, a prompt injection, another language, a request for too much detail), against two versions of a system prompt. Check each output with deterministic rules, find the regressions in the "friendlier" version, publish pass rates to CloudWatch and alarm on them.

- **Time:** about 25 minutes
- **Cost:** under US$0.02
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; Amazon Nova 2 Lite (US inference profile); `cloudwatch:PutMetricData` and `cloudwatch:PutMetricAlarm`

## Files

| File | What it is |
| --- | --- |
| `prompts/v1.txt` | The current system prompt: rules for scope, false premises, injection, language and length |
| `prompts/v2.txt` | A shorter, "friendlier" rewrite that quietly drops most of those rules |
| `test_cases.json` | Eight cases, each with expected-output checks |
| `prompt_tests.py` | Runner, verifier, CloudWatch metric and alarm; also a Lambda handler |
| `prompt_tests.asl.json` | Optional Step Functions workflow that runs the cases in parallel |

## Run it

```bash
pip install boto3
python prompt_tests.py run v1
python prompt_tests.py run v2
python prompt_tests.py compare
python prompt_tests.py alarm
```

Checks are plain code: response format, required and forbidden phrases, word limit. Model outputs vary a little between runs even at temperature 0, so look at which cases fail consistently.

## Optional: Step Functions

Create a Lambda function `prompt-qa` from `prompt_tests.py` and the `prompts` folder (handler `prompt_tests.handler`, timeout 60 s, permission to invoke Nova 2 Lite). Create a state machine from `prompt_tests.asl.json` with `${PromptQaArn}` replaced, and start it with `{"version": "v2", "cases": <contents of test_cases.json>}`.

## Clean up

Delete the `prompt-qa-v2-pass-rate` alarm. Custom metrics expire on their own. Delete the optional Lambda function and state machine if you created them.
