"""Lab: Skill 1.5.2 - choose and configure an embedding model.

  python embeddings_lab.py dims      # step 1: vector size and storage at 256, 512 and 1,024 dimensions
  python embeddings_lab.py quality   # step 2: retrieval quality and latency per dimension on 8 test questions
  python embeddings_lab.py models    # step 3: Titan Text Embeddings V2 vs Cohere Embed English v3
  python embeddings_lab.py batch     # step 4: Lambda-style batch embedding with parallel calls
"""
import json, statistics, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
import search  # noqa: E402  (shared corpus, embed(), vector_search())

TESTS = json.loads((Path(__file__).parent.parent / "shared" / "test_questions.json").read_text())


def step_dims():
    for d in (256, 512, 1024):
        v = search.embed("How long can I return a hedge trimmer?", d)
        per_vec = len(v) * 4                                   # float32
        print(f"{d:5} dims  length={len(v)}  {per_vec:>5} bytes/vector  "
              f"{per_vec * 1_000_000 / 1e9:.1f} GB per million vectors")


def evaluate(dims):
    ranks, times = [], []
    for t in TESTS:
        start = time.perf_counter()
        ids = [r["id"] for r in search.vector_search(t["q"], k=len(search.CORPUS), dims=dims)]
        times.append((time.perf_counter() - start) * 1000)
        ranks.append(ids.index(t["answer"]) + 1)
    return {"recall@1": sum(r == 1 for r in ranks) / len(ranks),
            "recall@3": sum(r <= 3 for r in ranks) / len(ranks),
            "MRR": round(statistics.mean(1 / r for r in ranks), 3),
            "median ms per query": round(statistics.median(times))}


def step_quality():
    for d in (256, 512, 1024):
        search.corpus_vectors(d)                               # embed the corpus once per size (cached)
        print(f"{d:5} dims  {evaluate(d)}")


def cohere_embed(texts, input_type):
    body = json.dumps({"texts": texts, "input_type": input_type})
    res = search.bedrock().invoke_model(modelId="cohere.embed-english-v3", body=body)
    return json.loads(res["body"].read())["embeddings"]


def step_models():
    print("Titan Text Embeddings V2 (1,024 dims):", evaluate(1024))
    try:
        docs = cohere_embed([d["text"] for d in search.CORPUS], "search_document")
        ranks = []
        for t in TESTS:
            q = cohere_embed([t["q"]], "search_query")[0]
            def cos(a, b): return sum(x * y for x, y in zip(a, b)) / ((sum(x * x for x in a) * sum(y * y for y in b)) ** 0.5)
            order = sorted(range(len(docs)), key=lambda i: -cos(q, docs[i]))
            ranks.append([search.CORPUS[i]["id"] for i in order].index(t["answer"]) + 1)
        print("Cohere Embed English v3 (1,024 dims):", {
            "recall@1": sum(r == 1 for r in ranks) / len(ranks), "recall@3": sum(r <= 3 for r in ranks) / len(ranks),
            "MRR": round(statistics.mean(1 / r for r in ranks), 3)})
    except Exception as e:                                     # model not enabled in this account or Region
        print(f"Cohere skipped: {type(e).__name__}: {e}")


def batch_handler(event, context=None):
    """What a batch-embedding Lambda function does: embed a list of records in parallel."""
    records = event["records"]
    dims = event.get("dimensions", 512)
    with ThreadPoolExecutor(max_workers=8) as pool:           # parallel calls; the SDK retries throttling
        vectors = list(pool.map(lambda r: search.embed(r["text"], dims), records))
    return [{"id": r["id"], "embedding": v} for r, v in zip(records, vectors)]


def step_batch():
    records = [{"id": d["id"], "text": d["text"]} for d in search.CORPUS] * 4     # 48 records
    for workers_note, fn in (("one at a time", None), ("8 in parallel", batch_handler)):
        start = time.perf_counter()
        if fn is None:
            for r in records:
                search.embed(r["text"], 512)
        else:
            fn({"records": records, "dimensions": 512})
        print(f"{len(records)} records, {workers_note}: {time.perf_counter() - start:.1f} s")


if __name__ == "__main__":
    steps = {"dims": step_dims, "quality": step_quality, "models": step_models, "batch": step_batch}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python embeddings_lab.py dims|quality|models|batch")
    steps[step]()
