# Skill 1.1.3 lab: Review a GenAI design with the Generative AI Lens

Import the AWS Well-Architected Generative AI Lens into the AWS Well-Architected Tool, apply it to a workload, answer a few questions and generate a report.

- **Time:** about 30 minutes
- **Cost:** the AWS Well-Architected Tool has no additional charge
- **Region:** us-west-2 (the Well-Architected Tool is Regional; custom lenses live in the Region you import them into)

## 1. Download the lens

The lens is published by AWS as a custom lens JSON file in the
[aws-samples/sample-well-architected-custom-lens](https://github.com/aws-samples/sample-well-architected-custom-lens)
repository, folder `generative-ai-lens/generative-ai-lens.json`.

```bash
curl -L -o generative-ai-lens.json \
  https://raw.githubusercontent.com/aws-samples/sample-well-architected-custom-lens/main/generative-ai-lens/generative-ai-lens.json
```

## 2. Import and publish it

Well-Architected Tool console → **Custom lenses** → **Create custom lens** → **Import lens** → upload the JSON.
Use **Preview** to browse it, then **Publish** a version (for example `1.0`) so it can be applied to workloads.

## 3. Define a workload and apply the lens

**Workloads** → **Define workload**. Name it `returns-assistant-poc`, Region us-west-2, environment pre-production.
On the lens step, select **AWS Well-Architected Framework** and your published **Generative AI Lens**.

## 4. Answer four questions honestly

For the returns assistant built in the Skill 1.1.2 lab, answer:

| Question | Choice to tick for the PoC | Why |
| --- | --- | --- |
| GENOPS01: How do you achieve and verify consistent model output quality? | Periodically evaluate functional performance | The golden-set harness does this (user feedback isn't collected yet) |
| GENREL05: How do you distribute inference workloads over multiple regions of availability? | None of these | Single Region, no cross-Region strategy yet |
| GENSEC02: How do you stop generative AI applications from generating harmful, biased, or factually incorrect responses? | None of these | Grounded in the policy text only; no guardrails yet |
| GENCOST01: How do you select the appropriate model to optimize costs? | Right-size model selection to optimize inference costs | Two models were compared on quality, latency and cost |

## 5. Generate the report and save a milestone

**Generate report** for the Generative AI Lens, then **Save milestone** (for example `poc-review-1`).
The improvement plan lists the risks you marked, with links to the lens guidance for each.

## Clean up

Delete the workload, then delete the custom lens (published versions must be removed from workloads first). Neither has a cost.

## Reference

- [Generative AI Lens](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/generative-ai-lens.html)
- [Design principles](https://docs.aws.amazon.com/wellarchitected/latest/generative-ai-lens/design-principles.html)
- [Custom lenses in the AWS WA Tool](https://docs.aws.amazon.com/wellarchitected/latest/userguide/lenses-custom.html)
