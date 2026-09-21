FROM lscr.io/linuxserver/blender:latest AS base

# ─── Python deps per il backend ───────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-venv \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ─── Crea virtualenv (non sporca l'ambiente Blender) ───
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY services/blender-agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── App code ──────────────────────────────────────────
COPY services/blender-agent/app/ ./app/

# ─── Porte ─────────────────────────────────────────────
EXPOSE 3000 8100 8200

# ─── Entrypoint: avvia Blender web + backend Python ───
COPY docker-entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]