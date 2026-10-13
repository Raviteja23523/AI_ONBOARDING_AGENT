from pathlib import Path
import os
import sys

import streamlit as st
from dotenv import load_dotenv


# --------------------------------------------------
# Paths and configuration
# --------------------------------------------------
APP_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = APP_DIR.parent if APP_DIR.name == "app" else APP_DIR
DATA_DIR = PROJECT_ROOT / "data"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

st.set_page_config(
    page_title="AI Onboarding Assistant",
    page_icon="🤖",
    layout="centered",
)

st.title("AI Onboarding Assistant")
st.caption("Ask questions about onboarding, IT setup, company policies, and account access.")

# --------------------------------------------------
# Check the knowledge base BEFORE importing graph.py.
# This prevents the empty-FAISS-index IndexError.
# --------------------------------------------------
md_files = sorted(DATA_DIR.glob("*.md")) if DATA_DIR.exists() else []
nonempty_files = []

for md_file in md_files:
    try:
        if md_file.read_text(encoding="utf-8").strip():
            nonempty_files.append(md_file)
    except OSError:
        pass

if not md_files or not nonempty_files:
    st.error("The onboarding knowledge base is missing or empty.")
    st.write(f"Expected folder: `{DATA_DIR}`")
    st.write("Add at least one non-empty `.md` file to the `data` folder, for example:")
    st.code(
        "AI_Onboarding_Assistant/\n"
        "├── data/\n"
        "│   └── onboarding_guide.md\n"
        "└── app/\n"
        "    ├── Streamlit_app.py\n"
        "    ├── graph.py\n"
        "    ├── nodes.py\n"
        "    ├── rag.py\n"
        "    └── state.py",
        language="text",
    )
    st.info("The current RAG code builds FAISS from these Markdown files. Without non-empty documents, it cannot create a searchable index.")
    st.stop()

if not os.getenv("GROQ_API_KEY"):
    st.error("GROQ_API_KEY was not found. Add it to the project's .env file.")
    st.code("GROQ_API_KEY=your_groq_api_key", language="text")
    st.stop()

# --------------------------------------------------
# Load the existing LangGraph workflow
# --------------------------------------------------
@st.cache_resource
def load_graph():
    from app.graph import build_graph
    return build_graph()

try:
    with st.spinner("Loading onboarding assistant..."):
        graph = load_graph()
except Exception as exc:
    st.error("The workflow could not be loaded.")
    with st.expander("Technical details"):
        st.code(f"{type(exc).__name__}: {exc}")
    st.stop()

# --------------------------------------------------
# Session state
# --------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_state" not in st.session_state:
    st.session_state.pending_state = None

# --------------------------------------------------
# Sidebar
# --------------------------------------------------
with st.sidebar:
    st.header("Settings")
    role = st.selectbox(
        "Your role",
        ["employee", "manager", "it_admin", "hr"],
        format_func=lambda value: {
            "employee": "Employee",
            "manager": "Manager",
            "it_admin": "IT Administrator",
            "hr": "HR",
        }[value],
    )

    st.caption(f"Knowledge files loaded: {len(nonempty_files)}")

    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.pending_state = None
        st.rerun()

# --------------------------------------------------
# Show chat history
# --------------------------------------------------
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --------------------------------------------------
# Approval controls
# --------------------------------------------------
if st.session_state.pending_state is not None:
    st.warning("This account-access request needs an approval decision.")
    approve_col, reject_col = st.columns(2)

    def finish_approval(status: str):
        state = dict(st.session_state.pending_state)
        state["approval_status"] = status
        state["query_type"] = "account_access"

        try:
            result = graph.invoke(state)
            answer = result.get("answer") or "No answer was generated."
            tool_result = result.get("tool_result")
            if tool_result:
                answer += f"\n\n**Tool result:** `{tool_result}`"
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as exc:
            st.session_state.messages.append(
                {"role": "assistant", "content": f"Request failed: {type(exc).__name__}: {exc}"}
            )
        finally:
            st.session_state.pending_state = None

        st.rerun()

    with approve_col:
        if st.button("Approve", type="primary", use_container_width=True):
            finish_approval("approved")

    with reject_col:
        if st.button("Reject", use_container_width=True):
            finish_approval("rejected")

# --------------------------------------------------
# Chat input
# --------------------------------------------------
question = st.chat_input("Ask an onboarding question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})

    state = {
        "question": question,
        "role": role,
        "retrieved_context": [],
        "citations": [],
        "query_type": "",
        "answer": "",
        "approval_status": "pending",
        "tool_result": {},
    }

    try:
        with st.spinner("Processing your question..."):
            result = graph.invoke(state)

        if result.get("query_type") == "account_access":
            st.session_state.pending_state = result
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": "**Approval required.** Please choose Approve or Reject above.",
                }
            )
        else:
            answer = result.get("answer") or "No answer was generated."
            tool_result = result.get("tool_result")
            if tool_result:
                answer += f"\n\n**Tool result:** `{tool_result}`"
            st.session_state.messages.append({"role": "assistant", "content": answer})

    except Exception as exc:
        st.session_state.messages.append(
            {"role": "assistant", "content": f"Request failed: {type(exc).__name__}: {exc}"}
        )

    st.rerun()
