# InvoWise – Roadmap & TODO

This document contains the **full development roadmap** for the InvoWise project: backend, dashboard, integrations and future improvements.

---

## 🎯 High-level roadmap

### Phase 1 – Analytics (backend) ✅
- `/analytics`
- monthly aggregates
- YTD summary

### Phase 2 – Exporting (backend) ✅
- `/reports/export`
- JSON/CSV output
- optional month filter

### Phase 3 – Dashboard MVP (frontend) ✅
- KPI cards
- Trend chart
- Export panel
- Filters
- Loading/toasts

### Phase 4 – Dashboard Enhancements (WIP)
- income/expense breakdown
- second dataset (income vs cost)
- mobile layout improvements
- settings.json

### Phase 5 – Integrations (planned)
- S3 backups
- Email monthly summary
- Slack alerts
- Multi-user dashboard

---

## 📝 Detailed TODO

### Backend
- add Invoice.type (`income|expense`)
- recompute income/expense aggregates
- expand analytics JSON
- add settings endpoint
- add tests

### Frontend
- support new analytics JSON
- add income vs expense chart dataset
- new KPIs (costs YTD)
- simple settings panel

### Dev / DX
- add make test
- keep tree.txt updated
- docs expansion (optional)

---

## 📌 Notes
Roadmap is meant to be updated frequently. README stays short and recruiter-friendly; this file holds all technical plans.
