FROM lscr.io/linuxserver/blender:latest

# ─── Python deps per il backend ───────────────────────
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3-pip \
    python3-venv \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

COPY services/blender-agent/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/blender-agent/app/ ./app/

EXPOSE 3000 8100 8200

COPY docker-entrypoint.sh /opt/start-backend.sh
RUN chmod +x /opt/start-backend.sh

# Usa s6-overlay service per avviare il backend prima di /init
RUN echo "#!/usr/bin/with-contenv bash" > /etc/cont-init.d/99-backend && \
    echo "/opt/start-backend.sh &" >> /etc/cont-init.d/99-backend && \
    chmod +x /etc/cont-init.d/99-backend