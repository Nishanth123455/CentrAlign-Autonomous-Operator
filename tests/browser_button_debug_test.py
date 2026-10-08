from app.tools.browser_tool import BrowserTool


def test_button_debug():
    browser = BrowserTool()

    try:
        browser.start()
        browser.search_invoice("INV1001")

        button_count = browser.page.locator("#process_invoice_button").count()

        print("Process button count:")
        print(button_count)

        print("\nCurrent URL:")
        print(browser.page.url)

        print("\nPage text:")
        print(browser.page.locator("body").inner_text())

    finally:
        browser.close()


if __name__ == "__main__":
    test_button_debug()