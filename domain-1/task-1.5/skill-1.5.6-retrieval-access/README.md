# Skill 1.5.6 lab: Give models a standard way to search

Wrap vector search in **one retrieval contract** and expose it three ways: as a **tool** the model calls through the Converse API, as an **MCP server** any MCP client can discover, and as an **HTTP API** handler for API Gateway.

- **Time:** about 30 minutes
- **Cost:** under US$0.05
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3` and `mcp` (`pip install boto3 mcp`); Amazon Nova 2 Lite (US inference profile) and Titan Text Embeddings V2

## Files

| File | What it is |
| --- | --- |
| `retrieval_api.py` | The contract: `retrieve(query, k)` → `{query, results: [{id, source, text, score}]}`, the tool name, description and JSON schema, and an API Gateway Lambda handler |
| `tool_calling.py` | Converse API tool loop: the model decides when to search |
| `mcp_server.py` | The same search as an MCP tool (stdio) |
| `mcp_client.py` | Discovers the MCP tool, calls it, then hands it to a Bedrock model |

## Run it (from this folder)

```bash
pip install boto3 mcp
python tool_calling.py
python mcp_client.py
python mcp_client.py --with-model
```

In `tool_calling.py`, watch the third question: the model answers a general question without calling the tool.

## Optional: HTTP API

Zip `retrieval_api.py`, `../shared/search.py` and `../shared/corpus.json`, create a Lambda function with handler `retrieval_api.lambda_handler`, and add an HTTP API in API Gateway with route `POST /retrieve`. Any service can then call `{"query": "...", "k": 3}` and get the same result shape as the tool and MCP callers.

## Clean up

Nothing to delete unless you created the optional Lambda function and API.
