# Domain 1 · Task 1.6: Implement prompt engineering strategies and governance for FM interactions

Companion files for the seven Medium posts on Task 1.6 of the AIP-C01 exam guide. Region: **us-west-2**.

| Post | Medium title | Type | Lab folder |
| --- | --- | --- | --- |
| 1 | AIP-C01 Skill 1.6.1: Control Model Behaviour with Prompt Management and Guardrails | Lab, ~30 min | [`skill-1.6.1-instructions`](skill-1.6.1-instructions) |
| 2 | AIP-C01 Skill 1.6.2: Keep Context in Conversations | Notes | — |
| 3 | AIP-C01 Skill 1.6.3: Govern Prompts with Versions, Approval and Audit | Lab, ~30 min | [`skill-1.6.3-governance`](skill-1.6.3-governance) |
| 4 | AIP-C01 Skill 1.6.4: Test Prompts Like Code | Lab, ~25 min | [`skill-1.6.4-prompt-qa`](skill-1.6.4-prompt-qa) |
| 5 | AIP-C01 Skill 1.6.5: Improve Prompts Step by Step | Lab, ~25 min | [`skill-1.6.5-refinement`](skill-1.6.5-refinement) |
| 6 | AIP-C01 Skill 1.6.6: Chain Prompts with Bedrock Flows | Lab, ~30 min | [`skill-1.6.6-flows`](skill-1.6.6-flows) |
| 7 | AIP-C01 Task 1.6 Exam Notes: Prompt Engineering and Governance | Exam notes | — |

The Skill 1.6.3 lab reuses the prompt created in the Skill 1.6.1 lab.

## Clean up

- **Skill 1.6.1:** delete the `returns-assistant` prompt and the `returns-assistant-guardrail` guardrail.
- **Skill 1.6.3:** delete `prompt-templates/` (all versions) from your bucket; turn off model invocation logging and delete its log group if you enabled it.
- **Skill 1.6.4:** delete the `prompt-qa-v2-pass-rate` alarm, and the optional Lambda function and state machine.
- **Skill 1.6.6:** delete the `live` alias, the `returns-router` flow and the `aip-lab-flow-role` role.
