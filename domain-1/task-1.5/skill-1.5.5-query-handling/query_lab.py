"""Lab: Skill 1.5.5 - query expansion and decomposition.

  python query_lab.py baseline    # step 1: informal and multi-part questions, searched as typed
  python query_lab.py expand      # step 2: query expansion with Bedrock
  python query_lab.py decompose   # step 3: query decomposition, retrieve per part, merge, answer
  python query_lab.py pipeline    # step 4: classify, then expand or decompose: what the Step Functions workflow runs
"""
import sys
import query_tools as qt

INFORMAL = "my trimmer's busted after 10 days, can i get my cash back??"
COMPOUND = "Can I return a drill after 2 months, and which blade fits the HT-650?"


def show(results):
    for r in results:
        print(f"   {r['score']:>7}  {r['id']:22} {r['text'][:70]}")


def step_baseline():
    for q in (INFORMAL, COMPOUND):
        print(f"\n{q}")
        show(qt.search.search(q, 3))


def step_expand():
    queries = qt.expand(INFORMAL)
    print("Expanded queries:\n   " + "\n   ".join(queries))
    print("\nFused results:")
    show(qt.merge(qt.retrieve_all(queries), k=3))


def step_decompose():
    parts = qt.decompose(COMPOUND)
    print("Sub-questions:\n   " + "\n   ".join(parts))
    passages = qt.merge(qt.retrieve_all(parts), k=4)
    print("\nMerged passages:")
    show(passages)
    print("\nAnswer:\n" + qt.answer(COMPOUND, passages))


def step_pipeline():
    for q in (INFORMAL, COMPOUND):
        kind = qt.classify(q)
        queries = qt.expand(q) if kind == "simple" else qt.decompose(q)
        passages = qt.merge(qt.retrieve_all(queries), k=4)
        print(f"\n{q}\n   kind: {kind}; {len(queries)} queries; passages: {[p['id'] for p in passages]}")
        print("   " + qt.answer(q, passages).replace("\n", "\n   "))


if __name__ == "__main__":
    steps = {"baseline": step_baseline, "expand": step_expand, "decompose": step_decompose, "pipeline": step_pipeline}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python query_lab.py baseline|expand|decompose|pipeline")
    steps[step]()
