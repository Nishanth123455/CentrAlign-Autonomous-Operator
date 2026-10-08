from app.retrieval.company_context import CompanyContext
from app.tools.browser_tool import BrowserTool
from app.tools.company_data_tool import CompanyDataTool


class ToolExecutor:
    def __init__(self):
        self.browser = BrowserTool()
        self.company_data = CompanyDataTool()
        self.company_context = CompanyContext()

    def execute(
        self,
        tool_name,
        invoice_id=None,
        vendor_id=None,
        po_id=None,
        keyword=None,
        approval_granted=False,
    ):
        if tool_name == "search_invoice":
            self.browser.start()

            try:
                return self.browser.search_invoice(invoice_id)
            finally:
                self.browser.close()

        if tool_name == "find_vendor":
            return self.company_data.find_vendor(vendor_id)

        if tool_name == "find_purchase_order":
            return self.company_data.find_purchase_order(po_id)

        if tool_name == "search_policy":
            return self.company_context.search(keyword)

        if tool_name == "process_invoice":
            self.browser.start()

            try:
                return self.browser.process_invoice(
                    invoice_id,
                    approval_granted=approval_granted,
                )
            finally:
                self.browser.close()

        if tool_name == "verify_invoice":
            self.browser.start()

            try:
                invoice = self.browser.search_invoice(invoice_id)

                return {
                    "invoice_id": invoice["invoice_id"],
                    "status": invoice["status"],
                }
            finally:
                self.browser.close()

        raise ValueError(f"Unknown tool: {tool_name}")