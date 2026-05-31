# 🧟 ZombieGuard Production Dockerfile
# Full-Stack Monolith Deployment (Approach B)

FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

WORKDIR /app

# Install lightweight compiler dependencies required for lxml/scikit-learn
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libxml2-dev \
    libxslt-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Cache requirements layer
COPY requirements.txt .

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend files
COPY . .

# Expose default port
EXPOSE 8000

# Bootstrap ASGI server dynamically using Render/PaaS port environmental variables
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port $PORT"]
