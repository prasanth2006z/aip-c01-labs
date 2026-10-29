# Skill 1.1.3 lab: Review a GenAI design with the Generative AI Lens

Review the returns-assistant proof of concept from the [Skill 1.1.2 lab](../skill-1.1.2-poc) with the AWS Well-Architected Generative AI Lens, read the risks it finds, and save a milestone to track the path to production.

- **Time:** about 30 minutes
- **Cost:** the AWS Well-Architected Tool has no additional charge
- **Region:** us-west-2. Import the lens and define the workload in the **same** Region: custom lenses are Regional.

## Why this lab

Same system, different question:

| | Skill 1.1.2: proof of concept | Skill 1.1.3: lens review |
| --- | --- | --- |
| Question | Does it work? | Is it built well enough to go further? |
| Checks | Accuracy, latency, cost against exit criteria | Design practices: quality, security, reliability, cost |
| How | Runs the system against a golden set | Answers lens questions with evidence; runs nothing |
| Result | GO / NO-GO | Risks, an improvement plan, a saved milestone |

## How a lens works

A lens is a JSON file of questions. Each question has best-practice **choices**, **risk rules** that turn your ticks into high, medium or no risk, and **improvement guidance** for each practice you haven't ticked. You apply it to a **workload** (a record describing your system), answer, and the tool builds an **improvement plan**. A **milestone** saves a snapshot to compare with later reviews.

**The review never touches your workload.** The WA Tool doesn't scan your account or call your models. A tick is a statement that a practice exists; the evidence is what you built.

## Steps

1. **Download the lens**

   ```bash
   curl -L -o generative-ai-lens.json \
     https://raw.githubusercontent.com/aws-samples/sample-well-architected-custom-lens/main/generative-ai-lens/generative-ai-lens.json
   ```

2. **Import and publish it.** Well-Architected Tool console → **Custom lenses** → **Create custom lens** → **Import lens** → upload the JSON. **Preview** is read-only: nothing you tick there is saved. Then **Publish** a version (for example `1.0`).

3. **Define the workload.** **Workloads** → **Define workload**: name `returns-assistant-poc`, environment pre-production, Region us-west-2. On the lens step, select **AWS Well-Architected Framework** and **Generative AI Lens**.

4. **Answer four questions.** The console numbers questions by pillar (GENOPS01 appears as **OPS 1**). Answer only these and leave the rest unanswered:

   | Console | Lens ID | Tick | Evidence |
   | --- | --- | --- | --- |
   | OPS 1 | GENOPS01 | Periodically evaluate functional performance | The golden-set harness (one manual run is a generous yes at PoC stage) |
   | SEC 2 | GENSEC02 | None of these | No guardrails yet |
   | REL 5 | GENREL05 | None of these | Single Region |
   | COST 1 | GENCOST01 | Right-size model selection to optimize inference costs | Two models compared on quality, latency and cost |

5. **Read the result and save a milestone.** Expected improvement plan, decided by the lens's risk rules:

   | Console | Result | Why |
   | --- | --- | --- |
   | OPS 1 | **High risk** | No risk needs both evaluation *and* user feedback |
   | SEC 2 | **High risk** | No guardrails |
   | REL 5 | **Medium risk** | Multi-Region practices missing |
   | COST 1 | No risk | Best practice met |

   Then **Save milestone** as `poc-review-1`.

## From PoC to production

| Step | Who | What happens | Milestone |
| --- | --- | --- | --- |
| 1. Set up once | Platform or architecture team | Import the Generative AI Lens (plus any company lens), publish and share it | |
| 2. Define | Workload team | Define the workload and apply the lenses | |
| 3. Review | Team with an architect or security reviewer | Answer with evidence; the tool calculates the risks | `poc-review-1` |
| 4. Fix | Workload team | Build the missing pieces: user feedback and scheduled evaluation (OPS 1), Bedrock Guardrails (SEC 2), cross-Region inference and a fallback model (REL 5) | |
| 5. Review again | Same reviewers | Re-answer, compare milestones, confirm risks are closed | `prod-review-1` |
| 6. Gate | Approver | Go live with no high risks open; review again after major changes | each release |

The lens doesn't fix or enforce anything. The fixes are real services; the lens makes sure every team checks the same things and records what was fixed.

## Clean up

Delete the workload, then the custom lens (remove it from workloads first). Neither has a cost, so you can keep them to repeat the review after later labs.

## Reference

- [Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html)
- [Design principles](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/design-principles.html)
- [Custom lenses in the AWS WA Tool](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-custom.html)
- [Milestones](https://docs.aws.amazon.com/wellarchitected/latest/userguide/milestones.html)
