"""Lab: Skill 1.6.3 - prompt governance: a template repository, an approval gate, versions and an audit trail.

  export LAB_BUCKET=your-bucket PROMPT_ID=XXXXXXXXXX     # PROMPT_ID: the prompt from the Skill 1.6.1 lab
  python governance_lab.py submit      # step 1: upload the template to the S3 repository as pending review
  python governance_lab.py promote     # step 2: try to promote it: refused, not approved yet
  python governance_lab.py approve     # step 3: a reviewer approves it (an S3 object tag)
  python governance_lab.py promote     # step 4: update the managed prompt and create an immutable version
  python governance_lab.py versions    # step 5: list versions and compare them
  python governance_lab.py audit       # step 6: who changed prompts, from CloudTrail
  python governance_lab.py logs        # step 7: recent model invocations, from CloudWatch Logs
"""
import json, os, sys, time
from datetime import datetime, timedelta, timezone
from pathlib import Path
import boto3

REGION = "us-west-2"
KEY = "prompt-templates/returns-assistant.json"
s3 = boto3.client("s3", region_name=REGION)
agent = boto3.client("bedrock-agent", region_name=REGION)
cloudtrail = boto3.client("cloudtrail", region_name=REGION)
logs = boto3.client("logs", region_name=REGION)


def env(name):
    return os.environ.get(name) or sys.exit(f"Set {name} first (see the README).")


def submit():
    bucket = env("LAB_BUCKET")
    s3.put_bucket_versioning(Bucket=bucket, VersioningConfiguration={"Status": "Enabled"})
    body = (Path(__file__).parent / "templates" / "returns-assistant.json").read_bytes()
    res = s3.put_object(Bucket=bucket, Key=KEY, Body=body, ContentType="application/json",
                        Tagging="status=pending-review&submitted-by=" + os.environ.get("USER", "author"))
    print(f"submitted s3://{bucket}/{KEY}  version {res['VersionId']}  status=pending-review")


def tags(bucket):
    return {t["Key"]: t["Value"] for t in s3.get_object_tagging(Bucket=bucket, Key=KEY)["TagSet"]}


def approve():
    bucket = env("LAB_BUCKET")
    t = tags(bucket)
    t.update({"status": "approved", "approved-by": "reviewer", "approved-at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%MZ")})
    s3.put_object_tagging(Bucket=bucket, Key=KEY, Tagging={"TagSet": [{"Key": k, "Value": v} for k, v in t.items()]})
    print(f"approved: {t}")


def promote():
    bucket = env("LAB_BUCKET")
    t = tags(bucket)
    if t.get("status") != "approved":
        sys.exit(f"Refused: template status is '{t.get('status')}'. A reviewer must approve it first.")
    obj = s3.get_object(Bucket=bucket, Key=KEY)
    tpl = json.loads(obj["Body"].read())
    pid = env("PROMPT_ID")
    current = agent.get_prompt(promptIdentifier=pid)
    agent.update_prompt(
        promptIdentifier=pid, name=current["name"], defaultVariant="v1",
        description=f"{tpl['version_note']} (S3 version {obj['VersionId']})",
        variants=[{
            "name": "v1", "templateType": "CHAT", "modelId": tpl["model_id"],
            "inferenceConfiguration": {"text": tpl["inference"]},
            "templateConfiguration": {"chat": {
                "system": [{"text": tpl["system"]}],
                "messages": [{"role": "user", "content": [{"text": tpl["user"]}]}],
                "inputVariables": [{"name": v} for v in tpl["variables"]],
            }},
        }],
    )
    v = agent.create_prompt_version(promptIdentifier=pid,
                                    description=f"{tpl['version_note']} | approved-by {t.get('approved-by')} | s3 {obj['VersionId']}")
    print(f"promoted: version {v['version']}\nARN: {v['arn']}\nApplications pin this ARN; the DRAFT keeps changing.")


def versions():
    pid = env("PROMPT_ID")
    summaries = agent.list_prompts(promptIdentifier=pid)["promptSummaries"]
    for s in sorted(summaries, key=lambda s: s["version"]):
        print(f"{s['version']:6} {s['updatedAt']:%Y-%m-%d %H:%M}  {s.get('description', '')}")
    numbered = [s["version"] for s in summaries if s["version"] != "DRAFT"]
    if len(numbered) >= 2:
        a, b = (agent.get_prompt(promptIdentifier=pid, promptVersion=v) for v in sorted(numbered, key=int)[-2:])
        sa = a["variants"][0]["templateConfiguration"]["chat"]["system"][0]["text"].splitlines()
        sb = b["variants"][0]["templateConfiguration"]["chat"]["system"][0]["text"].splitlines()
        print(f"\nLines added in version {b['version']}:")
        for line in sb:
            if line not in sa:
                print("  + " + line)


def audit():
    start = datetime.now(timezone.utc) - timedelta(hours=24)
    for name in ("CreatePrompt", "UpdatePrompt", "CreatePromptVersion", "DeletePrompt"):
        events = cloudtrail.lookup_events(LookupAttributes=[{"AttributeKey": "EventName", "AttributeValue": name}],
                                          StartTime=start, MaxResults=20)["Events"]
        for e in events:
            print(f"{e['EventTime']:%Y-%m-%d %H:%M}  {name:20} {e.get('Username', '?')}")
    print("\n(CloudTrail can take up to 15 minutes to show new events.)")


def logs_step():
    group = env("INVOCATION_LOG_GROUP")
    since = int((time.time() - 3600) * 1000)
    events = logs.filter_log_events(logGroupName=group, startTime=since, limit=10)["events"]
    for e in events:
        rec = json.loads(e["message"])
        print(f"{rec.get('timestamp')}  {rec.get('modelId')}  identity={rec.get('identity', {}).get('arn', '?')}")
    if not events:
        print("No invocations in the last hour. Is model invocation logging enabled (see the README)?")


if __name__ == "__main__":
    steps = {"submit": submit, "approve": approve, "promote": promote, "versions": versions, "audit": audit, "logs": logs_step}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python governance_lab.py submit|approve|promote|versions|audit|logs")
    steps[step]()
