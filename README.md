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
