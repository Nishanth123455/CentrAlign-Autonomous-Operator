from app.agent.approval import HumanApproval
from app.agent.audit import AuditTrail
from app.agent.observer import TaskObserver
from app.agent.planner import TaskPlanner
from app.agent.policy_engine import InvoicePolicyEngine
from app.agent.recovery import TaskRecovery
from app.agent.state import TaskState
from app.agent.tool_executor import ToolExecutor
from app.agent.understanding import TaskUnderstanding
from app.retrieval.company_context import CompanyContext
from app.tools.company_data_tool import CompanyDataTool
from app.verification.verifier import InvoiceVerifier


class AutonomousAgent:
    def __init__(self):
        self.understanding = TaskUnderstanding()
        self.context = CompanyContext()
        self.planner = TaskPlanner()
        self.executor = ToolExecutor()
        self.observer = TaskObserver()
        self.verifier = InvoiceVerifier()
        self.company_data = CompanyDataTool()
        self.policy_engine = InvoicePolicyEngine()
        self.approval = HumanApproval()
        self.recovery = TaskRecovery()
        self.audit = AuditTrail()

    def _save_audit(
        self,
        state,
        invoice,
        vendor,
        purchase_order,
        policy_result,
        verification,
    ):
        report = self.audit.create_report(
            state=state,
            invoice=invoice,
            vendor=vendor,
            purchase_order=purchase_order,
            policy_result=policy_result,
            verification=verification,
        )

        state.audit_report = report
        state.audit_file = str(self.audit.save_report(report))

    def _process_and_verify(self, state):
        invoice = state.invoice
        vendor = state.vendor
        purchase_order = state.purchase_order
        policy_result = state.policy_result
        invoice_id = state.invoice_id

        process_result = self.executor.execute(
            tool_name="process_invoice",
            invoice_id=invoice_id,
            approval_granted=True,
        )

        if process_result.get("success") is False:
            recovery_result = self.recovery.recover(
                tool_name="process_invoice",
                result=process_result,
            )

            state.observations.append(
                f"Recovery decision: {recovery_result['action']} - "
                f"{recovery_result['reason']}"
            )

            if recovery_result["action"] == "retry":
                process_result = self.executor.execute(
                    tool_name="process_invoice",
                    invoice_id=invoice_id,
                    approval_granted=True,
                )

            elif recovery_result["action"] == "request_human":
                state.awaiting_human = True
                state.final_result = recovery_result["reason"]

                self._save_audit(
                    state=state,
                    invoice=invoice,
                    vendor=vendor,
                    purchase_order=purchase_order,
                    policy_result=policy_result,
                    verification=None,
                )

                return state

            else:
                state.errors.append(recovery_result["reason"])
                state.final_result = (
                    f"Invoice {invoice_id} could not be processed."
                )

                self._save_audit(
                    state=state,
                    invoice=invoice,
                    vendor=vendor,
                    purchase_order=purchase_order,
                    policy_result=policy_result,
                    verification=None,
                )

                return state

        if process_result.get("success") is False:
            state.observations.append(
                "Processing response was unsuccessful. "
                "Re-checking the finance portal to reconcile the actual state."
            )

            verification = self.verifier.verify(
                invoice_id=invoice_id,
                expected_status="processed",
            )

            state.observations.append(
                f"Recovery verification result: {verification}"
            )

            if verification["verified"]:
                state.completed_steps.append(
                    "Reconcile processing result."
                )
                state.completed_steps.append(
                    "Verify final invoice status."
                )
                state.completed = True
                state.awaiting_human = False
                state.final_result = (
                    f"Invoice {invoice_id} was processed and independently "
                    f"verified after recovery."
                )

                self._save_audit(
                    state=state,
                    invoice=invoice,
                    vendor=vendor,
                    purchase_order=purchase_order,
                    policy_result=policy_result,
                    verification=verification,
                )

                return state

            state.errors.append(
                process_result.get(
                    "message",
                    "Processing failed after recovery.",
                )
            )

            state.final_result = (
                f"Invoice {invoice_id} could not be processed after recovery."
            )

            self._save_audit(
                state=state,
                invoice=invoice,
                vendor=vendor,
                purchase_order=purchase_order,
                policy_result=policy_result,
                verification=verification,
            )

            return state

        state.completed_steps.append("Process invoice.")

        process_observation = self.observer.observe(
            step="Process invoice.",
            result=process_result,
        )

        state.observations.append(process_observation["observation"])

        verification = self.verifier.verify(
            invoice_id=invoice_id,
            expected_status="processed",
        )

        state.completed_steps.append("Verify final invoice status.")

        state.observations.append(
            f"Independent verification result: {verification}"
        )

        if verification["verified"]:
            state.completed = True
            state.awaiting_human = False
            state.final_result = (
                f"Invoice {invoice_id} was processed and independently verified."
            )
        else:
            state.errors.append(
                "Final invoice status did not match the expected processed state."
            )
            state.final_result = (
                f"Invoice {invoice_id} could not be verified as processed."
            )

        self._save_audit(
            state=state,
            invoice=invoice,
            vendor=vendor,
            purchase_order=purchase_order,
            policy_result=policy_result,
            verification=verification,
        )

        return state

    def run(self, request, approval_granted=False):
        state = TaskState(request=request)

        understanding = self.understanding.understand(request)

        state.goal = understanding["goal"]
        state.invoice_id = understanding["invoice_id"]

        invoice_id = state.invoice_id

        if not invoice_id:
            state.errors.append("No invoice ID was found in the request.")
            state.final_result = "Could not identify an invoice."

            self._save_audit(
                state=state,
                invoice=None,
                vendor=None,
                purchase_order=None,
                policy_result=None,
                verification=None,
            )

            return state

        policies = self.context.search("invoice")

        state.plan = self.planner.create_plan(
            goal=state.goal,
            invoice_id=invoice_id,
            context=policies,
        )

        invoice = self.executor.execute(
            tool_name="search_invoice",
            invoice_id=invoice_id,
        )

        if not invoice:
            state.errors.append("Invoice could not be retrieved.")
            state.final_result = f"Could not retrieve invoice {invoice_id}."

            self._save_audit(
                state=state,
                invoice=None,
                vendor=None,
                purchase_order=None,
                policy_result=None,
                verification=None,
            )

            return state

        state.invoice = invoice
        state.completed_steps.append("Retrieve invoice details.")

        observation = self.observer.observe(
            step="Retrieve invoice details.",
            result=invoice,
        )

        state.observations.append(observation["observation"])

        vendor = self.company_data.find_vendor(invoice["vendor_id"])
        state.vendor = vendor or {}

        state.completed_steps.append("Validate vendor information.")

        if vendor:
            state.observations.append(
                f"Vendor {vendor['vendor_name']} has status {vendor['status']}."
            )
        else:
            state.observations.append("Vendor could not be found.")

        purchase_order = self.company_data.find_purchase_order(
            invoice["purchase_order"]
        )
        state.purchase_order = purchase_order or {}

        state.completed_steps.append("Validate purchase order information.")

        if purchase_order:
            state.observations.append(
                f"Purchase order {purchase_order['po_id']} "
                f"has approved amount ₹{purchase_order['amount']}."
            )
        else:
            state.observations.append("Purchase order could not be found.")

        policy_result = self.policy_engine.evaluate(
            invoice=invoice,
            vendor=vendor,
            purchase_order=purchase_order,
        )

        state.policy_result = policy_result

        state.observations.append(
            f"Policy decision: {policy_result['decision']} - "
            f"{policy_result['reason']}"
        )

        if policy_result["decision"] == "blocked":
            state.final_result = (
                f"Invoice {invoice_id} cannot be processed. "
                f"{policy_result['reason']}"
            )

            self._save_audit(
                state=state,
                invoice=invoice,
                vendor=vendor,
                purchase_order=purchase_order,
                policy_result=policy_result,
                verification=None,
            )

            return state

        if policy_result["decision"] == "human_approval":
            approval_request = self.approval.request(
                invoice_id=invoice_id,
                reason=policy_result["reason"],
                vendor=vendor["vendor_name"] if vendor else "Unknown",
                amount=invoice["amount"],
            )

            state.approval_request = approval_request

            if not approval_granted:
                state.awaiting_human = True
                state.final_result = (
                    f"Human approval required for invoice {invoice_id}. "
                    f"{policy_result['reason']}"
                )

                self._save_audit(
                    state=state,
                    invoice=invoice,
                    vendor=vendor,
                    purchase_order=purchase_order,
                    policy_result=policy_result,
                    verification=None,
                )

                return state

            approved_request = self.approval.approve(approval_request)
            state.approval_request = approved_request

            state.observations.append(
                f"Human approval received for invoice {invoice_id}."
            )

        return self._process_and_verify(state)

    def resume_after_approval(self, state, approved):
        if not state.awaiting_human:
            raise ValueError("The task is not waiting for human approval.")

        if not approved:
            state.approval_request["approved"] = False
            state.approval_request["status"] = "rejected"
            state.awaiting_human = False
            state.completed = False
            state.final_result = (
                f"Human approval was rejected for invoice {state.invoice_id}."
            )

            state.observations.append(
                f"Human approval rejected for invoice {state.invoice_id}."
            )

            self._save_audit(
                state=state,
                invoice=state.invoice,
                vendor=state.vendor,
                purchase_order=state.purchase_order,
                policy_result=state.policy_result,
                verification=None,
            )

            return state

        state.approval_request = self.approval.approve(
            state.approval_request
        )

        state.observations.append(
            f"Human approval received for invoice {state.invoice_id}."
        )

        state.awaiting_human = False

        return self._process_and_verify(state)