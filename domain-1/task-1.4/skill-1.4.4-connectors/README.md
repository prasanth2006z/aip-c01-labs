# Skill 1.4.4 lab: Connect an internal wiki to a knowledge base

Add a **custom data source** to the knowledge base from the [Skill 1.4.2 lab](../skill-1.4.2-metadata), push pages from an internal wiki export straight into the index with metadata, check their status, query them, and delete an outdated page, all without a full sync.

- **Time:** about 25 minutes
- **Cost:** a few cents (embedding four short pages)
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; the `aip-lab-kb` knowledge base from the Skill 1.4.2 lab

## Files

| File | What it is |
| --- | --- |
| `wiki_export.json` | Four pages from a made-up internal wiki, as a wiki API would return them |
| `wiki_connector.py` | The connector: maps each page to a knowledge base document with metadata |

## Run it

```bash
pip install boto3
export KB_ID=XXXXXXXXXX
python wiki_connector.py create      # prints: export WIKI_DS_ID=...
export WIKI_DS_ID=XXXXXXXXXX
python wiki_connector.py ingest
python wiki_connector.py status      # repeat until every page shows INDEXED
python wiki_connector.py ask
python wiki_connector.py delete
python wiki_connector.py status
```

## Native connectors

For systems with a built-in connector, configure the data source in the console instead of writing code: **Confluence**, **SharePoint**, **Salesforce**, **Web Crawler** and **Amazon S3**. Credentials go in AWS Secrets Manager. Use a custom data source like this one for anything else, or when you need to push changes the moment they happen.

## Clean up

Keep the data source for the Skill 1.4.5 lab, or delete it: Knowledge Bases → `aip-lab-kb` → Data sources → `internal-wiki` → Delete.
