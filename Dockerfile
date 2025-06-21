# ── Imagen base ──────────────────────────────────────────────
FROM python:3.12-slim

# ── Evita pyc y buffers ──────────────────────────────────────
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# ── Dependencias del sistema ─────────────────────────────────
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# ── Directorio de trabajo ────────────────────────────────────
WORKDIR /app

# ── Instala dependencias Python ──────────────────────────────
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ── Copia código fuente ──────────────────────────────────────
COPY . .

# ── Usuario seguro ───────────────────────────────────────────
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# ── Puerto dinámico para Render ──────────────────────────────
EXPOSE 10000

# ── Comando de arranque ──────────────────────────────────────
CMD ["uvicorn", "gpt_legal_backend.main:app", "--host", "0.0.0.0", "--port", "10000"]
