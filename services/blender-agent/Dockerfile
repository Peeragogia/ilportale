FROM python:3.12-slim

WORKDIR /app

# ─── System deps ───────────────────────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# ─── Python deps ───────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── App code ──────────────────────────────────────────
COPY app/ ./app/

EXPOSE 8100 8200

CMD ["python", "-m", "app.api"]