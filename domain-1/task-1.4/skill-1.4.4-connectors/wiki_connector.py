"""Lab: Skill 1.4.4 - a custom connector that pushes internal wiki pages into a knowledge base.

  export KB_ID=XXXXXXXXXX                 # the knowledge base from the Skill 1.4.2 lab
  python wiki_connector.py create         # step 1: add a CUSTOM data source; then export WIKI_DS_ID
  python wiki_connector.py ingest         # step 2: push wiki pages straight into the index, with metadata
  python wiki_connector.py status         # step 3: check each page's indexing status
  python wiki_connector.py ask            # step 4: retrieve from wiki pages only
  python wiki_connector.py delete         # step 5: remove an outdated page without a full sync
"""
import json, os, sys
from pathlib import Path
import boto3

REGION = "us-west-2"
agent = boto3.client("bedrock-agent", region_name=REGION)
runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)
PAGES = json.loads((Path(__file__).parent / "wiki_export.json").read_text())


def env(name):
    if not os.environ.get(name):
        sys.exit(f"Set {name} first (see the README).")
    return os.environ[name]


def create():
    ds = agent.create_data_source(knowledgeBaseId=env("KB_ID"), name="internal-wiki",
                                  dataSourceConfiguration={"type": "CUSTOM"})["dataSource"]
    print(f"Created data source {ds['dataSourceId']}\n\nexport WIKI_DS_ID={ds['dataSourceId']}")


def to_document(page):
    """What a real connector does for every page it reads from the wiki's API."""
    def s(k, v): return {"key": k, "value": {"type": "STRING", "stringValue": v}}
    def n(k, v): return {"key": k, "value": {"type": "NUMBER", "numberValue": v}}
    return {
        "content": {
            "dataSourceType": "CUSTOM",
            "custom": {
                "customDocumentIdentifier": {"id": page["id"]},      # stable ID: re-ingesting replaces the page
                "sourceType": "IN_LINE",
                "inlineContent": {"type": "TEXT", "textContent": {"data": f"{page['title']}\n\n{page['body']}"}},
            },
        },
        "metadata": {"type": "IN_LINE_ATTRIBUTE", "inlineAttributes": [
            s("source", "wiki"), s("space", page["space"]), s("title", page["title"]),
            n("published", int(page["updated"].replace("-", ""))),
        ]},
    }


def ingest():
    res = agent.ingest_knowledge_base_documents(knowledgeBaseId=env("KB_ID"), dataSourceId=env("WIKI_DS_ID"),
                                                documents=[to_document(p) for p in PAGES])
    for d in res["documentDetails"]:
        print(f"{d['identifier']['custom']['id']:10} {d['status']}")


def status():
    res = agent.list_knowledge_base_documents(knowledgeBaseId=env("KB_ID"), dataSourceId=env("WIKI_DS_ID"))
    for d in res["documentDetails"]:
        print(f"{d['identifier']['custom']['id']:10} {d['status']:12} {d.get('statusReason', '')}")


def ask():
    q = "Who has to approve a $500 refund?"
    for label, flt in [("whole knowledge base", None), ("wiki only", {"equals": {"key": "source", "value": "wiki"}})]:
        cfg = {"numberOfResults": 3, **({"filter": flt} if flt else {})}
        res = runtime.retrieve(knowledgeBaseId=env("KB_ID"), retrievalQuery={"text": q},
                               retrievalConfiguration={"vectorSearchConfiguration": cfg})
        print(f"\n{q}  [{label}]")
        for r in res["retrievalResults"]:
            md = r.get("metadata", {})
            print(f"   {r.get('score', 0):.3f}  {md.get('title') or md.get('x-amz-bedrock-kb-source-uri', '?').rsplit('/', 1)[-1]}")


def delete():
    res = agent.delete_knowledge_base_documents(knowledgeBaseId=env("KB_ID"), dataSourceId=env("WIKI_DS_ID"),
                                                documentIdentifiers=[{"dataSourceType": "CUSTOM", "custom": {"id": "wiki-103"}}])
    for d in res["documentDetails"]:
        print(f"{d['identifier']['custom']['id']:10} {d['status']}")


if __name__ == "__main__":
    steps = {"create": create, "ingest": ingest, "status": status, "ask": ask, "delete": delete}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python wiki_connector.py create|ingest|status|ask|delete")
    steps[step]()
