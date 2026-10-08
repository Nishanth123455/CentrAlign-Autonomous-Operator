import json

from app.models.llm_client import LLMClient


class TaskUnderstanding:
    def __init__(self):
        self.llm = LLMClient()

    def understand(self, request):
        prompt = f"""
You are the task understanding component of an autonomous company operator.

Analyze the user's request and extract the intended task.

Return only a JSON object.
Do not use markdown.
Do not use code fences.
Do not add any explanation.

The JSON must contain exactly these fields:
{{
    "goal": "short description of the intended outcome",
    "invoice_id": "invoice ID if present, otherwise null"
}}

User request:
{request}
"""

        response = self.llm.generate(prompt).strip()

        if response.startswith("```"):
            response = response.replace("```json", "")
            response = response.replace("```", "")
            response = response.strip()

        try:
            return json.loads(response)
        except json.JSONDecodeError:
            raise ValueError(f"The LLM returned invalid JSON: {response}")