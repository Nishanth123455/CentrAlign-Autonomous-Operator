from app.agent.audit import AuditTrail
from app.agent.state import TaskState


def test_audit_save():
    state = TaskState(
        request="Process invoice INV1001 from Acme Supplies."
    )

    state.completed_steps = [
        "Retrieve invoice details.",
        "Validate vendor information.",
        "Validate purchase order information.",
        "Process invoice.",
        "Verify final invoice status.",
    ]

    state.observations = [
        "Invoice was processed successfully.",
        "Final status was independently verified.",
    ]

    state.final_result = (
        "Invoice INV1001 was processed and independently verified."
    )

    state.completed = True

    invoice = {
        "invoice_id": "INV1001",
        "amount": "₹42000",
    }

    vendor = {
        "vendor_name": "Acme Supplies",
    }

    purchase_order = {
        "po_id": "PO1001",
    }

    policy_result = {
        "decision": "automatic",
        "reason": "Invoice satisfies all automatic processing requirements.",
    }

    verification = {
        "invoice_id": "INV1001",
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

    file_path = audit.save_report(report)

    print("Audit report saved to:")
    print(file_path)

    print("\nAudit report:")
    print(report)


if __name__ == "__main__":
    test_audit_save()