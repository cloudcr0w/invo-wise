# services/api/main.py
# InvoWise API 
# Zawiera: globalne logowanie, serwowanie statycznego frontu, CORS,
# endpointy: /health, /invoices CRUD (light), /upload, /export/csv, /version,
# /analytics (miesięczne agregaty), /summary (pojedyncza, bez duplikatów).

from pathlib import Path
from collections import defaultdict
from datetime import datetime
import io
import csv
import logging

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from uuid import uuid4

from .models import Invoice, Item, Totals
from .storage import save_invoice, list_invoices, get_invoice, delete_invoice
from .parsers.pl_invoice import parse_text_to_fields

# --- LOGOWANIE GLOBALNE ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("invo-wise")

# --- APP ---
app = FastAPI(title="InvoWise API", version="0.1.0")
print("🚀 InvoWise API running — open http://127.0.0.1:8000/web/app.html for dev UI")

# --- STATYCZNY FRONT /web ---
BASE_DIR = Path(__file__).resolve().parents[2]  # repo root
STATIC_DIR = BASE_DIR / "apps" / "landing"
print("STATIC_DIR:", STATIC_DIR, "exists:", STATIC_DIR.exists())
app.mount("/web", StaticFiles(directory=str(STATIC_DIR), html=True), name="web")

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELE REQ ---
class InvoiceCreateRequest(BaseModel):
    raw_text: str


# =====================
# Health & Core Invoices
# =====================

@app.get("/health")
async def health():
    logger.info("Health endpoint called")
    return {"ok": True, "invoices": len(list_invoices())}


@app.get("/invoices")
async def invoices():
    data = [inv.model_dump() for inv in list_invoices()]
    logger.info("Listed invoices: %s", len(data))
    return data


@app.get("/invoices/{invoice_id}")
async def invoice_detail(invoice_id: str):
    inv = get_invoice(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="not found")
    logger.info("Invoice fetched: %s", invoice_id)
    return inv.model_dump()


@app.delete("/invoices/{invoice_id}")
async def invoice_delete(invoice_id: str):
    ok = delete_invoice(invoice_id)
    logger.info("Invoice deleted=%s id=%s", ok, invoice_id)
    return {"deleted": ok}


# =====================
# Create from raw text
# =====================
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
    logger.info("Invoice created from text: %s", inv.invoice_id)
    return JSONResponse(inv.model_dump())


# =====================
# Upload (mock, bez OCR)
# =====================
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    # Prosta walidacja rozszerzeń i rozmiaru
    allowed_ext = (".pdf", ".jpg", ".jpeg", ".png", ".txt")
    if not file.filename.lower().endswith(allowed_ext):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    content = await file.read()
    if len(content) > 2_000_000:
        raise HTTPException(status_code=400, detail="File too large (max 2MB)")
    await file.seek(0)

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
    logger.info("Invoice uploaded: %s (%s bytes)", inv.invoice_id, len(content))
    return inv.model_dump()


# =====================
# Export CSV
# =====================
@app.get("/export/csv")
async def export_csv():
    invoices = list_invoices()
    if not invoices:
        raise HTTPException(status_code=404, detail="No invoices to export")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["invoice_id", "nip", "file_uri", "gross", "confidence"])
    for inv in invoices:
        writer.writerow([
            inv.invoice_id,
            (inv.issuer or {}).get("nip", ""),
            getattr(inv, "file_uri", "") or "",
            getattr(inv.totals, "gross", 0.0),
            getattr(inv, "confidence", 0.0),
        ])
    output.seek(0)
    headers = {"Content-Disposition": "attachment; filename=invoices.csv"}
    logger.info("CSV exported for %s invoices", len(invoices))
    return StreamingResponse(output, media_type="text/csv", headers=headers)


# =====================
# Version
# =====================
@app.get("/version")
async def version():
    return {"version": "0.1.0", "env": "dev"}


# =====================
# Analytics (monthly)
# =====================
@app.get("/analytics")
async def analytics():
    """
    Miesięczne agregaty na podstawie Invoice.totals (net, vat, gross).
    Jeśli Invoice nie ma daty, wrzucam do miesiąca "unknown".
    """
    invoices = list_invoices()

    monthly = defaultdict(lambda: {
        "count": 0,
        "total_net": 0.0,
        "total_vat": 0.0,
        "total_gross": 0.0
    })

    for inv in invoices:
       
        month = "unknown"
        try:
            raw_date = getattr(inv, "date", None)
            if raw_date:
                if isinstance(raw_date, str):
                    month = raw_date[:7]  # 'YYYY-MM-DD' -> 'YYYY-MM'
                else:
                    month = raw_date.strftime("%Y-%m")
        except Exception:
            month = "unknown"

        net = float(getattr(getattr(inv, "totals", None), "net", 0.0) or 0.0)
        vat = float(getattr(getattr(inv, "totals", None), "vat", 0.0) or 0.0)
        gross = float(getattr(getattr(inv, "totals", None), "gross", 0.0) or 0.0)

        monthly[month]["count"] += 1
        monthly[month]["total_net"] += net
        monthly[month]["total_vat"] += vat
        monthly[month]["total_gross"] += gross

    def sort_key(k: str):
        return (k == "unknown", k)

    out = []
    for m in sorted(monthly.keys(), key=sort_key):
        agg = monthly[m]
        out.append({
            "month": m,
            "count": agg["count"],
            "total_net": round(agg["total_net"], 2),
            "total_vat": round(agg["total_vat"], 2),
            "total_gross": round(agg["total_gross"], 2),
        })

    ytd = {
        "count": sum(v["count"] for v in monthly.values()),
        "total_net": round(sum(v["total_net"] for v in monthly.values()), 2),
        "total_vat": round(sum(v["total_vat"] for v in monthly.values()), 2),
        "total_gross": round(sum(v["total_gross"] for v in monthly.values()), 2),
    }

    logger.info("/analytics generated for %s month buckets (YTD invoices: %s)", len(out), ytd["count"])
    return {
        "analytics": out,
        "ytd": ytd,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "version": "0.1.0"
    }
@app.get("/reports/export")
async def export_reports(format: str = "json", month: str = None):
    """
    Eksport raportu miesięcznego (JSON lub CSV).
    Jeśli nie podano miesiąca, zwraca pełne zestawienie.
    """
    invoices = list_invoices()
    if not invoices:
        raise HTTPException(status_code=404, detail="No invoices found")

    # filtrujemy po miesiącu jeśli jest podany
    if month:
        invoices = [inv for inv in invoices if getattr(inv, "date", "").startswith(month)]
        if not invoices:
            raise HTTPException(status_code=404, detail=f"No data for {month}")

    # przygotowujemy dane
    rows = [
        {
            "invoice_id": inv.invoice_id,
            "nip": (inv.issuer or {}).get("nip", ""),
            "gross": getattr(inv.totals, "gross", 0.0),
            "confidence": getattr(inv, "confidence", 0.0),
        }
        for inv in invoices
    ]

    # CSV lub JSON
    if format == "csv":
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
        output.seek(0)
        headers = {"Content-Disposition": f"attachment; filename=report_{month or 'all'}.csv"}
        logger.info(f"/reports/export -> CSV ({len(rows)} rows)")
        return StreamingResponse(output, media_type="text/csv", headers=headers)
    else:
        logger.info(f"/reports/export -> JSON ({len(rows)} rows)")
        return {"month": month or "all", "count": len(rows), "data": rows}


# =====================
# Summary (single, no duplicates)
# =====================
@app.get("/summary/{invoice_id}")
async def invoice_summary(invoice_id: str):
    """
    Mock AI summary – kategoryzacja i krótki opis.
    TODO: podpiąć prawdziwe LLM (Bedrock/OpenAI) + prompt z kontekstem (NIP, pozycje, kwoty).
    """
    inv = get_invoice(invoice_id)
    if not inv:
        raise HTTPException(status_code=404, detail="Invoice not found")

    issuer_nip = (inv.issuer or {}).get("nip") or "NIP nieznany"
    total = getattr(inv.totals, "gross", 0.0)

    # prosta reguła demo; później zastąpię LLM
    if total >= 500:
        category = "usługi IT"
    elif total >= 100:
        category = "media/operacyjne"
    else:
        category = "materiały biurowe"

    summary = f"Faktura od {issuer_nip} na {total} zł – kategoria: {category} (auto)."

    return {
        "invoice_id": inv.invoice_id,
        "category": category,
        "summary": summary,
        "confidence": getattr(inv, "confidence", 0.0),
    }
