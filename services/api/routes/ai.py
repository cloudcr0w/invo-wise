from fastapi import APIRouter, UploadFile, File, HTTPException
from pathlib import Path
import tempfile

from services.ai.models import InvoiceAIResult
from services.ai.engine import engine

router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/parse-invoice", response_model=InvoiceAIResult)
async def parse_invoice(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".pdf", ".png", ".jpg", ".jpeg")):
        raise HTTPException(status_code=400, detail="Unsupported file type")

    suffix = Path(file.filename).suffix

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=True, suffix=suffix) as tmp:
        content = await file.read()
        tmp.write(content)
        tmp.flush()

       
        result = engine.parse(Path(tmp.name))
        return result
