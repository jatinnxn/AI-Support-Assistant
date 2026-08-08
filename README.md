# AI Support Assistant

A production-oriented AI Support Assistant for automated support-ticket triage and Technical Account Manager (TAM) account intelligence.

The system combines Google Gemini, Retrieval-Augmented Generation (RAG), ChromaDB, Pydantic validation, FastAPI, and Streamlit to transform raw support information into structured, actionable outputs.

---

## Features

### AI Ticket Triage

Automatically analyzes incoming support tickets and generates:

- Product area
- Issue category
- Urgency / priority
- Reasoning
- Relevant knowledge-base article
- Responder team
- Suggested first response

The result is returned as structured, validated data.

### Technical Account Manager (TAM) Agent

Generates an account-level executive summary using customer/account information and recent support activity.

The TAM workflow produces:

- Executive summary
- Open risks
- Evidence supporting each risk
- Recommended talking points

### Retrieval-Augmented Generation

The ticket triage workflow uses the indexed knowledge base to retrieve relevant support information before generating the final response.

Pipeline:

Knowledge Base → Embeddings → ChromaDB → Retriever → Relevant Context → Gemini

### FastAPI Backend

The backend exposes API endpoints for:

- Ticket triage
- TAM account summaries

Interactive API documentation is available through Swagger UI.

### Streamlit UI

A web interface provides two workflows:

- Ticket Triage
- TAM Summary

The Streamlit application communicates with the FastAPI backend.

### Evaluation Harness

The project includes an evaluation workflow for testing:

- Triage predictions
- TAM summaries
- Output structure
- Required fields
- Risk evidence quality
- Aggregate evaluation metrics

---

# Architecture

```text
                         ┌─────────────────────┐
                         │    Streamlit UI     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI API     │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
             ┌───────────────┐             ┌───────────────┐
             │ Triage Agent  │             │   TAM Agent   │
             └───────┬───────┘             └───────┬───────┘
                     │                             │
                     ▼                             ▼
             ┌───────────────┐             ┌───────────────┐
             │   Retriever   │             │ Account Data  │
             └───────┬───────┘             │ Ticket Data   │
                     │                     └───────┬───────┘
                     ▼                             │
             ┌───────────────┐                     │
             │   ChromaDB    │                     │
             │ Vector Store  │                     │
             └───────┬───────┘                     │
                     │                             │
                     └──────────────┬──────────────┘
                                    ▼
                         ┌─────────────────────┐
                         │    LLM Service      │
                         │       Gemini        │
                         └─────────────────────┘
```

---

# Project Structure

```text
support-ai-assistant/
│
├── app/
│   └── main.py
│
├── agents/
│   ├── triage_agent.py
│   └── tam_agent.py
│
├── services/
│   └── llm_service.py
│
├── models/
│   └── schemas.py
│
├── rag/
│   ├── retriever.py
│   └── ...
│
├── prompts/
│   └── ...
│
├── evaluation/
│   ├── generate_predictions.py
│   ├── run_eval.py
│   ├── test_triage.py
│   ├── test_tam.py
│   ├── evaluator.py
│   └── predictions/
│
├── ui/
│   └── app.py
│
├── tests/
│   └── ...
│
├── data/
│   └── ...
│
├── knowledge-base/
│   └── ...
│
├── vector_store/
│   └── ...
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

---

# Technology Stack

| Component | Technology |
|---|---|
| Programming Language | Python |
| LLM | Google Gemini |
| Backend API | FastAPI |
| Data Validation | Pydantic |
| RAG | LangChain + ChromaDB |
| Embeddings | Hugging Face |
| Vector Database | ChromaDB |
| Frontend | Streamlit |
| Evaluation | Python |
| ASGI Server | Uvicorn |

---

# Requirements

- Python 3.10+
- Gemini API key
- Internet connection for Gemini API and embedding model access

Python 3.12 is recommended for the current project environment.

---

# Installation

## 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd support-ai-assistant
```

## 2. Create a virtual environment

### Windows

```powershell
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the project root.

```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.6-flash
```

Never commit the real `.env` file to GitHub.

Use `.env.example` as the public configuration template.

Example:

```env
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.6-flash
```

---

# Running the Backend

From the project root:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

# Ticket Triage API

## Endpoint

```text
POST /triage
```

## Request

```json
{
  "subject": "Unable to login",
  "body": "Customer cannot login after resetting the password."
}
```

## Example Response

```json
{
  "product_area": "Authentication & SSO",
  "issue_category": "Authentication Issue",
  "urgency": "P3",
  "reasoning": "The issue impacts a single customer and appears to be an isolated authentication problem.",
  "knowledge_base_article": "Troubleshooting: Authentication & SSO",
  "responder_team": "Identity & Access Management Support",
  "first_response": "Hello, thank you for reaching out to support..."
}
```

---

# TAM Account Summary API

## Endpoint

```text
GET /tam/{account_id}
```

Example:

```text
GET /tam/ACC-3336
```

## Example Response

```json
{
  "executive_summary": "The account is currently at risk due to declining usage and recent support escalations.",
  "open_risks": [
    {
      "risk": "Active churn risk",
      "evidence": "The account is evaluating competing vendors."
    }
  ],
  "talking_points": [
    "Review recent performance issues.",
    "Establish a technical stabilization plan.",
    "Schedule an executive account review."
  ]
}
```

---

# Running the Streamlit UI

Start FastAPI first:

```bash
uvicorn app.main:app --reload
```

Open a second terminal and activate the virtual environment.

Then run:

```bash
streamlit run ui/app.py
```

The Streamlit application will be available at:

```text
http://localhost:8501
```

---

# Streamlit Workflows

## Ticket Triage

Enter:

- Subject
- Ticket body

Then click:

```text
Analyze Ticket
```

The UI displays:

- Product Area
- Issue Category
- Urgency
- Reasoning
- Knowledge Base Article
- Responder Team
- Suggested First Response

## TAM Summary

Enter an account ID such as:

```text
ACC-3336
```

Then click:

```text
Generate Account Summary
```

The UI displays:

- Executive Summary
- Open Risks
- Risk Evidence
- Talking Points

---

# RAG Pipeline

The knowledge base is indexed into ChromaDB.

```text
Knowledge Base
      │
      ▼
Document Loading
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
Retriever
      │
      ▼
Relevant Context
      │
      ▼
Gemini
      │
      ▼
Structured Output
```

The retriever provides relevant knowledge-base context to the Triage Agent before final generation.

---

# Structured Output

Pydantic schemas define the expected application contracts.

## Triage Output

```text
product_area
issue_category
urgency
reasoning
knowledge_base_article
responder_team
first_response
```

## TAM Output

```text
executive_summary
open_risks
talking_points
```

Each risk contains:

```text
risk
evidence
```

This ensures downstream application logic receives predictable structured data rather than arbitrary free-form model output.

---

# Evaluation

Run the evaluation harness from the project root:

```bash
python -m evaluation.run_eval
```

The evaluation process validates generated outputs and produces evaluation results/reports.

Prediction generation can be run with:

```bash
python -m evaluation.generate_predictions
```

Generated prediction files are stored under:

```text
evaluation/predictions/
```

This allows generated model outputs to be reused during evaluation rather than repeatedly calling the Gemini API.

---

# Evaluation Considerations

The evaluation harness checks important output-quality requirements such as:

- Required fields
- Valid urgency values
- Non-empty text fields
- Summary quality
- Risk evidence quality
- Aggregate pass rate
- Average evaluation score

The evaluation layer is intentionally separated from the production agents so that model behavior can be tested independently.

---

# Testing

Run schema tests:

```bash
python tests/test_schema.py
```

Run the Triage test:

```bash
python test_triage.py
```

Run the TAM test:

```bash
python test_tam.py
```

Run the complete evaluation:

```bash
python -m evaluation.run_eval
```

---

# API Documentation

Once FastAPI is running, open:

```text
http://127.0.0.1:8000/docs
```

Swagger UI provides an interactive interface for testing the available endpoints.

---

# Error Handling

The application handles common failure scenarios including:

- Missing ticket fields
- Invalid account IDs
- Invalid structured model responses
- Gemini API failures
- API connectivity errors
- Retrieval failures
- Invalid evaluation outputs

The Streamlit interface converts backend failures into user-readable messages.

---

# Gemini API Quota

Gemini API usage is subject to the quota and rate limits of the configured Google project and API key.

During development or evaluation, repeated model calls can exhaust free-tier request limits.

For this reason, generated predictions can be cached under:

```text
evaluation/predictions/
```

When the API quota is temporarily unavailable, previously generated prediction artifacts can be used for evaluation where applicable.

---

# Security

Never commit API keys or other secrets.

The following file should remain local:

```text
.env
```

The repository should contain:

```text
.env.example
```

with placeholder values only:

```env
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3.6-flash
```

Before pushing to GitHub, verify:

```bash
git status
```

and ensure `.env` is ignored.

---

# Production Considerations

For a production deployment, the following improvements could be added:

- Authentication and authorization
- API rate limiting
- Centralized logging
- Distributed vector storage
- Observability and tracing
- LLM cost monitoring
- Prompt versioning
- Automated regression testing
- Persistent conversation history
- Secrets management
- Background processing for long-running TAM workflows
- Model fallback strategies
- Response caching

---

# Design Decisions

## FastAPI

FastAPI provides a clean API boundary between the application logic and the user interface.

## Agent Separation

Triage and TAM functionality are implemented as separate agents with focused responsibilities.

## RAG

RAG grounds ticket classification and knowledge-base selection using retrieved organizational support information.

## Pydantic

Pydantic provides explicit contracts for model inputs and outputs.

## ChromaDB

ChromaDB provides vector storage for the indexed knowledge base and enables semantic retrieval.

## Streamlit

Streamlit provides a lightweight interface for demonstrating the AI workflows without requiring a separate frontend framework.

## Evaluation Layer

Evaluation is kept separate from production inference so model quality can be measured without coupling evaluation logic to the application API.

---

# End-to-End Workflow

## Ticket Triage

```text
Customer Ticket
      │
      ▼
FastAPI /triage
      │
      ▼
Triage Agent
      │
      ├──────────────► RAG Retriever
      │                     │
      │                     ▼
      │                ChromaDB
      │
      ▼
Gemini LLM
      │
      ▼
Pydantic Validation
      │
      ▼
Structured Triage Result
      │
      ▼
Support Response
```

## TAM Summary

```text
Account ID
    │
    ▼
FastAPI /tam/{account_id}
    │
    ▼
TAM Agent
    │
    ├── Account information
    ├── Usage information
    ├── Recent tickets
    └── Escalation information
    │
    ▼
Gemini
    │
    ▼
Pydantic Validation
    │
    ▼
Executive Account Summary
```

---

# Troubleshooting

## ModuleNotFoundError

Make sure the command is executed from the project root:

```text
support-ai-assistant/
```

For evaluation modules, use:

```bash
python -m evaluation.run_eval
```

instead of:

```bash
python evaluation/run_eval.py
```

## Gemini `429 RESOURCE_EXHAUSTED`

This indicates that the configured Gemini project/model has exceeded its available quota.

Check the configured API key and Google project quota.

Creating another key in the same project does not necessarily provide an independent quota.

## Gemini `503 UNAVAILABLE`

This indicates temporary model availability or demand issues.

Retry after some time rather than changing application logic.

## FastAPI Connection Error

Start the backend:

```bash
uvicorn app.main:app --reload
```

Then start Streamlit in another terminal:

```bash
streamlit run ui/app.py
```

## ChromaDB Deprecation Warning

A LangChain Chroma integration deprecation warning may appear during development.

If the application continues running, this warning does not indicate an application failure.

The integration can be migrated to the newer `langchain-chroma` package as a future dependency cleanup.

## Hugging Face Authentication Warning

The embedding model may display a warning when accessing the Hugging Face Hub without a token.

This does not necessarily prevent the embedding model from loading or the application from running.

---

# Submission Checklist

Before submitting the repository:

- [ ] Remove API keys and secrets
- [ ] Add `.env.example`
- [ ] Verify `.gitignore`
- [ ] Verify `requirements.txt`
- [ ] Remove temporary debug `print()` statements
- [ ] Verify README instructions
- [ ] Run FastAPI successfully
- [ ] Test `/triage`
- [ ] Test `/tam/{account_id}`
- [ ] Run Streamlit
- [ ] Run evaluation
- [ ] Verify evaluation report
- [ ] Verify generated prediction artifacts
- [ ] Remove unnecessary temporary files
- [ ] Remove unnecessary caches
- [ ] Check Git status
- [ ] Commit final changes
- [ ] Push to GitHub
- [ ] Verify the repository from a clean clone

---

# Final Verification

From the project root:

```bash
uvicorn app.main:app --reload
```

In another terminal:

```bash
streamlit run ui/app.py
```

Then verify:

```text
FastAPI:
http://127.0.0.1:8000/docs

Streamlit:
http://localhost:8501
```

Finally run:

```bash
python -m evaluation.run_eval
```

A successful evaluation should finish with:

```text
Evaluation completed.
```

---

# Project Status

The project currently includes:

- AI-powered ticket triage
- RAG-based knowledge retrieval
- Gemini structured generation
- Pydantic validation
- TAM account intelligence
- FastAPI backend
- Streamlit interface
- Automated evaluation
- Prediction generation
- Evaluation reporting
