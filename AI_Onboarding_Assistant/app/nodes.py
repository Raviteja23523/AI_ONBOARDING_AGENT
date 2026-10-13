from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

from .rag import build_retriever
from .state import State


load_dotenv()

VALID_ROLES = {"employee", "manager", "it_admin", "hr"}
VALID_CATEGORIES = {"information", "account_access", "unsupported"}

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.4,
)

retriever = build_retriever()


# 1. VALIDATION
def validate_node(state: State):
    if not state["question"].strip():
        return {
            "answer": "Question cannot be empty.",
            "query_type": "invalid",
        }

    if state["role"] not in VALID_ROLES:
        return {
            "answer": "Invalid user role.",
            "query_type": "invalid",
        }

    return {}


# 2. RETRIEVAL
def retrieve_node(state: State):
    documents = retriever.invoke(state["question"])

    return {
        "retrieved_context": [
            doc.page_content for doc in documents
        ],
        "citations": [
            Path(doc.metadata.get("source", "unknown")).name
            for doc in documents
        ],
    }


# 3. CLASSIFICATION
def classifier_node(state: State):
    question = state["question"]

    prompt = f"""
Classify this user request into exactly one category:

information
account_access
unsupported

information = questions seeking onboarding-related knowledge, guidance, or instructions.
Examples: how to set up a laptop, how to install software, company policies,
where to find documents, how benefits work, IT setup steps, general how-to questions
about onboarding.

account_access = requests to create, grant, enable, or request access to a system,
account, or tool (e.g. "give me VPN access", "create my email account").

unsupported = requests unrelated to onboarding entirely (e.g. personal advice,
unrelated topics, requests outside company processes).

If the question is a how-to or informational question related to onboarding,
even loosely, classify it as "information", not "unsupported".

Return only the category name.

Question: {question}
"""

    category = llm.invoke(prompt).content.strip().lower()

    if category not in VALID_CATEGORIES:
        category = "unsupported"

    result = {"query_type": category}

    if category == "unsupported":
        result["answer"] = (
            "This request is outside the scope of onboarding support. "
            "Please contact HR or IT directly."
        )

    return result


# 4. GROUNDING CHECK
def grounding_node(state: State):
    if not state.get("retrieved_context", []):
        return {
            "answer": (
                "I don't have enough information in the approved "
                "documents to answer that."
            )
        }

    return {}


# 5. ANSWER GENERATION
def generate_node(state: State):
    if state.get("answer"):
        return {}

    context = "\n\n".join(state["retrieved_context"])

    prompt = f"""
Answer the question using ONLY the context below.

If the answer is not in the context, say:
I don't have enough information to answer this.

Context:
{context}

Question:
{state["question"]}
"""

    answer = llm.invoke(prompt).content.strip()

    return {"answer": answer}


# 6. APPROVAL
def approval_node(state: State):
    status = state["approval_status"]

    if status == "approved":
        return {}

    message = (
        "Access rejected. No action was executed."
        if status == "rejected"
        else "Approval required. No action was executed."
    )

    return {"answer": message}


# 7. MOCK ACCESS TOOL
def access_tool_node(state: State):
    result = {
        "status": "success",
        "message": f"Mock VPN access requested for {state['role']}",
    }

    return {
        "tool_result": result,
        "answer": result["message"],
    }


# 8. FINAL RESPONSE
def final_node(state: State):
    answer = state["answer"]

    if state.get("query_type") == "information" and state["citations"]:
        answer += "\nSources: " + ", ".join(state["citations"])

    return {"answer": answer}