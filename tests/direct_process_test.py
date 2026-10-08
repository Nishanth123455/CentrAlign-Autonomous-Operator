from app.tools.browser_tool import BrowserTool


def test_direct_process():
    browser = BrowserTool()

    try:
        browser.start()

        invoice = browser.search_invoice("INV1001")

        print("Before processing:")
        print(invoice)

        result = browser.process_invoice(
            "INV1001",
            approval_granted=False,
        )

        print("\nProcess result:")
        print(result)

        final_invoice = browser.search_invoice("INV1001")

        print("\nAfter processing:")
        print(final_invoice)

    finally:
        browser.close()


if __name__ == "__main__":
    test_direct_process()