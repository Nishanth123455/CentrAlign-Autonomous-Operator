from app.tools.browser_tool import BrowserTool


def test_browser_recovery():
    browser = BrowserTool()

    try:
        browser.start()

        browser.fail_next_process = True

        first_result = browser.process_invoice(
            "INV1001",
            approval_granted=False,
        )

        print("First attempt:")
        print(first_result)

        second_result = browser.process_invoice(
            "INV1001",
            approval_granted=False,
        )

        print("\nSecond attempt:")
        print(second_result)

    finally:
        browser.close()


if __name__ == "__main__":
    test_browser_recovery()