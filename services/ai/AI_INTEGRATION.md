
# InvoWise – AI Integration

This module defines the interface and data model for AI-based invoice parsing.

## Current state

- `/ai/parse-invoice` endpoint accepts PDF/PNG/JPG files.
- `InvoiceAIEngine` is a stub that returns demo data.
- `InvoiceAIResult` defines the parsed invoice structure (amounts, dates, supplier, etc.).

## Next steps

- Integrate real OCR/LLM provider (e.g. external API).
- Map model output to `InvoiceAIResult`.
- Connect AI parsing results with invoice storage and analytics pipeline.
