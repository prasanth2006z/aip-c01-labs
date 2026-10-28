"""Lab: Skill 1.1.2 - a proof-of-concept harness for a returns-policy assistant.

Runs every question in golden_set.json against each candidate model, then
reports accuracy, latency and estimated cost, and checks them against exit
criteria agreed before the PoC started.

Usage:  python poc_harness.py            (calls Amazon Bedrock in us-west-2)
"""
import json, statistics
from pathlib import Path
import boto3

HERE = Path(__file__).parent
POLICY = (HERE / "returns-policy.md").read_text()
GOLDEN = json.loads((HERE / "golden_set.json").read_text())

CANDIDATES = {
    "nova-2-lite": "us.amazon.nova-2-lite-v1:0",
    "nova-micro": "us.amazon.nova-micro-v1:0",
}

# USD per 1,000 tokens. Fill these in from the Amazon Bedrock pricing page
# for your Region; leave as None to skip the cost check.
PRICES = {
    "nova-2-lite": {"input": None, "output": None},
    "nova-micro": {"input": None, "output": None},
}

# Exit criteria: agree these with stakeholders BEFORE running the PoC.
EXIT_CRITERIA = {
    "min_accuracy": 0.90,               # share of golden questions answered correctly
    "max_p90_latency_ms": 3000,         # 90th-percentile latency per request
    "max_cost_per_1k_requests": 1.00,   # USD, only checked if PRICES are set
}

SYSTEM = ("You answer customer questions using ONLY the policy below. "
          "Reply in one short sentence. If the policy doesn't say, reply 'I don't know'.\n\n"
          + POLICY)


def is_correct(answer, case):
    """Correct if, for every group in any_of, at least one phrase appears."""
    text = answer.lower()
    return all(any(p.lower() in text for p in group) for group in case["any_of"])


def p90(values):
    return statistics.quantiles(values, n=10, method="inclusive")[8] if len(values) > 1 else values[0]


def evaluate(name, model_id, client):
    rows = []
    for case in GOLDEN:
        r = client.converse(
            modelId=model_id,
            system=[{"text": SYSTEM}],
            messages=[{"role": "user", "content": [{"text": case["q"]}]}],
            inferenceConfig={"maxTokens": 120, "temperature": 0},
        )
        answer = r["output"]["message"]["content"][0]["text"]
        rows.append({
            "q": case["q"], "answer": answer, "correct": is_correct(answer, case),
            "latency_ms": r["metrics"]["latencyMs"],
            "in_tokens": r["usage"]["inputTokens"], "out_tokens": r["usage"]["outputTokens"],
        })
    return summarise(name, rows)


def summarise(name, rows):
    n = len(rows)
    s = {
        "model": name,
        "accuracy": sum(r["correct"] for r in rows) / n,
        "p90_latency_ms": p90([r["latency_ms"] for r in rows]),
        "avg_in_tokens": sum(r["in_tokens"] for r in rows) / n,
        "avg_out_tokens": sum(r["out_tokens"] for r in rows) / n,
        "misses": [(r["q"], r["answer"]) for r in rows if not r["correct"]],
    }
    price = PRICES.get(name, {})
    if price.get("input") is not None and price.get("output") is not None:
        per_request = (s["avg_in_tokens"] * price["input"] + s["avg_out_tokens"] * price["output"]) / 1000
        s["cost_per_1k_requests"] = per_request * 1000
    return s


def decide(s):
    checks = {
        "accuracy": s["accuracy"] >= EXIT_CRITERIA["min_accuracy"],
        "latency": s["p90_latency_ms"] <= EXIT_CRITERIA["max_p90_latency_ms"],
    }
    if "cost_per_1k_requests" in s:
        checks["cost"] = s["cost_per_1k_requests"] <= EXIT_CRITERIA["max_cost_per_1k_requests"]
    return ("GO" if all(checks.values()) else "NO-GO"), checks


def report(results):
    print(f"\n{'model':<14}{'accuracy':>10}{'p90 ms':>9}{'in tok':>8}{'out tok':>9}{'$/1k req':>10}  decision")
    for s in results:
        verdict, checks = decide(s)
        cost = f"{s['cost_per_1k_requests']:.3f}" if "cost_per_1k_requests" in s else "n/a"
        failed = [k for k, ok in checks.items() if not ok]
        print(f"{s['model']:<14}{s['accuracy']:>10.0%}{s['p90_latency_ms']:>9.0f}"
              f"{s['avg_in_tokens']:>8.0f}{s['avg_out_tokens']:>9.0f}{cost:>10}  "
              f"{verdict}{' (failed: ' + ', '.join(failed) + ')' if failed else ''}")
        for q, a in s["misses"]:
            print(f"    miss: {q}\n          -> {a}")


if __name__ == "__main__":
    bedrock = boto3.client("bedrock-runtime", region_name="us-west-2")
    report([evaluate(name, mid, bedrock) for name, mid in CANDIDATES.items()])
