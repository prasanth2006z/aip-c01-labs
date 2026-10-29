# Skill 1.5.2 lab: Choose and use embedding models

Compare Amazon Titan Text Embeddings V2 at 256, 512 and 1,024 dimensions on storage, retrieval quality and latency; compare it with Cohere Embed English v3; and batch-generate embeddings the way a Lambda function would.

- **Time:** about 30 minutes
- **Cost:** under US$0.01 (a few hundred short embedding calls)
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; `bedrock:InvokeModel` on `amazon.titan-embed-text-v2:0` (and optionally `cohere.embed-english-v3`)

## Files

| File | What it is |
| --- | --- |
| `embeddings_lab.py` | The four lab steps |
| `../shared/corpus.json` | Twelve short policy, shipping, warranty and parts passages |
| `../shared/test_questions.json` | Eight questions, each with the passage that answers it |
| `../shared/search.py` | Shared helpers: embed, cosine search, keyword search |

## Run it

```bash
pip install boto3
python embeddings_lab.py dims
python embeddings_lab.py quality
python embeddings_lab.py models
python embeddings_lab.py batch
```

Corpus embeddings are cached in `../shared/.embeddings-<dims>.json`, so reruns are fast and free. Delete those files to re-embed.

| Metric | Meaning |
| --- | --- |
| recall@1 | Share of questions whose answer passage ranked first |
| recall@3 | Share whose answer was in the top 3 (what a RAG prompt would usually include) |
| MRR | Mean reciprocal rank: 1.0 if the answer is always first, 0.5 if always second |

## Clean up

Nothing to delete.
