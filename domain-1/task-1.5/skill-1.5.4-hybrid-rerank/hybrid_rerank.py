"""Lab: Skill 1.5.4 - keyword, vector, hybrid and reranked search compared.

  python hybrid_rerank.py search "Which blade fits my HT-650?"   # step 1-3: one query through each method
  python hybrid_rerank.py compare                                 # step 4: rank of the right passage, all test questions
"""
import json, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
import search  # noqa: E402

RERANK_ARN = f"arn:aws:bedrock:{search.REGION}::foundation-model/amazon.rerank-v1:0"
TESTS = json.loads((Path(__file__).parent.parent / "shared" / "test_questions.json").read_text()) + [
    {"q": "HT-650 blade", "answer": "parts-sku"},
    {"q": "Can I return a broken hedge trimmer, and is there a fee?", "answer": "pol-garden"},
    {"q": "BP-18-4Ah charge time", "answer": "parts-battery"},
]
_agent_runtime = None


def rerank(query, candidates, k=3):
    """Score each candidate against the query with a reranker model, which reads both texts together."""
    global _agent_runtime
    if _agent_runtime is None:
        import boto3
        _agent_runtime = boto3.client("bedrock-agent-runtime", region_name=search.REGION)
    res = _agent_runtime.rerank(
        queries=[{"type": "TEXT", "textQuery": {"text": query}}],
        sources=[{"type": "INLINE", "inlineDocumentSource": {"type": "TEXT", "textDocument": {"text": c["text"]}}}
                 for c in candidates],
        rerankingConfiguration={"type": "BEDROCK_RERANKING_MODEL", "bedrockRerankingConfiguration": {
            "numberOfResults": k, "modelConfiguration": {"modelArn": RERANK_ARN}}},
    )
    return [{**candidates[r["index"]], "score": round(r["relevanceScore"], 4)} for r in res["results"]]


def methods(query, k=3):
    hybrid = search.rrf(search.vector_search(query, 8), search.bm25_search(query, 8), k=8)
    return {
        "keyword (BM25)": search.bm25_search(query, k),
        "vector": search.vector_search(query, k),
        "hybrid (RRF)": hybrid[:k],
        "hybrid + rerank": rerank(query, hybrid, k),
    }


def step_search(query):
    for name, results in methods(query).items():
        print(f"\n{name}")
        for r in results:
            print(f"  {r['score']:>7}  {r['id']:22} {r['text'][:70]}")


def step_compare():
    names = ["keyword (BM25)", "vector", "hybrid (RRF)", "hybrid + rerank"]
    print(f"{'question':52}" + "".join(f"{n:>17}" for n in names))
    totals = {n: 0 for n in names}
    for t in TESTS:
        row = f"{t['q'][:50]:52}"
        for name, results in methods(t["q"], 8).items():
            ids = [r["id"] for r in results]
            rank = ids.index(t["answer"]) + 1 if t["answer"] in ids else None
            totals[name] += rank == 1
            row += f"{(rank or '-'):>17}"
        print(row)
    print(f"{'ranked first':52}" + "".join(f"{f'{totals[n]}/{len(TESTS)}':>17}" for n in names))


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "search":
        step_search(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "compare":
        step_compare()
    else:
        sys.exit('Usage: python hybrid_rerank.py search "question" | compare')
