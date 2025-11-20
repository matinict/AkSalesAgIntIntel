Here is your **completed CI/CD Pipeline section**, fully structured, professional, and production-ready.
I did **NOT** call any tools, because you only asked to “complete it,” not to generate diagrams.

You can paste this directly into your `README.md` or `docs/cicd_pipeline.md`.

---

# 🚀 **8. CI/CD Pipeline Setup**

This project includes a full **GitHub Actions–based CI/CD pipeline** that automates:

* Code testing
* Security scanning
* Docker image build
* Deployment to AWS EC2

Below is the complete and final configuration.

---

# **8.1 GitHub Actions Workflow**

File: **`.github/workflows/deploy.yml`**

```yaml
name: Deploy to Production

on:
  push:
    branches:
      - main
  pull_request:
    branches:
      - main

env:
  PYTHON_VERSION: '3.10'
  
jobs:
  test:
    name: Run Tests
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
      
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
          pip install pytest pytest-cov
      
      - name: Run tests
        run: |
          pytest tests/ --cov=. --cov-report=xml
      
      - name: Upload coverage to Codecov
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
          fail_ci_if_error: true

  security:
    name: Security Scan
    runs-on: ubuntu-latest
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Run Bandit security scan
        run: |
          pip install bandit
          bandit -r . -f json -o bandit-report.json
      
      - name: Run Safety vulnerability scan
        run: |
          pip install safety
          safety check --json

  build:
    name: Build Docker Image
    needs: [test, security]
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v2
      
      - name: Login to DockerHub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: matinict/akij-sales-intelligence:latest
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy:
    name: Deploy to Production (EC2)
    needs: build
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to EC2
        uses: appleboy/ssh-action@master
        with:
          host: ${{ secrets.EC2_HOST }}
          username: ${{ secrets.EC2_USERNAME }}
          key: ${{ secrets.EC2_SSH_KEY }}
          script: |
            cd /home/ubuntu/AkSalesAgIntIntel
            docker-compose pull
            docker-compose up -d
            docker system prune -f
```

---

# ✔️ **What This Pipeline Does**

### ✅ **1. Testing**

* Runs all PyTest tests
* Generates code coverage report
* Uploads results to Codecov

### ✅ **2. Security Checks**

* Runs **Bandit** (Python security scanner)
* Runs **Safety** (dependency vulnerability scanner)

### ✅ **3. Docker Build**

* Uses Docker Buildx
* Builds optimized production image
* Pushes to Docker Hub

### Image Tag Example:

```
matinict/akij-sales-intelligence:latest
```

### ✅ **4. Deployment**

* SSH into AWS EC2
* Pulls latest Docker image
* Restarts containers
* Cleans unused Docker layers

---

# 🔧 **Required GitHub Secrets**

Add these under:

**GitHub → Repository → Settings → Secrets → Actions**

| Secret Name       | Description                  |
| ----------------- | ---------------------------- |
| `DOCKER_USERNAME` | Docker Hub username          |
| `DOCKER_PASSWORD` | Docker Hub access token      |
| `EC2_HOST`        | Public IP of EC2             |
| `EC2_USERNAME`    | SSH user (e.g., `ubuntu`)    |
| `EC2_SSH_KEY`     | Private key for EC2 instance |

---

# 📦 **Docker Compose (required on EC2)**

Your EC2 must have a `docker-compose.yml` file like:

```yaml
version: '3.8'

services:
  sales-intel:
    image: matinict/akij-sales-intelligence:latest
    ports:
      - "8501:8501"
    restart: always
```

---

# 🎯 **CI/CD Section Complete** 
