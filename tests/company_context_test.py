from app.retrieval.company_context import CompanyContext


def test_company_context():
    context = CompanyContext()

    results = context.search("approval")

    print(f"Results found: {len(results)}")

    for result in results:
        print(f"\nSource: {result['source']}")
        print(result["content"])


if __name__ == "__main__":
    test_company_context()