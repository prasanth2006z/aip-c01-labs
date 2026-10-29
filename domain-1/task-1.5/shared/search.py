"""Shared search helpers for the Task 1.5 labs: Titan embeddings, cosine search, BM25 and fusion.

Embeddings are cached in .embeddings-<dims>.json next to this file, so each text is embedded once.
Set OFFLINE=1 to skip Bedrock and use keyword (BM25) search only, for testing without an AWS account.
"""
import json, math, os, re
from collections import Counter
from pathlib import Path

REGION = "us-west-2"
EMBED_MODEL = "amazon.titan-embed-text-v2:0"
HERE = Path(__file__).parent
CORPUS = json.loads((HERE / "corpus.json").read_text())
OFFLINE = os.environ.get("OFFLINE") == "1"
_bedrock = None


def bedrock():
    global _bedrock
    if _bedrock is None:
        import boto3
        _bedrock = boto3.client("bedrock-runtime", region_name=REGION)
    return _bedrock


def embed(text, dims=1024):
    body = json.dumps({"inputText": text, "dimensions": dims, "normalize": True})
    res = bedrock().invoke_model(modelId=EMBED_MODEL, body=body)
    return json.loads(res["body"].read())["embedding"]


def corpus_vectors(dims=1024):
    cache = HERE / f".embeddings-{dims}.json"
    vecs = json.loads(cache.read_text()) if cache.exists() else {}
    missing = [d for d in CORPUS if d["id"] not in vecs]
    for d in missing:
        vecs[d["id"]] = embed(d["text"], dims)
    if missing:
        cache.write_text(json.dumps(vecs))
    return vecs


def cosine(a, b):
    return sum(x * y for x, y in zip(a, b))          # vectors are normalised, so the dot product is the cosine


def vector_search(query, k=5, dims=1024, docs=None):
    docs = docs or CORPUS
    vecs, q = corpus_vectors(dims), embed(query, dims)
    scored = sorted(((cosine(q, vecs[d["id"]]), d) for d in docs), key=lambda x: -x[0])
    return [{"id": d["id"], "source": d["source"], "text": d["text"], "score": round(s, 4)} for s, d in scored[:k]]


TOKEN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")


def tokens(text):
    return TOKEN.findall(text.lower())


def bm25_search(query, k=5, docs=None, k1=1.5, b=0.75):
    docs = docs or CORPUS
    toks = [tokens(d["text"]) for d in docs]
    avg = sum(map(len, toks)) / len(toks)
    df = Counter(t for ts in toks for t in set(ts))
    n = len(docs)
    scores = []
    for d, ts in zip(docs, toks):
        tf = Counter(ts)
        s = 0.0
        for t in tokens(query):
            if t in tf:
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(ts) / avg))
        scores.append((s, d))
    scores.sort(key=lambda x: -x[0])
    return [{"id": d["id"], "source": d["source"], "text": d["text"], "score": round(s, 4)} for s, d in scores[:k] if s > 0]


def rrf(*result_lists, k=5, c=60):
    """Reciprocal rank fusion: combine ranked lists without comparing their raw scores."""
    fused, by_id = Counter(), {}
    for results in result_lists:
        for rank, r in enumerate(results, 1):
            fused[r["id"]] += 1 / (c + rank)
            by_id[r["id"]] = r
    return [{**by_id[i], "score": round(s, 4)} for i, s in fused.most_common(k)]


def search(query, k=5, mode="hybrid"):
    """One entry point used by the query-handling and access labs."""
    if OFFLINE or mode == "keyword":
        return bm25_search(query, k)
    if mode == "vector":
        return vector_search(query, k)
    return rrf(vector_search(query, k * 2), bm25_search(query, k * 2), k=k)
