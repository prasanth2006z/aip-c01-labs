# AIP-C01 Hands-on Labs

Companion repo for the **AIP-C01 Hands-on Labs** series on Medium: a skill-by-skill path to the **AWS Certified Generative AI Developer – Professional (AIP-C01)** exam, with hands-on labs and exam notes.

> Independent study resource. Not affiliated with or endorsed by Amazon Web Services.

**Start with the Medium post "AIP-C01 Hands-on Labs: Start Here".** It explains how the series works and where to begin.

## How the series and this repo are organised

The series follows the official exam guide exactly: each **domain** has **tasks**, and each task has **skills**.

- **One Medium post per skill**, titled with its number (for example "AIP-C01 Skill 1.1.1: From Requirements to Architecture"), plus **one exam-notes post at the end of each task**.
- **Notes posts** cover design skills; everything is in the post.
- **Lab posts** have a folder here with the sample data and scripts.

```
domain-1/
  task-1.1/                README: the task's posts, lab order, clean-up
    skill-1.1.2-poc/       one folder per lab skill
    skill-1.1.3-wa-lens/
  task-1.2/
    ...
SERVICES.md                every AWS service used in the series
```

## Domain 1: Foundation Model Integration, Data Management and Compliance (31%)

Six tasks, 28 skills and 34 posts. Work through the tasks in order.

| Task | Title in the exam guide | Posts | Lab folders |
| --- | --- | --- | --- |
| [1.1](domain-1/task-1.1) | Analyze requirements and design GenAI solutions | 1.1.1 notes · 1.1.2 lab · 1.1.3 lab · exam notes | [`skill-1.1.2-poc`](domain-1/task-1.1/skill-1.1.2-poc), [`skill-1.1.3-wa-lens`](domain-1/task-1.1/skill-1.1.3-wa-lens) |
| [1.2](domain-1/task-1.2) | Select and configure FMs | 1.2.1 notes · 1.2.2 lab · 1.2.3 lab · 1.2.4 notes · exam notes | [`skill-1.2.2-model-switching`](domain-1/task-1.2/skill-1.2.2-model-switching), [`skill-1.2.3-resilience`](domain-1/task-1.2/skill-1.2.3-resilience) |
| [1.3](domain-1/task-1.3) | Implement data validation and processing pipelines for FM consumption | 1.3.1 notes · 1.3.2 lab · 1.3.3 lab · 1.3.4 lab · exam notes | [`skill-1.3.2-multimodal`](domain-1/task-1.3/skill-1.3.2-multimodal), [`skill-1.3.3-format-input`](domain-1/task-1.3/skill-1.3.3-format-input), [`skill-1.3.4-enhance-input`](domain-1/task-1.3/skill-1.3.4-enhance-input) |
| [1.4](domain-1/task-1.4) | Design and implement vector store solutions | 1.4.1 notes · 1.4.2 lab · 1.4.3 notes · 1.4.4 lab · 1.4.5 lab · exam notes | [`skill-1.4.2-metadata`](domain-1/task-1.4/skill-1.4.2-metadata), [`skill-1.4.4-connectors`](domain-1/task-1.4/skill-1.4.4-connectors), [`skill-1.4.5-freshness`](domain-1/task-1.4/skill-1.4.5-freshness) |
| 1.5 | Design retrieval mechanisms for FM augmentation | coming soon | |
| 1.6 | Implement prompt engineering strategies and governance for FM interactions | coming soon | |

Domains 2–5 will follow the same layout (`domain-2/task-2.1/…`).

## Services reference

[`SERVICES.md`](SERVICES.md) lists every AWS service used in the series: purpose, when to use it, when not to, and the exam wording that points to it. It grows as the series does.

## Before your first lab

- **Use us-west-2 (Oregon).** Every Domain 1 feature used in the labs is available there.
- **Set a budget alert** in the AWS Billing console (for example US$10 a month). Most labs cost cents; a forgotten resource doesn't.
- **Check model access** in us-west-2 for Amazon Nova 2 Lite and Nova Micro through the US inference profiles. Later labs say what else they need.
- **Have a shell ready:** AWS CloudShell works for every lab, or AWS CLI v2 and Python 3.10+ with `boto3`.
- **Clean up after every lab** unless the post says the next lab reuses the resources. Each task README lists the clean-up steps.

## License

Code samples are provided under the [MIT License](LICENSE). Article text and images remain the author's.
