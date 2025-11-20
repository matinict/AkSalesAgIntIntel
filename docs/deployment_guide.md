# Deployment Guide

> **AkSalesAgIntIntel - Multi-Agent Sales Intelligence System**  
> **Author:** Abdul Matin  
> **Organization:** Akij Resource  
> **Date:** November 2025  
> **Version:** 2.0

---

## 📋 Table of Contents

1. [Deployment Overview](#1-deployment-overview)
2. [Prerequisites](#2-prerequisites)
3. [Local Development Setup](#3-local-development-setup)
4. [Docker Deployment](#4-docker-deployment)
5. [Cloud Deployment (AWS)](#5-cloud-deployment-aws)
6. [Streamlit Cloud Deployment](#6-streamlit-cloud-deployment)
7. [Production Configuration](#7-production-configuration)
8. [CI/CD Pipeline Setup](#8-cicd-pipeline-setup)
9. [Monitoring & Maintenance](#9-monitoring--maintenance)
10. [Troubleshooting](#10-troubleshooting)
11. [Rollback Procedures](#11-rollback-procedures)
12. [Security Hardening](#12-security-hardening)

---

## 1. Deployment Overview

### 1.1 Deployment Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT ARCHITECTURE                       │
└─────────────────────────────────────────────────────────────────┘

                    ┌──────────────────┐
                    │   End Users      │
                    │  (Web/Mobile)    │
                    └────────┬─────────┘
                             │
                    ┌────────▼─────────┐
                    │  Load Balancer   │
                    │   (Nginx/ALB)    │
                    └────────┬─────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
   ┌────▼────┐         ┌─────▼─────┐       ┌─────▼─────┐
   │Instance │         │ Instance  │       │ Instance  │
   │   #1    │         │    #2     │       │    #3     │
   │Streamlit│         │ Streamlit │       │ Streamlit │
   └────┬────┘         └─────┬─────┘       └─────┬─────┘
        │                    │                    │
        └────────────────────┼────────────────────┘
                             │
                    ┌────────▼─────────┐
                    │   Data Layer     │
                    │ (CSV/Database)   │
                    └──────────────────┘
```

### 1.2 Deployment Options

| Option | Best For | Difficulty | Cost |
|--------|----------|------------|------|
| **Local** | Development & Testing | Easy | Free |
| **Docker** | Containerized deployment | Medium | Low |
| **Streamlit Cloud** | Quick MVP deployment | Easy | Free tier available |
| **AWS EC2** | Production workloads | Medium-Hard | Medium |
| **AWS ECS** | Scalable containerized apps | Hard | Medium-High |

### 1.3 Deployment Checklist

**Pre-Deployment:**
- [ ] Code review completed
- [ ] All tests passing
- [ ] Documentation updated
- [ ] Environment variables configured
- [ ] Backup data created
- [ ] Security scan completed
- [ ] Performance testing done

**Deployment:**
- [ ] Deploy to staging first
- [ ] Smoke tests passing
- [ ] Monitor logs for errors
- [ ] Verify all features working
- [ ] Check integrations (n8n, etc.)

**Post-Deployment:**
- [ ] Monitor application performance
- [ ] Check error rates
- [ ] Verify user access
- [ ] Update documentation
- [ ] Notify stakeholders

---

## 2. Prerequisites

### 2.1 System Requirements

**Minimum Requirements:**
```
Operating System: Windows 10/11, macOS 10.15+, Ubuntu 20.04+
CPU: 2 cores, 2.0 GHz
RAM: 4 GB
Storage: 2 GB free space
Python: 3.8 or higher
```

**Recommended Requirements:**
```
Operating System: Windows 11, macOS 13+, Ubuntu 22.04+
CPU: 4+ cores, 3.0+ GHz
RAM: 8+ GB
Storage: 10+ GB SSD
Python: 3.10 or higher
```

### 2.2 Software Dependencies

**Core Dependencies:**
```bash
Python 3.8+
pip (latest version)
git
```

**Optional (for production):**
```bash
Docker & Docker Compose
Nginx
PostgreSQL (if using database)
Redis (for caching)
```

### 2.3 Access Requirements

**Required Access:**
- GitHub repository access
- Cloud provider account (AWS/Azure/GCP)
- Domain name (for production)
- SSL certificate (for HTTPS)
- SMTP credentials (for email alerts)

---

## 3. Local Development Setup

### 3.1 Step-by-Step Installation

#### Step 1: Clone Repository
```bash
# Clone from GitHub
git clone https://github.com/matinict/AkSalesAgIntIntel.git

# Navigate to project directory
cd AkSalesAgIntIntel
```

#### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python -m venv akij_env

# Activate virtual environment
# On Windows:
akij_env\Scripts\activate

# On macOS/Linux:
source akij_env/bin/activate
```

#### Step 3: Install Dependencies
```bash
# Upgrade pip
pip install --upgrade pip

# Install requirements
pip install -r requirements.txt

# Verify installation
pip list
```

#### Step 4: Generate Data
```bash
# Option 1: Using Jupyter Notebook
jupyter notebook sales_agents.py
# Run all cells (Cell → Run All)

# Option 2: Convert to script and run
jupyter nbconvert --to script sales_agents.py
python sales_agents.py
```

#### Step 5: Configure Environment
```bash
# Copy example environment file
cp .env.example .env

# Edit configuration
nano .env  # or use your preferred editor
```

**.env Configuration:**
```bash
# Application Settings
ENV=development
DEBUG=True
LOG_LEVEL=DEBUG

# Data Configuration
AKIJ_DATA_PATH=akij_sales_data_complete.csv
AKIJ_CURRENCY=BDT
AKIJ_TIMEZONE=Asia/Dhaka

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_HEADLESS=false
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# n8n Integration (Optional)
N8N_WEBHOOK_URL=https://your-n8n-instance.com/webhook/akij
N8N_API_KEY=your-api-key-here

# Notification Settings (Optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK
EMAIL_SMTP_SERVER=smtp.gmail.com
EMAIL_SMTP_PORT=587
EMAIL_FROM=alerts@akijresource.com
EMAIL_PASSWORD=your-password-here
```

#### Step 6: Run Application
```bash
# Start Streamlit server
streamlit run chatbot_ui.py

# Application will start at http://localhost:8501
```

#### Step 7: Verify Installation
```bash
# Open browser and navigate to
http://localhost:8501

# Check system status in sidebar
# Should show: ✅ System Ready

# Try a sample query
# Example: "What is the total revenue?"
```

### 3.2 Development Server Configuration

**Streamlit Configuration (.streamlit/config.toml):**
```toml
[server]
port = 8501
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200
headless = false

[browser]
serverAddress = "localhost"
gatherUsageStats = false
serverPort = 8501

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
font = "sans serif"

[logger]
level = "debug"
```

### 3.3 Hot Reload & Development

**Enable Hot Reload:**
```bash
# Streamlit automatically watches for file changes
# Edit your code and save - app will reload automatically
streamlit run chatbot_ui.py --server.runOnSave true
```

**Development Tips:**
```python
# Use st.cache_data for expensive operations
@st.cache_data(ttl=60)  # Cache for 60 seconds during dev
def load_data():
    return pd.read_csv('data.csv')

# Add debug information
if st.session_state.get('debug_mode'):
    st.write("Debug Info:", data.shape, data.columns)
```

---

## 4. Docker Deployment

### 4.1 Dockerfile

**Create Dockerfile:**
```dockerfile
# Multi-stage build for optimization
FROM python:3.10-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Final stage
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data /app/logs

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8501/_stcore/health || exit 1

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_HEADLESS=true

# Run application
CMD ["streamlit", "run", "chatbot_ui.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true", \
     "--server.enableCORS=false"]
```

### 4.2 Docker Compose

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Streamlit Application
  streamlit:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: akij-streamlit
    ports:
      - "8501:8501"
    environment:
      - ENV=production
      - DEBUG=False
      - AKIJ_DATA_PATH=/app/data/akij_sales_data_complete.csv
      - PYTHONUNBUFFERED=1
    volumes:
      - ./data:/app/data
      - ./logs:/app/logs
    restart: unless-stopped
    networks:
      - akij-network
    depends_on:
      - redis
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Redis Cache
  redis:
    image: redis:7-alpine
    container_name: akij-redis
    ports:
      - "6379:6379"
    volumes:
      - redis-data:/data
    restart: unless-stopped
    networks:
      - akij-network
    command: redis-server --appendonly yes
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 10s
      timeout: 3s
      retries: 3

  # Nginx Reverse Proxy
  nginx:
    image: nginx:alpine
    container_name: akij-nginx
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro
      - ./nginx/ssl:/etc/nginx/ssl:ro
      - ./nginx/logs:/var/log/nginx
    depends_on:
      - streamlit
    restart: unless-stopped
    networks:
      - akij-network
    healthcheck:
      test: ["CMD", "nginx", "-t"]
      interval: 30s
      timeout: 10s
      retries: 3

networks:
  akij-network:
    driver: bridge

volumes:
  redis-data:
    driver: local
```

### 4.3 Nginx Configuration

**nginx/nginx.conf:**
```nginx
events {
    worker_connections 1024;
}

http {
    upstream streamlit {
        server streamlit:8501;
    }

    # Rate limiting
    limit_req_zone $binary_remote_addr zone=one:10m rate=10r/s;

    server {
        listen 80;
        server_name akijsales.com www.akijsales.com;

        # Redirect HTTP to HTTPS
        return 301 https://$host$request_uri;
    }

    server {
        listen 443 ssl http2;
        server_name akijsales.com www.akijsales.com;

        # SSL Configuration
        ssl_certificate /etc/nginx/ssl/certificate.crt;
        ssl_certificate_key /etc/nginx/ssl/private.key;
        ssl_protocols TLSv1.2 TLSv1.3;
        ssl_ciphers HIGH:!aNULL:!MD5;
        ssl_prefer_server_ciphers on;

        # Security Headers
        add_header X-Frame-Options "SAMEORIGIN" always;
        add_header X-Content-Type-Options "nosniff" always;
        add_header X-XSS-Protection "1; mode=block" always;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

        # Logging
        access_log /var/log/nginx/access.log;
        error_log /var/log/nginx/error.log;

        # Client configuration
        client_max_body_size 100M;

        location / {
            limit_req zone=one burst=20 nodelay;

            proxy_pass http://streamlit;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 86400;
        }

        # Health check endpoint
        location /_stcore/health {
            proxy_pass http://streamlit;
            access_log off;
        }
    }
}
```

### 4.4 Docker Commands

**Build and Run:**
```bash
# Build image
docker-compose build

# Start services
docker-compose up -d

# View logs
docker-compose logs -f streamlit

# Stop services
docker-compose down

# Restart services
docker-compose restart

# View running containers
docker-compose ps
```

**Maintenance Commands:**
```bash
# Enter container shell
docker-compose exec streamlit /bin/bash

# View container logs
docker logs akij-streamlit

# Check container health
docker inspect --format='{{.State.Health.Status}}' akij-streamlit

# Clean up unused images/containers
docker system prune -a

# Backup volumes
docker run --rm -v akij_redis-data:/data -v $(pwd):/backup alpine tar czf /backup/redis-backup.tar.gz /data
```

---

## 5. Cloud Deployment (AWS)

### 5.1 AWS EC2 Deployment

**Step 1: Launch EC2 Instance**
```bash
# AWS CLI command to launch instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t3.medium \
    --key-name your-key-pair \
    --security-group-ids sg-xxxxxxxx \
    --subnet-id subnet-xxxxxxxx \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=AkijSalesIntelligence}]'
```

**Step 2: Connect to Instance**
```bash
# SSH into instance
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

**Step 3: Install Dependencies**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and tools
sudo apt install -y python3-pip python3-venv git nginx

# Install Docker (optional)
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

**Step 4: Clone and Setup Application**
```bash
# Clone repository
git clone https://github.com/matinict/AkSalesAgIntIntel.git
cd AkSalesAgIntIntel

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate data
jupyter nbconvert --to script sales_agents.py
python sales_agents.py
```

**Step 5: Configure Systemd Service**
```bash
# Create service file
sudo nano /etc/systemd/system/akij-dashboard.service
```

**akij-dashboard.service:**
```ini
[Unit]
Description=Akij Sales Intelligence Dashboard
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/AkSalesAgIntIntel
Environment="PATH=/home/ubuntu/AkSalesAgIntIntel/venv/bin"
ExecStart=/home/ubuntu/AkSalesAgIntIntel/venv/bin/streamlit run chatbot_ui.py --server.port 8501 --server.address 0.0.0.0 --server.headless true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Step 6: Start Service**
```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable service
sudo systemctl enable akij-dashboard

# Start service
sudo systemctl start akij-dashboard

# Check status
sudo systemctl status akij-dashboard

# View logs
sudo journalctl -u akij-dashboard -f
```

**Step 7: Configure Nginx**
```bash
# Create Nginx configuration
sudo nano /etc/nginx/sites-available/akij-dashboard
```

**Nginx Configuration:**
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

**Step 8: Enable Site**
```bash
# Create symbolic link
sudo ln -s /etc/nginx/sites-available/akij-dashboard /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

**Step 9: Setup SSL (Let's Encrypt)**
```bash
# Install Certbot
sudo apt install -y certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Test renewal
sudo certbot renew --dry-run
```

### 5.2 AWS Security Group Configuration

**Inbound Rules:**
```
Type        Protocol    Port Range    Source          Description
SSH         TCP         22            Your-IP/32      SSH access
HTTP        TCP         80            0.0.0.0/0       HTTP traffic
HTTPS       TCP         443           0.0.0.0/0       HTTPS traffic
Custom      TCP         8501          VPC-CIDR        Internal Streamlit (optional)
```

**Outbound Rules:**
```
Type        Protocol    Port Range    Destination     Description
All traffic All         All           0.0.0.0/0       Allow all outbound
```

### 5.3 AWS Auto Scaling Configuration

**Launch Template:**
```bash
# Create launch template
aws ec2 create-launch-template \
    --launch-template-name akij-streamlit-template \
    --version-description v1 \
    --launch-template-data '{
        "ImageId": "ami-0c55b159cbfafe1f0",
        "InstanceType": "t3.medium",
        "KeyName": "your-key-pair",
        "SecurityGroupIds": ["sg-xxxxxxxx"],
        "UserData": "'"$(base64 user-data.sh)"'",
        "TagSpecifications": [{
            "ResourceType": "instance",
            "Tags": [{"Key":"Name","Value":"AkijSalesInstance"}]
        }]
    }'
```

**Auto Scaling Group:**
```bash
# Create auto scaling group
aws autoscaling create-auto-scaling-group \
    --auto-scaling-group-name akij-streamlit-asg \
    --launch-template LaunchTemplateName=akij-streamlit-template \
    --min-size 2 \
    --max-size 10 \
    --desired-capacity 2 \
    --vpc-zone-identifier "subnet-xxxxx,subnet-yyyyy" \
    --health-check-type ELB \
    --health-check-grace-period 300 \
    --tags "Key=Environment,Value=Production,PropagateAtLaunch=true"
```

**Scaling Policies:**
```bash
# Scale up policy
aws autoscaling put-scaling-policy \
    --auto-scaling-group-name akij-streamlit-asg \
    --policy-name scale-up \
    --policy-type TargetTrackingScaling \
    --target-tracking-configuration '{
        "PredefinedMetricSpecification": {
            "PredefinedMetricType": "ASGAverageCPUUtilization"
        },
        "TargetValue": 70.0
    }'
```

---

## 6. Streamlit Cloud Deployment

### 6.1 Streamlit Cloud Setup

**Step 1: Push to GitHub**
```bash
# Ensure all code is committed
git add .
git commit -m "Prepare for Streamlit Cloud deployment"
git push origin main
```

**Step 2: Deploy on Streamlit Cloud**
```
1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select repository: matinict/AkSalesAgIntIntel
5. Select branch: main
6. Select main file: chatbot_ui.py
7. Click "Deploy"
```

**Step 3: Configure Secrets**
```toml
# In Streamlit Cloud dashboard, add secrets:
# Settings → Secrets

[general]
AKIJ_CURRENCY = "BDT"
AKIJ_TIMEZONE = "Asia/Dhaka"

[n8n]
WEBHOOK_URL = "https://your-n8n-instance.com/webhook/akij"
API_KEY = "your-api-key"

[notifications]
SLACK_WEBHOOK = "https://hooks.slack.com/services/YOUR/WEBHOOK"
EMAIL_SMTP = "smtp.gmail.com"
EMAIL_PORT = "587"
EMAIL_FROM = "alerts@akijresource.com"
EMAIL_PASSWORD = "your-password"
```

**Step 4: Monitor Deployment**
```
# Check logs in Streamlit Cloud dashboard
# Logs tab shows real-time deployment progress
# Look for "Your app is live at: https://xxx.streamlit.app"
```

### 6.2 Streamlit Cloud Configuration

**requirements.txt (Streamlit Cloud):**
```txt
streamlit==1.28.0
pandas==2.0.3
numpy==1.24.3
plotly==5.17.0
python-dateutil==2.8.2
```

**packages.txt (System Dependencies):**
```txt
# If you need system packages
# Example:
# build-essential
# python3-dev
```

**.streamlit/config.toml:**
```toml
[server]
headless = true
enableCORS = false

[browser]
gatherUsageStats = false
```

---

## 7. Production Configuration

### 7.1 Environment Variables

**Production .env:**
```bash
# Environment
ENV=production
DEBUG=False
LOG_LEVEL=WARNING

# Application
AKIJ_DATA_PATH=/app/data/akij_sales_data_complete.csv
AKIJ_CURRENCY=BDT
AKIJ_TIMEZONE=Asia/Dhaka

# Server
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Database (if using)
DATABASE_URL=postgresql://user:pass@host:5432/akij_db
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10

# Cache
REDIS_URL=redis://redis:6379/0
CACHE_TTL=3600

# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=akijsales.com,www.akijsales.com
CORS_ORIGINS=https://akijsales.com,https://www.akijsales.com

# n8n Integration
N8N_WEBHOOK_URL=https://n8n.akijresource.com/webhook/akij
N8N_API_KEY=your-production-api-key

# Monitoring
SENTRY_DSN=https://xxx@sentry.io/xxx
SENTRY_ENVIRONMENT=production
SENTRY_TRACES_SAMPLE_RATE=0.1

# Logging
LOG_FILE=/app/logs/application.log
LOG_MAX_BYTES=10485760
LOG_BACKUP_COUNT=10
```

### 7.2 Performance Optimization

**Caching Strategy:**
```python
import streamlit as st

# Cache data loading
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_sales_data():
    return pd.read_csv(DATA_PATH)

# Cache expensive computations
@st.cache_data(ttl=1800)  # Cache for 30 minutes
def calculate_analytics(data):
    desc_agent = DescriptiveAgent(data)
    return desc_agent.analyze()

# Cache resources
@st.cache_resource
def init_database_connection():
    return create_engine(DATABASE_URL)
```

**Connection Pooling:**
```python
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=3600
)
```

### 7.3 Security Configuration

**HTTPS Configuration:**
```bash
# Generate SSL certificate
sudo certbot certonly --standalone -d akijsales.com -d www.akijsales.com

# Certificate locations
# Certificate: /etc/letsencrypt/live/akijsales.com/fullchain.pem
# Private Key: /etc/letsencrypt/live/akijsales.com/privkey.pem
```

**Security Headers:**
```python
# Add to Streamlit app
import streamlit.components.v1 as components

components.html("""
<script>
// Set security headers (if not using Nginx)
if (window.location.protocol !== 'https:') {
    window.location.href = 'https:' + window.location.href.substring(window.location.protocol.length);
}
</script>
""", height=0)
```

 

## 8. CI/CD Pipeline Setup

    This project includes a full GitHub Actions–based CI/CD pipeline that automates:

    Code testing

    Security scanning

    Docker image build

    Deployment to AWS EC2

    Below is the complete and final configuration.

### 8.1 GitHub Actions Workflow

    File: .github/workflows/deploy.yml


    [CI/CD Pipeline] (docs/cicd_pipeline.md)




Here you go Matin — **full professional documentation sections** for:

✅ Monitoring & Maintenance
✅ Troubleshooting
✅ Rollback Procedures
✅ Security Hardening

These sections are designed for **enterprise-grade AI systems**, especially for your **AkSalesAgIntIntel** submission.

---

# 🛡️ **9. Monitoring & Maintenance**

A production AI system requires continuous observability, performance tracking, and automated alerts.
This project uses a **3-layer monitoring approach**:

---

## **9.1 Application Monitoring**

### **Tools**

* **Prometheus** – metrics collection
* **Grafana Dashboard** – real-time visualization
* **Streamlit logs** – API call latency, user activity
* **Custom logs inside agents** – error tracking, agent performance

### **Key Metrics to Monitor**

| Component             | Metrics                                        |
| --------------------- | ---------------------------------------------- |
| LLM Usage             | Token usage, latency, failure rate             |
| Agents                | Execution time, fallback triggers, error count |
| Sales Data Processing | Load time, memory usage                        |
| Streamlit UI          | Response latency, dashboard refresh stats      |
| n8n Workflows         | Webhook triggers, failure rate                 |

---

## **9.2 Infrastructure Monitoring**

### **Tools**

* AWS CloudWatch (EC2 CPU, RAM, Disk, Network)
* UptimeRobot (API uptime)
* Docker health checks

### **EC2 Health Checks**

```bash
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

---

## **9.3 Log Management**

Logs are captured as:

```
/logs/
│── agents.log
│── n8n_workflows.log
│── chatbot.log
└── errors.log
```

Best practice: stream logs to **AWS CloudWatch Logs** or **ELK stack**.

---

# 🛠️ **10. Troubleshooting Guide**

A practical guide for diagnosing the most common failures.

---

## **10.1 Streamlit Dashboard Not Loading**

### ❌ Issue:

* Page stuck
* "Cannot fetch data"

### ✅ Fix:

```bash
docker logs sales-intel
```

Check CSV location: `akij_sales_data_complete.csv`
Ensure file exists and has correct permissions.

---

## **10.2 Agents Not Returning Output**

### Possible Causes:

* Missing API keys
* Data filters too restrictive
* Pandas read failure

### Fix:

Check environment variables:

```bash
cat .env
```

Check agent logs:

```bash
cat logs/agents.log
```

---

## **10.3 n8n Workflow Not Triggering**

### Root Causes:

* Incorrect webhook URL
* Invalid JSON schema
* n8n server offline

### Fix:

1. Validate generated payload:

```bash
python3 validate_payload.py
```

2. Check Webhook:

```
https://n8n.yourserver.com/webhook/akij-sales
```

---

## **10.4 Docker Container Crashing**

### Fix:

```bash
docker-compose down
docker-compose up -d --build
docker logs sales-intel
```

---

## **10.5 CI/CD Pipeline Failing**

### Common Reasons:

* Syntax errors in YAML
* Missing GitHub secrets
* DockerHub authentication failure

### Fix:

Check YAML syntax:

```yaml
https://yamlchecker.com
```

Check secrets:

```
Settings → Secrets → Actions
```

---

# 🔄 **11. Rollback Procedures**

In case a deployment breaks production, **rollback instantly**.

---

## **11.1 Rollback to Previous Docker Image**

```bash
docker pull matinict/akij-sales-intelligence:stable
docker tag matinict/akij-sales-intelligence:stable sales-intel
docker-compose down
docker-compose up -d
```

---

## **11.2 Rollback Using Git Tags**

### Step 1: List tags

```bash
git tag
```

### Step 2: Checkout stable tag

```bash
git checkout v1.2.0-stable
```

### Step 3: Redeploy

```bash
docker-compose up -d --build
```

---

## **11.3 Automatic Rollback in CI/CD (Optional)**

Add inside GitHub Actions:

```yaml
if: failure()
run: |
  docker pull matinict/akij-sales-intelligence:stable
  docker-compose up -d
```

---

# 🔐 **12. Security Hardening (Production-Grade)**

Securing your AI system is mandatory for enterprise deployment.

---

## **12.1 Environment Security**

✔ Disable storing API keys in code
✔ Use `.env` + GitHub Secrets
✔ Rotate keys every 90 days
✔ Restrict keys with scope-based permissions

---

## **12.2 Server Security**

### On EC2:

```bash
sudo ufw enable
sudo ufw allow 22/tcp
sudo ufw allow 8501/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

✔ Disable password login
✔ Only allow SSH key authentication

---

## **12.3 Docker Security**

* Use non-root users inside containers
* Enable Docker Content Trust
* Keep base images lightweight & updated

---

## **12.4 Data Security**

✔ Encrypt data at rest (AES-256)
✔ Encrypt data in transit (HTTPS)
✔ Hash sensitive IDs (SHA-256)

---

## **12.5 LLM Security (Critical)**

✔ Rate limit queries
✔ Validate user input
✔ Prevent prompt injection (sanitize commands)
✔ Mask sensitive data before sending to LLMs

---
 

    