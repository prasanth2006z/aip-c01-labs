# Domain 1 · Task 1.4: Design and implement vector store solutions

Companion files for the six Medium posts on Task 1.4 of the AIP-C01 exam guide. Region: **us-west-2**.

| Post | Medium title | Type | Lab folder |
| --- | --- | --- | --- |
| 1 | AIP-C01 Skill 1.4.1: Choose a Vector Store Architecture | Notes | — |
| 2 | AIP-C01 Skill 1.4.2: Add Metadata to Sharpen Retrieval | Lab, ~45 min | [`skill-1.4.2-metadata`](skill-1.4.2-metadata) |
| 3 | AIP-C01 Skill 1.4.3: Vector Search at Scale | Notes | — |
| 4 | AIP-C01 Skill 1.4.4: Connect Wikis and Document Systems to a Knowledge Base | Lab, ~25 min | [`skill-1.4.4-connectors`](skill-1.4.4-connectors) |
| 5 | AIP-C01 Skill 1.4.5: Keep the Vector Store Fresh | Lab, ~30 min | [`skill-1.4.5-freshness`](skill-1.4.5-freshness) |
| 6 | AIP-C01 Task 1.4 Exam Notes: Vector Store Solutions | Exam notes | — |

The three labs share one knowledge base (`aip-lab-kb`, with an Amazon S3 Vectors store). Do them in order: the Skill 1.4.2 lab creates it.

## Clean up (after the Skill 1.4.5 lab)

1. EventBridge Scheduler: delete the `kb-sync` schedule.
2. S3: delete the event notification, then the `kb-docs/` objects.
3. Lambda: delete `kb-sync` and its log group and role.
4. Bedrock: delete the `aip-lab-kb` knowledge base (this deletes its data sources).
5. S3 Vectors: delete the vector index and vector bucket that quick create made (S3 console → **Vector buckets**).
6. IAM: delete the knowledge base service role (`AmazonBedrockExecutionRoleForKnowledgeBase_...`).
