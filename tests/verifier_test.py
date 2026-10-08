from app.verification.verifier import InvoiceVerifier


def test_verifier():
    verifier = InvoiceVerifier()

    result = verifier.verify(
        invoice_id="INV1001",
        expected_status="processed",
    )

    print("Verification result:")
    print(result)


if __name__ == "__main__":
    test_verifier()