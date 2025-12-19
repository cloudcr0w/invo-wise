# InvoWise backend Docker image
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default port for the backend (FastAPI planned)
EXPOSE 8000

# Temporary placeholder command (API entrypoint will replace this later)
CMD ["python", "-m", "http.server", "8000"]
