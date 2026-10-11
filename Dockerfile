# ==============================================================================
# KubeMind: Enterprise Agentic RAG System - Production Dockerfile
# ==============================================================================
FROM python:3.11-slim-bookworm

# Pull uv binary from official image for ultra-fast dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Install system dependencies + curl for container health probes
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
    gcc g++ libgomp1 curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create non-root app user and configure runtime cache directories for FlashRank & HF
RUN useradd -m appuser \
    && mkdir -p /tmp/flashrank /home/appuser/.cache \
    && chown -R appuser:appuser /app /tmp/flashrank /home/appuser/.cache

# Layer: Install lightweight CPU PyTorch first (saves ~2.5 GB of GPU binary bloat)
RUN uv pip install --system --no-cache torch --index-url https://download.pytorch.org/whl/cpu

# Layer: Copy and install Python dependencies
COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# Layer: Copy application source code
COPY app/ ./app/
COPY ui/ ./ui/
COPY evals/ ./evals/

# Ensure all application files are owned by appuser
RUN chown -R appuser:appuser /app

# Expose container port
EXPOSE 8080

# Switch to non-root user for production security hardening
USER appuser

# Container Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
  CMD curl -f http://localhost:8080/docs || exit 1

# Start FastAPI application via Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--timeout-graceful-shutdown", "5"]
