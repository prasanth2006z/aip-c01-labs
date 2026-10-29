# Skill 1.4.2 lab: Add metadata to sharpen retrieval

Upload five policy documents with S3 user metadata and object tags, turn that metadata into knowledge base metadata files, then ask the same question with and without metadata filters.

- **Time:** about 45 minutes (most of it waiting for the knowledge base to create and sync)
- **Cost:** under US$0.10 with an S3 Vectors store (a few embedding calls and tiny storage)
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; an S3 bucket in us-west-2; permission to create a Bedrock knowledge base

This lab creates the knowledge base that the Skill 1.4.4 and 1.4.5 labs reuse. Keep it until you've finished Task 1.4.

## Files

| File | What it is |
| --- | --- |
| `docs/` | Five short documents: two versions of the US returns policy, a UK returns policy, a warranty page and a shipping page |
| `metadata_lab.py` | The lab steps |

## 1. Upload the documents

```bash
pip install boto3
export LAB_BUCKET=your-bucket-name
python metadata_lab.py upload
```

Each object gets user metadata (`x-amz-meta-author`, `x-amz-meta-published`) and tags (`domain`, `region`).

## 2. Create the knowledge base (console, once)

Amazon Bedrock console → **Knowledge Bases** → **Create** → **Knowledge Base with vector store**:

| Setting | Value |
| --- | --- |
| Name | `aip-lab-kb` |
| Service role | Create and use a new service role |
| Data source | Amazon S3, URI `s3://your-bucket-name/kb-docs/` |
| Parsing and chunking | Defaults |
| Embeddings model | Titan Text Embeddings V2 |
| Vector store | **Quick create a new vector store** → **Amazon S3 Vectors** |

Don't sync yet. Copy the knowledge base ID and the data source ID:

```bash
export KB_ID=XXXXXXXXXX DS_ID=XXXXXXXXXX
```

## 3. Add metadata files, sync, ask

```bash
python metadata_lab.py sidecars   # writes <file>.metadata.json next to each document
python metadata_lab.py sync
python metadata_lab.py ask
```

| Query | Expected top results |
| --- | --- |
| No filter | A mix: the 2025 and 2026 US policies and the UK policy all mention returns |
| `domain = returns`, `region = US`, `published_year >= 2026` | Only the 2026 US policy (14 days for hedge trimmers) |
| `published > 20260301` | Only the warranty page: the filter applies even when the text is a weaker match |

## Clean up

Keep the knowledge base for the next two labs. When you finish Task 1.4, see the clean-up list in [the task README](../README.md).
