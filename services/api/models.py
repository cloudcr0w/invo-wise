from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date
from typing import List, Optional, Literal
from pydantic import field_validator, model_validator



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

@field_validator("vat_rate")
def validate_vat_rate(cls, value):
        allowed = {"0%", "5%", "8%", "23%"}
        if value not in allowed:
            raise ValueError(f"Unsupported VAT rate: {value}")
        return value
    
@model_validator(mode="after")
def validate_dates(self):
    if self.issue_date and self.due_date and self.issue_date > self.due_date:
        raise ValueError("issue_date cannot be later than due_date")
    return self

@field_validator("nip")
def validate_nip(cls, value):
    if not value:
        return value
    digits = "".join(filter(str.isdigit, value))
    if len(digits) != 10:
        raise ValueError("NIP must contain exactly 10 digits")
    return value

class Totals(BaseModel):
    net: float
    vat: float
    gross: float
    vat_amount_total: Optional[float] = None



class Payment(BaseModel):
    method: Optional[str] = None
    iban: Optional[str] = None
    paid: bool = False


class Invoice(BaseModel):
    invoice_id: str
    owner_id: str
    source: str = Field(default="upload", description="upload|email")
    type: Literal["income", "expense"] = "expense"
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
    category: Optional[str] = None
    status: str = "parsed"  # parsed|needs_review|confirmed|exported
    confidence: float = 0.0
