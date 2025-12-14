from datetime import date
from typing import List, Optional, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class Party(BaseModel):
    name: Optional[str] = None
    nip: Optional[str] = None
    address: Optional[str] = None

    @field_validator("nip")
    def validate_nip(cls, value):
        if not value:
            return value
        digits = "".join(filter(str.isdigit, value))
        if len(digits) != 10:
            raise ValueError("NIP must contain exactly 10 digits")
        return value


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
    
    class Totals(BaseModel):
    net: float
    vat: float
    gross: float
    vat_amount_total: Optional[float] = None


class Payment(BaseModel):
    method: Optional[str] = None
    iban: Optional[str] = None
    paid: bool = False

