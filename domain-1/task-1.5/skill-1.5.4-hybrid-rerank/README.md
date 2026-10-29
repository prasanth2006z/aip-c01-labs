# Skill 1.5.4 lab: Hybrid search and reranking

Run the same questions through keyword search (BM25), vector search, hybrid search (reciprocal rank fusion of both) and hybrid search followed by the Amazon Rerank model, and see which method puts the right passage first.

- **Time:** about 25 minutes
- **Cost:** under US$0.05 (embeddings plus a few dozen rerank queries)
- **Region:** us-west-2 (Amazon Rerank 1.0 is offered in a few Regions, including us-west-2)
- **Needs:** Python 3.10+ with `boto3`; `bedrock:InvokeModel` on Titan Text Embeddings V2 and on `amazon.rerank-v1:0`, and `bedrock:Rerank`

## Files

| File | What it is |
| --- | --- |
| `hybrid_rerank.py` | The lab steps |
| `../shared/search.py` | Keyword (BM25), vector and fusion (RRF) search over `../shared/corpus.json` |

## Run it

```bash
pip install boto3
python hybrid_rerank.py search "Which blade fits my HT-650?"
python hybrid_rerank.py search "How long do I have to return a hedge trimmer?"
python hybrid_rerank.py compare
```

The `compare` table shows the rank of the correct passage for each method (`-` means not in the top 8). Part numbers such as `HT-650` favour keyword search; paraphrased questions favour vectors; hybrid catches both, and reranking fixes the order.

## In a knowledge base or OpenSearch

- **Bedrock Knowledge Bases:** `retrieve` with `"overrideSearchType": "HYBRID"` (OpenSearch Serverless, Aurora and other supported stores) and a `rerankingConfiguration` in `vectorSearchConfiguration`.
- **OpenSearch:** a `hybrid` query with a `match` and a `neural` or `knn` clause, combined by a search pipeline with a normalisation processor.

## Clean up

Nothing to delete.
