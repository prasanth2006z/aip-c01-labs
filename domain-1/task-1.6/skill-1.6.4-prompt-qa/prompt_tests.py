"""Lab: Skill 1.6.4 - test prompts like code: expected-output checks, edge cases, regression metrics.

  python prompt_tests.py run v1        # step 1: run every test case against prompt v1
  python prompt_tests.py run v2        # step 2: the "friendlier" v2: find the regressions
  python prompt_tests.py compare       # step 3: side by side, and publish pass rates to CloudWatch
  python prompt_tests.py alarm         # step 4: alarm when the pass rate drops below 90%
"""
import json, re, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import boto3

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-2-lite-v1:0"
HERE = Path(__file__).parent
CASES = json.loads((HERE / "test_cases.json").read_text())
_clients = {}


def client(name):
    if name not in _clients:
        _clients[name] = boto3.client(name, region_name=REGION)
    return _clients[name]


def generate(version, question):
    system = (HERE / "prompts" / f"{version}.txt").read_text()
    res = client("bedrock-runtime").converse(
        modelId=MODEL_ID, system=[{"text": system}],
        messages=[{"role": "user", "content": [{"text": question}]}],
        inferenceConfig={"maxTokens": 300, "temperature": 0})
    return res["output"]["message"]["content"][0]["text"].strip()


def verify(output, checks):
    """The kind of function a verification Lambda runs: deterministic checks, a list of failures."""
    low = output.lower()
    fails = []
    if checks.get("format") and not re.search(r"^Answer:.+\n+Policy section:.+\n+Next step:.+", output.strip(), re.S | re.M):
        fails.append("format")
    for s in checks.get("contains_all", []):
        if s.lower() not in low:
            fails.append(f"missing '{s}'")
    if checks.get("contains_any") and not any(s.lower() in low for s in checks["contains_any"]):
        fails.append(f"none of {checks['contains_any']}")
    for s in checks.get("not_contains", []):
        if s.lower() in low:
            fails.append(f"contains '{s}'")
    if "max_words" in checks and len(output.split()) > checks["max_words"]:
        fails.append(f"{len(output.split())} words > {checks['max_words']}")
    return fails


def run_case(version, case):
    out = generate(version, case["question"])
    return {"id": case["id"], "version": version, "passed": not (f := verify(out, case["checks"])), "failures": f, "output": out}


def handler(event, context=None):
    """Lambda entry point for a Step Functions Map state: {"version": "v1", "case": {...}}."""
    return run_case(event["version"], event["case"])


def run(version, show=True):
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(lambda c: run_case(version, c), CASES))
    if show:
        for r in results:
            print(f"{'PASS' if r['passed'] else 'FAIL'}  {r['id']:15} {'; '.join(r['failures'])}")
            if not r["passed"]:
                print("      " + r["output"].replace("\n", "\n      "))
        print(f"\n{version}: {sum(r['passed'] for r in results)}/{len(results)} passed")
    return results


def publish(version, results):
    rate = sum(r["passed"] for r in results) / len(results)
    client("cloudwatch").put_metric_data(Namespace="AIPLab/PromptQA", MetricData=[
        {"MetricName": "PassRate", "Dimensions": [{"Name": "PromptVersion", "Value": version}], "Value": rate, "Unit": "None"}])
    return rate


def compare():
    res = {v: {r["id"]: r for r in run(v, show=False)} for v in ("v1", "v2")}
    print(f"{'case':16}{'v1':>6}{'v2':>6}")
    for c in CASES:
        a, b = res["v1"][c["id"]]["passed"], res["v2"][c["id"]]["passed"]
        flag = "   <- regression" if a and not b else ""
        print(f"{c['id']:16}{'pass' if a else 'FAIL':>6}{'pass' if b else 'FAIL':>6}{flag}")
    for v in ("v1", "v2"):
        print(f"{v} pass rate {publish(v, list(res[v].values())):.0%} (published to CloudWatch AIPLab/PromptQA)")


def alarm():
    client("cloudwatch").put_metric_alarm(
        AlarmName="prompt-qa-v2-pass-rate", Namespace="AIPLab/PromptQA", MetricName="PassRate",
        Dimensions=[{"Name": "PromptVersion", "Value": "v2"}], Statistic="Minimum", Period=300,
        EvaluationPeriods=1, Threshold=0.9, ComparisonOperator="LessThanThreshold", TreatMissingData="notBreaching")
    print("Alarm prompt-qa-v2-pass-rate created: fires when v2's pass rate is below 90%.")


if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "run":
        run(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] in ("compare", "alarm"):
        {"compare": compare, "alarm": alarm}[sys.argv[1]]()
    else:
        sys.exit("Usage: python prompt_tests.py run v1|v2 | compare | alarm")
