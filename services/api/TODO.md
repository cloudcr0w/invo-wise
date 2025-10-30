# 🧾 InvoWise – Dashboard Development Plan

This document outlines the next development milestones for the **InvoWise** project, focusing on analytics, reporting, and the frontend dashboard.

---

## 🧠 Overview
The goal of this iteration is to provide users with a **visual dashboard** showing key financial metrics (totals, VAT summaries, monthly trends) and to enable **exporting reports** directly from the backend.

---

## 🔧 Backend / API Layer

### ✅ Phase 1 – Analytics Expansion
- [ ] Extend `/analytics` endpoint to include:
  - [ ] Monthly income and expense aggregation  
  - [ ] VAT breakdown (input/output VAT, totals per month)
  - [ ] Year-to-date summary (`YTD` field)
- [ ] Use existing invoice model for data grouping and filtering
- [ ] Return JSON in structure:
  ```json
  {
    "month": "2025-09",
    "total_income": 12000,
    "total_expense": 3500,
    "vat_input": 500,
    "vat_output": 950
  }
  ```

### ✅ Phase 2 – Report Exporting
- [ ] Add endpoint `/reports/export`
  - [ ] Support formats: `json`, `csv`
  - [ ] Allow optional query params: `?month=2025-09&format=csv`
  - [ ] Auto-generate CSV using `pandas` or `csv` standard lib
  - [ ] Return downloadable file with proper headers

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

## 🧩 Tech Notes
- Use `Chart.js` or `Plotly.js` for rendering charts.
- Keep frontend API calls under `src/api/dashboard.js`.
- Backend endpoints should stay under `app/api/analytics.py` and `app/api/reports.py`.
- All new features should include at least one test case (backend or frontend).

---

## 🗓️ Next Steps
1. **Tomorrow:** start backend aggregation logic (`/analytics` extension)  
2. **Next commit:** add `/reports/export` endpoint  
3. **Weekend:** begin dashboard UI prototype  
4. **Following week:** connect backend + frontend and finalize MVP  

---

📌 **Goal:** deliver a functional analytics dashboard with export capabilities by **mid-November 2025**.
