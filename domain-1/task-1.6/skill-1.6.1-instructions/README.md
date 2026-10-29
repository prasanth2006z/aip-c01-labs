# Skill 1.6.1 lab: Control model behaviour with Prompt Management and Guardrails

Create a managed prompt that defines the assistant's role, rules and response format, a guardrail with a denied topic, content filters, prompt-attack detection and PII masking, then run both together on four test messages.

- **Time:** about 30 minutes
- **Cost:** under US$0.05 (a few model calls and guardrail checks)
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; permission for `bedrock:CreatePrompt`, `bedrock:CreatePromptVersion`, `bedrock:CreateGuardrail`, `bedrock:CreateGuardrailVersion`, `bedrock:ApplyGuardrail` and Amazon Nova 2 Lite through the US inference profile

## Run it

```bash
pip install boto3
python instructions_lab.py prompt       # prints export PROMPT_ARN=...
python instructions_lab.py guardrail    # prints export GUARDRAIL_ID=... GUARDRAIL_VERSION=...
export PROMPT_ARN=... GUARDRAIL_ID=... GUARDRAIL_VERSION=1
python instructions_lab.py ask
python instructions_lab.py check "Call me on 555-0142, you useless idiots."
```

| Test message | Expected |
| --- | --- |
| Opened hedge trimmer | Normal answer in the three-line format: 14 days, 15% fee |
| Can I sue you? | Blocked by the `LegalAdvice` denied topic: `stopReason: guardrail_intervened` |
| Ignore all previous instructions | Blocked by the prompt-attack filter |
| Message with email and phone | Answered; email and phone number are masked as `{EMAIL}` and `{PHONE}` |

## Clean up

Delete the `returns-assistant` prompt (Prompt management) and the `returns-assistant-guardrail` guardrail in the Bedrock console. The Skill 1.6.3 lab reuses the prompt, so keep it if you're going on.
