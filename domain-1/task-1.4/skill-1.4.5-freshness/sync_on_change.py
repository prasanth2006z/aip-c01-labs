"""Lambda function: start an incremental knowledge base sync.

Trigger it from S3 event notifications (near real time) and from an EventBridge Scheduler
schedule (a nightly safety net). Environment variables: KB_ID, DS_ID.
"""
import json, os
import boto3

agent = boto3.client("bedrock-agent")


def handler(event, context):
    source = "schedule" if event.get("source") == "aws.scheduler" or "Records" not in event else "s3"
    keys = [r["s3"]["object"]["key"] for r in event.get("Records", [])]
    try:
        job = agent.start_ingestion_job(knowledgeBaseId=os.environ["KB_ID"], dataSourceId=os.environ["DS_ID"],
                                        description=f"triggered by {source}")["ingestionJob"]
        print(json.dumps({"started": job["ingestionJobId"], "source": source, "keys": keys}))
    except agent.exceptions.ConflictException:
        # A sync is already running. It may miss this change, so the nightly schedule catches up.
        print(json.dumps({"skipped": "sync already running", "source": source, "keys": keys}))
    return {"ok": True}
