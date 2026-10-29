"""Lab: Skill 1.6.5 - refine a prompt step by step and measure each step.

  python refine_lab.py show v3     # print one prompt version
  python refine_lab.py run v0      # run one version on the six tickets
  python refine_lab.py compare     # all versions side by side: eligibility and day-count accuracy
"""
import json, re, sys
from datetime import date
from pathlib import Path
import boto3

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-2-lite-v1:0"
TODAY = "2026-10-12"
TICKETS = json.loads((Path(__file__).parent / "tickets.json").read_text())
POLICY = ("General items: 30 days. Garden equipment (hedge trimmers, mowers, leaf blowers): 14 days. "
          "Cordless power tools registered online: 90 days; unregistered power tools follow the general rule. "
          "Clearance items: final sale, no returns. Days are counted from the purchase date.")
runtime = boto3.client("bedrock-runtime", region_name=REGION)

# v0: the first draft anyone writes
V0 = "Is this return eligible?\n\n{ticket}"

# v1: structured input - policy, date and ticket clearly separated and labelled
V1 = """<policy>{policy}</policy>
<today>{today}</today>
<ticket>{ticket}</ticket>

Using only the policy, decide whether the return in the ticket is eligible today."""

# v2: + output format specification
V2 = V1 + """

Reply with only this JSON:
{{"category": "general|garden|power_registered|power_unregistered|clearance",
  "purchase_date": "YYYY-MM-DD", "days_since_purchase": <integer>, "limit_days": <integer or 0>,
  "eligible": <true|false>, "reason": "<one sentence>"}}"""

# v3: + chain-of-thought instructions
V3 = V1 + """

Work it out step by step inside <thinking> tags:
1. Identify the item and its policy category.
2. Find the purchase date and write it as YYYY-MM-DD (assume 2026; numeric dates are DD/MM).
3. Count the days from the purchase date to today.
4. Compare with the category's limit.
Then give only this JSON inside <answer> tags:
{{"category": "...", "purchase_date": "YYYY-MM-DD", "days_since_purchase": <integer>, "limit_days": <integer or 0>,
  "eligible": <true|false>, "reason": "<one sentence>"}}"""

VERSIONS = {"v0": V0, "v1": V1, "v2": V2, "v3": V3, "v4": V3}   # v4 = v3 + a feedback loop in code


def call(messages):
    res = runtime.converse(modelId=MODEL_ID, messages=messages, inferenceConfig={"maxTokens": 700, "temperature": 0})
    return res["output"]["message"]["content"][0]["text"]


def parse(text):
    """Pull eligibility and day count out of either JSON or free text."""
    m = re.search(r"<answer>(.*?)</answer>", text, re.S) or re.search(r"(\{.*\})", text, re.S)
    if m:
        try:
            j = json.loads(m.group(1).strip().strip("`").removeprefix("json"))
            return j, j.get("eligible"), j.get("days_since_purchase")
        except json.JSONDecodeError:
            pass
    low = text.lower()
    elig = False if re.search(r"not eligible|isn.t eligible|ineligible|cannot be returned|can.t be returned|\bno\b", low) \
        else True if re.search(r"eligible|\byes\b|can (be )?return", low) else None
    d = re.search(r"(\d+)\s*days?\s*(since|ago|after|have passed|from)", low)
    return None, elig, int(d.group(1)) if d else None


def feedback(j):
    """Deterministic checks a feedback loop sends back to the model."""
    problems = []
    try:
        days = (date.fromisoformat(TODAY) - date.fromisoformat(j["purchase_date"])).days
        if days != j.get("days_since_purchase"):
            problems.append(f"From {j['purchase_date']} to {TODAY} is {days} days, not {j.get('days_since_purchase')}.")
        if j.get("category") != "clearance" and j.get("limit_days") and (days <= j["limit_days"]) != j.get("eligible"):
            problems.append(f"{days} days against a {j['limit_days']}-day limit means eligible should be {days <= j['limit_days']}.")
    except (KeyError, TypeError, ValueError) as e:
        problems.append(f"The JSON is missing or has an invalid field ({e}).")
    return problems


def run_ticket(version, t):
    prompt = VERSIONS[version].format(policy=POLICY, today=TODAY, ticket=t["ticket"])
    messages = [{"role": "user", "content": [{"text": prompt}]}]
    out = call(messages)
    j, elig, days = parse(out)
    rounds = 0
    while version == "v4" and rounds < 2:
        problems = feedback(j) if j else ["Reply with the JSON inside <answer> tags."]
        if not problems:
            break
        rounds += 1
        messages += [{"role": "assistant", "content": [{"text": out}]},
                     {"role": "user", "content": [{"text": "Please fix these problems and answer again:\n- " + "\n- ".join(problems)}]}]
        out = call(messages)
        j, elig, days = parse(out)
    return {"id": t["id"], "eligible_ok": elig == t["eligible"], "days_ok": days == t["days"],
            "eligible": elig, "days": days, "revisions": rounds}


def run(version, show=True):
    rows = [run_ticket(version, t) for t in TICKETS]
    if show:
        for r, t in zip(rows, TICKETS):
            print(f"{r['id']}  eligible={r['eligible']!s:5} (want {t['eligible']!s:5})  days={r['days']!s:4} (want {t['days']})"
                  + (f"  revisions={r['revisions']}" if r["revisions"] else ""))
    return sum(r["eligible_ok"] for r in rows), sum(r["days_ok"] for r in rows)


def compare():
    notes = {"v0": "first draft", "v1": "+ structured input", "v2": "+ output format", "v3": "+ chain of thought", "v4": "+ feedback loop"}
    print(f"{'version':26}{'eligibility':>12}{'day count':>11}")
    for v in VERSIONS:
        e, d = run(v, show=False)
        print(f"{v + '  ' + notes[v]:26}{f'{e}/{len(TICKETS)}':>12}{f'{d}/{len(TICKETS)}':>11}")


if __name__ == "__main__":
    a = sys.argv[1:]
    if len(a) == 2 and a[0] == "show" and a[1] in VERSIONS:
        print(VERSIONS[a[1]].format(policy=POLICY, today=TODAY, ticket=TICKETS[0]["ticket"]))
    elif len(a) == 2 and a[0] == "run" and a[1] in VERSIONS:
        run(a[1])
    elif a == ["compare"]:
        compare()
    else:
        sys.exit("Usage: python refine_lab.py show|run v0..v4 | compare")
