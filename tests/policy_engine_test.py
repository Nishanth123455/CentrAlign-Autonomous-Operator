from app.agent.policy_engine import InvoicePolicyEngine
from app.tools.company_data_tool import CompanyDataTool


def test_policy_engine():
    data = CompanyDataTool()
    engine = InvoicePolicyEngine()

    for invoice_id in ["INV1001", "INV1002", "INV1004"]:
        invoice = data.find_invoice(invoice_id)

        vendor = None
        purchase_order = None

        if invoice:
            vendor = data.find_vendor(invoice["vendor_id"])
            purchase_order = data.find_purchase_order(invoice["po_id"])

        result = engine.evaluate(
            invoice=invoice,
            vendor=vendor,
            purchase_order=purchase_order,
        )

        print(f"{invoice_id}:")
        print(result)
        print()


if __name__ == "__main__":
    test_policy_engine()