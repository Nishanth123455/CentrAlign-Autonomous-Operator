from app.agent.tool_selector import ToolSelector


def test_tool_selector():
    selector = ToolSelector()

    result = selector.select_tool(
        "Retrieve invoice details for INV1001 from Acme Supplies."
    )

    print("Selected tool:")
    print(result)


if __name__ == "__main__":
    test_tool_selector()