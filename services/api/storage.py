# temporary in-memory storage for Week 1; replace with Postgres later
from typing import Dict
from .models import Invoice


_DB: Dict[str, Invoice] = {}


def save_invoice(inv: Invoice) -> None:
    _DB[inv.invoice_id] = inv


def get_invoice(invoice_id: str) -> Invoice | None:
    return _DB.get(invoice_id)


def list_invoices() -> list[Invoice]:
    return list(_DB.values())


def delete_invoice(invoice_id: str) -> bool:
    return _DB.pop(invoice_id, None) is not None
