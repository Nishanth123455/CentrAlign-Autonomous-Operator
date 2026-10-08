from dataclasses import dataclass, field


@dataclass
class TaskState:
    request: str
    goal: str = ""
    invoice_id: str = ""
    plan: list[str] = field(default_factory=list)
    completed_steps: list[str] = field(default_factory=list)
    observations: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)
    awaiting_human: bool = False
    approval_request: dict = field(default_factory=dict)
    audit_report: dict = field(default_factory=dict)
    audit_file: str = ""
    invoice: dict = field(default_factory=dict)
    vendor: dict = field(default_factory=dict)
    purchase_order: dict = field(default_factory=dict)
    policy_result: dict = field(default_factory=dict)
    completed: bool = False
    final_result: str = ""