# Domain 1 · Task 1.2: Select and configure FMs

Companion files for the five Medium posts on Task 1.2 of the AIP-C01 exam guide. Region: **us-west-2**.

| Post | Medium title | Type | Lab folder |
| --- | --- | --- | --- |
| 1 | AIP-C01 Skill 1.2.1: How to Choose the Right Foundation Model | Notes | — |
| 2 | AIP-C01 Skill 1.2.2: Switch Models Without Code Changes | Lab, ~40 min | [`skill-1.2.2-model-switching`](skill-1.2.2-model-switching) |
| 3 | AIP-C01 Skill 1.2.3: Resilient Model Access | Lab, ~40 min | [`skill-1.2.3-resilience`](skill-1.2.3-resilience) |
| 4 | AIP-C01 Skill 1.2.4: Customising Models and Managing Their Lifecycle | Notes | — |
| 5 | AIP-C01 Task 1.2 Exam Notes: Select and Configure FMs | Exam notes | — |

Notes and exam-notes posts have no files here; everything you need is in the post.

## Clean up

- **Skill 1.2.2:** delete the `model-router` Lambda function and its log group; stop any active deployment, then delete the `model-settings` profile, the `prod` environment and the `genai-lab` AppConfig application; delete the IAM role.
- **Skill 1.2.3:** nothing to delete unless you deployed the state machine; if you did, delete it and its role.
