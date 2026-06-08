FROM python:3.11-slim-bookworm

LABEL org.opencontainers.image.title="Smart Parenting Companion"
LABEL org.opencontainers.image.description="Evidence-based AI parenting guide — birth to adulthood, always learning"
LABEL org.opencontainers.image.source="https://github.com/your-org/smart-parenting-companion"

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV PIP_NO_CACHE_DIR=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ ./backend/
COPY main.py .
COPY scripts/ ./scripts/
COPY .env.example ./.env.example

RUN mkdir -p /app/data

VOLUME ["/app/data"]

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

CMD ["python", "main.py"]
