

<img width="1536" height="1024" alt="image" src="https://github.com/user-attachments/assets/6702847c-ace9-4cb6-a383-dea67e80009d" />
# AI Onboarding Assistant

A Retrieval-Augmented Generation (RAG) onboarding assistant built with **Python, LangGraph, LangChain, Groq, FAISS, Hugging Face Embeddings, and Streamlit**. It retrieves relevant information from approved onboarding documents and routes each request through a LangGraph workflow.

<!-- Replace the placeholder below with your deployed Streamlit app URL. -->
> **🚀 Live Demo:** [Open the AI Onboarding Assistant](YOUR_LIVE_APP_URL)

## Project Workflow

The application validates the user's question and role, retrieves relevant document chunks, and classifies the request using Groq:

- **Information:** check the retrieved context, generate a context-grounded response, and include source filenames when available.
- **Account access:** check approval status. If approved, run the project's mock VPN access tool; otherwise return without running the tool.
- **Unsupported:** return the configured fallback message.

Each path ends at the final response node.

## Key Features

- LangGraph workflow with conditional routing.
- RAG over approved Markdown files in `data/`.
- FAISS similarity search over embedded text chunks.
- Groq-powered request classification and response generation.
- Request categories: `information`, `account_access`, and `unsupported`.
- Input validation for the question and supported role.
- Source filenames included with information responses when available.
- Approval gate before the mock account-access action.
- Streamlit interface and command-line entry point.

## Tech Stack

| Component | Purpose |
|---|---|
| Python | Application logic |
| LangGraph | Workflow graph and conditional routing |
| LangChain | Document loading and LLM integration |
| Groq | Request classification and answer generation |
| Hugging Face Embeddings | Text embeddings using `sentence-transformers/all-MiniLM-L6-v2` |
| FAISS | Vector similarity search |
| Streamlit | Web interface |

## Repository Structure

```text
AI_Onboarding_Assistant/
├── app/
│   ├── __init__.py
│   ├── graph.py              # LangGraph workflow and routing
│   ├── main.py               # CLI entry point
│   ├── nodes.py              # Workflow node implementations
│   ├── rag.py                # Loading, chunking, embeddings and FAISS retrieval
│   ├── state.py              # Shared LangGraph state
│   └── Streamlit_app.py      # Streamlit UI
├── data/
│   ├── onboarding_guide.md
│   ├── product_faq.md
│   ├── security_policy.md
│   └── support_escalation_guide.md
├── tests/                    # Test folder
├── .env                      # Local secrets; do not commit
├── project-flowchart.png     # README workflow diagram
└── README.md
```

## How the Workflow Works

1. **Validate** — Rejects an empty question or an unsupported role (`employee`, `manager`, `it_admin`, or `hr`).
2. **Retrieve** — Loads `.md` documents from `data/`, splits them into chunks, and retrieves the top four matches using FAISS.
3. **Classify** — Uses the configured Groq chat model to classify the request.
4. **Information path** — Checks whether retrieved context exists, then generates an answer from that context.
5. **Account-access path** — Checks `approval_status`. The tool node runs only when the status is `approved`.
6. **Unsupported path** — Returns the app's fallback response.
7. **Final** — Returns the answer and any available sources or mock tool result.

### RAG Configuration

The current settings in `app/rag.py` are:

- **Embedding model:** `sentence-transformers/all-MiniLM-L6-v2`
- **Chunk size:** `800`
- **Chunk overlap:** `100`
- **Retriever results:** `k=4`
- **Vector index:** built in memory when the retriever is initialized

## Getting Started

### Prerequisites

- Python installed
- A Groq API key
- Internet connection for Groq requests and the initial embedding-model download

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd AI_Onboarding_Assistant
```

Replace `YOUR_GITHUB_REPOSITORY_URL` with your repository URL. If you already downloaded the project, open a terminal in the project root instead.

### 2. Create a virtual environment (recommended)

**Windows PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

If your repository contains `requirements.txt`:

```bash
pip install -r requirements.txt
```

If it does not, install the packages used by the current implementation:

```bash
pip install streamlit langgraph langchain-core langchain-community langchain-text-splitters langchain-groq langchain-huggingface sentence-transformers faiss-cpu python-dotenv
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

In `app/nodes.py`, confirm that the `ChatGroq` model ID is available to your Groq account. Model availability and rate limits can change. Never hard-code an API key in Python files or commit `.env` to GitHub.

### 5. Run the app

Run commands from the repository root.

**Streamlit UI:**

```bash
python -m streamlit run app/Streamlit_app.py
```

**CLI:**

```bash
python -m app.main
```

For the CLI, enter a question and role when prompted. Type `exit` to quit if supported by your current CLI loop.

## Example Questions

Questions based on the included knowledge documents:

- How do I set up my company laptop?
- What should I do on my first day?
- Who should I contact if my account activation fails?
- What information should I include in a support request?
- When should an issue be escalated to IT support?
- What details should a VPN access request include?
- What should I do if I suspect my credentials were exposed?
- What is the onboarding portal used for?
- I need VPN access.

## Testing Checklist

Use these scenarios to verify the workflow:

| Scenario | Expected behavior |
|---|---|
| Information question supported by documents | Answer based on retrieved context and include sources where available |
| Account access with `approved` status | Mock tool runs and returns a simulated result |
| Account access with `rejected` status | Tool does not run |
| Account access with `pending` status | Tool does not run |
| Unsupported question | Configured fallback response |
| Empty question | Validation error response |
| Invalid role | Validation error response |

LLM classification is not deterministic, so test results can vary by prompt, model, and retrieved context.

## Security and Limitations

- **Mock access only:** the VPN tool simulates an access request. It does not grant real VPN access or modify any external system.
- **Role checks:** the current implementation validates role names but does not implement a complete role-based authorization system.
- **Grounding:** the grounding node checks whether context is available; it does not independently prove that every generated claim is entailed by the retrieved text.
- **Citations:** sources are document filenames, not page-level citations.
- **Index persistence:** the FAISS index is built in memory and is not persisted by the current RAG code.
- **Secrets:** never commit `.env` or expose API keys, passwords, tokens, or private keys.
- **Production readiness:** real account-access workflows should use trusted authorization, audit logging, error handling, and secure integrations.

## Contributing

1. Create a feature branch.
2. Make changes and test the workflow locally.
3. Open a pull request describing the change and test results.

## License

No license file was included in the project structure shown. Add a `LICENSE` file before distributing the repository under an open-source license.

