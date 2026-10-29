# Skill 1.5.1 lab: Chunking documents for better retrieval

Chunk one returns policy two ways in code, then index it into two Bedrock knowledge bases (tiny fixed-size chunks and hierarchical chunks) and compare what each retrieves for a question whose answer depends on a section heading.

- **Time:** about 40 minutes
- **Cost:** under US$0.20 with S3 Vectors stores, if you clean up the same day
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; an S3 bucket in us-west-2; permission to create Bedrock knowledge bases

## Files

| File | What it is |
| --- | --- |
| `returns-policy.md` | A short policy where similar sentences sit under different headings |
| `chunkers.py` | Fixed-size and structure-based (hierarchical) chunking in plain Python, as a Lambda function would run it |
| `compare_kbs.py` | Retrieves from both knowledge bases and prints what each returns |

## Part 1: Chunk in code (no AWS)

```bash
python chunkers.py fixed
python chunkers.py structure
python chunkers.py compare
```

## Part 2: Two knowledge bases

```bash
aws s3 cp returns-policy.md s3://your-bucket-name/chunking-lab/
```

Bedrock console → **Knowledge Bases** → **Create** → **Knowledge Base with vector store**, twice. Everything is the same except chunking:

| Setting | `kb-chunk-fixed` | `kb-chunk-hier` |
| --- | --- | --- |
| Data source | S3, `s3://your-bucket-name/chunking-lab/` | same |
| Chunking | **Fixed-size**: max tokens 40, overlap 0% | **Hierarchical**: parent 400, child 40, overlap 20 tokens |
| Embeddings | Titan Text Embeddings V2 | same |
| Vector store | Quick create → Amazon S3 Vectors | same |

Sync both data sources, then:

```bash
pip install boto3
export KB_FIXED=XXXXXXXXXX KB_HIER=XXXXXXXXXX
python compare_kbs.py
python compare_kbs.py "Can I return a clearance drill?"
```

The 40-token size is deliberately tiny so the problem shows on a short document. Expect `kb-chunk-hier` to return fewer than 5 results: several child matches share one parent.

## Clean up

Delete both knowledge bases, the S3 vector buckets that quick create made, the `chunking-lab/` objects and the knowledge base service roles.
