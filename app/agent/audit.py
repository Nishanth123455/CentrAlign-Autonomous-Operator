from datetime import datetime
import json
from pathlib import Path


class AuditTrail:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.audit_dir = self.base_dir / "company" / "data" / "audit"

        self.audit_dir.mkdir(parents=True, exist_ok=True)

    def create_report(
        self,
        state,
        invoice,
        vendor,
        purchase_order,
        policy_result,
        verification,
    ):
        return {
            "timestamp": datetime.now().isoformat(timespec="seconds"),
            "invoice_id": invoice["invoice_id"] if invoice else None,
            "vendor": vendor["vendor_name"] if vendor else None,
            "amount": invoice["amount"] if invoice else None,
            "purchase_order": purchase_order["po_id"] if purchase_order else None,
            "policy_decision": (
                policy_result["decision"] if policy_result else None
            ),
            "policy_reason": (
                policy_result["reason"] if policy_result else None
            ),
            "actions_performed": state.completed_steps,
            "human_approval": state.approval_request,
            "verification": verification,
            "observations": state.observations,
            "errors": state.errors,
            "final_result": state.final_result,
            "completed": state.completed,
        }

    def save_report(self, report):
        invoice_id = report.get("invoice_id", "unknown")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        file_path = self.audit_dir / f"{invoice_id}_{timestamp}.json"

        file_path.write_text(
            json.dumps(report, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

        return file_path 