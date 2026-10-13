from .graph import build_graph

VALID_ROLES = ["employee", "manager", "it_admin", "hr"]


def main():
    graph = build_graph()
    role_prompt = f"Role ({'/'.join(VALID_ROLES)}): "

    while True:
        question = input("\nQuestion: ").strip()

        if question.lower() == "exit":
            break

        role = input(role_prompt).strip().lower()

        # Initial workflow state
        state = {
            "question": question,
            "role": role,
            "retrieved_context": [],
            "citations": [],
            "query_type": "",
            "answer": "",
            "approval_status": "pending",
            "tool_result": {}
        }

        # Run the graph
        result = graph.invoke(state)

        # Ask for approval if account access is requested
        if result.get("query_type") == "account_access":
            approval = input(
                "Approval (approved/rejected): "
            ).strip().lower()

            state["approval_status"] = approval
            state["query_type"] = "account_access"

            # Runs the complete graph again
            result = graph.invoke(state)

        # Display the final answer
        answer = result.get("answer") or "No answer was generated."
        print("\nAnswer:", answer)

        # Display the mock tool result if available
        tool_result = result.get("tool_result")

        if tool_result:
            print("Tool result:", tool_result)


if __name__ == "__main__":
    main()