from app.tools.browser_tool import BrowserTool


class InvoiceVerifier:
    def verify(self, invoice_id, expected_status):
        browser = BrowserTool()

        try:
            browser.start()
            invoice = browser.search_invoice(invoice_id)

            actual_status = invoice["status"]

            return {
                "invoice_id": invoice_id,
                "expected_status": expected_status,
                "actual_status": actual_status,
                "verified": actual_status == expected_status,
            }
        finally:
            browser.close() 