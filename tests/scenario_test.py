from app.agent.agent import AutonomousAgent


def print_result(invoice_id, state):
    print(f"\n{'=' * 50}")
    print(f"Scenario: {invoice_id}")
    print(f"{'=' * 50}")

    print("Final result:")
    print(state.final_result)

    print("\nAwaiting human:")
    print(state.awaiting_human)

    print("\nCompleted:")
    print(state.completed)

    print("\nAudit file:")
    print(state.audit_file)


def test_scenarios():
    agent = AutonomousAgent()

    automatic_state = agent.run(
        "Process invoice INV1001 from Acme Supplies."
    )

    print_result("INV1001", automatic_state)

    approval_state = agent.run(
        "Process invoice INV1002 from TechNova Systems.",
        approval_granted=True,
    )

    print_result("INV1002", approval_state)

    blocked_state = agent.run(
        "Process invoice INV1004 from Acme Supplies."
    )

    print_result("INV1004", blocked_state)


if __name__ == "__main__":
    test_scenarios()