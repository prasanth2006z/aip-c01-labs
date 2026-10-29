# AWS Services Reference

Every AWS service and feature used in the AIP-C01 Hands-on Labs series: what it's for, when to use it, when not to, and the exam wording that points to it. Grows as the series does.

## Models and model access

How your application reaches a foundation model, and how that model is served.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Amazon Bedrock** | Fully managed access to foundation models from many providers through one API | You want to use models without managing any infrastructure | The model you need isn't offered, or you need full control of the serving stack (use SageMaker AI) | "fully managed", "least operational overhead" | Skill 1.1.1 |
| **Converse API** | One request format for every Bedrock chat model, with conversation history and tool use | Switching models or providers without code changes; multi-turn chat | Embedding or image-generation models (call them with InvokeModel) | "switch models without code changes" | Skill 1.1.1 |
| **Cross-Region inference** | An inference profile spreads requests across Regions in a geography (us., eu.) or globally | Throttling at peak traffic; more throughput with no setup | Data must stay in one Region: use in-Region access, not a cross-Region profile | "throttling during peaks", "least effort to increase throughput" | Skill 1.1.1 |
| **Provisioned Throughput** | Reserved model capacity (model units), billed per hour whether used or not | Steady high volume that needs guaranteed throughput; serving some custom models | Spiky or low traffic: you pay for idle capacity | "guaranteed / consistent throughput" | Skill 1.1.1 |
| **Batch inference** | Processes a file of prompts from S3 asynchronously, at a lower price than on-demand | Large offline jobs where nobody waits for the answer | Interactive or real-time requests | "overnight", "millions of records", "lowest cost" | Skill 1.1.1 |
| **Amazon SageMaker AI endpoints** | Host your own or open-source models on instances you choose | Model isn't in Bedrock; custom containers; control over hardware | A Bedrock model fits and the team wants the least operations | "full control", "custom container" | Skill 1.1.1 |

## Amazon Bedrock features

Managed building blocks on top of the models.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Knowledge Bases** | Managed RAG: ingests documents, chunks and embeds them, stores vectors and retrieves passages | Answers must come from your own documents, which change over time | The task needs actions, not answers (Agents), or new behaviour or style (fine-tuning) | "internal documents", "cite sources" | Skill 1.1.1 |
| **Agents** | The model plans steps and calls APIs (action groups) and knowledge bases | Multi-step tasks that take actions, such as look up an order then refund it | The steps are fixed in advance (Flows, Step Functions) or it's plain Q&A | "call APIs", "take actions" | Skill 1.1.1 |
| **Guardrails** | Policies on inputs and outputs: content filters, denied topics, PII, word filters, grounding checks | One consistent safety policy across apps and models | Controlling who can call a model (that's IAM) | "block harmful content", "redact PII in responses" | Skill 1.1.1 |
| **Flows** | Visual workflows that link prompts, models, knowledge bases, Lambda and conditions | A fixed GenAI pipeline built with little code | Long-running orchestration across many AWS services or waits for humans (Step Functions) | "chain prompts", "low-code workflow" | Skill 1.1.1 |
| **Prompt Management** | Stores, versions and shares prompt templates with variables | Governing prompts across teams; changing prompts without redeploying | Throwaway experiments | "version and reuse prompts" | Skill 1.1.1 |

## Application and integration

The services around the model that receive requests and run the steps.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Amazon API Gateway** | Managed front door for REST, HTTP and WebSocket APIs, with auth and throttling | One stable, secured endpoint for clients; WebSocket for streamed chat | Long, non-streamed generations through REST APIs: the default integration timeout is 29 seconds | "expose securely", "throttle per client" | Skill 1.1.1 |
| **AWS Lambda** | Runs code on demand with no servers to manage | Glue code that calls Bedrock; agent action groups; event handling | Work longer than 15 minutes, or always-on servers | "serverless", "event-driven" | Skill 1.1.1 |
| **AWS Step Functions** | Orchestrates multi-step workflows with retries, branches, parallel steps and waits | Long or multi-service workflows, error handling, human approval | A single quick model call | "orchestrate", "human-in-the-loop" | Skill 1.1.1 |
| **Amazon EventBridge** | Routes events between services and runs schedules | React when something happens (a document arrives) or run nightly jobs | Synchronous request and response | "when a file arrives", "on a schedule" | Skill 1.1.1 |
| **Amazon EventBridge Scheduler** | Runs a target (such as Lambda) on a cron or rate schedule | Scheduled refreshes, nightly syncs, periodic evaluation | Reacting to an event as it happens (EventBridge rules, S3 events) | "scheduled", "nightly", "every hour" | Skill 1.4.5 |
| **AWS Secrets Manager** | Stores and rotates credentials and API keys | Connector credentials, third-party API keys | Non-secret configuration (AppConfig, Parameter Store) | "store credentials securely", "rotate" | Skill 1.4.4 |

## Data and storage

Where documents, state and vectors live.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Amazon S3** | Durable object storage | Source documents for knowledge bases; batch inputs and outputs; logs | Fast lookups by key, such as session state (DynamoDB) | "documents", "data lake" | Skill 1.1.1 |
| **Amazon DynamoDB** | Serverless key-value database with millisecond latency | Conversation history, session state, user preferences | Similarity search over embeddings; ad hoc analytics | "session state", "chat history" | Skill 1.1.1 |
| **OpenSearch Serverless (vector)** | Vector search plus keyword (hybrid) search, managed | Low-latency semantic or hybrid search at scale | Small or cost-first workloads: it has a minimum capacity charge | "hybrid search", "low latency at scale" | Skill 1.1.1 |
| **Amazon S3 Vectors** | Stores and queries vectors inside S3 at low cost | Large vector sets, cost first, moderate query rates | Highest query rates at lowest latency, or keyword plus vector search | "lowest-cost vector storage" | Skill 1.1.1 |
| **Aurora PostgreSQL with pgvector** | Vectors next to relational data in PostgreSQL | The team already runs PostgreSQL; queries join vectors with tables | No relational need and the team wants a fully managed vector service | "already using PostgreSQL" | Skill 1.1.1 |
| **Amazon OpenSearch Service (vector, neural plugin)** | Managed OpenSearch clusters with k-NN (HNSW) vector search; the neural plugin calls Bedrock embedding models for you | Custom index design, per-domain indexes, hybrid search, tuning shards and HNSW | The team wants no cluster to size or tune (Serverless or Knowledge Bases) | "sharding", "ef_search", "neural search" | Skill 1.4.1 |
| **Knowledge Bases custom data source** | Push and delete individual documents through the API (direct ingestion), no sync needed | Sources without a built-in connector; changes that must be searchable within seconds | A built-in connector (S3, Confluence, SharePoint, Salesforce, Web Crawler) already covers the source | "near real-time updates", "custom connector" | Skill 1.4.4 |
| **Amazon Q Business** | Managed enterprise assistant with many data connectors and per-user permissions | A ready-made assistant over company content with little building | You're building your own GenAI application and need full control | "enterprise search assistant", "40+ connectors" | Skill 1.4.4 |

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
| **Amazon Comprehend** | Pre-trained NLP: language, entities, key phrases, sentiment and PII | Detecting or masking PII and extracting entities without training a model | Rewriting or summarising text (a foundation model) | "detect PII", "extract entities" | Skill 1.3.4 |

## Observability and audit

How you see what the application and the models are doing.

| Service | Purpose | Use it when | Not recommended when | Exam cue | First used |
| --- | --- | --- | --- | --- | --- |
| **Amazon CloudWatch** | Metrics, logs, alarms and dashboards | Tracking latency, invocations, throttles and token counts; alarming on them | Auditing who called which API (CloudTrail) | "monitor", "alarm on" | Skill 1.1.1 |
| **Bedrock model invocation logging** | Logs full request and response payloads to CloudWatch Logs or S3; off by default | Debugging prompts, reviewing quality, keeping records | Payloads hold data you mustn't store: restrict access or mask it first | "log prompts and responses" | Skill 1.1.1 |
| **AWS CloudTrail** | Records API calls: who did what, and when | Security audit and governance | Seeing prompt and response content (invocation logging) | "audit who invoked the model" | Skill 1.1.1 |

_Independent study resource, not affiliated with AWS. Check the AWS documentation for current limits and features._
