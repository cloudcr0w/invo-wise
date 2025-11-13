# InvoWise – Dashboard (apps/landing)

This folder contains a small **HTML/JS dashboard** used to preview the InvoWise API locally.

Features:
- KPI cards (YTD)
- Monthly trend chart (Chart.js)
- CSV/JSON export
- Filters (`YYYY-MM`)
- Dark/light theme
- Toast notifications
- Loading states
- Mock mode (`?mock=1`)

---

## ▶️ Run (with backend)

Start FastAPI:

```bash
make api
# or:
# uvicorn app.main:app --reload
```

Then run the dashboard:

```bash
cd apps/landing
make serve
# or:
# python -m http.server 8080
```

Open:

```
http://127.0.0.1:8080/app.html
```

The frontend calls:

- `GET /health`
- `GET /invoices`
- `GET /analytics`
- `GET /reports/export`

---

## 🧪 Mock mode

Preview the dashboard without running the backend:

```bash
cd apps/landing
make serve
```

Then open:

```
http://127.0.0.1:8080/app.html?mock=1
```

Mock data comes from `mock.json`.

---

## 📂 Files

- `app.html` — main dashboard  
- `dashboard.css` — styles  
- `dashboard.js` — UI logic (fetch, charts, upload, export, filters)  
- `mock.json` — mock analytics for demo  
- `Makefile` — helpers for local serving  

---

## 🔧 Make targets

```bash
make serve   # Serve dashboard on localhost:8080
make mock    # Same server, for mock mode
```

