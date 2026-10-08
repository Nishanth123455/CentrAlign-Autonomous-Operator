from app.agent.agent import AutonomousAgent


def test_agent_resume():
    agent = AutonomousAgent()

    state = agent.run(
        "Process invoice INV1002 from TechNova Systems."
    )

    print("Initial state:")
    print("Awaiting human:", state.awaiting_human)
    print("Completed:", state.completed)
    print("Final result:", state.final_result)

    resumed_state = agent.resume_after_approval(
        state,
        approved=True,
    )

    print("\nAfter approval and resume:")
    print("Awaiting human:", resumed_state.awaiting_human)
    print("Completed:", resumed_state.completed)
    print("Final result:", resumed_state.final_result)

    print("\nObservations:")
    for observation in resumed_state.observations:
        print(f"- {observation}")

    print("\nAudit file:")
    print(resumed_state.audit_file)


if __name__ == "__main__":
    test_agent_resume()