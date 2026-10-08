class InvoicePolicyEngine:
    def _amount(self, value):
        cleaned_value = str(value).replace("₹", "").replace(",", "").strip()
        return float(cleaned_value)

    def evaluate(self, invoice, vendor, purchase_order):
        if not invoice:
            return {
                "decision": "blocked",
                "reason": "Invoice could not be verified."
            }

        if invoice["status"] != "pending":
            return {
                "decision": "blocked",
                "reason": "Invoice is not pending and should not be processed again."
            }

        if not vendor:
            return {
                "decision": "human_approval",
                "reason": "Vendor could not be verified."
            }

        if vendor["status"] != "approved":
            return {
                "decision": "human_approval",
                "reason": "Vendor is not approved."
            }

        if not purchase_order:
            return {
                "decision": "human_approval",
                "reason": "Purchase order could not be verified."
            }

        if purchase_order["status"] != "approved":
            return {
                "decision": "human_approval",
                "reason": "Purchase order is not approved."
            }

        invoice_amount = self._amount(invoice["amount"])
        po_amount = self._amount(purchase_order["amount"])

        if invoice_amount != po_amount:
            return {
                "decision": "human_approval",
                "reason": "Invoice amount does not match the purchase order amount."
            }

        if invoice_amount > 50000:
            return {
                "decision": "human_approval",
                "reason": "Invoice amount exceeds the automatic processing limit of ₹50,000."
            }

        return {
            "decision": "automatic",
            "reason": "Invoice satisfies all automatic processing requirements."
        }