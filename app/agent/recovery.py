class TaskRecovery:
    def recover(self, tool_name, result):
        if not result:
            return {
                "recoverable": True,
                "action": "retry",
                "reason": "The tool returned no result."
            }

        if isinstance(result, dict):
            if result.get("success") is False:
                message = result.get("message", "")

                if "not found" in message.lower():
                    return {
                        "recoverable": False,
                        "action": "stop",
                        "reason": "The requested resource could not be found."
                    }

                if "human approval required" in message.lower():
                    return {
                        "recoverable": False,
                        "action": "request_human",
                        "reason": message
                    }

                return {
                    "recoverable": True,
                    "action": "retry",
                    "reason": "The tool action did not succeed."
                }

        return {
            "recoverable": False,
            "action": "continue",
            "reason": "No recovery action is required."
        } 