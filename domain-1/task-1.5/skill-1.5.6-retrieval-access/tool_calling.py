"""Lab: Skill 1.5.6, part 1 - the model calls vector search as a tool (Converse API function calling).

  python tool_calling.py
"""
import json, sys
import retrieval_api as api

MODEL_ID = "us.amazon.nova-2-lite-v1:0"
SYSTEM = ("You are Acme Tools' support assistant. Use the search tool for any question about our policies, "
          "and cite passage IDs in brackets. Answer general questions directly.")


def run_with_tools(question, tool_specs, call_tool, max_turns=4):
    """Generic tool loop: the model asks for a tool, we run it, we send the result back, repeat."""
    messages = [{"role": "user", "content": [{"text": question}]}]
    for _ in range(max_turns):
        res = api.search.bedrock().converse(modelId=MODEL_ID, system=[{"text": SYSTEM}], messages=messages,
                                            toolConfig={"tools": tool_specs},
                                            inferenceConfig={"maxTokens": 400, "temperature": 0})
        msg = res["output"]["message"]
        messages.append(msg)
        if res["stopReason"] != "tool_use":
            return next(b["text"] for b in msg["content"] if "text" in b)
        results = []
        for block in msg["content"]:
            if "toolUse" in block:
                tu = block["toolUse"]
                print(f"   -> model called {tu['name']}({json.dumps(tu['input'])})")
                output = call_tool(tu["name"], tu["input"])
                print(f"   <- {len(output['results'])} passages: {[r['id'] for r in output['results']]}")
                results.append({"toolResult": {"toolUseId": tu["toolUseId"], "content": [{"json": output}]}})
        messages.append({"role": "user", "content": results})
    return "(stopped: too many tool calls)"


TOOL_SPECS = [{"toolSpec": {"name": api.TOOL_NAME, "description": api.TOOL_DESCRIPTION,
                            "inputSchema": {"json": api.INPUT_SCHEMA}}}]


def call_local(name, args):
    if name != api.TOOL_NAME:
        raise ValueError(name)
    return api.retrieve(**args)


if __name__ == "__main__":
    questions = sys.argv[1:] or [
        "How long do I have to return a hedge trimmer, and is there a fee?",
        "Which blade fits the HT-650, and how long would delivery take?",
        "What's a good way to sharpen garden shears?",
    ]
    for q in questions:
        print(f"\nQ: {q}")
        print("A: " + run_with_tools(q, TOOL_SPECS, call_local))
