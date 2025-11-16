# InvoWise

**InvoWise** is a lightweight invoice helper for sole proprietors (freelancers / one-person businesses).  
Goal: **paste or upload invoice → get clean totals and monthly insights**, without digging through PDFs and spreadsheets.

This repo contains:

- 🧠 **FastAPI backend** – parsing, storage, analytics, exports  
- 📊 **Minimal dashboard** – KPI cards, monthly trend chart, CSV/JSON export  
- 🧪 **Local mock mode** – demo without running the backend  

---

## 🚀 Features (current state)

- Upload invoice files (PDF / image / text draft)
- Store parsed invoices locally (dev mode)
- `/analytics` endpoint:
  - Year-to-date totals (count, net, VAT, gross)
  - Monthly aggregates (per `YYYY-MM`)
- `/reports/export`:
  - Export JSON or CSV
  - Optional `?month=YYYY-MM` filter
- Dashboard:
  - KPI cards (invoices YTD, total gross, VAT)
  - Monthly trend chart (Chart.js)
  - Export buttons (CSV / JSON)
  - Basic filters (`YYYY-MM`), toasts, loading states, dark mode

---

## 🧰 Tech Stack

- **Backend:** Python, FastAPI  
- **Frontend:** Vanilla HTML / CSS / JS  
- **Charts:** Chart.js  
- **Storage:** simple local store (dev), CSV/JSON export  
- **Dev UX:** Makefile targets, mock mode for the dashboard  

---

## ▶️ Quickstart (local dev)

### 1. Backend API

From repo root:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Option A: using Makefile
make api

# Option B: direct
uvicorn app.main:app --reload
```

API is available at:

```
http://127.0.0.1:8000
```

---

### 2. Dashboard (apps/landing)

```bash
cd apps/landing
make serve
# or: python -m http.server 8080
```

Open:

```
http://127.0.0.1:8080/app.html
```

---

## 🧪 Mock mode (no backend needed)

```bash
cd apps/landing
make serve
```

Then open:

```
http://127.0.0.1:8080/app.html?mock=1
```

Mock mode uses local `mock.json`.

---

## 📂 Project Structure

```
.
├── apps/
│   └── landing/
│       ├── app.html
│       ├── dashboard.css
│       ├── dashboard.js
│       ├── index.html
│       ├── Makefile
│       └── README.md
│
├── infra/
│   └── (future Terraform / IaC files)
│
├── services/
│   ├── api/
│   │   ├── parsers/
│   │   │   └── (invoice parsing helpers)
│   │   ├── tests/
│   │   │   └── test_*.py
│   │   ├── analytics.py        # /analytics
│   │   ├── reports.py          # /reports/export
│   │   ├── main.py             # FastAPI app entrypoint
│   │   ├── models.py           # Pydantic models
│   │   ├── storage.py          # local store loader/saver
│   │   ├── requirements.txt
│   │   ├── Dockerfile
│   │   ├── README.md
│
```

---

## 🗺️ Roadmap

### Phase 1 – Analytics (backend) ✅  
### Phase 2 – Exporting (backend) ✅  
### Phase 3 – Dashboard MVP (frontend) ✅  
### Phase 4 – Enhancements (in progress)
- [ ] Income vs expense breakdown
- [ ] Additional KPI (costs YTD)
- [ ] Filters for month/year presets
- [ ] Mobile polish

### Phase 5 – Integrations (planned)
- [ ] S3 backups  
- [ ] SES email summaries  
- [ ] Slack notifications  
- [ ] Multi-user mode  

---

## ⚠️ Known Issues

- In mock mode (`?mock=1`), the trend chart may not refresh fully on first load  
- Safari requires a polyfill for `toLocaleString('pl-PL')`  
- `API_BASE` in `dashboard.js` is hardcoded (future: env-based config)  
- Downloading JSON on Firefox may trigger “open file dialog” instead of saving


## 💬 Notes

This project is primarily a **learning & portfolio** app:  
lightweight, clean, easy to extend with cloud services later.
