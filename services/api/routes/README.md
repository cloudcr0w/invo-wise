# API Routes – Overview

Ten katalog zawiera główne endpointy backendu InvoWise. 
Każdy plik odpowiada za osobną część API.

---

## `health.py`
Prosty endpoint sprawdzający, czy API działa.  
Używany do monitoringu, testów oraz jako "heartbeat" dla dockera, load balancera czy systemów orkiestracji.

`GET /health` → zwraca `{"status": "ok"}`

---

## `version.py`
Endpoint zwracający aktualną wersję API.  
Przydatny przy debugowaniu, wdrożeniach i sprawdzaniu, czy działa odpowiednia wersja kontenera.

`GET /version` → zwraca `{"version": "0.1.0"}`

---

## `ai.py`
Router odpowiedzialny za logikę związaną z przetwarzaniem faktur przy użyciu AI.  
Na razie działa w trybie "stub" – przyjmuje pliki PDF/PNG/JPG i zwraca przykładowe dane.  
W przyszłości zostanie połączony z modułem AI (`engine.py`), który będzie analizował faktury i wyciągał z nich strukturę danych.

`POST /ai/parse-invoice` → upload pliku, zwrot danych wyciągniętych z faktury

---

README będzie uzupełniane w miarę dodawania kolejnych endpointów.
