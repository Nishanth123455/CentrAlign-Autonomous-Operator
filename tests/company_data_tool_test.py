from app.tools.company_data_tool import CompanyDataTool


def test_company_data_tool():
    data = CompanyDataTool()

    vendor = data.find_vendor("V001")
    purchase_order = data.find_purchase_order("PO1001")
    invoice = data.find_invoice("INV1001")

    print("Vendor:")
    print(vendor)

    print("\nPurchase Order:")
    print(purchase_order)

    print("\nInvoice:")
    print(invoice)


if __name__ == "__main__":
    test_company_data_tool()