# AWS Services Reference

Every AWS service and feature used in the AIP-C01 Hands-on Labs series: what it's for, when to use it, when not to, and the exam wording that points to it. Grows as the series does. Up to date with Domain 1 (Skill 1.6.6): 52 services and features, plus 6 commonly confused services.

## Models and model access

How your application reaches a foundation model, and how that model is served.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Amazon Bedrock** | Fully managed access to foundation models from many providers through one API | You want to use models without managing any infrastructure | The model you need isn't offered, or you need full control of the serving stack (use SageMaker AI) | "fully managed", "least operational overhead" | Skill 1.1.1 |
| **Converse API** | One request format for every Bedrock chat model, with conversation history, images and tool use | Switching models without code changes; multi-turn chat; schema-shaped JSON through tool use | Embedding or image-generation models (call them with InvokeModel) | "switch models without code changes", "conversation history" | Skill 1.1.1 |
| **Cross-Region inference** | An inference profile spreads requests across Regions in a geography (us., eu., apac.) or globally | Throttling at peak traffic; models with limited Regional availability | Data must stay in one Region; use a geographic, not global, profile for residency within a geography | "throttling during peaks", "limited regional availability" | Skill 1.1.1 |
| **Provisioned Throughput** | Reserved model capacity (model units), billed per hour whether used or not | Steady high volume that needs guaranteed throughput; serving some custom models | Spiky, low or one-off traffic: you pay for idle capacity | "guaranteed / consistent throughput" | Skill 1.1.1 |
| **Batch inference** | Processes a file of prompts from S3 asynchronously, at a lower price than on-demand | Large offline jobs where nobody waits for the answer, including bulk embeddings | Interactive or real-time requests | "overnight", "millions of records", "lowest cost" | Skill 1.1.1 |
| **Amazon SageMaker AI endpoints** | Host your own, open-source or fine-tuned models on instances you choose | Model isn't in Bedrock; custom containers; control over hardware | A Bedrock model fits and the team wants the least operations | "full control", "custom container" | Skill 1.1.1 |

## Choosing, customizing and releasing models

How a model is picked, adapted to a domain and replaced safely.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Bedrock model evaluation** | Compares models on your own prompt dataset with automatic metrics, an LLM-as-a-judge or human reviewers | Choosing between models in a PoC; checking a new model before switching | Judging by public leaderboards, which don't reflect your data | "compare models on our data", "evaluate quality" | Skill 1.1.2 |
| **Bedrock Intelligent Prompt Routing** | Sends each prompt to the model in a family that's expected to answer it well at lower cost | A mix of simple and complex prompts; cut cost without writing routing logic | Every prompt needs the largest model, or models from different families must be mixed | "reduce cost", "simple and complex requests", "no custom routing" | Skill 1.2.1 |
| **Model customization (fine-tuning)** | Trains a copy of a model on your examples to change its behaviour, style or domain skill | Prompting and RAG are exhausted and the task needs consistent learned behaviour | Adding fresh or changing facts (use RAG); data is small or unvalidated | "domain-specific style", "consistent format at scale" | Skill 1.2.4 |
| **LoRA and adapters (PEFT)** | Parameter-efficient fine-tuning: train small adapter weights on a frozen base model | Cheaper, faster customization; serving several adapters on one base model | Prompting already meets the quality bar | "parameter-efficient", "low-rank adaptation" | Skill 1.2.4 |
| **SageMaker Model Registry** | Versions models with metrics and an approval status | Tracking which model version is approved for deployment; audit of model lineage | Prompt versions (Prompt Management) or app configuration (AppConfig) | "versioning", "approve before deploy" | Skill 1.2.4 |
| **SageMaker deployment guardrails** | Blue/green deployments with traffic shifting and automatic rollback on CloudWatch alarms | Releasing a new model version safely to a SageMaker AI endpoint | Bedrock-hosted models, where you switch model IDs through configuration instead | "roll back automatically", "shift traffic gradually" | Skill 1.2.4 |

## Bedrock retrieval (RAG)

Getting the right passages from your content into the prompt.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Knowledge Bases** | Managed RAG: ingests documents, chunks and embeds them, stores vectors and retrieves passages, with metadata filters | Answers must come from your own documents, which change over time | The task needs actions, not answers (Agents), or new behaviour or style (fine-tuning) | "internal documents", "cite sources", "least overhead RAG" | Skill 1.1.1 |
| **Knowledge Bases connectors and chunking** | Built-in data sources (S3, Confluence, SharePoint, Salesforce, Web Crawler); chunking strategies; custom transformation Lambda | Indexing common systems without code; hierarchical or semantic chunking; custom splitting rules | Changing the chunking of an existing data source: it's fixed, so create a new one | "Confluence", "SharePoint", "missing context", "custom chunking" | Skill 1.4.4 |
| **Knowledge Bases custom data source** | Push and delete individual documents through the API (direct ingestion), no sync needed | Sources without a built-in connector; changes that must be searchable within seconds | A built-in connector already covers the source | "near real-time updates", "custom connector" | Skill 1.4.4 |
| **Embedding models (Titan Text Embeddings V2, Titan Multimodal, Cohere Embed)** | Turn text (or images) into vectors for semantic search | Every vector store; choose dimensions and model by measured recall | Mixing models or dimensions between documents and queries | "dimensions", "multilingual", "images and text" | Skill 1.5.2 |
| **Reranker models (Amazon Rerank, Cohere Rerank)** | Score each retrieved passage against the question and reorder them | Relevant passages are retrieved but ranked too low | The right passage isn't retrieved at all (fix retrieval first) | "improve relevance", "rerank" | Skill 1.5.4 |
| **Amazon Q Business** | Managed enterprise assistant with many data connectors and per-user permissions | A ready-made assistant over company content with little building | You're building your own GenAI application and need full control | "enterprise search assistant", "40+ connectors" | Skill 1.4.4 |

## Bedrock prompts, safety and agents

Controlling what the model is told, what it may say, and what it can do.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Prompt Management** | Stores prompt templates with variables, model and settings; immutable versions called by ARN | One reviewed prompt across apps; governed changes; rollback to a previous version | Throwaway experiments | "version and reuse prompts", "role definition" | Skill 1.1.1 |
| **Guardrails** | Policies on inputs and outputs: content filters, denied topics, prompt-attack filter, PII masking, grounding checks | Rules that must always hold, whatever users type | Controlling who can call a model (that's IAM) | "never discuss", "mask PII", "prompt injection" | Skill 1.1.1 |
| **ApplyGuardrail API** | Evaluates any text against a guardrail without calling a Bedrock model | Same safety policy for SageMaker, third-party or self-hosted models, or for stored text | Calls to Bedrock models, where guardrailConfig in Converse already applies it | "same policy for any model" | Skill 1.6.1 |
| **Flows** | Visual, versioned workflows that link prompts, conditions, knowledge bases and Lambda | A fixed GenAI pipeline built with little code: classify, branch, answer | Long-running orchestration across many AWS services or waits for humans (Step Functions) | "chain prompts", "conditional branching", "low-code workflow" | Skill 1.1.1 |
| **Agents** | The model plans steps and calls APIs (action groups) and knowledge bases | Multi-step tasks that take actions, where the steps aren't known in advance | The steps are fixed in advance (Flows, Step Functions) or it's plain Q&A | "call APIs", "take actions" | Skill 1.1.1 |
| **Amazon Bedrock AgentCore Gateway** | Turns APIs and Lambda functions into MCP tools that agents can discover and call | Sharing tools such as retrieval across many agents and AI applications | One application calling one tool (plain function calling is simpler) | "MCP", "expose APIs as tools" | Skill 1.5.6 |
| **Model Context Protocol (MCP)** | Open standard for offering tools and data to AI applications; clients discover tools and schemas | Many AI clients (assistants, IDEs, agents) need the same tool | Your own app's model deciding when to search (Converse function calling is enough) | "standard tool interface", "MCP client" | Skill 1.5.6 |

## Application and integration

The services around the model that receive requests, hold configuration and run the steps.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Amazon API Gateway** | Managed front door for REST, HTTP and WebSocket APIs, with auth and throttling | One stable, secured endpoint for clients; WebSocket for streamed chat | Long, non-streamed generations through REST APIs: the default integration timeout is 29 seconds | "expose securely", "throttle per client" | Skill 1.1.1 |
| **AWS Lambda** | Runs code on demand with no servers to manage | Glue code that calls Bedrock; validation and normalisation; event handling | Work longer than 15 minutes, or always-on servers | "serverless", "event-driven" | Skill 1.1.1 |
| **AWS Step Functions** | Orchestrates multi-step workflows with retries, branches, parallel steps and waits | Circuit breakers; parallel retrieval (Map); human approval or user replies (task token) | A single quick model call | "orchestrate", "circuit breaker", "wait for a reply" | Skill 1.1.1 |
| **AWS AppConfig** | Deploys application configuration with validation, gradual rollout and alarm-based rollback | Switching model IDs, prompt versions or feature flags without code changes | Secrets such as API keys (Secrets Manager) | "without code changes", "feature flag", "gradual rollout" | Skill 1.2.2 |
| **Amazon EventBridge** | Routes events between services and runs schedules | React when something happens (a document arrives) or run nightly jobs | Synchronous request and response | "when a file arrives", "on a schedule" | Skill 1.1.1 |
| **Amazon EventBridge Scheduler** | Runs a target (such as Lambda) on a cron or rate schedule | Scheduled refreshes, nightly syncs, periodic evaluation | Reacting to an event as it happens (EventBridge rules, S3 events) | "scheduled", "nightly", "every hour" | Skill 1.4.5 |
| **AWS Secrets Manager** | Stores and rotates credentials and API keys | Connector credentials, third-party API keys | Non-secret configuration (AppConfig, Parameter Store) | "store credentials securely", "rotate" | Skill 1.4.4 |

## Data and storage

Where documents, state and vectors live.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Amazon S3** | Durable object storage | Source documents for knowledge bases; batch inputs and outputs; template repositories; logs | Fast lookups by key, such as session state (DynamoDB) | "documents", "data lake" | Skill 1.1.1 |
| **Amazon DynamoDB** | Serverless key-value database with millisecond latency and TTL expiry | Conversation history, session state, fast-changing metadata, circuit-breaker state | Similarity search over embeddings; ad hoc analytics | "session state", "chat history" | Skill 1.1.1 |
| **OpenSearch Serverless (vector)** | Vector search plus keyword (hybrid) search, managed; access via data access policies | Low-latency semantic or hybrid search with no cluster to size | Small or cost-first workloads: it has a minimum capacity charge | "hybrid search", "no nodes to manage" | Skill 1.1.1 |
| **Amazon OpenSearch Service (vector, neural plugin)** | Managed OpenSearch clusters with k-NN (HNSW) vector search; the neural plugin calls Bedrock embedding models for you | Custom index design, per-domain indexes, tuning shards, replicas and HNSW | The team wants no cluster to size or tune (Serverless or Knowledge Bases) | "sharding", "ef_search", "neural search" | Skill 1.4.1 |
| **Amazon S3 Vectors** | Stores and queries vectors inside S3 at low cost | Large vector sets, cost first, moderate query rates | Highest query rates at lowest latency, or keyword plus vector search | "lowest-cost vector storage", "billions of vectors" | Skill 1.1.1 |
| **Aurora PostgreSQL with pgvector** | Vectors next to relational data in PostgreSQL | The team already runs PostgreSQL; queries join vectors with tables | No relational need and the team wants a fully managed vector service | "already using PostgreSQL", "join with tables" | Skill 1.1.1 |

## Data preparation and processing

How data is checked, converted and cleaned before a model sees it.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **AWS Glue Data Quality** | Data quality rules (DQDL) on tables in S3 or the Data Catalog, run on a schedule or in ETL jobs | Checking completeness, uniqueness and value ranges of tabular data before ingestion | Single unstructured documents arriving one at a time (Lambda) | "data quality rules", "least custom code" | Skill 1.3.1 |
| **SageMaker Data Wrangler** | Visual data exploration and preparation with a data quality and insights report | Profiling a new dataset before deciding what to check or fix | Automated checks on every new batch (Glue Data Quality) | "explore", "profile", "visual" | Skill 1.3.1 |
| **Amazon Transcribe** | Speech to text, as asynchronous jobs or streaming | Voicemails, call recordings and other audio a text model must use | Text already exists | "audio", "call recordings" | Skill 1.3.2 |
| **Amazon Polly** | Text to speech | Creating spoken output (in this series, test audio) | Understanding audio (Transcribe) | "text to speech" | Skill 1.3.2 |
| **Amazon Textract** | Extracts text, tables and form fields from scanned documents | Scanned forms, invoices and PDFs with tables | Understanding what a photo shows (a multimodal model) | "scanned documents", "forms", "tables" | Skill 1.3.2 |
| **Bedrock Data Automation** | Managed extraction of structured fields from documents, images, audio and video | Many file types into one structured output with little custom code | One simple file type a single service already handles | "multimodal extraction", "least effort" | Skill 1.3.2 |
| **SageMaker Processing** | Runs your own preprocessing code as a managed job on chosen instances | Large batches or long-running custom preprocessing | Small per-file work (Lambda) | "preprocess a large dataset", "custom code" | Skill 1.3.2 |
| **Amazon Comprehend** | Pre-trained NLP: language, entities, key phrases, sentiment, PII; custom classification | Masking PII, extracting entities, recognising intent or sentiment without a large model | Rewriting or summarising text (a foundation model) | "detect PII", "extract entities", "intent" | Skill 1.3.4 |

## Governance, observability and audit

How workloads are standardized, reviewed and watched.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **AWS Well-Architected Tool + Generative AI Lens** | Reviews a workload against AWS generative AI best practices; risks, improvement plan, milestones | Consistent design reviews across teams; tracking risk from PoC to production | Checking live resource settings (AWS Config) or account checks (Trusted Advisor) | "best practices review", "Generative AI Lens" | Skill 1.1.3 |
| **AWS Service Catalog** | Lets teams launch approved, versioned products (infrastructure templates) | Standardized components every team deploys the same way | One-off experiments | "approved", "standardized", "self-service" | Skill 1.1.3 |
| **AWS CloudFormation / AWS CDK** | Infrastructure as code: define resources once, deploy them repeatably | Reusable, reviewable stacks such as an approved RAG pattern | Clicking the same steps in the console for each team | "repeatable", "infrastructure as code" | Skill 1.1.3 |
| **Amazon CloudWatch** | Metrics, logs, alarms and dashboards | Latency, throttles, token counts, data-quality and prompt pass-rate metrics; alarms | Auditing who called which API (CloudTrail) | "monitor", "alarm on", "regression" | Skill 1.1.1 |
| **Bedrock model invocation logging** | Logs full request and response payloads to CloudWatch Logs or S3; off by default | Debugging prompts, reviewing quality, auditing what the model received | Payloads hold data you mustn't store: restrict access or mask it first | "log prompts and responses" | Skill 1.1.1 |
| **AWS CloudTrail** | Records API calls: who did what, and when | Security audit; who changed a prompt, guardrail or model setting | Seeing prompt and response content (invocation logging) | "audit who invoked", "who changed" | Skill 1.1.1 |

## Commonly confused services

Real services that often appear as wrong options. Know what they do, and when they ARE the answer.

| Service | What it actually does | It IS the answer when | Why it's usually a distractor in GenAI questions | Exam cue | Appears in |
| --- | --- | --- | --- | --- | --- |
| **AWS Config** | Records resource configurations and checks them against rules | Compliance of resource settings (for example, encryption enabled) | It doesn't review a workload's design against GenAI best practices (WA Tool + Lens) | "resource compliance" | Skill 1.1.3 |
| **AWS Trusted Advisor** | Account-level checks for cost, limits, security and resilience | Finding idle resources, quota limits or open security groups | It doesn't assess generative AI workload design | "account checks", "service limits" | Skill 1.1.3 |
| **Amazon SQS** | Message queues between components | Decoupling and buffering work; dead-letter queues for failed messages | A queue alone isn't a circuit breaker, fallback or graceful degradation | "decouple", "buffer" | Skill 1.2.3 |
| **Amazon EC2** | Virtual servers you manage | Workloads that need full control of the operating system | Usually the most operational overhead; managed services win when 'least effort' is asked | "full control of the OS" | Skill 1.1.1 |
| **Amazon RDS** | Managed relational databases | Relational data; with PostgreSQL and pgvector, vectors next to tables | Chat history with auto-expiry is simpler in DynamoDB with TTL | "relational", "SQL" | Skill 1.6.2 |
| **AWS IAM** | Who can call which API on which resource | Access control for models, knowledge bases and data | It doesn't filter content (Guardrails) or grant OpenSearch Serverless data access on its own | "permissions", "least privilege" | Skill 1.1.1 |

_Independent study resource, not affiliated with AWS. Check the AWS documentation for current limits and features._
