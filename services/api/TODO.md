# 🧾 InvoWise – Dashboard Development Plan

This document outlines the next development milestones for the **InvoWise** project, focusing on analytics, reporting, and the frontend dashboard.

---

## 🧠 Overview
The goal of this iteration is to provide users with a **visual dashboard** showing key financial metrics (totals, VAT summaries, monthly trends) and to enable **exporting reports** directly from the backend.

---

## 🔧 Backend / API Layer

### ✅ Phase 1 – Analytics Expansion
- [x] Extend `/analytics` endpoint to include:
  - [x] Monthly aggregation (count, total_net, total_vat, total_gross)
  - [ ] VAT breakdown **input/output** (wymaga pola `type: income|expense` w Invoice)
  - [x] Year-to-date summary (`ytd`)
- [x] Use existing invoice model for grouping/filtering
- [x] Return structured JSON:
  ```json
  {
    "month": "2025-09",
    "count": 3,
    "total_net": 300.0,
    "total_vat": 69.0,
    "total_gross": 369.0
  }
```

### ✅ Phase 2 – Report Exporting
- [x] Add endpoint `/reports/export`
  - [x] Support formats: `json`, `csv`
  - [x] Allow optional query params: `?month=2025-09&format=csv`
  - [x] Auto-generate CSV using `pandas` or `csv` standard lib
  - [x] Return downloadable file with proper headers

Example:
```bash
GET /reports/export?month=2025-09&format=csv
```

---

## 💻 Frontend / Dashboard Layer

### ✅ Phase 3 – Dashboard UI (MVP)
- [ ] Create minimal dashboard view with:
  - [ ] Total income, expense, and VAT cards
  - [ ] Monthly trend chart (line or bar chart)
  - [ ] “Export” button (CSV/JSON)
- [ ] Fetch data from `/analytics` and `/reports/export`
- [ ] Display loading states and error handling

### ✅ Phase 4 – Enhancements
- [ ] Add filters (month/year selector)
- [ ] Dark mode compatibility
- [ ] Responsive layout (mobile/tablet)

---

---

## 🚀 Phase 5 – Upcoming Integrations (Planned)

- [ ] **S3 Data Backup:** automate daily export of analytics reports to AWS S3  
- [ ] **Email Summary Reports:** send monthly financial summary via AWS SES or SMTP  
- [ ] **Slack Notifications:** optional integration to alert about overdue invoices  
- [ ] **Multi-user Dashboard:** prepare base structure for team-level access and permissions  

🗓️ *Target timeframe: late November 2025*


## 🧩 Tech Notes
- Use `Chart.js` or `Plotly.js` for rendering charts.
- Keep frontend API calls under `src/api/dashboard.js`.
- Backend endpoints should stay under `app/api/analytics.py` and `app/api/reports.py`.
- All new features should include at least one test case (backend or frontend).

---
## ✅ Progress Log (2025-11-05)

- Backend phase completed (analytics + report export fully functional)
- Preparing for frontend dashboard MVP next week
- Next step: connect `/analytics` and `/reports/export` data to UI mock

---

📌 **Goal:** deliver a functional analytics dashboard with export capabilities by **mid-November 2025**.
