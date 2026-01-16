# --- Stage 1: Build React ---
FROM node:20-slim AS frontend-builder
#WORKDIR /app
WORKDIR /build-repo

# Assuming your frontend source is in a sibling folder '../frontend'
# during the 'docker build' context
COPY ../frontend/package*.json ./
RUN npm install
COPY ../frontend/ .
RUN npm run build

# --- Stage 2: Production Backend ---
FROM python:3.11-slim
WORKDIR /app

# NEW: Critical fix for the init_fs_encoding error
# Unset these to prevent host environment leaks from breaking the container
ENV PYTHONPATH=/
ENV PYTHONHOME=

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY . .

# Copy the React build from Stage 1 into the FastAPI static folder
# Vite defaults to the 'dist' folder
COPY --from=frontend-builder /build-repo/dist ./app/static

# Expose port and run
EXPOSE 8000
# IMPORTANT: Bind to 0.0.0.0 for Docker networking
#CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["python", "-m", "uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]