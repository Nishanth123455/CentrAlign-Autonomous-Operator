class TaskObserver:
    def observe(self, step, result):
        if result is None:
            return {
                "observation": "No tool result was returned.",
                "status": "blocked",
                "next_action": "request human approval",
            }

        if isinstance(result, dict):
            if result.get("success") is False:
                message = result.get("message", "")

                if "human approval required" in message.lower():
                    return {
                        "observation": message,
                        "status": "blocked",
                        "next_action": "request human approval",
                    }

                return {
                    "observation": message,
                    "status": "needs_action",
                    "next_action": "retrieve more information",
                }

            if result.get("verified") is True:
                return {
                    "observation": "The final invoice state matches the expected state.",
                    "status": "success",
                    "next_action": "complete the task",
                }

            if result.get("status") == "processed":
                return {
                    "observation": "The invoice is currently processed.",
                    "status": "success",
                    "next_action": "verify the invoice",
                }

            if result.get("status") == "pending":
                return {
                    "observation": "The invoice is currently pending.",
                    "status": "success",
                    "next_action": "continue the plan",
                }

        return {
            "observation": "The tool action completed successfully.",
            "status": "success",
            "next_action": "continue the plan",
        }