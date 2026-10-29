"""Query handling functions for Skill 1.5.5. Used by query_lab.py, and deployable as one Lambda function
(handler: query_tools.handler) for the Step Functions workflow in query_pipeline.asl.json."""
import json, os, sys
from pathlib import Path

for p in (Path(__file__).parent, Path(__file__).parent.parent / "shared"):    # works locally and in Lambda
    if (p / "search.py").exists():
        sys.path.insert(0, str(p))
import search  # noqa: E402

MODEL_ID = os.environ.get("MODEL_ID", "us.amazon.nova-2-lite-v1:0")


def _tool_call(prompt, name, schema):
    """Ask the model for JSON that matches a schema, via tool use (see Skill 1.3.3)."""
    res = search.bedrock().converse(
        modelId=MODEL_ID,
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 300, "temperature": 0},
        toolConfig={"tools": [{"toolSpec": {"name": name, "description": name, "inputSchema": {"json": schema}}}],
                    "toolChoice": {"tool": {"name": name}}},
    )
    return next(b["toolUse"]["input"] for b in res["output"]["message"]["content"] if "toolUse" in b)


def classify(question):
    out = _tool_call(
        "Does this customer question ask about one thing or several separate things?\n\n" + question,
        "classify", {"type": "object", "properties": {"kind": {"type": "string", "enum": ["simple", "compound"]}},
                     "required": ["kind"]})
    return out["kind"]


def expand(question):
    """Query expansion: rewrite informal questions into the wording the documents use."""
    out = _tool_call(
        "Rewrite this customer question as 3 search queries for a retailer's policy documents. Use formal "
        "policy wording, include product category names and likely keywords.\n\n" + question,
        "queries", {"type": "object", "properties": {"queries": {"type": "array", "items": {"type": "string"}}},
                    "required": ["queries"]})
    return [question] + out["queries"][:3]


def decompose(question):
    """Query decomposition: one sub-question per thing asked."""
    out = _tool_call(
        "Split this customer question into separate, self-contained search questions, one per thing asked.\n\n" + question,
        "subquestions", {"type": "object", "properties": {"questions": {"type": "array", "items": {"type": "string"}}},
                         "required": ["questions"]})
    return out["questions"]


def retrieve_all(queries, k=3, mode="hybrid"):
    return [search.search(q, k, mode) for q in queries]


def merge(result_lists, k=4):
    return search.rrf(*result_lists, k=k)


def answer(question, passages):
    context = "\n".join(f"[{p['id']}] {p['text']}" for p in passages)
    res = search.bedrock().converse(
        modelId=MODEL_ID,
        system=[{"text": "Answer only from the passages. Cite passage IDs in brackets. If something isn't covered, say so."}],
        messages=[{"role": "user", "content": [{"text": f"Passages:\n{context}\n\nQuestion: {question}"}]}],
        inferenceConfig={"maxTokens": 300, "temperature": 0},
    )
    return res["output"]["message"]["content"][0]["text"]


def handler(event, context=None):
    """One Lambda function, several actions, called by each Step Functions state."""
    action = event["action"]
    if action == "classify":
        return {**event, "kind": classify(event["question"])}
    if action == "expand":
        return {**event, "queries": expand(event["question"])}
    if action == "decompose":
        return {**event, "queries": decompose(event["question"])}
    if action == "retrieve":
        return {"results": search.search(event["query"], event.get("k", 3))}
    if action == "merge_and_answer":
        passages = merge([r["results"] for r in event["retrieved"]])
        return {"question": event["question"], "passages": [p["id"] for p in passages],
                "answer": answer(event["question"], passages)}
    raise ValueError(f"unknown action {action}")
