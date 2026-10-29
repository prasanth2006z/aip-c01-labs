"""Lab: Skill 1.4.2 - metadata that makes retrieval precise.

  export LAB_BUCKET=your-bucket KB_ID=XXXXXXXXXX DS_ID=XXXXXXXXXX
  python metadata_lab.py upload     # step 1: upload documents with S3 user metadata and object tags
  python metadata_lab.py sidecars   # step 2: turn S3 metadata and tags into .metadata.json files
  python metadata_lab.py sync       # step 3: sync the knowledge base and wait
  python metadata_lab.py ask        # step 4: the same question with and without metadata filters
"""
import json, os, sys, time
from pathlib import Path
import boto3

REGION = "us-west-2"
BUCKET = os.environ.get("LAB_BUCKET", "")
PREFIX = "kb-docs/"
s3 = boto3.client("s3", region_name=REGION)
agent = boto3.client("bedrock-agent", region_name=REGION)
runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)

# What each document's owner would set when publishing it.
DOCS = {
    "returns-policy-2025.txt":  {"meta": {"author": "returns-team", "published": "2025-01-15"}, "tags": {"domain": "returns", "region": "US"}},
    "returns-policy-2026.txt":  {"meta": {"author": "returns-team", "published": "2026-02-01"}, "tags": {"domain": "returns", "region": "US"}},
    "warranty-power-tools.txt": {"meta": {"author": "product-team", "published": "2026-03-10"}, "tags": {"domain": "warranty", "region": "US"}},
    "shipping-times.txt":       {"meta": {"author": "logistics",    "published": "2026-01-20"}, "tags": {"domain": "shipping", "region": "US"}},
    "store-returns-uk.txt":     {"meta": {"author": "uk-retail",    "published": "2026-02-01"}, "tags": {"domain": "returns", "region": "UK"}},
}


def need(*names):
    missing = [n for n in names if not os.environ.get(n)]
    if missing:
        sys.exit(f"Set {', '.join(missing)} first (see the README).")


def upload():
    need("LAB_BUCKET")
    for name, d in DOCS.items():
        body = (Path(__file__).parent / "docs" / name).read_bytes()
        tagging = "&".join(f"{k}={v}" for k, v in d["tags"].items())
        s3.put_object(Bucket=BUCKET, Key=PREFIX + name, Body=body, Metadata=d["meta"], Tagging=tagging)
        print(f"uploaded {name}  metadata={d['meta']}  tags={d['tags']}")


def sidecars():
    """The knowledge base reads metadata only from <file>.metadata.json, so build those from S3."""
    need("LAB_BUCKET")
    for name in DOCS:
        key = PREFIX + name
        head = s3.head_object(Bucket=BUCKET, Key=key)
        tags = {t["Key"]: t["Value"] for t in s3.get_object_tagging(Bucket=BUCKET, Key=key)["TagSet"]}
        published = head["Metadata"]["published"]                      # user metadata: x-amz-meta-published
        attrs = {
            "domain": tags["domain"],                                   # tag: domain classification
            "region": tags["region"],
            "author": head["Metadata"]["author"],                       # user metadata: x-amz-meta-author
            "published_year": int(published[:4]),                       # numbers allow range filters
            "published": int(published.replace("-", "")),               # 2026-02-01 -> 20260201
            "last_modified": head["LastModified"].strftime("%Y-%m-%d"), # system metadata from S3
        }
        s3.put_object(Bucket=BUCKET, Key=key + ".metadata.json",
                      Body=json.dumps({"metadataAttributes": attrs}).encode(), ContentType="application/json")
        print(f"{key}.metadata.json -> {attrs}")


def sync():
    need("KB_ID", "DS_ID")
    job = agent.start_ingestion_job(knowledgeBaseId=os.environ["KB_ID"], dataSourceId=os.environ["DS_ID"])["ingestionJob"]
    while job["status"] not in ("COMPLETE", "FAILED", "STOPPED"):
        time.sleep(5)
        job = agent.get_ingestion_job(knowledgeBaseId=os.environ["KB_ID"], dataSourceId=os.environ["DS_ID"],
                                      ingestionJobId=job["ingestionJobId"])["ingestionJob"]
        print("  ", job["status"])
    print(json.dumps(job.get("statistics", {}), indent=2))


def retrieve(question, flt=None):
    cfg = {"numberOfResults": 3}
    if flt:
        cfg["filter"] = flt
    res = runtime.retrieve(knowledgeBaseId=os.environ["KB_ID"], retrievalQuery={"text": question},
                           retrievalConfiguration={"vectorSearchConfiguration": cfg})
    for r in res["retrievalResults"]:
        md = r.get("metadata", {})
        src = md.get("x-amz-bedrock-kb-source-uri", "?").rsplit("/", 1)[-1]
        print(f"   {r.get('score', 0):.3f}  {src:28} domain={md.get('domain')} region={md.get('region')} year={md.get('published_year')}")


def ask():
    need("KB_ID")
    q = "How long do I have to return a hedge trimmer?"
    print(f"\nQ: {q}\n\n1. No filter:")
    retrieve(q)
    print("\n2. Only current US returns documents:")
    retrieve(q, {"andAll": [
        {"equals": {"key": "domain", "value": "returns"}},
        {"equals": {"key": "region", "value": "US"}},
        {"greaterThanOrEquals": {"key": "published_year", "value": 2026}},
    ]})
    print("\n3. Only documents published after 1 March 2026:")
    retrieve(q, {"greaterThan": {"key": "published", "value": 20260301}})


if __name__ == "__main__":
    steps = {"upload": upload, "sidecars": sidecars, "sync": sync, "ask": ask}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python metadata_lab.py upload|sidecars|sync|ask")
    steps[step]()
