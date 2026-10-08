from app.agent.understanding import TaskUnderstanding


def test_understanding():
    understanding = TaskUnderstanding()

    result = understanding.understand(
        "Process invoice INV1001 from Acme Supplies."
    )

    print("Understanding result:")
    print(result)


if __name__ == "__main__":
    test_understanding()