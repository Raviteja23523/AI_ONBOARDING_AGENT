from langgraph.graph import StateGraph, START, END

from .state import State

from .nodes import (
    validate_node,
    retrieve_node,
    grounding_node,
    classifier_node,
    generate_node,
    approval_node,
    access_tool_node,
    final_node
)

# CONDITIONAL ROUTING

def route_after_validation(state: State):

    if state.get("query_type") == "invalid":
        return "final"

    return "retrieve"

def route_after_classification(state: State):

    query_type = state.get(
        "query_type"
    )

    if query_type == "account_access":
        return "approval"

    if query_type == "information":
        return "grounding"

    return "final"

def route_after_approval(state: State):

    approval_status = state.get(
        "approval_status",
        "pending"
    )

    if approval_status == "approved":
        return "tool"

    return "final"

# BUILD GRAPH

def build_graph():

    graph = StateGraph(State)

    # Nodes

    graph.add_node("validate",validate_node)

    graph.add_node("retrieve",retrieve_node)

    graph.add_node("grounding",grounding_node)

    graph.add_node("classify",classifier_node)

    graph.add_node("generate",generate_node)

    graph.add_node("approval",approval_node)

    graph.add_node("tool",access_tool_node)

    graph.add_node("final",final_node)

    # START

    graph.add_edge(START,"validate")

    # Validation routing

    graph.add_conditional_edges("validate",
        route_after_validation,
        {
            "retrieve": "retrieve",
            "final": "final"
        }
    )

    # Retrieval

    graph.add_edge("retrieve","classify")

    # Classification routing

    graph.add_conditional_edges(
        "classify",
        route_after_classification,
        {
            "grounding": "grounding",
            "approval": "approval",
            "final": "final"
        }
    )

    # Grounding check (information queries only)

    graph.add_edge("grounding","generate")

    # Normal answer

    graph.add_edge("generate","final")

    # Approval routing

    graph.add_conditional_edges(
        "approval",
        route_after_approval,
        {
            "tool": "tool",
            "final": "final"
        }
    )

    # Tool

    graph.add_edge("tool","final")

    # End

    graph.add_edge("final",END)

    return graph.compile()