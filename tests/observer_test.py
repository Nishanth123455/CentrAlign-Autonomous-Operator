from app.agent.observer import TaskObserver


def test_observer():
    observer = TaskObserver()

    result = observer.observe(
        step="Retrieve invoice details for INV1001.",
        result={
            "invoice_id": "INV1001",
            "vendor_id": "V001",
            "purchase_order": "PO1001",
            "description": "Office laptops and accessories",
            "amount": "₹42000",
            "status": "processed",
        },
    )

    print("Observation result:")
    print(result)


if __name__ == "__main__":
    test_observer()