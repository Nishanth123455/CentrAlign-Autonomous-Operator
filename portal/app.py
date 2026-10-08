from pathlib import Path
import csv

from flask import Flask, render_template, request

app = Flask(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
INVOICE_FILE = BASE_DIR / "company" / "data" / "invoice_records.csv"
VENDOR_FILE = BASE_DIR / "company" / "data" / "vendors.csv"
PO_FILE = BASE_DIR / "company" / "data" / "purchase_orders.csv"


def read_csv_file(file_path):
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def find_invoice(invoice_id):
    invoices = read_csv_file(INVOICE_FILE)

    for invoice in invoices:
        if invoice["invoice_id"].strip().upper() == invoice_id.strip().upper():
            return invoice

    return None


def find_vendor(vendor_id):
    vendors = read_csv_file(VENDOR_FILE)

    for vendor in vendors:
        if vendor["vendor_id"].strip() == vendor_id.strip():
            return vendor

    return None


def find_purchase_order(po_id):
    purchase_orders = read_csv_file(PO_FILE)

    for purchase_order in purchase_orders:
        if purchase_order["po_id"].strip() == po_id.strip():
            return purchase_order

    return None


def update_invoice_status(invoice_id, new_status):
    invoices = read_csv_file(INVOICE_FILE)

    for invoice in invoices:
        if invoice["invoice_id"].strip().upper() == invoice_id.strip().upper():
            invoice["status"] = new_status
            break

    with open(INVOICE_FILE, "w", newline="", encoding="utf-8") as file:
        fieldnames = [
            "invoice_id",
            "vendor_id",
            "po_id",
            "description",
            "amount",
            "status",
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(invoices)


@app.route("/")
def home():
    invoice_id = request.args.get("invoice_id", "").strip()

    invoice = None
    searched = False

    if invoice_id:
        searched = True
        invoice = find_invoice(invoice_id)

    return render_template(
        "index.html",
        invoice=invoice,
        searched=searched,
        invoice_id=invoice_id,
    )


@app.route("/process", methods=["POST"])
def process_invoice():
    invoice_id = request.form.get("invoice_id", "").strip()
    approval_granted = (
        request.form.get("approval_granted", "false").strip().lower() == "true"
    )

    invoice = find_invoice(invoice_id)

    if not invoice:
        return "Invoice not found", 404

    vendor = find_vendor(invoice["vendor_id"])
    purchase_order = find_purchase_order(invoice["po_id"])

    invoice_status = invoice["status"].strip().lower()

    if not vendor or vendor["status"].strip().lower() != "approved":
        if not approval_granted:
            return "Human approval required: vendor cannot be verified."

    if not purchase_order:
        if not approval_granted:
            return "Human approval required: purchase order cannot be verified."

    if invoice_status != "pending":
        return "Invoice cannot be processed because it is not pending."

    if purchase_order:
        invoice_amount = float(
            invoice["amount"].replace("₹", "").replace(",", "").strip()
        )
        po_amount = float(
            purchase_order["amount"].replace("₹", "").replace(",", "").strip()
        )

        if invoice_amount != po_amount and not approval_granted:
            return "Human approval required: invoice amount does not match purchase order."

    invoice_amount = float(
        invoice["amount"].replace("₹", "").replace(",", "").strip()
    )

    if invoice_amount > 50000 and not approval_granted:
        return "Human approval required: invoice exceeds the automatic processing limit."

    update_invoice_status(invoice_id, "processed")

    return f"Invoice {invoice_id} processed successfully."


if __name__ == "__main__":
    app.run(debug=True)