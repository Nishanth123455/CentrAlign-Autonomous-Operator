from app.agent.agent import AutonomousAgent


def test_agent_recovery():
    agent = AutonomousAgent()

    agent.executor.browser.fail_next_process = True

    state = agent.run(
        "Process invoice INV1001 from Acme Supplies."
    )

    print("Goal:")
    print(state.goal)

    print("\nObservations:")
    for observation in state.observations:
        print(f"- {observation}")

    print("\nErrors:")
    print(state.errors)

    print("\nFinal result:")
    print(state.final_result)

    print("\nCompleted:")
    print(state.completed)


if __name__ == "__main__":
    test_agent_recovery()