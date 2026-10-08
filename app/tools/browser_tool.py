from playwright.sync_api import sync_playwright


class BrowserTool:
    def __init__(self, base_url="http://127.0.0.1:5000"):
        self.base_url = base_url
        self.playwright = None
        self.browser = None
        self.page = None
        self.fail_next_process = False

    def start(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(headless=False)
        self.page = self.browser.new_page()
        self.page.goto(self.base_url)

    def search_invoice(self, invoice_id):
        self.page.goto(f"{self.base_url}?invoice_id={invoice_id}")
        self.page.wait_for_selector("#invoice_details")

        return {
            "invoice_id": self.page.locator("#invoice_id_value").inner_text(),
            "vendor_id": self.page.locator("#vendor_id").inner_text(),
            "purchase_order": self.page.locator("#purchase_order").inner_text(),
            "description": self.page.locator("#description").inner_text(),
            "amount": self.page.locator("#invoice_amount").inner_text(),
            "status": self.page.locator("#invoice_status").inner_text(),
        }

    def process_invoice(self, invoice_id, approval_granted=False):
        if self.fail_next_process:
            self.fail_next_process = False

            return {
                "success": False,
                "message": "Temporary browser failure.",
            }

        self.search_invoice(invoice_id)

        process_button = self.page.locator("#process_invoice_button")

        if process_button.count() == 0:
            return {
                "success": False,
                "message": "Process Invoice button was not found.",
            }

        self.page.locator("#approval_granted").evaluate(
            """(element, value) => {
                element.value = value;
            }""",
            "true" if approval_granted else "false",
        )

        with self.page.expect_navigation():
            process_button.click()

        result = self.page.locator("body").inner_text()

        return {
            "success": "processed successfully" in result.lower(),
            "message": result,
        }

    def close(self):
        if self.browser:
            self.browser.close()

        if self.playwright:
            self.playwright.stop()