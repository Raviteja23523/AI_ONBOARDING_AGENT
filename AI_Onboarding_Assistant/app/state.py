from typing import TypedDict

class State(TypedDict):
    question: str
    role: str
    retrieved_context: list
    citations: list
    query_type: str
    answer: str
    approval_status: str
    tool_result: dict