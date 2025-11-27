![Status](https://img.shields.io/badge/InvoWise-DevBuild-blue?style=flat-square)


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

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r services/api/requirements.txt
make api
```

API runs at:

```
http://127.0.0.1:8000
```

---

### 2. Dashboard (apps/landing)

```bash
cd apps/landing
make serve
```

Then open:

```
http://127.0.0.1:8080/app.html
```

---

## 🧪 Mock mode (no backend needed)

```
http://127.0.0.1:8080/app.html?mock=1
```

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
│   └── api/
│       ├── parsers/
│       ├── tests/
│       ├── analytics.py
│       ├── reports.py
│       ├── main.py
│       ├── models.py
│       ├── storage.py
│       ├── requirements.txt
│       ├── Dockerfile
│       ├── README.md
│       └── __init__.py
│
├── .env.example
├── .gitignore
├── Makefile
├── README.md
└── tree.txt
```

---
## 🏗️ Infrastructure (Terraform)

Infrastructure-as-Code for InvoWise lives under:

infra/terraform


This includes:
- root Terraform module (`main.tf`, `providers.tf`, `outputs.tf`)
- skeleton module for future S3/DynamoDB backend (`modules/state-backend/`)
- example locals and variable definitions

🟢 The infrastructure is not active yet, but will be expanded during Phase 5.


## 🗺️ Roadmap

Full development roadmap:  
👉 See **ROADMAP.md**

---

## ⚠️ Known Issues

- Trend chart may not refresh fully on first mock load  
- Safari requires polyfill for locale formatting  
- API base is hardcoded inside dashboard.js  

---

## 💬 Notes

This project is a learning & portfolio app designed to be easy to extend later.
