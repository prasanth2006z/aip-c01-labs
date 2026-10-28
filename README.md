# AIP-C01 Hands-on Labs

Lab files for a hands-on study series for the **AWS Certified Generative AI Developer – Professional (AIP-C01)** exam. Each lab has a matching article on Medium that explains the concepts, walks through the steps and covers how the exam tests the topic.

> Independent study resource. Not affiliated with or endorsed by Amazon Web Services.

## How to use this repo

1. Read the Medium article for the lab.
2. Open the matching folder here for the sample data, scripts and commands.
3. Run the lab in **us-west-2** unless the lab says otherwise.
4. Follow the clean-up steps at the end of each lab to avoid ongoing charges.

## Services reference

[`SERVICES.md`](SERVICES.md) lists every AWS service used in the series: purpose, when to use it, when not to, and the exam wording that points to it.

## Labs

The series follows the official exam guide: each **domain** has **tasks**, and each task has **skills**. There is one Medium post per skill, plus exam notes at the end of each task. Skills that can be practised hands-on have a lab folder here.

### Domain 1: Foundation Model Integration, Data Management and Compliance (31%)

| Task | Skill | Lab | Folder |
| --- | --- | --- | --- |
| 1.1 Analyze requirements and design GenAI solutions | 1.1.2 Prove it works: a GenAI proof of concept | ~35 min | [`domain-1/task-1.1/skill-1.1.2-poc`](domain-1/task-1.1/skill-1.1.2-poc) |
| | 1.1.3 Review it with the Generative AI Lens | ~30 min | [`domain-1/task-1.1/skill-1.1.3-wa-lens`](domain-1/task-1.1/skill-1.1.3-wa-lens) |
| 1.2 Select and configure FMs | 1.2.2 Switch models without code changes | ~40 min | [`domain-1/task-1.2/skill-1.2.2-model-switching`](domain-1/task-1.2/skill-1.2.2-model-switching) |
| | 1.2.3 Resilient model access | ~40 min | [`domain-1/task-1.2/skill-1.2.3-resilience`](domain-1/task-1.2/skill-1.2.3-resilience) |
| 1.3 to 1.6 | | _coming soon_ | |

Skills without a lab (1.1.1, 1.2.1, 1.2.4) are covered as notes posts on Medium. Each task folder has a README listing all of its posts.

Domains 2–5 will follow the same layout (`domain-2/task-2.1/…`).

## Prerequisites for all labs

- An AWS account with permission to use Amazon Bedrock and the services named in each lab
- AWS CLI v2 (or AWS CloudShell)
- Python 3.10+ with `boto3` for the Python labs

## Cost

Most labs cost under US$1 if you clean up the same day. Each lab states its estimate.

## License

Code samples are provided under the MIT License. Article text and images remain the author's.
