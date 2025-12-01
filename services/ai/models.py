from pydantic import BaseModel
from datetime import date
from typing import Optional


class InvoiceAIResult(BaseModel):
    supplier_name: Optional[str]
    invoice_number: Optional[str]
    issue_date: Optional[date]
    total_net: Optional[float]
    total_vat: Optional[float]
    total_gross: Optional[float]
    currency: Optional[str] = "PLN"
    raw_text: Optional[str] = None
