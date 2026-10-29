"""Lab: Skill 1.4.5 - keep the knowledge base current.

  export LAB_BUCKET=your-bucket KB_ID=XXXXXXXXXX DS_ID=XXXXXXXXXX   # from the Skill 1.4.2 lab
  python freshness.py ask       # step 1: what the knowledge base says now
  python freshness.py change    # step 2: update one policy, retire another
  python freshness.py detect    # step 3: compare S3 with the index: what is stale or orphaned?
  python freshness.py sync      # step 4: incremental sync; read the statistics
  python freshness.py ask       # step 5: the answer now reflects the change
"""
import os, sys, time
from pathlib import Path
import boto3

REGION = "us-west-2"
PREFIX = "kb-docs/"
s3 = boto3.client("s3", region_name=REGION)
agent = boto3.client("bedrock-agent", region_name=REGION)
runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)


def env(name):
    if not os.environ.get(name):
        sys.exit(f"Set {name} first (see the README).")
    return os.environ[name]


def ask():
    res = runtime.retrieve(knowledgeBaseId=env("KB_ID"),
                           retrievalQuery={"text": "How long do I have to return a hedge trimmer?"},
                           retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 2}})
    for r in res["retrievalResults"]:
        src = r.get("metadata", {}).get("x-amz-bedrock-kb-source-uri", "?").rsplit("/", 1)[-1]
        print(f"{r.get('score', 0):.3f}  {src}\n       {r['content']['text'][:160]}...")


def change():
    bucket = env("LAB_BUCKET")
    key = PREFIX + "returns-policy-2026.txt"
    old = s3.head_object(Bucket=bucket, Key=key)
    body = (Path(__file__).parent / "docs-v2" / "returns-policy-2026.txt").read_bytes()
    s3.put_object(Bucket=bucket, Key=key, Body=body, Metadata=old["Metadata"])     # keep author/published
    print(f"updated  {key}")
    for k in (PREFIX + "returns-policy-2025.txt", PREFIX + "returns-policy-2025.txt.metadata.json"):
        s3.delete_object(Bucket=bucket, Key=k)
        print(f"deleted  {k}")


def detect():
    """Change detection without syncing: compare each S3 object with what the index last saw."""
    bucket = env("LAB_BUCKET")
    in_s3 = {o["Key"]: o["LastModified"]
             for o in s3.list_objects_v2(Bucket=bucket, Prefix=PREFIX).get("Contents", [])
             if not o["Key"].endswith(".metadata.json")}
    docs = agent.list_knowledge_base_documents(knowledgeBaseId=env("KB_ID"), dataSourceId=env("DS_ID"))["documentDetails"]
    indexed = {d["identifier"]["s3"]["uri"].split(f"s3://{bucket}/", 1)[-1]: d["updatedAt"] for d in docs}
    for key, modified in sorted(in_s3.items()):
        if key not in indexed:
            print(f"NEW       {key}")
        elif modified > indexed[key]:
            print(f"STALE     {key}  (changed {modified:%H:%M:%S}, indexed {indexed[key]:%H:%M:%S})")
        else:
            print(f"current   {key}")
    for key in sorted(set(indexed) - set(in_s3)):
        print(f"ORPHANED  {key}  (deleted from S3, still in the index)")


def sync():
    kb, ds = env("KB_ID"), env("DS_ID")
    job = agent.start_ingestion_job(knowledgeBaseId=kb, dataSourceId=ds)["ingestionJob"]
    while job["status"] not in ("COMPLETE", "FAILED", "STOPPED"):
        time.sleep(5)
        job = agent.get_ingestion_job(knowledgeBaseId=kb, dataSourceId=ds, ingestionJobId=job["ingestionJobId"])["ingestionJob"]
    print(f"status: {job['status']}")
    for k, v in job.get("statistics", {}).items():
        print(f"  {k:40} {v}")


if __name__ == "__main__":
    steps = {"ask": ask, "change": change, "detect": detect, "sync": sync}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python freshness.py ask|change|detect|sync")
    steps[step]()
