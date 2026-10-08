from pathlib import Path
import csv


class CompanyDataTool:
    def __init__(self):
        self.base_dir = Path(__file__).resolve().parent.parent.parent
        self.data_dir = self.base_dir / "company" / "data"

    def _read_csv(self, file_name):
        file_path = self.data_dir / file_name

        with open(file_path, "r", newline="", encoding="utf-8") as file:
            return list(csv.DictReader(file))

    def find_vendor(self, vendor_id):
        vendors = self._read_csv("vendors.csv")

        for vendor in vendors:
            if vendor["vendor_id"] == vendor_id:
                return vendor

        return None

    def find_purchase_order(self, po_id):
        purchase_orders = self._read_csv("purchase_orders.csv")

        for purchase_order in purchase_orders:
            if purchase_order["po_id"] == po_id:
                return purchase_order

        return None

    def find_invoice(self, invoice_id):
        invoices = self._read_csv("invoice_records.csv")

        for invoice in invoices:
            if invoice["invoice_id"].upper() == invoice_id.upper():
                return invoice

        return None 