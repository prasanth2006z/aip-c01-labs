# Skill 1.5.5 lab: Rewrite queries for better retrieval

Search an informal question and a two-part question as typed, then improve retrieval with **query expansion** (Bedrock rewrites the question into document wording) and **query decomposition** (split into sub-questions, retrieve each, merge). Optionally run the same logic as a Step Functions workflow.

- **Time:** about 30 minutes (plus 20 for the optional Step Functions part)
- **Cost:** under US$0.05
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; Amazon Nova 2 Lite (US inference profile) and Titan Text Embeddings V2

## Files

| File | What it is |
| --- | --- |
| `query_tools.py` | classify, expand, decompose, retrieve, merge and answer; also a Lambda handler |
| `query_lab.py` | The lab steps |
| `query_pipeline.asl.json` | Step Functions workflow: classify → expand or decompose → retrieve in parallel → merge and answer |

## Run it

```bash
pip install boto3
python query_lab.py baseline
python query_lab.py expand
python query_lab.py decompose
python query_lab.py pipeline
```

## Optional: Step Functions

1. Build a zip with `query_tools.py`, `../shared/search.py` and `../shared/corpus.json` at its root, and create a Python Lambda function `query-tools` from it (handler `query_tools.handler`, timeout 60 s). Its role needs `bedrock:InvokeModel` on Nova 2 Lite (inference profile and the underlying models) and Titan Text Embeddings V2.
2. Create a Standard state machine from `query_pipeline.asl.json`, replacing `${QueryToolsArn}` with the function ARN. Let the console create a role that can invoke it.
3. Start an execution with `{"question": "Can I return a drill after 2 months, and which blade fits the HT-650?"}` and follow it in the graph view.

## Clean up

Delete the state machine, the `query-tools` function, their roles and log groups. Nothing else to delete.
