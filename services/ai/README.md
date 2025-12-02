# InvoWise – AI Module

This directory contains the foundations for the future AI-driven invoice parser.

## Current state
- Defines the `InvoiceAIResult` model.
- Provides placeholder API endpoint `/ai/parse-invoice`.
- Actual AI logic will be added in the engine module.

## Goal
The AI module will parse PDF/PNG/JPG invoices and return structured financial data.

## Next steps
- Implement `engine.py` with real AI parsing logic.
- Connect engine to `/ai/parse-invoice`.
