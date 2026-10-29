"""Lab: Skill 1.6.6 - a prompt flow with classification, conditional branching and per-branch prompts.

  python flows_lab.py role      # step 1: an IAM role the flow runs as
  python flows_lab.py create    # step 2: create, prepare, version and alias the flow
  export FLOW_ID=... FLOW_ALIAS_ID=...
  python flows_lab.py invoke    # step 3: run three messages through it, with traces
"""
import json, os, sys, time
import boto3

REGION = "us-west-2"
MODEL_ID = "us.amazon.nova-2-lite-v1:0"
ROLE_NAME = "aip-lab-flow-role"
agent = boto3.client("bedrock-agent", region_name=REGION)
runtime = boto3.client("bedrock-agent-runtime", region_name=REGION)
iam = boto3.client("iam")
sts = boto3.client("sts")

RETURNS_POLICY = ("General items: 30 days. Garden equipment (hedge trimmers, mowers, leaf blowers): 14 days, "
                  "15% restocking fee if opened. Registered cordless power tools: 90 days. Clearance: final sale.")
WARRANTY_POLICY = ("Power tools: 2-year limited warranty against manufacturing defects. Batteries: 1 year. "
                   "Not covered: blades, wear parts, misuse. To claim: order number and a photo of the fault.")


def env(name):
    return os.environ.get(name) or sys.exit(f"Set {name} first (printed by an earlier step).")


def step_role():
    account = sts.get_caller_identity()["Account"]
    trust = {"Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Principal": {"Service": "bedrock.amazonaws.com"},
             "Action": "sts:AssumeRole", "Condition": {"StringEquals": {"aws:SourceAccount": account}}}]}
    role = iam.create_role(RoleName=ROLE_NAME, AssumeRolePolicyDocument=json.dumps(trust))["Role"]
    iam.put_role_policy(RoleName=ROLE_NAME, PolicyName="invoke-models", PolicyDocument=json.dumps({
        "Version": "2012-10-17", "Statement": [{"Effect": "Allow", "Action": ["bedrock:InvokeModel"],
        "Resource": [f"arn:aws:bedrock:*:{account}:inference-profile/{MODEL_ID}", "arn:aws:bedrock:*::foundation-model/amazon.nova-2-lite-v1:0"]}]}))
    print(f"Created {role['Arn']}  (IAM changes can take ~10 seconds to apply)")


def prompt_node(name, template, variables, max_tokens=250):
    return {"name": name, "type": "Prompt",
            "configuration": {"prompt": {"sourceConfiguration": {"inline": {
                "modelId": MODEL_ID, "templateType": "TEXT",
                "inferenceConfiguration": {"text": {"temperature": 0, "maxTokens": max_tokens}},
                "templateConfiguration": {"text": {"text": template, "inputVariables": [{"name": v} for v in variables]}}}}}},
            "inputs": [{"name": v, "type": "String", "expression": "$.data"} for v in variables],
            "outputs": [{"name": "modelCompletion", "type": "String"}]}


def output_node(name):
    return {"name": name, "type": "Output", "configuration": {"output": {}},
            "inputs": [{"name": "document", "type": "String", "expression": "$.data"}]}


def data(src, out, dst, inp):
    return {"name": f"{src}_{dst}_{inp}", "source": src, "target": dst, "type": "Data",
            "configuration": {"data": {"sourceOutput": out, "targetInput": inp}}}


def cond(dst, condition):
    return {"name": f"Route_{dst}", "source": "Route", "target": dst, "type": "Conditional",
            "configuration": {"conditional": {"condition": condition}}}


ANSWER_RULES = ("Answer only from the policy. Keep it under 60 words. If the policy doesn't cover it, say so.\n"
                "Format:\nAnswer: <answer>\nNext step: <what the customer should do>")

DEFINITION = {
    "nodes": [
        {"name": "FlowInput", "type": "Input", "configuration": {"input": {}},
         "outputs": [{"name": "document", "type": "String"}]},
        prompt_node("Classify", "Classify this customer message as exactly one lowercase word: return, warranty or other.\n"
                                "Reply with the word only.\n\nMessage: {{message}}", ["message"], max_tokens=5),
        {"name": "Route", "type": "Condition",
         "configuration": {"condition": {"conditions": [
             {"name": "IsReturn", "expression": 'intent == "return"'},
             {"name": "IsWarranty", "expression": 'intent == "warranty"'},
             {"name": "default"}]}},
         "inputs": [{"name": "intent", "type": "String", "expression": "$.data"}]},
        prompt_node("ReturnsAnswer", f"Returns policy: {RETURNS_POLICY}\n{ANSWER_RULES}\n\nCustomer: {{{{message}}}}", ["message"]),
        prompt_node("WarrantyAnswer", f"Warranty policy: {WARRANTY_POLICY}\n{ANSWER_RULES}\n\nCustomer: {{{{message}}}}", ["message"]),
        prompt_node("Handoff", "Write one friendly sentence telling the customer a human agent will reply within one "
                               "business day, mentioning their topic briefly.\n\nCustomer: {{message}}", ["message"], max_tokens=80),
        output_node("ReturnsOut"), output_node("WarrantyOut"), output_node("HandoffOut"),
    ],
    "connections": [
        data("FlowInput", "document", "Classify", "message"),
        data("Classify", "modelCompletion", "Route", "intent"),
        cond("ReturnsAnswer", "IsReturn"), cond("WarrantyAnswer", "IsWarranty"), cond("Handoff", "default"),
        data("FlowInput", "document", "ReturnsAnswer", "message"),
        data("FlowInput", "document", "WarrantyAnswer", "message"),
        data("FlowInput", "document", "Handoff", "message"),
        data("ReturnsAnswer", "modelCompletion", "ReturnsOut", "document"),
        data("WarrantyAnswer", "modelCompletion", "WarrantyOut", "document"),
        data("Handoff", "modelCompletion", "HandoffOut", "document"),
    ],
}


def step_create():
    account = sts.get_caller_identity()["Account"]
    flow = agent.create_flow(name="returns-router", description="Skill 1.6.6 lab",
                             executionRoleArn=f"arn:aws:iam::{account}:role/{ROLE_NAME}", definition=DEFINITION)
    fid = flow["id"]
    agent.prepare_flow(flowIdentifier=fid)
    while (status := agent.get_flow(flowIdentifier=fid)["status"]) not in ("Prepared", "Failed"):
        time.sleep(2)
    if status == "Failed":
        sys.exit(f"Prepare failed: {agent.get_flow(flowIdentifier=fid).get('validations')}")
    version = agent.create_flow_version(flowIdentifier=fid)["version"]
    alias = agent.create_flow_alias(flowIdentifier=fid, name="live", routingConfiguration=[{"flowVersion": version}])
    print(f"Flow {fid} version {version} alias {alias['id']}\n\nexport FLOW_ID={fid} FLOW_ALIAS_ID={alias['id']}")


def step_invoke():
    messages = sys.argv[2:] or [
        "I opened a hedge trimmer 10 days ago and don't like it. Can I return it?",
        "My drill stopped working after 8 months. Is that covered?",
        "Do you have any jobs going at your Leeds store?",
    ]
    for m in messages:
        res = runtime.invoke_flow(flowIdentifier=env("FLOW_ID"), flowAliasIdentifier=env("FLOW_ALIAS_ID"), enableTrace=True,
                                  inputs=[{"content": {"document": m}, "nodeName": "FlowInput", "nodeOutputName": "document"}])
        print(f"\nCustomer: {m}")
        for event in res["responseStream"]:
            if "flowTraceEvent" in event:
                trace = event["flowTraceEvent"]["trace"]
                if "conditionNodeResultTrace" in trace:
                    print(f"   branch: {[c['conditionName'] for c in trace['conditionNodeResultTrace']['satisfiedConditions']]}")
            elif "flowOutputEvent" in event:
                out = event["flowOutputEvent"]
                print(f"   [{out['nodeName']}] {out['content']['document'].strip()}")


if __name__ == "__main__":
    steps = {"role": step_role, "create": step_create, "invoke": step_invoke}
    step = sys.argv[1] if len(sys.argv) > 1 else ""
    if step not in steps:
        sys.exit("Usage: python flows_lab.py role|create|invoke [message ...]")
    steps[step]()
