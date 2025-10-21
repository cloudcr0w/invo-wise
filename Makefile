.PHONY: api dev test fmt


api:
cd services/api && uvicorn main:app --reload --host $$API_HOST --port $$API_PORT


venv:
python3 -m venv .venv && . .venv/bin/activate && pip install --upgrade pip


api-deps:
. .venv/bin/activate && pip install -r services/api/requirements.txt


fmt:
. .venv/bin/activate && python -m pip install ruff black && ruff format services/api && black services/api


test:
@echo "(tests will go here)"