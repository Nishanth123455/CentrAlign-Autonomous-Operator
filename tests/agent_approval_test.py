from app.agent.agent import AutonomousAgent


def test_human_approval():
    agent = AutonomousAgent()

    state = agent.run(
        "Process invoice INV1002 from TechNova Systems."
    )

    print("Goal:")
    print(state.goal)

    print("\nFinal result:")
    print(state.final_result)

    print("\nAwaiting human approval:")
    print(state.awaiting_human)

    print("\nCompleted:")
    print(state.completed)

    print("\nObservations:")
    for observation in state.observations:
        print(f"- {observation}")


if __name__ == "__main__":
    test_human_approval()