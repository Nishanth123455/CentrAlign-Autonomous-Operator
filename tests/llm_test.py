from app.models.llm_client import LLMClient


def test_llm():
    client = LLMClient()

    response = client.generate(
        "Reply with exactly: CentrAlign Gemini connection successful."
    )

    print(response)


if __name__ == "__main__":
    test_llm()