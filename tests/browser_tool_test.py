from app.tools.browser_tool import BrowserTool


def test_browser_tool():
    browser = BrowserTool()

    try:
        browser.start()

        invoice = browser.search_invoice("INV1001")

        print("Invoice details:")
        print(invoice)

    finally:
        browser.close()


if __name__ == "__main__":
    test_browser_tool()