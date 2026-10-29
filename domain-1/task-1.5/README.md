# Domain 1 · Task 1.5: Design retrieval mechanisms for FM augmentation

Companion files for the seven Medium posts on Task 1.5 of the AIP-C01 exam guide. Region: **us-west-2**.

| Post | Medium title | Type | Lab folder |
| --- | --- | --- | --- |
| 1 | AIP-C01 Skill 1.5.1: Chunking Documents for Better Retrieval | Lab, ~40 min | [`skill-1.5.1-chunking`](skill-1.5.1-chunking) |
| 2 | AIP-C01 Skill 1.5.2: Choose and Use Embedding Models | Lab, ~30 min | [`skill-1.5.2-embeddings`](skill-1.5.2-embeddings) |
| 3 | AIP-C01 Skill 1.5.3: Deploy Vector Search: OpenSearch, pgvector or Knowledge Bases | Notes | — |
| 4 | AIP-C01 Skill 1.5.4: Hybrid Search and Reranking | Lab, ~25 min | [`skill-1.5.4-hybrid-rerank`](skill-1.5.4-hybrid-rerank) |
| 5 | AIP-C01 Skill 1.5.5: Rewrite Queries for Better Retrieval | Lab, ~30 min | [`skill-1.5.5-query-handling`](skill-1.5.5-query-handling) |
| 6 | AIP-C01 Skill 1.5.6: Give Models a Standard Way to Search | Lab, ~30 min | [`skill-1.5.6-retrieval-access`](skill-1.5.6-retrieval-access) |
| 7 | AIP-C01 Task 1.5 Exam Notes: Retrieval Mechanisms | Exam notes | — |

Labs 1.5.2, 1.5.4, 1.5.5 and 1.5.6 share a small corpus and search helpers in [`shared`](shared): twelve passages, eight test questions, Titan embeddings with a local cache, BM25 keyword search and reciprocal rank fusion. They need no vector database, so they cost cents. Set `OFFLINE=1` to try the keyword-only paths without an AWS account.

## Clean up

- **Skill 1.5.1:** delete the two knowledge bases, their S3 vector buckets, the `chunking-lab/` objects and the service roles.
- **Skill 1.5.5 and 1.5.6 (optional parts):** delete the Lambda functions, state machine, HTTP API and their roles.
- Everything else runs on demand and leaves nothing behind.
