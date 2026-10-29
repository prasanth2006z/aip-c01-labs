"""Lab: Skill 1.5.1 - chunking in code, the way a Lambda function would do it.

  python chunkers.py fixed         # fixed-size chunks with overlap (word-based approximation of tokens)
  python chunkers.py structure     # hierarchical chunks from the document's headings
  python chunkers.py compare       # which chunk would a search for "hedge trimmer" return, and what does it say?
"""
import json, re, sys
from pathlib import Path

DOC = (Path(__file__).parent / "returns-policy.md").read_text()


def fixed_size(text, size=30, overlap=5):
    """Split into windows of `size` words that overlap by `overlap` words. Ignores structure on purpose."""
    words = text.split()
    step = size - overlap
    return [{"id": f"fixed-{i}", "text": " ".join(words[s:s + size])}
            for i, s in enumerate(range(0, max(len(words) - overlap, 1), step))]


def by_structure(text, child_size=12):
    """Parent = a whole section under a '##' heading. Children = small pieces of it, each carrying the heading."""
    parents, children = [], []
    title = text.splitlines()[0].lstrip("# ").strip()
    for n, sec in enumerate(re.split(r"\n(?=## )", text)[1:]):
        heading, body = sec.split("\n", 1)
        heading = heading.lstrip("# ").strip()
        pid = f"parent-{n}"
        parents.append({"id": pid, "heading": heading, "text": f"{title} > {heading}\n{body.strip()}"})
        words = body.split()
        for i in range(0, len(words), child_size):
            children.append({"id": f"{pid}-child-{i // child_size}", "parent": pid,
                             "text": f"[{heading}] " + " ".join(words[i:i + child_size])})
    return parents, children


def show(chunks):
    for ch in chunks:
        print(f"--- {ch['id']} ({len(ch['text'].split())} words)\n{ch['text']}\n")


def compare():
    q = {"hedge", "trimmer", "trimmers", "return", "returns", "fee"}
    def hits(t): return sum(w.strip(".,").lower() in q for w in t.split())
    best_fixed = max(fixed_size(DOC), key=lambda c: hits(c["text"]))
    parents, children = by_structure(DOC)
    best_child = max(children, key=lambda c: hits(c["text"]))
    parent = next(p for p in parents if p["id"] == best_child["parent"])
    print("Fixed-size: the best-matching chunk is what the model gets\n" + best_fixed["text"] + "\n")
    print("Structure-based: match on the child ...\n" + best_child["text"] + "\n")
    print("... but give the model its parent section\n" + parent["text"])


if __name__ == "__main__":
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step == "fixed":
        show(fixed_size(DOC))
    elif step == "structure":
        parents, children = by_structure(DOC)
        show(parents); print(f"{len(children)} child chunks, each tagged with its heading")
    elif step == "compare":
        compare()
    else:
        sys.exit("Usage: python chunkers.py fixed|structure|compare")
