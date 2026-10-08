class ToolSelector:
    def select_tool(self, step):
        step_lower = step.lower()

        if "verify" in step_lower:
            return {
                "tool": "verify_invoice",
                "reason": "The step requires checking the invoice's final state."
            }

        if "process" in step_lower or "submit" in step_lower:
            return {
                "tool": "process_invoice",
                "reason": "The step requires submitting the invoice for processing."
            }

        if "vendor" in step_lower:
            return {
                "tool": "find_vendor",
                "reason": "The step requires checking the vendor record."
            }

        if "purchase order" in step_lower:
            return {
                "tool": "find_purchase_order",
                "reason": "The step requires checking the related purchase order."
            }

        if "policy" in step_lower or "approval" in step_lower:
            return {
                "tool": "search_policy",
                "reason": "The step requires checking company policy or approval rules."
            }

        if "invoice" in step_lower or "retrieve" in step_lower:
            return {
                "tool": "search_invoice",
                "reason": "The step requires retrieving invoice information."
            }

        return {
            "tool": None,
            "reason": "No available tool is required for this step."
        }