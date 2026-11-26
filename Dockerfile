# DocSearch — API FastAPI + frontend React (même origine)
FROM node:22-alpine AS frontend-build
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
# Même origine que l'API (chaîne vide)
ENV VITE_API_URL=
RUN npm run build

FROM python:3.12-slim AS runtime
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8010

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

COPY backend/ /app/backend/
COPY data/db/documents.db /app/data/db/documents.db
COPY data/db/.gitkeep /app/data/db/.gitkeep
COPY data/raw/ /app/data/raw/
COPY --from=frontend-build /frontend/dist /app/frontend/dist

WORKDIR /app/backend
EXPOSE 8010

CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8010}"]
