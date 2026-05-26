# ---- Backend ----
FROM python:3.11-slim AS backend

WORKDIR /

COPY pyproject.toml uv.lock ./
COPY backend ./backend/

RUN pip install --no-cache-dir uv && uv sync --no-dev --frozen

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]


# ---- Frontend dependencies ----
FROM node:20-alpine AS frontend-deps
WORKDIR /
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci


# ---- Frontend build ----
FROM node:22-alpine AS frontend-build
WORKDIR /app
COPY --from=frontend-deps /app/node_modules ./node_modules
COPY frontend/ .
RUN npm run build


# ---- Frontend ----
FROM node:22-alpine AS frontend
WORKDIR /app
ENV NODE_ENV=production

COPY --from=frontend-build /app/.next ./.next
COPY --from=frontend-build /app/public ./public
COPY --from=frontend-build /app/package.json ./package.json
COPY --from=frontend-deps /app/node_modules ./node_modules

EXPOSE 3000
CMD ["npm", "start"]
