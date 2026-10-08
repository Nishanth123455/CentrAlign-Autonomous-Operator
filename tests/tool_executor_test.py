from app.agent.tool_executor import ToolExecutor


def test_tool_executor():
    executor = ToolExecutor()

    result = executor.execute(
        tool_name="search_invoice",
        invoice_id="INV1001",
    )

    print("Tool execution result:")
    print(result)


if __name__ == "__main__":
    test_tool_executor()