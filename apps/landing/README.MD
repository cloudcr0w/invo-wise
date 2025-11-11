# InvoWise Landing / Dashboard

## Run (backend)
`make api`

## Run (static UI)
`cd apps/landing && python -m http.server 8080`

- Mock mode: `http://127.0.0.1:8080/app.html?mock=1`
- Export działa tylko z backendem (`/reports/export`).

## Build notes
- `dashboard.js`: logika UI, fetche, wykres.
- `dashboard.css`: dark/light, KPI grid, toasty, spinnery.
