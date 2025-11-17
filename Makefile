.PHONY: api dev test fmt venv api-deps

api:
	@uvicorn services.api.main:app --reload --host $(API_HOST) --port $(API_PORT) --reload-dir services/api

venv:
	@python3 -m venv .venv && . .venv/bin/activate && pip install --upgrade pip

api-deps:
	@. .venv/bin/activate && pip install -r services/api/requirements.txt

fmt:
	@. .venv/bin/activate && python -m pip install ruff black && ruff format services/api && black services/api

test:
	@echo "(tests will go here)"

help:
	@echo "Available commands:"
	@echo "  make api        Run FastAPI locally"
	@echo "  make test       Run tests (if present)"
	@echo "  make fmt        Format code"
	@echo "  make infra-fmt   Format Terraform modules"
