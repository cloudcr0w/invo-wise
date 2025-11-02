# InvoWise — inteligentny asystent do faktur (MVP)


## Dev quickstart
1) Python 3.10+
2) `make venv && export $(grep -v '^#' .env.example | xargs) && make api-deps`
3) `cp .env.example .env`
4) `make api` → http://localhost:8000/health


Landing: open `apps/landing/index.html` in your browser (or host via GitHub Pages / Vercel).


## Week 1 scope
- Local FastAPI with endpoints: /health, /invoices (CRUD mock), /upload (stub)
- Simple in-memory storage (later S3 + Postgres)
- Parser stub for PL invoices (regex for NIP, dates) — to be expanded

##  Dev UI (local testing)

To quickly test the backend without Postman, open the lightweight HTML dev UI:

```bash
make api
```

Then upload any .pdf, .jpg, .png, or .txt file — results are stored in-memory and visible in the table below.

### 🚀 Quickstart

Create virtualenv and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r services/api/requirements.txt
make api
```

The API will run at http://127.0.0.1:8000

### 📡 API Endpoints

- `GET /health` – health check  
- `GET /invoices` – list invoices  
- `POST /upload` – upload a file  
- `GET /export/csv` – download all invoices as CSV  
- `GET /version` – API version info
- `GET /summary/{invoice_id}` – mock AI summary (category + opis)

### 🧪 Dev UI
Open: `http://127.0.0.1:8000/web/app.html`  
Now includes quick analytics widget (refresh button).

## 🧠 Analytics Endpoint (Preview)

The `/analytics` endpoint provides monthly summaries of invoices based on `Invoice.totals`.

Example:
```json
{
  "month": "2025-10",
  "count": 4,
  "total_net": 400.0,
  "total_vat": 92.0,
  "total_gross": 492.0
}
```

Notes:

Values are aggregated per month (YYYY-MM).

If no date is present, data is grouped under "unknown".

Response also includes a ytd (year-to-date) summary and generated_at timestamp