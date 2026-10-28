# Skill 1.2.2 lab: Switch models without code changes

A Lambda function reads its model ID from AWS AppConfig and calls Amazon Bedrock with the Converse API. Changing the model is a configuration deployment, not a code change.

- **Time:** about 40 minutes
- **Cost:** under US$0.50
- **Region:** us-west-2
- **Needs:** permission for Lambda, AppConfig, IAM and Bedrock; Amazon Nova 2 Lite and Nova Micro through the US inference profiles

## Files

| File | What it is |
| --- | --- |
| `appconfig-model-settings.json` | The freeform AppConfig profile (starts on Nova 2 Lite) |
| `appconfig-validator.json` | JSON Schema validator that blocks empty or malformed model IDs |
| `lambda_function.py` | The `model-router` function |

## Steps (summary)

1. Create AppConfig application `genai-lab`, environment `prod`, freeform JSON profile `model-settings` from `appconfig-model-settings.json`, with `appconfig-validator.json` as its validator. Deploy it.
2. Create a Python 3.12 Lambda function `model-router` (30-second timeout) from `lambda_function.py`. Add the **AWS-AppConfig-Extension** layer. Allow `appconfig:StartConfigurationSession`, `appconfig:GetLatestConfiguration` and `bedrock:InvokeModel` on the Nova inference profiles and their underlying models.
3. Invoke it, then deploy a new configuration with `"model_id": "us.amazon.nova-micro-v1:0"`. After the extension's next poll, `model_used` changes.
4. Try deploying `"model_id": ""` and watch the validator reject it.

Full walkthrough: the Medium post **AIP-C01 Skill 1.2.2: Switch Models Without Code Changes**.
