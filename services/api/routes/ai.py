from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import tempfile

from services.ai.models import InvoiceAIResult

router = APIRouter(prefix="/ai", tags=["ai"])


@router.post("/parse-invoice", response_model=InvoiceAIResult)
async def parse_invoice(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Temporary storage
    suffix = Path(file.filename).suffix
    with tempfile.NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()

        # stub – will be replaced by engine later
        return InvoiceAIResult(
            supplier_name="Demo Supplier",
            invoice_number=file.filename,
            total_net=100.0,
            total_vat=23.0,
            total_gross=123.0,
            raw_text="Stub AI output",
        )
