class HumanApproval:
    def request(self, invoice_id, reason, vendor, amount):
        return {
            "status": "awaiting_approval",
            "invoice_id": invoice_id,
            "vendor": vendor,
            "amount": amount,
            "reason": reason,
            "approved": False,
        }

    def approve(self, approval_request):
        approval_request["approved"] = True
        approval_request["status"] = "approved"
        return approval_request 