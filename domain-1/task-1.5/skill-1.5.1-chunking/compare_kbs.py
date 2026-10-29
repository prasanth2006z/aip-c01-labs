"""Lab: Skill 1.5.1 - ask two knowledge bases with different chunking the same question.

  export KB_FIXED=XXXXXXXXXX KB_HIER=XXXXXXXXXX
  python compare_kbs.py "How long do I have to return a hedge trimmer, and is there a fee?"
"""
import os, sys
import boto3

runtime = boto3.client("bedrock-agent-runtime", region_name="us-west-2")
question = sys.argv[1] if len(sys.argv) > 1 else "How long do I have to return a hedge trimmer, and is there a fee?"

for label in ("KB_FIXED", "KB_HIER"):
    kb = os.environ.get(label) or sys.exit(f"Set {label} (see the README).")
    res = runtime.retrieve(knowledgeBaseId=kb, retrievalQuery={"text": question},
                           retrievalConfiguration={"vectorSearchConfiguration": {"numberOfResults": 5}})
    results = res["retrievalResults"]
    print(f"\n=== {label}: asked for 5, got {len(results)}")
    for r in results:
        print(f"{r.get('score', 0):.3f}  {r['content']['text'][:220]!r}")
