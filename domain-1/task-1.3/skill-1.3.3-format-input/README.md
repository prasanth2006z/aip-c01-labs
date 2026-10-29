# Skill 1.3.3 lab: Format input for Amazon Bedrock

Build Converse API requests step by step: a system prompt and inference settings, a multi-turn conversation, a deliberately broken conversation, and JSON output that matches a schema using tool use.

- **Time:** about 30 minutes
- **Cost:** under US$0.02
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; `bedrock:InvokeModel` on Amazon Nova 2 Lite through the US inference profile

## Run it

```bash
pip install boto3
python format_input.py basic
python format_input.py history
python format_input.py broken
python format_input.py structured
```

Each step prints the request it sends, then the model's answer (or the error), so you can see exactly how the input is shaped.

## Clean up

Nothing to delete: the lab only calls a model on demand.
