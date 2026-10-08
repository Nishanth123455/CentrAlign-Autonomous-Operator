from app.agent.agent import AutonomousAgent


def test_agent():
    agent = AutonomousAgent()

    state = agent.run(
        "Process invoice INV1001 from Acme Supplies."
    )

    print("Goal:")
    print(state.goal)

    print("\nPlan:")
    for step in state.plan:
        print(f"- {step}")

    print("\nCompleted steps:")
    for step in state.completed_steps:
        print(f"- {step}")

    print("\nObservations:")
    for observation in state.observations:
        print(f"- {observation}")

    print("\nFinal result:")
    print(state.final_result)

    print("\nCompleted:")
    print(state.completed)


if __name__ == "__main__":
    test_agent()