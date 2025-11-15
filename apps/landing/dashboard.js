// InvoWise dashboard JS (light polish; order + tiny UX)
// Build: auto-updated in footer elsewhere

// ========= Consts / DOM refs =========
const API_BASE = 'http://127.0.0.1:8000'

const statusEl = document.getElementById('status')
const tbody = document.getElementById('invoices-body')
const uploadForm = document.getElementById('upload-form')
const uploadMsg = document.getElementById('upload-msg')
const detailCard = document.getElementById('detail-card')
const detailJson = document.getElementById('detail-json')
const aiCard = document.getElementById('ai-card')
const aiSummary = document.getElementById('ai-summary')

const analyticsBox = document.getElementById('analytics')
const monthlyBox = document.getElementById('monthly')
const genInfo = document.getElementById('gen-info')
const refreshBtn = document.getElementById('refresh-analytics')

const exportBtn = document.getElementById('export-btn')
const exportJsonBtn = document.getElementById('export-json-btn')
const exportMsg = document.getElementById('export-msg')
const monthInput = document.getElementById('month-input')

// KPI
const kpiCount = document.getElementById('kpi-count')
const kpiGross = document.getElementById('kpi-gross')
const kpiVat = document.getElementById('kpi-vat')

// Filters (optional UI)
const filterMonth = document.getElementById('filter-month')
const applyFilter = document.getElementById('apply-filter')
const filterMsg = document.getElementById('filter-msg')

// Chart
let trendChart

// ===============================================
// Helpers (formatting, loading, notifications)
// ===============================================

function numberPL(n) {
	return (n ?? 0).toLocaleString('pl-PL', { minimumFractionDigits: 2, maximumFractionDigits: 2 })
}

function withLoading(btn, fn) {
	const prevText = btn.textContent
	btn.classList.add('btn--loading')
	btn.disabled = true
	return Promise.resolve(fn())
		.catch(err => {
			console.error('Error during action:', err)
			throw err
		})
		.finally(() => {
			btn.classList.remove('btn--loading')
			btn.disabled = false
			btn.textContent = prevText
		})
}

function toast(msg, type = 'ok') {
	const el = document.getElementById('toast')
	if (!el) return

	el.textContent = msg
	el.className = `toast toast--${type} show`
	el.style.display = 'block'

	clearTimeout(el._timeout)
	el._timeout = setTimeout(() => {
		el.classList.remove('show')
		setTimeout(() => (el.style.display = 'none'), 250)
	}, 2400)
}

// ===============================================
// API + Rendering logic
// ===============================================

async function health() {
	try {
		const res = await fetch(`${API_BASE}/health`)
		const json = await res.json()
		statusEl.innerHTML = json.ok ? `✅ OK (faktur: ${json.invoices ?? '?'})` : '❌ Błąd'
		statusEl.className = json.ok ? 'ok' : 'err'
		if (json.ok) toast('Połączono z API ✅', 'ok')
	} catch {
		statusEl.textContent = '❌ API niedostępne (sprawdź make api)'
		statusEl.className = 'err'
		toast('API niedostępne ❌', 'err')
	}
}

async function listInvoices() {
	try {
		const res = await fetch(`${API_BASE}/invoices`)
		const data = await res.json()
		if (!Array.isArray(data) || data.length === 0) {
			tbody.innerHTML = `<tr><td colspan="5" class="muted">Brak danych…</td></tr>`
			return
		}
		tbody.innerHTML = data
			.map(
				inv => `
      <tr data-id="${inv.invoice_id}" class="inv-row">
        <td><code>${inv.invoice_id}</code></td>
        <td>${inv.issuer?.nip || '-'}</td>
        <td>${inv.file_uri || '-'}</td>
        <td>${inv.totals?.gross ?? '-'}</td>
        <td>${(inv.confidence ?? 0).toFixed(2)}</td>
      </tr>
    `
			)
			.join('')

		for (const tr of document.querySelectorAll('.inv-row')) {
			tr.addEventListener('click', async () => {
				const id = tr.getAttribute('data-id')
				detailJson.textContent = 'Ładowanie…'
				detailCard.style.display = 'block'
				try {
					const res = await fetch(`${API_BASE}/invoices/${id}`)
					if (!res.ok) throw new Error(`HTTP ${res.status}`)
					const json = await res.json()
					detailJson.textContent = JSON.stringify(json, null, 2)
					detailCard.scrollIntoView({ behavior: 'smooth', block: 'start' })

					try {
						const res2 = await fetch(`${API_BASE}/summary/${id}`)
						if (res2.ok) {
							const s = await res2.json()
							aiSummary.textContent = s.summary
							aiCard.style.display = 'block'
						} else {
							aiCard.style.display = 'none'
						}
					} catch {
						aiCard.style.display = 'none'
					}
				} catch {
					detailJson.textContent = 'Błąd pobierania szczegółów.'
					aiCard.style.display = 'none'
				}
			})
		}
	} catch (err) {
		console.error('Invoice list error:', err)
		tbody.innerHTML = `<tr><td colspan="5" class="err">Błąd pobierania listy</td></tr>`
	}
}

function renderTrendChart(monthlyArr = []) {
	const el = document.getElementById('trendChart')
	const labels = monthlyArr.map(m => m.month)
	const data = monthlyArr.map(m => Number(m?.total_gross ?? 0))

	if (trendChart) {
		trendChart.data.labels = labels
		trendChart.data.datasets[0].data = data
		trendChart.update()
		return
	}

	trendChart = new Chart(el, {
		type: 'bar',
		data: {
			labels,
			datasets: [
				{
					label: 'Suma brutto (zł)',
					data,
					borderWidth: 1,
				},
			],
		},
		options: {
			responsive: true,
			maintainAspectRatio: false,
			scales: {
				y: { beginAtZero: true, ticks: { callback: v => v.toLocaleString('pl-PL') } },
			},
			plugins: { legend: { display: false } },
		},
	})
}

// /analytics: { analytics: [], ytd: {...}, generated_at }
async function loadAnalytics(filter) {
	try {
		const res = await fetch(`${API_BASE}/analytics`)
		const a = await res.json()

		// 🔎 filtr: „YYYY-MM” → pokaż tylko miesiące >= filter
		if (Array.isArray(a.analytics) && filter) {
			a.analytics = a.analytics.filter(x => !filter || x.month >= filter)
		}

		const y = a.ytd || {}

		// KPI
		kpiCount.textContent = (y.count ?? 0).toString()
		kpiGross.textContent = `${numberPL(y.total_gross)} zł`
		kpiVat.textContent = `${numberPL(y.total_vat)} zł`

		// opisowe
		analyticsBox.innerHTML = `Faktur: <b>${y.count ?? 0}</b> · Suma brutto: <b>${numberPL(
			y.total_gross
		)} zł</b> · VAT: <b>${numberPL(y.total_vat)} zł</b>`
		genInfo.textContent = a.generated_at ? `generated ${a.generated_at}` : '–'

		// Ostatnie 3 miesiące (po filtrze, jeśli jest)
		if (Array.isArray(a.analytics) && a.analytics.length) {
			const last = a.analytics.slice(-3)
			monthlyBox.innerHTML = last
				.map(m => `<span class="tag">${m.month} • ${numberPL(m.total_gross)} zł</span>`)
				.join(' ')
		} else {
			monthlyBox.textContent = 'Brak danych miesięcznych.'
		}

		// Wykres — cała seria (już przefiltrowana)
		renderTrendChart(Array.isArray(a.analytics) ? a.analytics : [])
	} catch {
		analyticsBox.textContent = 'Błąd pobierania statystyk'
		monthlyBox.textContent = '—'
		genInfo.textContent = '—'
	}
}
// ===============================================
// Event bindings
// ===============================================

refreshBtn.addEventListener('click', () => withLoading(refreshBtn, () => loadAnalytics()))

// upload
uploadForm.addEventListener('submit', e => {
	e.preventDefault()
	const btn = uploadForm.querySelector("button[type='submit']")
	uploadMsg.textContent = ''
	withLoading(btn, async () => {
		uploadMsg.textContent = 'Wysyłanie…'
		const file = document.getElementById('file').files[0]
		const fd = new FormData()
		fd.append('file', file)

		const res = await fetch(`${API_BASE}/upload`, { method: 'POST', body: fd })
		if (!res.ok) {
			const errJson = await res.json().catch(() => ({}))
			throw new Error(errJson.detail || `HTTP ${res.status}`)
		}
		await res.json()
		uploadMsg.textContent = 'Gotowe ✅'
		toast('Faktura przesłana pomyślnie ✅', 'ok')
		await listInvoices()
		await loadAnalytics()
	}).catch(err => {
		uploadMsg.textContent = `Błąd: ${err.message}`
		toast('Błąd podczas wysyłania ❌', 'err')
	})
})

// export
async function doExport(format) {
	const month = (monthInput.value || '').trim()
	const query = month ? `?format=${format}&month=${encodeURIComponent(month)}` : `?format=${format}`
	exportMsg.textContent = 'Generowanie…'
	try {
		const url = `${API_BASE}/reports/export${query}`
		const res = await fetch(url)
		if (!res.ok) throw new Error(`HTTP ${res.status}`)

		if (format === 'csv') {
			const blob = await res.blob()
			const link = URL.createObjectURL(blob)
			const a = document.createElement('a')
			a.href = link
			a.download = `report_${month || 'all'}.csv`
			a.click()
		} else {
			const json = await res.json()
			const blob = new Blob([JSON.stringify(json, null, 2)], { type: 'application/json' })
			const link = URL.createObjectURL(blob)
			const a = document.createElement('a')
			a.href = link
			a.download = `report_${month || 'all'}.json`
			a.click()
		}
		exportMsg.textContent = 'Gotowe ✅'
		toast('Eksport zakończony sukcesem ✅', 'ok')
	} catch (err) {
		exportMsg.textContent = `Błąd eksportu ❌ (${err.message})`
		toast('Błąd eksportu ❌', 'err')
	}
}

exportBtn.addEventListener('click', () => withLoading(exportBtn, () => doExport('csv')))
exportJsonBtn.addEventListener('click', () => withLoading(exportJsonBtn, () => doExport('json')))

// Filters
applyFilter?.addEventListener('click', async () => {
	const m = (filterMonth?.value || '').trim()
	await loadAnalytics(m)
	monthInput.value = m // podłóż do eksportu
	filterMsg.textContent = m ? `Zastosowano filtr dla: ${m}` : 'Wyczyszczono filtr'
})

// ===============================================
// Init
// ===============================================

;(async function init() {
	await health()
	await listInvoices()
	await loadAnalytics()
	document.querySelector('.footer-note')?.replaceChildren(`Build: ${new Date().toISOString().slice(0, 10)}`)
})()
