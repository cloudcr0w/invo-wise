from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

from .models import Invoice, Item, Totals
from .storage import save_invoice, list_invoices, get_invoice, delete_invoice
from .parsers.pl_invoice import parse_text_to_fields


app = FastAPI(title="InvoWise API", version="0.1.0")

from pathlib import Path
from fastapi.staticfiles import StaticFiles

BASE_DIR = Path(__file__).resolve().parents[2]  # repo root
STATIC_DIR = BASE_DIR / "apps" / "landing"
print("STATIC_DIR:", STATIC_DIR, "exists:", STATIC_DIR.exists())

app.mount("/web", StaticFiles(directory=str(STATIC_DIR), html=True), name="web")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*",],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InvoiceCreateRequest(BaseModel):
    raw_text: str


@app.get("/health")
async def health():
    return {"ok": True, "invoices": len(list_invoices())}


@app.get("/invoices")
async def invoices():
    return [inv.model_dump() for inv in list_invoices()]


@app.get("/invoices/{invoice_id}")
async def invoice_detail(invoice_id: str):
    inv = get_invoice(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="not found")
    return inv.model_dump()


@app.delete("/invoices/{invoice_id}")
async def invoice_delete(invoice_id: str):
    ok = delete_invoice(invoice_id)
    return {"deleted": ok}


@app.post("/invoices/text")
async def create_from_text(body: InvoiceCreateRequest):
    fields = parse_text_to_fields(body.raw_text)
    inv = Invoice(
        invoice_id=str(uuid4()),
        owner_id="local-dev",
        issuer={"nip": fields.get("nip")},
        items=[
            Item(
                name="Pozycja demo",
                qty=1,
                net=100.0,
                vat_rate="23%",
                vat=23.0,
                gross=123.0,
            )
        ],
        totals=Totals(net=100.0, vat=23.0, gross=123.0),
        confidence=0.42,
    )
    save_invoice(inv)
    return JSONResponse(inv.model_dump())


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Week 1: accept file, read text very naively (no OCR yet)
    # services/api/main.py – dopisz na górze endpointu /upload:
    if not file.filename.lower().endswith((".pdf", ".jpg", ".jpeg", ".png", ".txt")):
        raise HTTPException(status_code=400, detail="Unsupported file type")
    if len(await file.read()) > 2_000_000:
        raise HTTPException(status_code=400, detail="File too large (max 2MB)")
    await file.seek(0)

    content = await file.read()
    try:
        text = content.decode("utf-8", errors="ignore")
    except Exception:
        text = ""

    fields = parse_text_to_fields(text)
    inv = Invoice(
        invoice_id=str(uuid4()),
        owner_id="local-dev",
        file_uri=f"local://{file.filename}",
        issuer={"nip": fields.get("nip")},
        items=[
            Item(
                name=file.filename or "Pozycja",
                qty=1,
                net=100.0,
                vat_rate="23%",
                vat=23.0,
                gross=123.0,
            )
        ],
        totals=Totals(net=100.0, vat=23.0, gross=123.0),
        confidence=0.20,
    )
    save_invoice(inv)
    return inv.model_dump()
