from app.agent.approval import HumanApproval


def test_approval():
    approval = HumanApproval()

    request = approval.request(
        invoice_id="INV1002",
        reason="Invoice amount exceeds the automatic processing limit.",
        vendor="TechNova Systems",
        amount="₹68000",
    )

    print("Approval request:")
    print(request)

    approved_request = approval.approve(request)

    print("\nAfter human approval:")
    print(approved_request)


if __name__ == "__main__":
    test_approval()