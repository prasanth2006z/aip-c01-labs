"""Lab: Skill 1.3.3 - formatting input for Amazon Bedrock with the Converse API.

  python format_input.py basic       # system prompt + one user message + inference settings
  python format_input.py history     # multi-turn conversation history
  python format_input.py broken      # a badly formatted conversation, and the error it causes
  python format_input.py structured  # JSON output that matches a schema, using tool use
"""
import json, sys
import boto3
from botocore.exceptions import ClientError

MODEL_ID = "us.amazon.nova-2-lite-v1:0"
bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")

SYSTEM = [{"text": "You are a returns assistant for a garden-tools shop. "
                   "Standard items: 30-day returns. Hedge trimmers: 14 days. "
                   "Registered power tools: 90 days. Answer in one sentence."}]
SETTINGS = {"maxTokens": 200, "temperature": 0}


def show(label, request):
    print(f"\n--- {label}: request ---")
    printable = {k: v for k, v in request.items() if k != "modelId"}
    print(json.dumps(printable, indent=2))


def basic():
    req = {"modelId": MODEL_ID, "system": SYSTEM, "inferenceConfig": SETTINGS,
           "messages": [{"role": "user", "content": [{"text": "How long do I have to return a hedge trimmer?"}]}]}
    show("basic", req)
    r = bedrock.converse(**req)
    print("--- answer ---\n" + r["output"]["message"]["content"][0]["text"])


def history():
    # The model has no memory: every request carries the whole conversation so far.
    messages = [
        {"role": "user", "content": [{"text": "I bought a leaf blower three weeks ago."}]},
        {"role": "assistant", "content": [{"text": "Thanks. A leaf blower is a standard item, so it has a 30-day return window."}]},
        {"role": "user", "content": [{"text": "So how many days do I have left?"}]},
    ]
    req = {"modelId": MODEL_ID, "system": SYSTEM, "inferenceConfig": SETTINGS, "messages": messages}
    show("history", req)
    r = bedrock.converse(**req)
    print("--- answer ---\n" + r["output"]["message"]["content"][0]["text"])


def broken():
    # Two user turns in a row: Converse expects user and assistant turns to alternate.
    req = {"modelId": MODEL_ID, "inferenceConfig": SETTINGS, "messages": [
        {"role": "user", "content": [{"text": "I bought a leaf blower."}]},
        {"role": "user", "content": [{"text": "Can I return it?"}]},
    ]}
    show("broken", req)
    try:
        bedrock.converse(**req)
        print("--- no error (this model accepted it) ---")
    except ClientError as e:
        print(f"--- {e.response['Error']['Code']} ---\n{e.response['Error']['Message']}")


RETURN_TOOL = {"toolSpec": {
    "name": "record_return",
    "description": "Record a customer's return request.",
    "inputSchema": {"json": {
        "type": "object",
        "properties": {
            "item": {"type": "string"},
            "days_since_purchase": {"type": "integer"},
            "eligible": {"type": "boolean"},
            "reason": {"type": "string"},
        },
        "required": ["item", "days_since_purchase", "eligible"],
    }},
}}


def structured():
    req = {"modelId": MODEL_ID, "system": SYSTEM, "inferenceConfig": SETTINGS,
           "messages": [{"role": "user", "content": [{"text":
               "My hedge trimmer stopped working. I bought it 10 days ago. Record my return."}]}],
           "toolConfig": {"tools": [RETURN_TOOL], "toolChoice": {"any": {}}}}
    show("structured", req)
    r = bedrock.converse(**req)
    for block in r["output"]["message"]["content"]:
        if "toolUse" in block:
            print("--- structured output (toolUse.input) ---")
            print(json.dumps(block["toolUse"]["input"], indent=2))


if __name__ == "__main__":
    steps = {"basic": basic, "history": history, "broken": broken, "structured": structured}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python format_input.py basic|history|broken|structured")
    steps[step]()
