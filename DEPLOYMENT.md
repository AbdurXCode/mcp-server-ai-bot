# 🚀 Deployment Guide

This guide covers deploying the MCP LLM Server to various platforms.

## 📋 Table of Contents

- [Prerequisites](#prerequisites)
- [Local Deployment](#local-deployment)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment](#cloud-deployment)
- [Environment Configuration](#environment-configuration)
- [Monitoring](#monitoring)

## Prerequisites

- Python 3.10+
- API keys configured
- Domain name (for production)
- SSL certificate (for production)

## 🏠 Local Deployment

### Development

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env from template
cp .env.example .env
# Edit .env with your credentials

# Run with auto-reload
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Production (Local)

```bash
# Run with multiple workers
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## 🐳 Docker Deployment

### Build Image

```bash
# Build the image
docker build -t mcp-llm-server:latest .

# Or with specific version
docker build -t mcp-llm-server:1.0.0 .
```

### Run Container

```bash
# Run with environment file
docker run -d \
  --name mcp-llm-server \
  -p 8000:8000 \
  --env-file .env \
  mcp-llm-server:latest

# Or with individual env vars
docker run -d \
  --name mcp-llm-server \
  -p 8000:8000 \
  -e API_KEY=your_key \
  -e GEMINI_API_KEY=your_gemini_key \
  -e API_URL=https://api.example.com \
  mcp-llm-server:latest
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  mcp-llm-server:
    build: .
    ports:
      - "8000:8000"
    environment:
      - API_KEY=${API_KEY}
      - GEMINI_API_KEY=${GEMINI_API_KEY}
      - API_URL=${API_URL}
      - SERVER_HOST=0.0.0.0
      - SERVER_PORT=8000
      - DEBUG=false
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

Run:
```bash
docker-compose up -d
```

## ☁️ Cloud Deployment

### AWS (EC2)

1. **Launch EC2 Instance**
   ```bash
   # Ubuntu 22.04 LTS
   # t3.small or larger
   ```

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install -y python3.11 python3.11-venv nginx
   ```

3. **Deploy Application**
   ```bash
   git clone https://github.com/yourusername/mcp-llm-server.git
   cd mcp-llm-server
   python3.11 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

4. **Configure Systemd Service**
   Create `/etc/systemd/system/mcp-llm-server.service`:
   ```ini
   [Unit]
   Description=MCP LLM Server
   After=network.target

   [Service]
   User=ubuntu
   WorkingDirectory=/home/ubuntu/mcp-llm-server
   Environment="PATH=/home/ubuntu/mcp-llm-server/venv/bin"
   EnvironmentFile=/home/ubuntu/mcp-llm-server/.env
   ExecStart=/home/ubuntu/mcp-llm-server/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

5. **Start Service**
   ```bash
   sudo systemctl enable mcp-llm-server
   sudo systemctl start mcp-llm-server
   sudo systemctl status mcp-llm-server
   ```

6. **Configure Nginx**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
   }
   ```

### Google Cloud Platform (Cloud Run)

1. **Build and Push to Container Registry**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT-ID/mcp-llm-server
   ```

2. **Deploy to Cloud Run**
   ```bash
   gcloud run deploy mcp-llm-server \
     --image gcr.io/PROJECT-ID/mcp-llm-server \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars API_KEY=xxx,GEMINI_API_KEY=xxx
   ```

### Azure (App Service)

1. **Create App Service**
   ```bash
   az webapp create \
     --resource-group myResourceGroup \
     --plan myAppServicePlan \
     --name mcp-llm-server \
     --runtime "PYTHON:3.11"
   ```

2. **Deploy**
   ```bash
   az webapp up --name mcp-llm-server
   ```

3. **Configure Environment**
   ```bash
   az webapp config appsettings set \
     --name mcp-llm-server \
     --settings API_KEY=xxx GEMINI_API_KEY=xxx
   ```

### Heroku

1. **Create Procfile**
   ```
   web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Deploy**
   ```bash
   heroku create mcp-llm-server
   heroku config:set API_KEY=xxx
   heroku config:set GEMINI_API_KEY=xxx
   git push heroku main
   ```

## 🔧 Environment Configuration

### Production Environment Variables

```env
# Production API Configuration
API_KEY=prod_live_key_xxxxx
API_URL=https://api.production.com
API_TIMEOUT=30

# LLM Configuration
GEMINI_API_KEY=AIza...production...key

# Server Configuration
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=false

# MCP Configuration
MCP_SERVER_NAME=production-mcp-server
MCP_SERVER_VERSION=1.0.0
```

### Using Secret Managers

#### AWS Secrets Manager
```python
import boto3
from botocore.exceptions import ClientError

def get_secret(secret_name):
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name='us-east-1'
    )
    
    try:
        response = client.get_secret_value(SecretId=secret_name)
        return response['SecretString']
    except ClientError as e:
        raise e
```

#### Google Secret Manager
```python
from google.cloud import secretmanager

def get_secret(project_id, secret_id):
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

## 📊 Monitoring

### Health Checks

The server provides built-in health check endpoint:
```bash
curl http://localhost:8000/
```

### Logging

Configure logging in production:

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/mcp-llm-server/app.log'),
        logging.StreamHandler()
    ]
)
```

### Monitoring Tools

- **Prometheus + Grafana**: For metrics
- **ELK Stack**: For log aggregation
- **Sentry**: For error tracking
- **Datadog**: All-in-one monitoring

### Example Prometheus Configuration

```yaml
scrape_configs:
  - job_name: 'mcp-llm-server'
    static_configs:
      - targets: ['localhost:8000']
```

## 🔒 SSL/TLS Configuration

### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal
sudo certbot renew --dry-run
```

### Nginx with SSL

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

## 🚦 Load Balancing

### Nginx Load Balancer

```nginx
upstream mcp_llm_backend {
    least_conn;
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}

server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://mcp_llm_backend;
    }
}
```

## 📝 Deployment Checklist

Before deploying to production:

- [ ] Environment variables configured
- [ ] Secrets stored securely (not in code)
- [ ] SSL/TLS enabled
- [ ] Firewall configured
- [ ] Logging configured
- [ ] Monitoring set up
- [ ] Backup strategy in place
- [ ] Auto-scaling configured (if needed)
- [ ] Rate limiting enabled
- [ ] CORS configured properly
- [ ] Health checks working
- [ ] Documentation updated
- [ ] Team notified of deployment

## 🔄 CI/CD Pipeline

See `.github/workflows/ci.yml` for automated deployment pipeline.

## 📞 Support

For deployment issues:
- Check logs: `sudo journalctl -u mcp-llm-server -f`
- Health check: `curl http://localhost:8000/`
- Configuration: `curl http://localhost:8000/config`

---

**Last Updated**: October 2025

