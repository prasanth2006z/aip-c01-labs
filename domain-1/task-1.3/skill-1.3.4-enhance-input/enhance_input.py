"""Lab: Skill 1.3.4 - enhance input quality before it reaches the model.

  python enhance_input.py normalize   # step 1: Lambda-style normalisation in plain Python
  python enhance_input.py comprehend  # step 2: language, entities and PII with Amazon Comprehend
  python enhance_input.py reformat    # step 3: Bedrock rewrites each ticket into a clean summary
  python enhance_input.py compare     # step 4: raw vs enhanced input, same question, three runs each
"""
import json, re, sys, unicodedata
from pathlib import Path
import boto3

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-2-lite-v1:0"
TICKETS = json.loads((Path(__file__).parent / "tickets.json").read_text())
comprehend = boto3.client("comprehend", region_name=REGION)
bedrock = boto3.client("bedrock-runtime", region_name=REGION)

MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}


def normalize(text):
    """What a normalisation Lambda typically does: cheap, deterministic clean-up."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"[\U0001F300-\U0001FAFF]", "", text)              # emoji
    text = re.sub(r"([!?.])\1+", r"\1", text)                        # !!! -> !
    text = re.sub(r"\s+", " ", text).strip()
    # Order IDs: "a-4471", "#B 2096" -> "A-4471", "B-2096"
    text = re.sub(r"#?\b([a-cA-C])[\s-]?(\d{4})\b", lambda m: f"{m.group(1).upper()}-{m.group(2)}", text)
    # Dates: "3rd oct 2026" -> 2026-10-03 ; "10/05/2026" (MM/DD) -> 2026-10-05
    text = re.sub(r"\b(\d{1,2})(?:st|nd|rd|th)? (jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)\w* (\d{4})\b",
                  lambda m: f"{m.group(3)}-{MONTHS[m.group(2).lower()]:02d}-{int(m.group(1)):02d}", text, flags=re.I)
    text = re.sub(r"\b(\d{2})/(\d{2})/(\d{4})\b", r"\3-\1-\2", text)
    # Shouting: if most letters are capitals, use sentence case
    letters = [c for c in text if c.isalpha()]
    if letters and sum(c.isupper() for c in letters) / len(letters) > 0.5:
        text = text.lower()
    return text[0].upper() + text[1:] if text else text


def mask_pii(text):
    pii = comprehend.detect_pii_entities(Text=text, LanguageCode="en")["Entities"]
    for e in sorted(pii, key=lambda e: e["BeginOffset"], reverse=True):
        text = text[:e["BeginOffset"]] + f"[{e['Type']}]" + text[e["EndOffset"]:]
    return text, [e["Type"] for e in pii]


def enhance(text):
    text = normalize(text)
    text, pii_types = mask_pii(text)
    return text, pii_types


def ask(prompt, system=None, max_tokens=200):
    kwargs = {"modelId": MODEL_ID, "messages": [{"role": "user", "content": [{"text": prompt}]}],
              "inferenceConfig": {"maxTokens": max_tokens, "temperature": 0.7}}
    if system:
        kwargs["system"] = [{"text": system}]
    return bedrock.converse(**kwargs)["output"]["message"]["content"][0]["text"].strip()


def step_normalize():
    for t in TICKETS:
        print(f"\n{t['id']} raw:        {t['text']}\n{t['id']} normalized: {normalize(t['text'])}")


def step_comprehend():
    for t in TICKETS:
        text = normalize(t["text"])
        lang = comprehend.detect_dominant_language(Text=text)["Languages"][0]
        ents = comprehend.detect_entities(Text=text, LanguageCode="en")["Entities"]
        masked, pii_types = mask_pii(text)
        print(f"\n{t['id']} language: {lang['LanguageCode']} ({lang['Score']:.2f})")
        print(f"   entities: {[(e['Type'], e['Text']) for e in ents]}")
        print(f"   PII found: {pii_types}")
        print(f"   masked:   {masked}")


SUMMARY_PROMPT = ("Rewrite this customer message as a neutral support summary with these lines: "
                  "Item:, Order:, Purchase date:, Problem:, Customer wants:. Use 'unknown' if not stated.\n\n")


def step_reformat():
    for t in TICKETS:
        text, _ = enhance(t["text"])
        print(f"\n{t['id']}:\n{ask(SUMMARY_PROMPT + text)}")


POLICY = ("Policy: standard items 30-day returns; hedge trimmers 14 days; registered power tools 90 days; "
          "today is 2026-10-12.")
QUESTION = "\n\nIs this return within policy? Answer 'yes' or 'no' and the number of days since purchase."


def step_compare():
    t = TICKETS[1]                                    # the leaf blower ticket with the ambiguous date
    enhanced, _ = enhance(t["text"])
    for label, text in [("raw", t["text"]), ("enhanced", enhanced)]:
        print(f"\n{label} input -> three answers:")
        for _ in range(3):
            print("  ", ask(text + QUESTION, system=POLICY, max_tokens=60).replace("\n", " "))


if __name__ == "__main__":
    steps = {"normalize": step_normalize, "comprehend": step_comprehend, "reformat": step_reformat, "compare": step_compare}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python enhance_input.py normalize|comprehend|reformat|compare")
    steps[step]()
