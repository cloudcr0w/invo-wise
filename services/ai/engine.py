from pathlib import Path
from .models import InvoiceAIResult


class InvoiceAIEngine:
    """
    Placeholder engine for AI-driven invoice parsing.
    Later this will call a real OCR / LLM model.
    """

    def parse(self, path: Path) -> InvoiceAIResult:
        return InvoiceAIResult(
            supplier_name="AI Supplier",
            invoice_number=path.stem,
            total_net=199.0,
            total_vat=45.77,
            total_gross=244.77,
            raw_text=f"Stub parsed output from {path.name}",
        )


engine = InvoiceAIEngine()
