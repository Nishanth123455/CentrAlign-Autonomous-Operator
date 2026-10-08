from app.agent.audit import AuditTrail
from app.agent.state import TaskState


def test_audit():
    state = TaskState(
        request="Process invoice INV1002 from TechNova Systems."
    )

    state.completed_steps = [
        "Retrieve invoice details.",
        "Validate vendor information.",
        "Validate purchase order information.",
        "Process invoice.",
        "Verify final invoice status.",
    ]

    state.final_result = (
        "Invoice INV1002 was processed and independently verified."
    )

    state.completed = True

    invoice = {
        "invoice_id": "INV1002",
        "amount": "₹68000",
    }

    vendor = {
        "vendor_name": "TechNova Systems",
    }

    purchase_order = {
        "po_id": "PO1002",
    }

    policy_result = {
        "decision": "human_approval",
        "reason": "Invoice exceeds the automatic processing limit.",
    }

    verification = {
        "invoice_id": "INV1002",
        "expected_status": "processed",
        "actual_status": "processed",
        "verified": True,
    }

    audit = AuditTrail()

    report = audit.create_report(
        state=state,
        invoice=invoice,
        vendor=vendor,
        purchase_order=purchase_order,
        policy_result=policy_result,
        verification=verification,
    )

    print("Audit report:")

    for key, value in report.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    test_audit()