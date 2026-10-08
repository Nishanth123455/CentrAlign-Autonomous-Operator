from app.agent.agent import AutonomousAgent


def test_approval_resume():
    agent = AutonomousAgent()

    state = agent.run(
        "Process invoice INV1002 from TechNova Systems.",
        approval_granted=True,
    )

    print("Goal:")
    print(state.goal)

    print("\nApproval request:")
    print(state.approval_request)

    print("\nObservations:")
    for observation in state.observations:
        print(f"- {observation}")

    print("\nFinal result:")
    print(state.final_result)

    print("\nCompleted:")
    print(state.completed)


if __name__ == "__main__":
    test_approval_resume()