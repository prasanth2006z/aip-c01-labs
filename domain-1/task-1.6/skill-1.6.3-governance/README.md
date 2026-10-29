# Skill 1.6.3 lab: Govern prompts with versions, approval and audit

Keep prompt templates in a versioned S3 repository, gate changes behind an approval tag, promote approved templates into Bedrock Prompt Management as immutable versions, and trace changes and usage with CloudTrail and CloudWatch Logs.

- **Time:** about 30 minutes
- **Cost:** under US$0.01
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; the `returns-assistant` prompt from the [Skill 1.6.1 lab](../skill-1.6.1-instructions) (its ID is the part of `PROMPT_ARN` after `prompt/` and before `:`); an S3 bucket in us-west-2

## Files

| File | What it is |
| --- | --- |
| `templates/returns-assistant.json` | Version 2 of the prompt template, with an owner and a change note |
| `governance_lab.py` | The lab steps |

## Run it

```bash
pip install boto3
export LAB_BUCKET=your-bucket-name PROMPT_ID=XXXXXXXXXX
python governance_lab.py submit
python governance_lab.py promote     # refused: not approved yet
python governance_lab.py approve
python governance_lab.py promote     # creates version 2
python governance_lab.py versions
python governance_lab.py audit
```

## Optional: invocation logs

Bedrock console → **Settings** → **Model invocation logging** → enable, destination **CloudWatch Logs**, log group `/aws/bedrock/invocations` (let the console create the role). Run the Skill 1.6.1 `ask` step again, then:

```bash
export INVOCATION_LOG_GROUP=/aws/bedrock/invocations
python governance_lab.py logs
```

Invocation logs hold full prompts and responses, so restrict access to the log group and set a retention period.

## In production

- Only a CI/CD role can call `UpdatePrompt` and `CreatePromptVersion`; authors can only write to S3.
- Approval is a separate identity: a pull request review, a CodePipeline manual approval, or a Step Functions task that waits for a reviewer.
- Applications call a pinned prompt version ARN, so a new version changes nothing until it's deliberately rolled out.

## Clean up

Delete `prompt-templates/` (all versions) from the bucket; turn off invocation logging and delete the log group if you enabled them. Delete the prompt when you finish Task 1.6.
