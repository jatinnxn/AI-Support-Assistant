# Design Note — AI Support Assistant

## 1. Overview

The AI Support Assistant is designed to automate two common support and customer-success workflows:

1. **AI Ticket Triage** — classify and route incoming support tickets while generating a customer-ready first response.
2. **Technical Account Manager (TAM) Account Summary** — synthesize account health, recent support activity, risks, and recommended discussion points into an executive-ready summary.

The implementation separates API handling, agent logic, retrieval, LLM interaction, schemas, evaluation, and UI concerns so that each component has a clear responsibility.

---

## 2. System Architecture

```text
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         └──────────┬──────────┘
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
             ┌───────────────┐               ┌───────────────┐
             │ Triage Agent  │               │   TAM Agent   │
             └───────┬───────┘               └───────┬───────┘
                     │                               │
                     ▼                               ▼
             ┌───────────────┐               ┌───────────────┐
             │   Retriever   │               │ Account/Ticket│
             └───────┬───────┘               │     Data      │
                     │                       └───────┬───────┘
                     ▼                               │
             ┌───────────────┐                       │
             │   ChromaDB    │                       │
             └───────┬───────┘                       │
                     │                               │
                     └───────────────┬───────────────┘
                                     ▼
                           ┌──────────────────┐
                           │   LLM Service    │
                           │      Gemini      │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │ Pydantic Schemas │
                           └──────────────────┘
```

---

## 3. Component Responsibilities

### 3.1 FastAPI Application

`app/main.py` acts as the application/API boundary.

Responsibilities:

- Accept HTTP requests.
- Validate incoming request data.
- Invoke the appropriate agent.
- Return structured responses.
- Expose interactive API documentation.

The API layer does not contain the core LLM reasoning logic.

---

### 3.2 Triage Agent

`agents/triage_agent.py`

Responsibilities:

- Accept a support ticket.
- Retrieve relevant knowledge-base context.
- Construct the triage prompt.
- Invoke the LLM service.
- Return validated structured output.

The Triage Agent is responsible for the ticket-level workflow rather than API transport.

---

### 3.3 TAM Agent

`agents/tam_agent.py`

Responsibilities:

- Retrieve account information.
- Identify recent account activity.
- Analyze relevant support tickets and escalations.
- Construct the account-level prompt.
- Invoke the LLM service.
- Return a structured executive summary.

The TAM Agent focuses on account-level synthesis rather than individual ticket classification.

---

### 3.4 LLM Service

`services/llm_service.py`

The LLM service provides a centralized abstraction around Gemini.

Responsibilities:

- Configure the Gemini client.
- Load model configuration from environment variables.
- Send prompts to Gemini.
- Request structured responses.
- Return model output to the calling agent.

Centralizing LLM access avoids duplicating Gemini client configuration across agents.

---

### 3.5 Pydantic Schemas

`models/schemas.py`

Pydantic models define explicit contracts for application inputs and outputs.

This provides:

- Type validation.
- Required-field validation.
- Consistent API responses.
- Easier testing.
- Safer downstream processing.

The LLM is therefore not treated as an unrestricted text generator.

---

## 4. Ticket Triage Design

The ticket triage workflow is:

```text
Incoming Ticket
      │
      ▼
Input Validation
      │
      ▼
Triage Agent
      │
      ▼
Knowledge Retrieval
      │
      ▼
Relevant KB Context
      │
      ▼
Prompt Construction
      │
      ▼
Gemini
      │
      ▼
Structured Response
      │
      ▼
Pydantic Validation
      │
      ▼
Triage Result
```

### Output

The triage response contains:

- `product_area`
- `issue_category`
- `urgency`
- `reasoning`
- `knowledge_base_article`
- `responder_team`
- `first_response`

The design intentionally separates classification information from the customer-facing first response.

---

## 5. RAG Design

The RAG pipeline uses the indexed knowledge base as grounding context for ticket triage.

```text
Knowledge Base Documents
          │
          ▼
      Chunking
          │
          ▼
     Embeddings
          │
          ▼
       ChromaDB
          │
          ▼
      Similarity
      Retrieval
          │
          ▼
 Relevant Documents
          │
          ▼
      Triage Prompt
          │
          ▼
        Gemini
```

### Why RAG is used

Support classification should be grounded in organization-specific information.

A general-purpose LLM may know concepts such as authentication, billing, or integrations, but it does not inherently know:

- Internal knowledge-base articles.
- Internal product terminology.
- Internal responder teams.
- Organization-specific troubleshooting guidance.

RAG supplies this context at inference time.

---

## 6. TAM Agent Design

The TAM workflow operates at account level.

```text
Account ID
   │
   ▼
Account Data
   │
   ├── Account Health
   ├── ARR / Commercial Context
   ├── Usage Information
   ├── Recent Tickets
   └── Escalations
   │
   ▼
Relevant Account Context
   │
   ▼
TAM Prompt
   │
   ▼
Gemini
   │
   ▼
Structured TAM Output
```

The output is intended for a TAM or customer-success stakeholder rather than directly for an end customer.

---

## 7. Risk Identification

The TAM output contains structured risks.

Each risk contains:

```text
risk
evidence
```

The separation is intentional.

A risk statement alone is not sufficient for an operational account review. Evidence provides traceability back to account or support information.

Example:

```json
{
  "risk": "Active churn risk",
  "evidence": "The account is evaluating competing vendors."
}
```

This structure also allows the evaluation harness to verify that risks contain supporting evidence.

---

## 8. Structured Generation

Gemini is used for natural-language reasoning and synthesis, but the application expects structured output.

Conceptually:

```text
Prompt
  │
  ▼
Gemini
  │
  ▼
Structured JSON
  │
  ▼
Pydantic
  │
  ▼
Application Object
```

This reduces the risk of downstream code receiving unexpected free-form output.

---

## 9. Evaluation Strategy

The project includes a dedicated evaluation layer.

The evaluation workflow is separated from production API execution:

```text
Evaluation Dataset
       │
       ▼
Agent Inference
       │
       ▼
Predictions
       │
       ▼
Evaluation Checks
       │
       ▼
Metrics / Report
```

The evaluation checks structural and quality-oriented properties such as:

- Required fields are present.
- Urgency belongs to the expected set.
- Required text fields are non-empty.
- Summaries satisfy configured length constraints.
- TAM risks contain non-empty evidence.
- Aggregate pass rate is calculated.
- Average evaluation score is calculated.

This provides a repeatable regression layer rather than relying only on manual inspection.

---

## 10. Prediction Generation

Prediction generation is separated from evaluation where prediction artifacts are available.

```text
Agent
  │
  ▼
Generated Prediction
  │
  ▼
evaluation/predictions/
  │
  ▼
Evaluation Harness
```

This is useful because LLM calls can be affected by:

- API quota.
- Temporary model availability.
- Network failures.
- Model output variability.

Cached prediction artifacts can make later evaluation runs faster and less dependent on external API availability.

---

## 11. API Design

The application exposes two primary workflows.

### Ticket Triage

```text
POST /triage
```

Input:

```json
{
  "subject": "Unable to login",
  "body": "Customer cannot login after resetting the password."
}
```

Output:

```json
{
  "product_area": "...",
  "issue_category": "...",
  "urgency": "P3",
  "reasoning": "...",
  "knowledge_base_article": "...",
  "responder_team": "...",
  "first_response": "..."
}
```

### TAM Summary

```text
GET /tam/{account_id}
```

Output:

```json
{
  "executive_summary": "...",
  "open_risks": [
    {
      "risk": "...",
      "evidence": "..."
    }
  ],
  "talking_points": [
    "..."
  ]
}
```

---

## 12. UI Design

The Streamlit application acts as a presentation layer.

It does not duplicate the agent logic.

```text
Streamlit
    │
    │ HTTP
    ▼
FastAPI
    │
    ▼
Agents
```

This separation means the same backend can later support:

- Web UI.
- External applications.
- REST clients.
- Internal support tooling.
- Automated workflows.

---

## 13. Error Handling

The system needs to distinguish between application errors and external-service errors.

Examples include:

### Validation errors

Invalid or missing input should be rejected before invoking the LLM.

### Account errors

An unknown account ID should return an appropriate API error rather than generating fabricated account information.

### Gemini errors

Temporary or quota-related Gemini failures should be surfaced as service failures rather than silently converted into fabricated responses.

### Retrieval errors

If the retrieval layer cannot access its vector store, the application should fail clearly rather than implying that retrieved knowledge was available.

---

## 14. Reliability Considerations

LLM-backed systems have external dependencies that traditional deterministic applications do not.

Relevant failure modes include:

- API quota exhaustion.
- Temporary model unavailability.
- Network failures.
- Model response validation failures.
- Embedding-model download issues.
- Vector-store availability issues.

For production deployment, the next reliability improvements would include:

- Exponential backoff for transient LLM failures.
- Request timeouts.
- Circuit breaking.
- Model fallback.
- Response caching.
- Centralized logging.
- Metrics and tracing.

---

## 15. Security Considerations

API credentials are loaded from environment variables.

Secrets should never be embedded directly in source code.

The repository should contain:

```text
.env.example
```

rather than a production `.env`.

Before submission:

- Remove API-key debug statements.
- Confirm `.env` is ignored by Git.
- Check `git status`.
- Inspect staged files before committing.
- Never commit raw credentials.

---

## 16. Production Scalability

The current implementation is appropriate for an assignment and local demonstration.

For larger production workloads, the architecture can evolve without changing the agent responsibilities.

Potential changes include:

```text
                   Load Balancer
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          API Instance         API Instance
              │                     │
              └──────────┬──────────┘
                         ▼
                  Agent Services
                         │
              ┌──────────┴──────────┐
              ▼                     ▼
          Vector DB             LLM Provider
```

Additional infrastructure could include:

- Managed vector database.
- Redis for caching.
- Queue workers for asynchronous processing.
- Centralized observability.
- Secrets manager.
- Horizontal API scaling.

---

## 17. Key Trade-offs

### Gemini

**Benefit:** Strong general-purpose reasoning and structured generation.

**Trade-off:** External API dependency, quota limits, latency, and cost.

### RAG

**Benefit:** Grounds responses in organization-specific knowledge.

**Trade-off:** Retrieval quality becomes an additional source of system error.

### ChromaDB

**Benefit:** Simple local vector-store setup suitable for development and assignment deployment.

**Trade-off:** A managed vector database would be more appropriate for large-scale production workloads.

### Streamlit

**Benefit:** Fast development and effective AI application demonstration.

**Trade-off:** It is not intended to replace a full production frontend for complex multi-user applications.

### Pydantic

**Benefit:** Strong interface contracts and validation.

**Trade-off:** Schema changes must be managed carefully as the application evolves.

---

## 18. Observability Recommendations

A production version should capture:

- Request ID.
- Endpoint latency.
- Retrieval latency.
- LLM latency.
- LLM model used.
- Token usage where available.
- API failures.
- Validation failures.
- Retrieval failures.
- Evaluation scores.

Sensitive ticket and customer information should not be written to logs unnecessarily.

---

## 19. Future Improvements

The current architecture can be extended with:

1. Human-in-the-loop approval for high-impact responses.
2. Automated ticket routing into support systems.
3. Conversation memory.
4. Feedback collection from support agents.
5. Continuous evaluation from production examples.
6. Prompt version tracking.
7. Model comparison and A/B testing.
8. LLM observability.
9. Cost monitoring.
10. Automated regression gates in CI/CD.

---

## 20. Conclusion

The architecture separates the responsibilities of API handling, agent workflows, retrieval, LLM interaction, structured validation, evaluation, and presentation.

The resulting flow is:

```text
User / Support System
        │
        ▼
     FastAPI
        │
        ▼
     Agent
        │
        ├───────────────┐
        │               │
        ▼               ▼
    Retrieval        Account Data
        │               │
        └───────┬───────┘
                ▼
              Gemini
                │
                ▼
          Pydantic Schema
                │
                ▼
        Structured Result
                │
                ▼
          API / Streamlit
```

This provides a clean foundation for a production-oriented AI support workflow while keeping the current implementation appropriately lightweight for development, evaluation, and demonstration.
