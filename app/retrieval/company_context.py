from pathlib import Path


class CompanyContext:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.policies_dir = self.base_dir / "company" / "policies"

    def get_policies(self):
        policies = {}

        for file_path in self.policies_dir.glob("*.txt"):
            policies[file_path.name] = file_path.read_text(encoding="utf-8")

        return policies

    def search(self, keyword):
        results = []

        for file_name, content in self.get_policies().items():
            if keyword.lower() in content.lower():
                results.append({
                    "source": file_name,
                    "content": content,
                })

        return results 