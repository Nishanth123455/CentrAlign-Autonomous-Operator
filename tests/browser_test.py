from playwright.sync_api import sync_playwright


def test_invoice_processing():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("http://127.0.0.1:5000")
        page.locator("#invoice_id").fill("INV1001")
        page.locator("#search_button").click()

        invoice_id = page.locator("#invoice_id_value").inner_text()
        initial_status = page.locator("#invoice_status").inner_text()

        print(f"Invoice: {invoice_id}")
        print(f"Initial status: {initial_status}")

        page.locator("#process_invoice_button").click()

        result = page.locator("body").inner_text()
        print(f"Action result: {result}")

        page.goto("http://127.0.0.1:5000?invoice_id=INV1001")

        final_status = page.locator("#invoice_status").inner_text()
        print(f"Verified status: {final_status}")

        browser.close()


if __name__ == "__main__":
    test_invoice_processing()