# Domain 1, Task 1.2: Select and configure FMs

Lab files for the Medium post covering Task 1.2. Region: **us-west-2**.

| Skill | Format | Folder |
| --- | --- | --- |
| 1.2.1 Choosing a foundation model | Exam notes (in the post) | — |
| 1.2.2 Switching models without code changes | Lab, ~40 min | [`skill-1.2.2-model-switching`](skill-1.2.2-model-switching) |
| 1.2.3 Resilient model access | Lab, ~40 min | [`skill-1.2.3-resilience`](skill-1.2.3-resilience) |
| 1.2.4 Customisation and model lifecycle | Exam notes (in the post) | — |

## Skill 1.2.2 files

- `appconfig-model-settings.json`: the freeform AppConfig profile (version 1 uses Nova 2 Lite; the lab then switches to Nova Micro)
- `appconfig-validator.json`: JSON Schema validator that blocks empty or malformed model IDs
- `lambda_function.py`: the `model-router` function. Needs the **AWS-AppConfig-Extension** layer and IAM permissions for AppConfig and `bedrock:InvokeModel`.

## Skill 1.2.3 files

- `profiles.py`: calls Nova 2 Lite by bare model ID, US profile and global profile
- `fallback.py`: adaptive retries plus a fallback model on retryable errors only (`SIMULATE = True` fakes a throttle)
- `circuit-breaker-statemachine.json`: Step Functions definition with retry, backoff and fallback

## Clean up

Delete the Lambda function and log group; stop deployments and delete the AppConfig profile, environment and application; delete the IAM role and any state machine you created.
