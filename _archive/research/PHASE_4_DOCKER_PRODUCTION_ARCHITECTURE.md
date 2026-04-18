# Phase 4A: Docker & Production Deployment Architecture

**Status**: Design Phase (for review and approval)  
**Scope**: Containerization, WSGI server, production deployment readiness  
**Priority**: Highest (enables deployment)

---

## 1. Current State (Phase 3 End)

**What Exists**:
- ✅ Flask development server (`tracker_flask_api.py`)
- ✅ 10 API endpoints (health, platforms, scrape, status, results, analysis, jobs, export, clear-cache)
- ✅ Dashboard HTML UI (responsive)
- ✅ 9 core Python modules (2,950 lines)
- ✅ In-memory job queue (SQLite cache)
- ✅ Mock data generation

**What's Needed for Production**:
- ❌ Docker containerization (Dockerfile)
- ❌ Production WSGI server (Gunicorn)
- ❌ Docker Compose (multi-container: web + postgres)
- ❌ Health checks (container liveness/readiness)
- ❌ Logging & monitoring setup
- ❌ Environment configuration (.env, config files)

---

## 2. Architecture: Three-Tier Deployment Model

### Tier 1: Development (Current)
```
localhost:5000
├── Flask dev server (single process)
├── In-memory job queue
├── SQLite cache (file-based)
├── Mock data (always works)
└── Hot reload enabled
```

### Tier 2: Production (Single Container)
```
Docker Container (tracker-api:latest)
├── Gunicorn WSGI server (4 workers)
├── Persistent PostgreSQL (external)
├── Environment variables (.env)
├── Health endpoint (/health)
├── Structured logging (JSON)
└── No hot reload (immutable container)
```

### Tier 3: Production Cluster (Kubernetes, future)
```
K8s Cluster
├── Multiple API pods (auto-scaled)
├── PostgreSQL StatefulSet
├── Redis cache layer
├── Ingress controller
└── Monitoring stack
```

**Phase 4 Target**: Move from Tier 1 → Tier 2 (single production-ready container)

---

## 3. Dockerfile Strategy

### Design Principles
- **Multi-stage build**: Separate build and runtime stages
- **Minimal base image**: Alpine Linux (50MB) or Debian slim (100MB)
- **Production dependencies only**: No dev tools in final image
- **Security hardening**: Non-root user, read-only filesystem where possible
- **Health checks**: Built-in container health monitoring
- **Logging**: JSON format for log aggregation

### Dockerfile Specification

```dockerfile
# Stage 1: Builder
FROM python:3.10-slim as builder

WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.10-slim

# Metadata
LABEL maintainer="Trust Tracker <contact@tracker.local>"
LABEL version="1.0"
LABEL description="Universal Platform Tracker API"

# Create non-root user
RUN useradd -m -u 1000 tracker

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /home/tracker/.local

# Copy application code
COPY --chown=tracker:tracker . .

# Set environment
ENV PATH=/home/tracker/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FLASK_ENV=production

# Switch to non-root user
USER tracker

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')" || exit 1

# Expose port
EXPOSE 5000

# Run Gunicorn WSGI server
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "4", \
     "--worker-class", "sync", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "tracker_flask_api:app"]
```

### Key Features
1. **Multi-stage**: Builder stage discarded (smaller final image)
2. **Non-root user**: Security best practice
3. **Health check**: Automatically detects crashed containers
4. **Environment variables**: Production-safe defaults
5. **Gunicorn**: Production-grade WSGI server (4 workers = 2 CPU cores)
6. **Logging**: stdout/stderr for container log aggregation

---

## 4. Requirements File Strategy

### requirements.txt (Generated)
```
Flask==2.3.2
Flask-CORS==4.0.0
gunicorn==21.2.0
praw==7.7.0
requests==2.31.0
scikit-learn==1.3.0
python-dotenv==1.0.0
psycopg2-binary==2.9.7
SQLAlchemy==2.0.20
```

**Build Strategy**:
- Current: `pip freeze > requirements.txt` (all dependencies with pinned versions)
- Reproducible: Exact same versions every build
- Updates: Periodic security patches via `pip list --outdated`

---

## 5. Docker Compose Strategy

### Multi-Container Architecture
```yaml
version: '3.9'

services:
  # Phase 4A: API server with Gunicorn
  web:
    build: .
    container_name: tracker-api
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://tracker:password@db:5432/tracker
      - REDIS_URL=redis://cache:6379
      - FLASK_ENV=production
      - LOG_LEVEL=info
    depends_on:
      db:
        condition: service_healthy
      cache:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "python", "-c", "import requests; requests.get('http://localhost:5000/api/health')"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped
    volumes:
      - ./logs:/app/logs
    networks:
      - tracker-network

  # Phase 4C: PostgreSQL database
  db:
    image: postgres:15-alpine
    container_name: tracker-db
    environment:
      - POSTGRES_USER=tracker
      - POSTGRES_PASSWORD=secure_password_here
      - POSTGRES_DB=tracker
    volumes:
      - postgres-data:/var/lib/postgresql/data
      - ./migrations:/docker-entrypoint-initdb.d
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U tracker"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - tracker-network

  # Phase 4D: Redis cache (optional, for future)
  cache:
    image: redis:7-alpine
    container_name: tracker-cache
    ports:
      - "6379:6379"
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped
    networks:
      - tracker-network

volumes:
  postgres-data:

networks:
  tracker-network:
    driver: bridge
```

### Startup Sequence
1. `docker-compose up` initiated
2. PostgreSQL starts, runs health check (5s retry × 5)
3. Redis starts, runs health check
4. API container waits for db health check to pass
5. API container starts Gunicorn
6. Gunicorn runs health check endpoint
7. All services ready for requests (40s total startup)

---

## 6. Production Configuration Strategy

### Environment Variables (.env)
```bash
# Flask/WSGI Configuration
FLASK_ENV=production
DEBUG=False
LOG_LEVEL=info

# Database (Phase 4C)
DATABASE_URL=postgresql://tracker:password@db:5432/tracker
DB_POOL_SIZE=10
DB_POOL_RECYCLE=3600

# Cache (Phase 4D)
REDIS_URL=redis://cache:6379
CACHE_TTL=3600

# API Configuration
API_PORT=5000
API_WORKERS=4
API_TIMEOUT=120
MAX_CONTENT_LENGTH=16777216

# Security
SECRET_KEY=generate_random_32_char_key_here
CORS_ORIGINS=http://localhost:3000,https://example.com

# Logging
LOG_FORMAT=json
LOG_FILE=/app/logs/tracker.log
```

### Config File Hierarchy
```
/app/config.py
├── Config (base)
│   ├── database connection
│   ├── cache settings
│   ├── logging format
│   └── security defaults
├── DevelopmentConfig(Config)
│   ├── DEBUG=True
│   ├── TESTING=False
│   └── SQLite (local)
├── ProductionConfig(Config)
│   ├── DEBUG=False
│   ├── TESTING=False
│   └── PostgreSQL + Redis
└── TestingConfig(Config)
    ├── DEBUG=True
    ├── TESTING=True
    └── SQLite (memory)
```

---

## 7. Deployment Scenarios

### Development (Current - Phase 3)
```bash
python tracker_flask_api.py
# Result: http://localhost:5000
```

### Production Single Container (Phase 4A Target)
```bash
docker build -t tracker-api:latest .
docker run -p 5000:5000 \
  -e DATABASE_URL=postgresql://... \
  tracker-api:latest
```

### Production Docker Compose (Phase 4A+C)
```bash
docker-compose up -d
# Result: http://localhost:5000 with persistent PostgreSQL
```

### Production Kubernetes (Phase 5+, future)
```bash
kubectl apply -f k8s/
# Result: Auto-scaled cluster with monitoring
```

---

## 8. Health Check & Monitoring

### Built-in Health Endpoint
```python
@app.route('/api/health', methods=['GET'])
def health():
    return {
        'status': 'healthy',
        'database': db_connection_status(),
        'cache': redis_connection_status(),
        'adapters': len(coordinator.adapters),
        'uptime_seconds': app.uptime()
    }, 200
```

### Container Health Check
```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')"
```

### Kubernetes Liveness/Readiness Probes (Phase 5)
```yaml
livenessProbe:
  httpGet:
    path: /api/health
    port: 5000
  initialDelaySeconds: 40
  periodSeconds: 30

readinessProbe:
  httpGet:
    path: /api/health
    port: 5000
  initialDelaySeconds: 20
  periodSeconds: 10
```

---

## 9. Logging Strategy

### Development (Current)
```
stdout/stderr → Console (human-readable)
```

### Production (Phase 4)
```
Application → JSON structured logs → stdout → (ELK/Splunk/etc)
```

### Log Format (JSON)
```json
{
  "timestamp": "2026-04-18T10:30:45.123Z",
  "level": "INFO",
  "logger": "tracker_flask_api",
  "request_id": "req-abc123",
  "message": "Scraping job started",
  "user_id": "job-xyz789",
  "duration_ms": 1250
}
```

### Python Logging Config
```python
import logging
import json

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module
        }
        return json.dumps(log_data)

# Configure
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger()
logger.addHandler(handler)
```

---

## 10. Build & Deployment Commands

### Local Development
```bash
# Build image locally
docker build -t tracker-api:dev .

# Run single container (development)
docker run -p 5000:5000 tracker-api:dev

# Run with docker-compose
docker-compose up -d
docker-compose logs -f web
docker-compose down
```

### Production Registry (GitHub Container Registry)
```bash
# Tag for registry
docker tag tracker-api:latest ghcr.io/acidfang/tracker-api:latest

# Push to registry
docker login ghcr.io
docker push ghcr.io/acidfang/tracker-api:latest

# Deploy from registry
docker pull ghcr.io/acidfang/tracker-api:latest
docker run ghcr.io/acidfang/tracker-api:latest
```

### Docker Compose Production
```bash
# Start all services
docker-compose -f docker-compose.yml up -d

# View logs
docker-compose logs -f web

# Scale API (for future phase)
docker-compose up -d --scale web=3

# Stop all
docker-compose down -v
```

---

## 11. Implementation Checklist (Phase 4A)

**Files to Create**:
- [ ] `Dockerfile` (multi-stage, non-root, health checks)
- [ ] `docker-compose.yml` (web + db + cache)
- [ ] `.dockerignore` (exclude unnecessary files)
- [ ] `requirements.txt` (pip freeze output)
- [ ] `.env.example` (template for .env)
- [ ] `config.py` (Flask config class hierarchy)
- [ ] `logging_config.json` (structured logging setup)
- [ ] `DOCKER_DEPLOYMENT_GUIDE.md` (operational guide)

**Modifications to Existing Files**:
- [ ] `tracker_flask_api.py` → Use config from environment
- [ ] `universal_tracker_core.py` → Database connection ready
- [ ] Add requirements to all module imports

**Testing Before Push**:
1. `docker build -t tracker-api:test .` → Succeeds
2. `docker run -p 5000:5000 tracker-api:test` → Server starts
3. `curl http://localhost:5000/api/health` → 200 OK
4. `docker-compose up -d` → All services healthy
5. `curl http://localhost:5000/api/platforms` → Returns platforms

**Deploy to GitHub**:
- [ ] `git add [all files]`
- [ ] `git commit -m "PHASE 4A COMPLETE: Docker & Production Deployment"`
- [ ] `git push origin main`

---

## 12. Success Criteria

✅ **Phase 4A Complete When**:
1. Docker image builds without errors
2. Container starts and passes health check
3. All 10 API endpoints respond 200/202 from container
4. docker-compose up succeeds with all services healthy
5. PostgreSQL persists data across container restarts
6. Logs are JSON-formatted and visible via `docker logs`
7. All code pushed to GitHub with Dockerfile + compose
8. 15+ minute startup → 40 second production startup ✓

---

## 13. Future Phases (Beyond Phase 4)

**Phase 5: Kubernetes & Auto-Scaling**
- Helm charts
- HPA (Horizontal Pod Autoscaler)
- Persistent volumes for PostgreSQL
- Service mesh (Istio)

**Phase 5+: Monitoring & Observability**
- Prometheus metrics
- Grafana dashboards
- ELK stack (Elasticsearch/Logstash/Kibana)
- Distributed tracing (Jaeger)

---

## End Architecture Document

**Next**: User review → Approval → Implementation of Phase 4A
