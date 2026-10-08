import json

from app.models.llm_client import LLMClient


class TaskPlanner:
    def __init__(self):
        self.llm = LLMClient()

    def create_plan(self, goal, invoice_id, context):
        prompt = f"""
You are the planning component of an autonomous company operator.

Create a practical plan for completing the user's task.

The plan must use the available company context and should not invent
systems, data, or actions that are not supported by the context.

Return only valid JSON.
Do not use markdown or code fences.

Return this structure:
{{
    "plan": [
        "step 1",
        "step 2",
        "step 3"
    ]
}}

Task goal:
{goal}

Invoice ID:
{invoice_id}

Company context:
{context}
"""

        response = self.llm.generate(prompt).strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        try:
            result = json.loads(response)
        except json.JSONDecodeError:
            raise ValueError(f"The LLM returned invalid JSON: {response}")

        if "plan" not in result or not isinstance(result["plan"], list):
            raise ValueError("The LLM returned an invalid plan.")

        return result["plan"] 