"""One retrieval contract for every caller: tool calling, MCP and HTTP all go through retrieve()."""
import json, sys
from pathlib import Path

for p in (Path(__file__).parent, Path(__file__).parent.parent / "shared"):
    if (p / "search.py").exists():
        sys.path.insert(0, str(p))
import search  # noqa: E402

TOOL_NAME = "search_knowledge"
TOOL_DESCRIPTION = ("Search Acme Tools' policies, shipping, warranty and parts documents. "
                    "Use it for any question about returns, refunds, delivery, warranty or spare parts.")
INPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "query": {"type": "string", "description": "A self-contained search query"},
        "k": {"type": "integer", "description": "Number of passages to return (1-5)", "default": 3},
    },
    "required": ["query"],
}


def retrieve(query: str, k: int = 3) -> dict:
    """The contract: same input, same output shape, whoever calls it."""
    k = max(1, min(int(k), 5))
    results = search.search(query, k)
    return {"query": query, "results": [
        {"id": r["id"], "source": r["source"], "text": r["text"], "score": r["score"]} for r in results]}


def lambda_handler(event, context=None):
    """HTTP access: API Gateway (REST or HTTP API) proxy integration, POST /retrieve {"query": ..., "k": 3}."""
    body = json.loads(event.get("body") or "{}")
    if not body.get("query"):
        return {"statusCode": 400, "body": json.dumps({"error": "query is required"})}
    return {"statusCode": 200, "headers": {"Content-Type": "application/json"},
            "body": json.dumps(retrieve(body["query"], body.get("k", 3)))}
