from app.agent.planner import TaskPlanner
from app.retrieval.company_context import CompanyContext


def test_planner():
    context = CompanyContext()

    policies = context.search("invoice")

    planner = TaskPlanner()

    result = planner.create_plan(
        goal="Process invoice from Acme Supplies",
        invoice_id="INV1001",
        context=policies,
    )

    print("Generated plan:")

    for step in result:
        print(f"- {step}")


if __name__ == "__main__":
    test_planner()