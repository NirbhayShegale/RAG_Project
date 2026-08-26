


# RAG AGENT

A reliable, multi-turn AI customer support agent built for **Aster & Row** (a fictional ecommerce brand selling bags, drinkware, and travel accessories). The system orchestrates document retrieval over policy knowledge bases and deterministic order lookups using **LangGraph**, **Qdrant**, **Cohere Reranker**, **Groq**, **FastAPI**, and **Streamlit**.

---

## 📺 Demonstration

https://github.com/user-attachments/assets/9c742f6f-11aa-43e4-9d39-2438b62ad654

---

## 🏗️ Architecture & Technology Choices

```
                        User Query
                            │
                            ▼
                  ┌───────────────────┐
                  │   Intent Router   │  (LLM Structured Classification)
                  └─────────┬─────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
    ┌───────────────────┐       ┌───────────────────┐
    │  OrderLookup Tool │       │  Retrieval Engine │
    │  (orders.json)    │       │  (HyDE + Hybrid)  │
    └─────────┬─────────┘       └─────────┬─────────┘
              │                           │
              │  PII Sanitized Context   │  Top-K Passages
              └─────────────┬─────────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │  RAG Agent Node   │  (Grounded System Prompt + Memory)
                  └─────────┬─────────┘
                            │
                            ▼
                      Final Response
```

### Core Stack

| Component | Choice | Rationale |
|---|---|---|
| **Orchestration** | **LangGraph (`StateGraph`)** | Cyclic graph workflow with state persistence (`MemorySaver`) for multi-turn session tracking and deterministic tool routing. |
| **Primary LLM** | **Groq (`openai/gpt-oss-120b`)** | Low-latency inference with zero temperature for reliable, reproducible, and hallucination-free generation. |
| **Embeddings** | **BAAI/bge-m3** (via HuggingFace Inference API) | 1024-dimensional dense representations optimized for multilingual and domain-specific semantic similarity. |
| **Retrieval & Reranking**| **Hybrid Search + HyDE + Cohere (`rerank-v3.5`)** | Combines dense vector search with sparse BM25 keyword matching, enhanced by Hypothetical Document Embeddings and Cohere reranker for cross-encoder precision. |
| **Vector Storage** | **Qdrant (Local Embedded DB)** | Embedded, high-performance vector database (`qdrant.db`) with in-memory option for isolation. |
| **API & UI** | **FastAPI + Streamlit** | Clean client-server separation; FastAPI manages session lifespans while Streamlit provides a simple customer chat interface. |

---

## 🚀 Setup and Run Instructions

### Prerequisites
- Python 3.12+
- `uv` (recommended) or standard `pip`

### 1. Clone the repository
```bash
git clone https://github.com/NirbhayShegale/RAG_Project.git
cd RAG_Project
```

### 2. Install dependencies

**Using `uv` (recommended):**
```bash
uv sync
```

**Using standard `pip` / `venv`:**
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

pip install -e .
```

### 3. Configure Environment Variables
Copy `.env.example` to `.env` and insert your API keys:
```bash
cp .env.example .env
```

`.env` content:
```env
GROQ_API_KEY=gsk_your_groq_key
HUGGINGFACEHUB_API_TOKEN=hf_your_huggingface_token
COHERE_API_KEY=your_cohere_key

# Optional settings
DEBUG_MODE=0
LANGSMITH_TRACING=false
```

### 4. Run the Application

**Start the FastAPI Backend:**
```bash
# Using uv:
uv run uvicorn API.api:app --reload --port 8000

# Or with activated venv:
uvicorn API.api:app --reload --port 8000
```

**Start the Streamlit UI (in a separate terminal):**
```bash
# Using uv:
uv run streamlit run Frontend/app.py

# Or with activated venv:
streamlit run Frontend/app.py
```
Access the chat UI at `http://localhost:8501`.

---

## 🧪 Evaluation

> **Note / Apology:**  I did not add the automated evaluation suite . All test cases in `evaluation/visible-cases.json` can be tested manually through the Streamlit UI or the FastAPI `/chat` endpoint.

---

## 📓 Bug Diary

### 1. LangGraph State Serialization Failure with `MemorySaver`
- **Symptom:** Graph invocations crashed with `TypeError: can't pickle / serialize QdrantVectorStore` when attempting multi-turn state persistence.
- **Root Cause:** Large, unpicklable objects (`vector_store`, `chunked_documents`) were placed inside `RAGState`. LangGraph's `MemorySaver` attempts to serialize all state fields with `msgpack`.
- **Fix:** Extracted runtime infrastructure objects out of `RAGState` and injected them per-turn via `RunnableConfig` (`config["configurable"]["vector_store"]`), keeping `RAGState` strictly serializable.
- **Regression Test:** Ran multi-turn conversation sessions ensuring state persistence across 5+ consecutive turns without serialization errors.

### 2. Hallucinated Order Status on Missing Order ID
- **Symptom:** When a user asked *"Where is my order?"* without providing an order ID, the agent previously routed to `order_lookup_tool_node` and returned random or invented order details.
- **Root Cause:** Lack of strict validation guardrails before tool invocation and missing-field prompting.
- **Fix:** Added Rule 5 in `RAG_Agent_prompt.py` enforcing that when no order ID is present, the agent must ask for the order ID explicitly before invoking lookups or referencing statuses.
- **Regression Test:** Evaluated case `missing-order-id`; verified that the agent asks for the order ID and makes zero tool calls.

### 3. Windows Terminal Character Encoding & Qdrant File Lock
- **Symptom:** Evaluation script threw `UnicodeEncodeError: 'charmap' codec can't encode character` and `RuntimeError: Storage folder qdrant.db is already accessed by another instance`.
- **Root Cause:** Windows default `cp1252` encoding failed on Unicode symbols (`→`, `✓`), and local Qdrant locks the disk folder, preventing concurrent eval execution alongside the running API.
- **Fix:** Added `sys.stdout.reconfigure(encoding="utf-8")` at script initialization, sanitized log strings to ASCII, and added an in-memory override (`QDRANT_EVAL_MODE=1`) for non-conflicting evaluation runs.
- **Regression Test:** Executed `eval.py` in concurrent terminals under Windows PowerShell without locks or encoding crashes.

---

## Known Limitations & Future Improvements

1. **Document Conflict Resolution:**
   - *Limitation:* Contradictory documents (e.g. current vs legacy returns policies) can both be retrieved if semantically similar.
   - *Production Improvement:* Implement metadata-based filtering to prioritize active documents (`status: active`) and deprecate superseded docs (`status: legacy`).
2. **Context Bloat:**
   - Retrieving documents for multiple sub-queries floods the LLM context window, causing "Lost in the Middle" hallucinations. 
---

## AI Assistance Disclosure

- **AI Tools Used:**
- Codex AI 
- Antigravity AI (Google DeepMind) for architectural scaffolding, LangGraph state graph wiring, prompt guardrail drafting, and evaluation harness design.
- **Example of an Incorrect AI Suggestion:**
  - *The Mistake:* An early AI-generated prompt suggested having the Router LLM return JSON containing the full order query string rather than classifying the target graph node enum.
  - *Why it was wrong:* It broke LangGraph's conditional routing edge, causing all queries to default to the RAG retrieval node.
  - *Correction:* Replaced it with a strict `PydanticOutputParser` enforcing `Literal["RAG_node", "order_lookup_tool_node"]`.

