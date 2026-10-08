from app.agent.recovery import TaskRecovery


def test_recovery():
    recovery = TaskRecovery()

    failed_result = {
        "success": False,
        "message": "Temporary browser failure."
    }

    result = recovery.recover(
        tool_name="process_invoice",
        result=failed_result,
    )

    print("Recovery result:")
    print(result)


if __name__ == "__main__":
    test_recovery()