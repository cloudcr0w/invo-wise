from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class Party(BaseModel):
    name: Optional[str] = None
    nip: Optional[str] = None
    address: Optional[str] = None


class Item(BaseModel):
    name: str
    qty: float = 1
    unit: str = "szt"
    net: float
    vat_rate: str = "23%"
    vat: float
    gross: float
    category: Optional[str] = None


class Totals(BaseModel):
    net: float
    vat: float
    gross: float


class Payment(BaseModel):
    method: Optional[str] = None
    iban: Optional[str] = None
    paid: bool = False


class Invoice(BaseModel):
    invoice_id: str
    owner_id: str
    source: str = Field(default="upload", description="upload|email")
    file_uri: Optional[str] = None
    issuer: Party = Party()
    buyer: Party = Party()
    invoice_no: Optional[str] = None
    issue_date: Optional[date] = None
    due_date: Optional[date] = None
    currency: str = "PLN"
    items: List[Item] = []
    totals: Optional[Totals] = None
    payment: Payment = Payment()
    tags: List[str] = []
    status: str = "parsed"  # parsed|needs_review|confirmed|exported
    confidence: float = 0.0
