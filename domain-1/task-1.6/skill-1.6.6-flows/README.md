# Skill 1.6.6 lab: Chain prompts with Amazon Bedrock Flows

Build a prompt flow in code: a classification prompt, a condition node that branches on the model's answer, a separate prompt per branch (returns, warranty, hand-off to a human) and an output per branch. Then run three messages through it with tracing on, and see which branch each one took.

- **Time:** about 30 minutes
- **Cost:** under US$0.02
- **Region:** us-west-2
- **Needs:** Python 3.10+ with `boto3`; permission to create an IAM role and Bedrock flows; Amazon Nova 2 Lite (US inference profile)

## Flow

```
FlowInput ─► Classify (prompt: return | warranty | other) ─► Route (condition)
                                                              ├─ IsReturn   ─► ReturnsAnswer  ─► ReturnsOut
                                                              ├─ IsWarranty ─► WarrantyAnswer ─► WarrantyOut
                                                              └─ default    ─► Handoff        ─► HandoffOut
FlowInput also feeds the original message into each branch prompt.
```

## Run it

```bash
pip install boto3
python flows_lab.py role
python flows_lab.py create          # prints export FLOW_ID=... FLOW_ALIAS_ID=...
export FLOW_ID=... FLOW_ALIAS_ID=...
python flows_lab.py invoke
python flows_lab.py invoke "The blade on my HT-450 snapped after a week."
```

Open the flow in the Bedrock console (**Flows** → `returns-router`) to see the same graph in the visual builder, and use its test pane with the trace view.

## Clean up

Delete the `live` alias, then the `returns-router` flow (Bedrock console → Flows), then the `aip-lab-flow-role` IAM role.
