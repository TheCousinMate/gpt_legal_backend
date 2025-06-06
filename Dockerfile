# ── Base ───────────────────────────────────────────────────────────────
FROM python:3.12-slim

# Evita archivos .pyc y buffers
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ── Dependencias de sistema (gcc, tesseract para pytesseract, etc.) ────
RUN apt-get update && apt-get install -y \
        gcc \
        g++ \
        tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# ── Código ─────────────────────────────────────────────────────────────
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

# ── Usuario no-root ────────────────────────────────────────────────────
RUN useradd --create-home --shell /bin/bash app \
 && chown -R app:app /app
USER app

# ── Puerto dinámico que Render inyecta ─────────────────────────────────
#   Render define $PORT en tiempo de ejecución (ej.: 10000).
EXPOSE $PORT

# ── Arranque ───────────────────────────────────────────────────────────
#   Cambia 'main:app' si tu punto de entrada es distinto.
CMD ["uvicorn", "gpt_legal_backend.main:app", "--host", "0.0.0.0", "--port", "10000"]
